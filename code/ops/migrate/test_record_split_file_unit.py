"""File-unit tests for record_split (T215 A3 seam, ticket T5b).

A --root that is one regular file splits as a file unit: {"root": the file, "leaves": [one row with path "."]},
read without following a link, through its parent's fd as the same entry the held root fd names.
"""
from __future__ import annotations

import errno
import stat
import re
import types
import json
import os
import unittest
from unittest import mock

import fault_kit as FK
import record_split as R
from test_record_split import Fixture, sha, before_open


class FileUnitSplit(Fixture):
    def split_file(self, name: str, data: bytes, *extra):
        root = self.base / name
        root.write_bytes(data)
        out = self.base / "split.json"
        proc = self.cli("--root", root, "--out", out, *extra)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return root, json.loads(out.read_text())

    def test_record_named_file_unit_is_one_tracked_record_at_dot(self):
        data = b"\x00binary but named as a record"
        root, doc = self.split_file("model.json", data)
        self.assertEqual(doc, {"root": str(root), "leaves": [
            {"path": ".", "class": R.TRACKED, "kind": "file", "size": len(data), "sha256": sha(data),
             "link": None}]})

    def test_binary_file_unit_is_a_governed_payload(self):
        _, doc = self.split_file("weights.bin", b"\x00\x01")
        self.assertEqual([(r["path"], r["class"]) for r in doc["leaves"]], [(".", R.PAYLOAD)])

    def test_attested_file_unit_is_bulk(self):
        data = b"\x00regenerable"
        att = self.attest([(".", sha(data))])
        _, doc = self.split_file("cache.bin", data, "--attestation", att)
        self.assertEqual(doc["leaves"][0]["class"], R.BULK)

    def test_output_beside_the_file_root_is_allowed(self):
        root = self.unit / "model.json"
        root.write_bytes(b"{}\n")
        code, err = self.main("--root", root, "--out", self.unit / "split.json")
        self.assertEqual(code, 0, err)

    def test_symlink_to_a_file_root_refuses(self):
        target = self.base / "model.json"
        target.write_bytes(b"{}\n")
        link = self.base / "link.json"
        os.symlink(target, link)
        self.assertRefusedCleanly(self.cli("--root", link, "--out", self.base / "split.json"))
        self.assertFalse((self.base / "split.json").exists())

    def test_file_root_replaced_after_its_open_refuses(self):
        root = self.base / "model.json"
        root.write_bytes(b"{}\n")
        real, fired = os.fstat, []

        def fstat(fd):
            st = real(fd)
            if not fired and os.path.samestat(st, os.stat(root)):
                fired.append(True)
                os.replace(root, self.base / "moved.json")
                root.write_bytes(b"other bytes, another inode")
            return st
        with mock.patch.object(os, "fstat", fstat):
            with self.assertRaisesRegex(R.Refusal, "changed after it was opened"):
                R.split_unit(root, [])
        self.assertTrue(fired)


# [LAW:behavior-not-structure] Classify through the public split boundary so the
# original implementation fails on refused file units, not on a new signature.
class ClassifyThroughRoot(Fixture):
    def classify_file(self, name, data, attested=False):
        root = self.base / name
        root.write_bytes(data)
        out = self.base / (name + ".split")
        extra = ["--attestation", self.attest([(".", sha(data))])] if attested else []
        code, err = self.main("--root", root, "--out", out, *extra)
        self.assertEqual(code, 0, err)
        return json.loads(out.read_text())["leaves"]

    def test_file_unit_leaf_is_a_record_by_the_root_name(self):
        for name in ("model.json", "trace.JSONL", "nb.ipynb", "run.log", "run_manifest.bin"):
            with self.subTest(name=name):
                rows = self.classify_file(name, b"\x00binary")
                self.assertEqual([(r["path"], r["class"]) for r in rows], [(".", R.TRACKED)])

    def test_file_unit_leaf_without_a_record_name_follows_its_bytes(self):
        self.assertEqual(self.classify_file("weights.bin", b"\x00")[0]["class"], R.PAYLOAD)
        self.assertEqual(self.classify_file("notes.txt", b"notes")[0]["class"], R.TRACKED)

    def test_attested_file_unit_leaf_is_bulk_and_an_attested_record_name_refuses(self):
        self.assertEqual(self.classify_file("weights.bin", b"\x00", True)[0]["class"], R.BULK)
        root = self.base / "model.json"
        root.write_bytes(b"\x00")
        with self.assertRaisesRegex(R.Refusal, "scientific record"):
            R.split_unit(root, [self.attest([(".", sha(b"\x00"))])])

    def test_directory_leaf_name_is_its_own_last_component(self):
        self.unit = self.base / "unit.json"
        self.unit.mkdir()
        self.put("sub/model.json", b"\x00")
        self.put("weights.bin", b"\x00")
        rows = R.split_unit(self.unit, [])
        self.assertEqual([(r.path, r.cls) for r in rows],
                         [("sub/model.json", R.TRACKED), ("weights.bin", R.PAYLOAD)])


