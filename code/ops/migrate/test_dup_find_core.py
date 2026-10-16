"""Tests for dup_find_core: the pure comparison core of dup_find (ICM v2.1 Part 2, Step 216).

The core takes Step 201 manifests (unit_manifest.py's {schema_version, root, leaves, git_roots}) and
optional toolkit sha256 hint rows as values. RED list for a pure function: malformed input of each
field, boundary values and unexpected types; each refuses with fdsafe.Refusal.
"""
from __future__ import annotations

import builtins
import contextlib
import copy
import hashlib
import io
import itertools
import os
import shutil
import subprocess
import unittest
from unittest import mock

from ops.migrate import dup_find_core as core
from ops.migrate import fdsafe

_INODES = itertools.count(100)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def leaf(root: str, rel: str, data: bytes = b"x", kind: str = "file", link_text: str | None = None) -> dict:
    """A LeafRecord exactly as unit_manifest.py emits it."""
    if kind == "symlink":
        data = os.fsencode(link_text)
    elif kind == "socket":
        data = b""
    return {"source": f"{root}/{rel}", "kind": kind, "bytes": len(data), "sha256": sha(data),
            "link_text": link_text if kind == "symlink" else None, "device": 16777230,
            "inode": next(_INODES), "nlink": 1}


def manifest(root: str, *leaves: dict, git_roots: list | None = None) -> dict:
    out = {"schema_version": 1, "root": root, "leaves": list(leaves)}
    if git_roots is not None:
        out["git_roots"] = git_roots
    return out


def by_source(rows: list[dict]) -> dict:
    return {row["source"]: row for row in rows}


U, R1, R2 = "/v/unit", "/p/ref1", "/p/ref2"
DEFAULT = object()