class FileRootFaults(Fixture):
    def root(self):
        root = self.base / "model.json"
        root.write_bytes(b"\x00record")
        return root

    def test_fifo_replacing_file_before_open_refuses_without_blocking(self):
        root = self.root()
        try:
            with FK.fifo_in_place(root, name="open", match=lambda p, *a, **kw: p == root,
                                  timeout=1) as fault:
                with self.assertRaisesRegex(R.Refusal, "changed after it was opened"):
                    R.split_unit(root, [])
            self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail(str(exc))

    def test_link_replacing_file_before_open_refuses_even_to_same_inode(self):
        root = self.root()
        target = self.base / "same-inode"
        os.link(root, target)
        with FK.swap_for_symlink("open", 1, root, target,
                                 match=lambda p, *a, **kw: p == root) as fault:
            with self.assertRaisesRegex(R.Refusal, "unit root.*ELOOP"):
                R.split_unit(root, [])
        self.assertEqual(fault.fired, 1)

    def test_file_parent_swapped_to_symlink_refuses(self):
        root = self.unit / "model.json"
        root.write_bytes(b"record")
        parked = self.base / "parked-parent"
        def replace():
            self.unit.rename(parked)
            self.unit.symlink_to(parked, target_is_directory=True)
        with before_open(lambda p, kw: p == str(self.unit), replace) as fired:
            with self.assertRaisesRegex(R.Refusal, re.escape(str(self.unit)) + r": (ENOTDIR|ELOOP)"):
                R.split_unit(root, [])
        self.assertTrue(fired)

    def test_file_parent_replaced_by_regular_file_names_parent_in_refusal(self):
        root = self.unit / "model.json"
        root.write_bytes(b"record")
        def replace():
            self.unit.rename(self.base / "parked-parent")
            self.unit.write_bytes(b"not a directory")
        with before_open(lambda p, kw: p == str(self.unit), replace) as fired:
            with self.assertRaisesRegex(R.Refusal, re.escape(str(self.unit)) + r": ENOTDIR"):
                R.split_unit(root, [])
        self.assertTrue(fired)

    def test_held_root_on_another_device_refuses(self):
        root = self.root()
        real = os.fstat
        def shifted(fd):
            st = real(fd)
            return types.SimpleNamespace(st_mode=st.st_mode, st_dev=st.st_dev + 1, st_ino=st.st_ino,
                                         st_size=st.st_size, st_mtime_ns=st.st_mtime_ns)
        with mock.patch.object(os, "fstat", shifted):
            with self.assertRaisesRegex(R.Refusal, "changed after it was opened"):
                R.split_unit(root, [])

    def test_held_root_must_be_regular_even_with_matching_identity(self):
        root = self.root()
        real = os.fstat
        def special(fd):
            st = real(fd)
            return types.SimpleNamespace(st_mode=stat.S_IFIFO, st_dev=st.st_dev, st_ino=st.st_ino,
                                         st_size=st.st_size, st_mtime_ns=st.st_mtime_ns)
        with mock.patch.object(os, "fstat", special):
            with self.assertRaisesRegex(R.Refusal, "changed after it was opened"):
                R.split_unit(root, [])

    def test_file_root_filesystem_errors_are_refusals_and_release_fds(self):
        root = self.root()
        before = len(os.listdir("/dev/fd"))
        for name, n in (("open", 1), ("open", 2), ("fstat", 1), ("close", 1), ("close", 2)):
            with self.subTest(name=name, n=n):
                with FK.inject_oserror(name, n, errno.EIO):
                    with self.assertRaisesRegex(R.Refusal, "EIO"):
                        R.split_unit(root, [])
                self.assertEqual(len(os.listdir("/dev/fd")), before)

    def test_unexpected_root_error_propagates(self):
        root = self.root()
        with FK.raise_unexpected("open", 1, RuntimeError):
            with self.assertRaisesRegex(RuntimeError, "unexpected"):
                R.split_unit(root, [])