class Classify(unittest.TestCase):
    def test_equal_to_a_reference_file_at_another_relpath(self):
        rows = core.classify(manifest(U, leaf(U, "a/x.json", b"same")),
                             [manifest(R1, leaf(R1, "other/y.json", b"same"))])
        self.assertEqual(rows, [{"source": f"{U}/a/x.json", "relpath": "a/x.json", "class": "equal",
                                 "equal_to": [f"{R1}/other/y.json"], "differing_from": [], "same_inode": [],
                                 "hint": None}])

    def test_equal_to_lists_every_equal_reference_path_sorted(self):
        rows = core.classify(manifest(U, leaf(U, "x", b"same")),
                             [manifest(R2, leaf(R2, "b", b"same"), leaf(R2, "c", b"no")),
                              manifest(R1, leaf(R1, "z", b"same"), leaf(R1, "a", b"same"))])
        self.assertEqual(rows[0]["class"], "equal")
        self.assertEqual(rows[0]["equal_to"], [f"{R1}/a", f"{R1}/z", f"{R2}/b"])

    def test_differing_same_relpath_other_bytes(self):
        rows = core.classify(manifest(U, leaf(U, "a/x.log", b"new")),
                             [manifest(R1, leaf(R1, "a/x.log", b"old"))])
        self.assertEqual(rows[0]["class"], "differing")
        self.assertEqual(rows[0]["differing_from"], [f"{R1}/a/x.log"])
        self.assertEqual(rows[0]["equal_to"], [])

    def test_unique_when_no_relpath_and_no_content_match(self):
        rows = core.classify(manifest(U, leaf(U, "a/x", b"one")), [manifest(R1, leaf(R1, "a/y", b"two"))])
        self.assertEqual(rows[0]["class"], "unique")
        self.assertEqual((rows[0]["equal_to"], rows[0]["differing_from"]), ([], []))

    def test_differing_from_excludes_an_equal_reference_at_the_same_relpath(self):
        # T216 ruling 1: /u/x = A, /r1/x = A, /r2/x = B.
        rows = core.classify(manifest("/u", leaf("/u", "x", b"A")),
                             [manifest("/r1", leaf("/r1", "x", b"A")), manifest("/r2", leaf("/r2", "x", b"B"))])
        self.assertEqual(rows[0]["class"], "equal")
        self.assertEqual(rows[0]["equal_to"], ["/r1/x"])
        self.assertEqual(rows[0]["differing_from"], ["/r2/x"])

    def test_differing_from_lists_every_differing_reference_at_one_relpath_sorted(self):
        # T216 ruling 1: two differing references at one relpath, given in reverse order, listed sorted.
        rows = core.classify(manifest("/u", leaf("/u", "x", b"A")),
                             [manifest("/r2", leaf("/r2", "x", b"C")), manifest("/r1", leaf("/r1", "x", b"B"))])
        self.assertEqual(rows[0]["class"], "differing")
        self.assertEqual(rows[0]["equal_to"], [])
        self.assertEqual(rows[0]["differing_from"], ["/r1/x", "/r2/x"])

    def test_equal_wins_and_keeps_the_differing_same_relpath_copy(self):
        rows = core.classify(manifest(U, leaf(U, "x", b"keep")),
                             [manifest(R1, leaf(R1, "x", b"other")), manifest(R2, leaf(R2, "q", b"keep"))])
        self.assertEqual(rows[0]["class"], "equal")
        self.assertEqual(rows[0]["equal_to"], [f"{R2}/q"])
        self.assertEqual(rows[0]["differing_from"], [f"{R1}/x"])

    def test_hard_link_to_a_reference_is_reported_in_same_inode(self):
        # T216 ruling 2: a hard link stays "equal" by content and is named, not hidden.
        unit_leaf = dict(leaf("/u", "x", b"A"), device=7, inode=42, nlink=2)
        rows = core.classify(manifest("/u", unit_leaf), [manifest("/r", dict(leaf("/r", "y", b"A"), device=7, inode=42, nlink=2))])
        self.assertEqual((rows[0]["class"], rows[0]["same_inode"]), ("equal", ["/r/y"]))
        rows = core.classify(manifest("/u", unit_leaf), [manifest("/r", dict(leaf("/r", "y", b"A"), device=7, inode=43))])
        self.assertEqual((rows[0]["class"], rows[0]["same_inode"]), ("equal", []))
        rows = core.classify(manifest("/u", unit_leaf), [manifest("/r", dict(leaf("/r", "y", b"A"), device=8, inode=42))])
        self.assertEqual((rows[0]["class"], rows[0]["same_inode"]), ("equal", []))
        rows = core.classify(manifest("/u", dict(unit_leaf, nlink=3)),
                             [manifest("/r2", dict(leaf("/r2", "b", b"A"), device=7, inode=42, nlink=3)),
                              manifest("/r1", dict(leaf("/r1", "c", b"A"), device=7, inode=42, nlink=3))])
        self.assertEqual(rows[0]["same_inode"], ["/r1/c", "/r2/b"])

    def test_relpath_is_relative_to_each_manifest_root(self):
        rows = core.classify(manifest(U, leaf(U, "d/e/f", b"1")), [manifest("/p/deep/ref", leaf("/p/deep/ref", "d/e/f", b"2"))])
        self.assertEqual(rows[0]["relpath"], "d/e/f")
        self.assertEqual(rows[0]["class"], "differing")

    def test_same_digest_other_kind_is_not_equal(self):
        # A symlink whose link text equals a file's bytes has the same sha256 and size, but other content.
        rows = core.classify(manifest(U, leaf(U, "x", b"target")),
                             [manifest(R1, leaf(R1, "x", kind="symlink", link_text="target"))])
        self.assertEqual(rows[0]["class"], "differing")
        self.assertEqual(rows[0]["equal_to"], [])

    def test_same_digest_other_byte_count_is_not_equal(self):
        unit_leaf = leaf(U, "x", b"abc")
        ref_leaf = dict(leaf(R1, "y", b"abc"), bytes=4)
        rows = core.classify(manifest(U, unit_leaf), [manifest(R1, ref_leaf)])
        self.assertEqual(rows[0]["class"], "unique")

    def test_symlinks_compare_by_link_text_digest(self):
        rows = core.classify(manifest(U, leaf(U, "l", kind="symlink", link_text="../t")),
                             [manifest(R1, leaf(R1, "m", kind="symlink", link_text="../t"),
                                       leaf(R1, "l", kind="symlink", link_text="../u"))])
        self.assertEqual(rows[0]["class"], "equal")
        self.assertEqual(rows[0]["equal_to"], [f"{R1}/m"])
        self.assertEqual(rows[0]["differing_from"], [f"{R1}/l"])

    def test_one_row_per_unit_leaf_in_relpath_utf8_order(self):
        unit = manifest(U, leaf(U, "b", b"1"), leaf(U, "a/z", b"2"), leaf(U, "é", b"3"), leaf(U, "a-", b"4"))
        rows = core.classify(unit, [manifest(R1)])
        self.assertEqual([r["relpath"] for r in rows], sorted(["b", "a/z", "é", "a-"], key=str.encode))
        self.assertTrue(all(r["class"] == "unique" for r in rows))

    def test_unit_leaves_are_not_compared_with_each_other(self):
        rows = core.classify(manifest(U, leaf(U, "a", b"same"), leaf(U, "b", b"same")), [manifest(R1)])
        self.assertEqual([r["class"] for r in rows], ["unique", "unique"])

    def test_git_roots_are_accepted_and_ignored(self):
        git_roots = [{"path": f"{U}/repo", "head": None, "branch": None, "dirty": []}]
        rows = core.classify(manifest(U, leaf(U, "x", b"1"), git_roots=git_roots),
                             [manifest(R1, leaf(R1, "x", b"1"), git_roots=[])])
        self.assertEqual(rows[0]["class"], "equal")

    def test_tuples_are_accepted_for_sequences(self):
        rows = core.classify(dict(manifest(U, leaf(U, "x", b"1")), leaves=(leaf(U, "x", b"1"),)),
                             (manifest(R1, leaf(R1, "x", b"1")),), ())
        self.assertEqual(rows[0]["class"], "equal")

    def test_output_has_only_comparison_fields(self):
        rows = core.classify(manifest(U, leaf(U, "a", b"1"), leaf(U, "b", b"2"), leaf(U, "c", b"3")),
                             [manifest(R1, leaf(R1, "q", b"1"), leaf(R1, "b", b"9"))],
                             [{"path": f"{U}/a", "sha256": sha(b"1")}])
        self.assertEqual({r["class"] for r in rows}, {"equal", "differing", "unique"})
        for row in rows:
            self.assertEqual(set(row), {"source", "relpath", "class", "equal_to", "differing_from", "same_inode",
                                        "hint"})
            self.assertNotRegex(repr(sorted(row)) + row["class"], r"(?i)delete|purge|skip|remove|action")

    def test_inputs_are_not_mutated(self):
        unit = manifest(U, leaf(U, "b", b"1"), leaf(U, "a", b"2"))
        refs = [manifest(R1, leaf(R1, "z", b"1"), leaf(R1, "a", b"x"))]
        hints = [{"path": f"{U}/a", "sha256": sha(b"0")}]
        before = copy.deepcopy((unit, refs, hints))
        core.classify(unit, refs, hints)
        self.assertEqual((unit, refs, hints), before)

    def test_result_lists_are_not_shared(self):
        rows = core.classify(manifest(U, leaf(U, "a", b"1"), leaf(U, "b", b"2")), [manifest(R1)])
        rows[0]["equal_to"].append("x")
        self.assertEqual(rows[1]["equal_to"], [])