# [LAW:behavior-not-structure] Pin the owning refusal so later checks cannot mask it.
class RootAndLeafRefusals(Fixture):
    def test_file_root_fifo_at_digest_open_refuses(self):
        root = self.base / "model.json"
        root.write_bytes(b"record")
        with FK.fifo_in_place(
                root, name="open",
                match=lambda p, *a, **kw: p == root.name and "dir_fd" in kw,
                timeout=5.0) as fault:
            with self.assertRaisesRegex(R.Refusal, "changed before it was hashed"):
                R.split_unit(root, [])
        self.assertEqual(fault.fired, 1)

    def test_directory_leaf_fifo_at_digest_open_refuses(self):
        leaf = self.unit / "model.json"
        leaf.write_bytes(b"record")
        with FK.fifo_in_place(
                leaf, name="open",
                match=lambda p, *a, **kw: p == leaf.name and "dir_fd" in kw,
                timeout=5.0) as fault:
            with self.assertRaisesRegex(R.Refusal, "changed before it was hashed"):
                R.split_unit(self.unit, [])
        self.assertEqual(fault.fired, 1)

    def test_open_root_fifo_refuses_at_kind_check(self):
        root = self.base / "fifo"
        os.mkfifo(root)
        with self.assertRaisesRegex(R.Refusal, "neither a real directory nor a regular file"):
            held = R.open_root(root)
            os.close(held.fd)

    def test_open_root_symlink_to_file_refuses_at_kind_check(self):
        target = self.base / "model.json"
        target.write_bytes(b"record")
        root = self.base / "link"
        root.symlink_to(target)
        with self.assertRaisesRegex(R.Refusal, "neither a real directory nor a regular file"):
            held = R.open_root(root)
            os.close(held.fd)

    def test_open_root_symlink_to_directory_refuses_at_kind_check(self):
        root = self.base / "link"
        root.symlink_to(self.unit, target_is_directory=True)
        with self.assertRaisesRegex(R.Refusal, "neither a real directory nor a regular file"):
            held = R.open_root(root)
            os.close(held.fd)

    def test_scan_file_root_rebound_to_symlink_refuses_before_hash(self):
        root = self.base / "model.json"
        root.write_bytes(b"record")
        held = R.open_root(root)
        try:
            sibling = self.base / "moved.json"
            root.rename(sibling)
            root.symlink_to(sibling)
            with self.assertRaisesRegex(R.Refusal, "changed after it was opened"):
                R.scan(held, str(root))
        finally:
            os.close(held.fd)

    def test_open_root_directory_replaced_by_file_refuses_enotdir(self):
        root = self.unit

        def replace():
            root.rename(self.base / "parked")
            root.write_bytes(b"not a directory")

        match = lambda p, kw: os.fspath(p) == str(root) and "dir_fd" not in kw
        with before_open(match, replace) as fired:
            with self.assertRaisesRegex(R.Refusal, "ENOTDIR"):
                held = R.open_root(root)
                os.close(held.fd)
        self.assertTrue(fired)


if __name__ == "__main__":
    unittest.main()