class Boundaries(unittest.TestCase):
    def test_empty_unit_gives_no_rows(self):
        self.assertEqual(core.classify(manifest(U), [manifest(R1, leaf(R1, "x"))]), [])

    def test_empty_reference_manifest_makes_every_leaf_unique(self):
        rows = core.classify(manifest(U, leaf(U, "x")), [manifest(R1)])
        self.assertEqual(rows[0]["class"], "unique")

    def test_zero_byte_files_are_equal(self):
        rows = core.classify(manifest(U, leaf(U, "e", b"")), [manifest(R1, leaf(R1, "f", b""))])
        self.assertEqual(rows[0]["class"], "equal")

    def test_sockets_compare_by_kind_and_digest(self):
        rows = core.classify(manifest(U, leaf(U, "s", kind="socket")),
                             [manifest(R1, leaf(R1, "s", kind="socket"), leaf(R1, "e", b""))])
        self.assertEqual(rows[0]["equal_to"], [f"{R1}/s"])

    def test_large_and_zero_integers_are_accepted(self):
        big = dict(leaf(U, "x", b"1"), bytes=2**63, device=0, inode=0, nlink=1)
        rows = core.classify(manifest(U, big), [manifest(R1)])
        self.assertEqual(rows[0]["class"], "unique")

    def test_sibling_root_with_common_prefix_is_not_overlap(self):
        rows = core.classify(manifest("/p/u", leaf("/p/u", "x", b"1")), [manifest("/p/u2", leaf("/p/u2", "x", b"1"))])
        self.assertEqual(rows[0]["class"], "equal")

    def test_unit_root_at_depth_one(self):
        rows = core.classify(manifest("/u", leaf("/u", "x", b"1")), [manifest("/r", leaf("/r", "x", b"1"))])
        self.assertEqual((rows[0]["relpath"], rows[0]["class"]), ("x", "equal"))


class Hints(unittest.TestCase):
    def test_no_hint_gives_none(self):
        rows = core.classify(manifest(U, leaf(U, "x", b"1")), [manifest(R1)], [])
        self.assertIsNone(rows[0]["hint"])

    def test_agreeing_hint_is_reported(self):
        rows = core.classify(manifest(U, leaf(U, "x", b"1")), [manifest(R1)], [{"path": f"{U}/x", "sha256": sha(b"1")}])
        self.assertEqual(rows[0]["hint"], {"sha256": sha(b"1"), "agrees": True})

    def test_hint_that_claims_equality_does_not_decide(self):
        # The toolkit says the unit file has the reference's digest; the re-hashed manifest says otherwise.
        rows = core.classify(manifest(U, leaf(U, "x", b"new")), [manifest(R1, leaf(R1, "x", b"old"), leaf(R1, "y", b"old"))],
                             [{"path": f"{U}/x", "sha256": sha(b"old")}])
        self.assertEqual(rows[0]["class"], "differing")
        self.assertEqual(rows[0]["equal_to"], [])
        self.assertEqual(rows[0]["hint"], {"sha256": sha(b"old"), "agrees": False})

    def test_hint_that_denies_equality_does_not_decide(self):
        rows = core.classify(manifest(U, leaf(U, "x", b"same")), [manifest(R1, leaf(R1, "y", b"same"))],
                             [{"path": f"{U}/x", "sha256": sha(b"else")}, {"path": f"{R1}/y", "sha256": sha(b"else2")}])
        self.assertEqual(rows[0]["class"], "equal")
        self.assertEqual(rows[0]["equal_to"], [f"{R1}/y"])
        self.assertFalse(rows[0]["hint"]["agrees"])

    def test_hint_for_a_path_outside_the_unit_is_not_attached(self):
        rows = core.classify(manifest(U, leaf(U, "x", b"1")), [manifest(R1, leaf(R1, "x", b"1"))],
                             [{"path": f"{R1}/x", "sha256": sha(b"1")}, {"path": "/elsewhere/x", "sha256": sha(b"1")}])
        self.assertIsNone(rows[0]["hint"])


class NoFilesystem(unittest.TestCase):
    def test_classify_makes_no_filesystem_or_subprocess_call(self):
        unit = manifest(U, leaf(U, "a", b"1"), leaf(U, "b", b"2"), leaf(U, "l", kind="symlink", link_text="a"))
        refs = [manifest(R1, leaf(R1, "a", b"1"), leaf(R1, "b", b"3"))]
        hints = [{"path": f"{U}/a", "sha256": sha(b"1")}]

        def forbidden(*args, **kwargs):
            raise AssertionError(f"filesystem or process call: {args!r}")

        names = ["open", "stat", "lstat", "fstat", "scandir", "listdir", "readlink", "getcwd", "access",
                 "walk", "path.exists", "path.lexists", "path.isdir", "path.isfile", "path.islink",
                 "path.realpath", "path.abspath", "path.samefile", "getenv"]
        with contextlib.ExitStack() as stack:
            for name in names:
                target = os.path if name.startswith("path.") else os
                stack.enter_context(mock.patch.object(target, name.split(".")[-1], forbidden))
            for target, name in [(builtins, "open"), (io, "open"), (subprocess, "run"), (subprocess, "Popen"),
                                 (shutil, "copy"), (os, "environ")]:
                stack.enter_context(mock.patch.object(target, name, forbidden if name != "environ" else {}))
            rows = core.classify(unit, refs, hints)
        self.assertEqual([r["class"] for r in rows], ["equal", "differing", "unique"])

    def test_module_names_no_filesystem_entry_point(self):
        text = core.__loader__.get_source(core.__name__)
        for token in ("import os", "open(", "import subprocess", "import shutil", "import time", "import datetime",
                      "os.environ", "getenv"):
            self.assertFalse(token in text, f"dup_find_core names {token!r}")


class Malformed(unittest.TestCase):
    """Every malformed field refuses with fdsafe.Refusal; nothing is guessed or repaired."""

    def refuses(self, unit=DEFAULT, refs=DEFAULT, hints=(), names=None):
        unit = manifest(U, leaf(U, "x", b"1")) if unit is DEFAULT else unit
        refs = [manifest(R1, leaf(R1, "x", b"1"))] if refs is DEFAULT else refs
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.classify(unit, refs, hints)
        if names is not None:
            self.assertEqual(caught.exception.path, names)
            self.assertIn(repr(names), str(caught.exception))
        return caught.exception

    def unit_with(self, **fields):
        return manifest(U, dict(leaf(U, "x", b"1"), **fields))

    # top-level types
    def test_unit_not_a_mapping(self):
        for bad in (None, [], "m", 1, (U, [])):
            with self.subTest(bad=bad):
                self.refuses(unit=bad)

    def test_references_not_a_list(self):
        for bad in (None, "refs", manifest(R1), 1, iter([manifest(R1)])):
            with self.subTest(bad=type(bad)):
                self.refuses(refs=bad)

    def test_no_reference_manifest(self):
        self.refuses(refs=[])

    def test_reference_not_a_mapping(self):
        for bad in (None, [], "m"):
            with self.subTest(bad=bad):
                self.refuses(refs=[bad])

    def test_hints_not_a_list(self):
        for bad in (None, "h", {"path": f"{U}/x", "sha256": sha(b"1")}, iter([])):
            with self.subTest(bad=type(bad)):
                self.refuses(hints=bad)

    # manifest fields
    def test_manifest_missing_field(self):
        for key in ("schema_version", "root", "leaves"):
            unit = manifest(U, leaf(U, "x"))
            del unit[key]
            with self.subTest(key=key):
                self.refuses(unit=unit)
                ref = manifest(R1)
                del ref[key]
                self.refuses(refs=[ref])

    def test_manifest_unknown_field(self):
        self.refuses(unit=dict(manifest(U, leaf(U, "x")), extra=1))
        self.refuses(refs=[dict(manifest(R1), extra=1)])

    def test_schema_version(self):
        for bad in (0, 2, "1", True, 1.0, None):
            with self.subTest(bad=bad):
                self.refuses(unit=dict(manifest(U, leaf(U, "x")), schema_version=bad))
                self.refuses(refs=[dict(manifest(R1), schema_version=bad)])

    def test_root(self):
        for bad in (None, 1, b"/v/unit", "", "v/unit", "/v/unit/", "/v//unit", "//v/unit", "/v/./unit", "/v/x/../unit", "/v/\0u"):
            with self.subTest(bad=bad):
                self.refuses(unit=dict(manifest(U), root=bad))
                self.refuses(refs=[dict(manifest(R1), root=bad)])

    def test_leaves_not_a_list(self):
        for bad in (None, "x", {}, leaf(U, "x"), iter([])):
            with self.subTest(bad=type(bad)):
                self.refuses(unit=dict(manifest(U), leaves=bad))
                self.refuses(refs=[dict(manifest(R1), leaves=bad)])

    # leaf fields
    def test_leaf_not_a_mapping(self):
        for bad in (None, "x", [], (f"{U}/x",)):
            with self.subTest(bad=bad):
                self.refuses(unit=dict(manifest(U), leaves=[bad]))
                self.refuses(refs=[dict(manifest(R1), leaves=[bad])])

    def test_leaf_missing_field(self):
        for key in leaf(U, "x"):
            row = leaf(U, "x")
            del row[key]
            with self.subTest(key=key):
                self.refuses(unit=manifest(U, row))
                ref_row = leaf(R1, "x")
                del ref_row[key]
                self.refuses(refs=[manifest(R1, ref_row)])

    def test_leaf_unknown_field(self):
        self.refuses(unit=self.unit_with(mtime_ns=1), names=f"{U}/x")
        self.refuses(refs=[manifest(R1, dict(leaf(R1, "x"), extra=None))], names=f"{R1}/x")

    def test_source(self):
        for bad in (None, 1, b"/v/unit/x", "", "x", "/v/unit", "/v/unit/", "/v/unit//x", "/v/unit/./x",
                    "/v/unit/a/../x", "/v/unit/..", "/v/unit2/x", "/v/other/x", "/v/unit/\udcff", "/v/unit/a\0b"):
            with self.subTest(bad=bad):
                self.refuses(unit=self.unit_with(source=bad))
                self.refuses(refs=[manifest(R1, dict(leaf(R1, "x"), source=bad))])

    def test_kind(self):
        for bad in (None, "directory", "git-root", "FILE", "link", 1):
            with self.subTest(bad=bad):
                self.refuses(unit=self.unit_with(kind=bad), names=f"{U}/x")
                self.refuses(refs=[manifest(R1, dict(leaf(R1, "x"), kind=bad))], names=f"{R1}/x")

    def test_bytes(self):
        for bad in (-1, True, False, 1.0, "1", None):
            with self.subTest(bad=bad):
                self.refuses(unit=self.unit_with(bytes=bad), names=f"{U}/x")
                self.refuses(refs=[manifest(R1, dict(leaf(R1, "x"), bytes=bad))], names=f"{R1}/x")

    def test_sha256(self):
        good = sha(b"1")
        for bad in (good.upper(), good[:-1], good + "0", "g" * 64, " " + good[1:], None, 1, 10**63, good.encode()):
            with self.subTest(bad=bad):
                self.refuses(unit=self.unit_with(sha256=bad), names=f"{U}/x")
                self.refuses(refs=[manifest(R1, dict(leaf(R1, "x"), sha256=bad))], names=f"{R1}/x")

    def test_link_text(self):
        self.refuses(unit=self.unit_with(link_text="t"), names=f"{U}/x")
        self.refuses(unit=self.unit_with(kind="socket", link_text=""), names=f"{U}/x")
        for bad in (None, 1, b"t"):
            with self.subTest(bad=bad):
                link = dict(leaf(U, "x", kind="symlink", link_text="t"), link_text=bad)
                self.refuses(unit=manifest(U, link), names=f"{U}/x")
                self.refuses(refs=[manifest(R1, dict(leaf(R1, "x", kind="symlink", link_text="t"), link_text=bad))])

    def test_device_inode_nlink(self):
        for key, bads in (("device", (-1, True, 1.0, "1", None)), ("inode", (-1, False, 2.0, "2", None)),
                          ("nlink", (0, -1, True, 1.0, "1", None))):
            for bad in bads:
                with self.subTest(key=key, bad=bad):
                    self.refuses(unit=self.unit_with(**{key: bad}), names=f"{U}/x")
                    self.refuses(refs=[manifest(R1, dict(leaf(R1, "x"), **{key: bad}))], names=f"{R1}/x")

    def test_duplicate_source_in_one_manifest(self):
        self.refuses(unit=manifest(U, leaf(U, "x", b"1"), leaf(U, "x", b"1")), names=f"{U}/x")
        self.refuses(refs=[manifest(R1, leaf(R1, "y", b"1"), leaf(R1, "y", b"2"))], names=f"{R1}/y")

    # roots that overlap would compare a file with itself
    def test_reference_root_equal_to_unit_root(self):
        self.refuses(refs=[manifest(U, leaf(U, "x", b"1"))], names=U)

    def test_reference_root_inside_or_around_unit_root(self):
        self.refuses(refs=[manifest(f"{U}/sub", leaf(f"{U}/sub", "x"))], names=f"{U}/sub")
        self.refuses(refs=[manifest("/v", leaf("/v", "unit/x", b"1"))], names="/v")
        self.refuses(refs=[manifest("/", leaf("", "y"))], names="/")

    def test_reference_roots_overlap_each_other(self):
        self.refuses(refs=[manifest(R1, leaf(R1, "a")), manifest(R1, leaf(R1, "b"))], names=R1)
        self.refuses(refs=[manifest(R1, leaf(R1, "a")), manifest(f"{R1}/a2", leaf(f"{R1}/a2", "b"))], names=f"{R1}/a2")

    # hint rows
    def test_hint_row_not_a_mapping(self):
        for bad in (None, (f"{U}/x", sha(b"1")), f"{U}/x"):
            with self.subTest(bad=bad):
                self.refuses(hints=[bad])

    def test_hint_row_fields(self):
        good = {"path": f"{U}/x", "sha256": sha(b"1")}
        for key in good:
            row = dict(good)
            del row[key]
            with self.subTest(missing=key):
                self.refuses(hints=[row])
        self.refuses(hints=[dict(good, size=1)], names=f"{U}/x")
        for bad in (None, 1, "", "x", "/v/unit/./x", "/v/unit/x/", "//v/unit/x", b"/v/unit/x", "/v/\udcffx"):
            with self.subTest(path=bad):
                self.refuses(hints=[dict(good, path=bad)])
        for bad in (None, 1, 10**63, sha(b"1").upper(), sha(b"1")[:10], "z" * 64):
            with self.subTest(sha256=bad):
                self.refuses(hints=[dict(good, sha256=bad)], names=f"{U}/x")

    def test_duplicate_hint_path(self):
        row = {"path": f"{U}/x", "sha256": sha(b"1")}
        self.refuses(hints=[row, dict(row)], names=f"{U}/x")
        self.refuses(hints=[row, dict(row, sha256=sha(b"2"))], names=f"{U}/x")

    def test_refusal_is_one_line_naming_the_path(self):
        exc = self.refuses(unit=self.unit_with(bytes=-1), names=f"{U}/x")
        self.assertEqual(len(str(exc).splitlines()), 1)
        self.assertIsNone(exc.errno)


if __name__ == "__main__":
    unittest.main()
