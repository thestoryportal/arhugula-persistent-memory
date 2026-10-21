"""Behavioral contract for the pure notebook comparison core (T382)."""
import builtins
import contextlib
import hashlib
import io
import json
import os
import pathlib
import random
import shutil
import socket
import subprocess
import time
import unittest
from collections.abc import Mapping
from unittest import mock

from ops.migrate import fdsafe
from ops.migrate import notebook_compare_core as core
from ops.migrate.unit_manifest import canonical

C, L = "/checkpoint/é.ipynb", "/live/é.ipynb"
PAIR = ("checkpoint", "live", "status", "checkpoint_sha256", "live_sha256",
        "checkpoint_cells", "live_cells", "unique_cells")
CELL = ("checkpoint", "index", "cell_type", "cell_sha256", "source_sha256", "in_live")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def cell(source="x", kind="code", **extra):
    return dict(cell_type=kind, source=source, **extra)


def notebook(cells, **metadata):
    return json.dumps(dict(cells=cells, metadata=metadata, nbformat=4, nbformat_minor=5)).encode()


@contextlib.contextmanager
def forbid_external_access():
    class UnreadableEnvironment(Mapping):
        def __getitem__(self, key):
            raise AssertionError("os.environ access")

        def __iter__(self):
            raise AssertionError("os.environ iteration")

        def __len__(self):
            raise AssertionError("os.environ length")

    def forbidden(*args, **kwargs):
        raise AssertionError("external access")

    targets = [(module, name)
               for module in (os, os.path, time, random, subprocess, shutil, socket, pathlib.Path)
               for name in dir(module)
               if not name.startswith("_") and callable(getattr(module, name))
               and not isinstance(getattr(module, name), type)]
    targets.extend(((builtins, "open"), (io, "open")))
    with contextlib.ExitStack() as stack:
        for target, name in targets:
            stack.enter_context(mock.patch.object(target, name, new=forbidden))
        stack.enter_context(mock.patch.object(os, "environ", UnreadableEnvironment()))
        yield


class Compare(unittest.TestCase):
    def test_exact_and_row_shape(self):
        cells = [cell(["α\n", "β"]), cell("text", "markdown"), cell("", "raw")]
        data = notebook(cells)
        pair, rows = core.compare(C, data, L, data)
        self.assertEqual(core.PAIR_FIELDS, PAIR)
        self.assertEqual(core.CELL_FIELDS, CELL)
        self.assertEqual(tuple(pair), PAIR)
        self.assertEqual(pair, dict(zip(PAIR, (C, L, "exact", sha(data), sha(data), "3", "3", "0"))))
        for i, row in enumerate(rows):
            self.assertEqual(tuple(row), CELL)
            source = cells[i]["source"]
            text = source if isinstance(source, str) else "".join(source)
            self.assertEqual(row, dict(zip(CELL, (C, str(i), cells[i]["cell_type"],
                                                 sha(canonical(cells[i])), sha(text.encode()), "yes"))))
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(isinstance(v, str) for row in [pair, *rows] for v in row.values()))

    def test_differing_same_cells(self):
        a, b = notebook([cell()], version=1), notebook([cell()], version=2)
        pair, rows = core.compare(C, a, L, b)
        self.assertEqual(pair["status"], "differing")
        self.assertEqual((pair["checkpoint_sha256"], pair["live_sha256"]), (sha(a), sha(b)))
        self.assertEqual([r["in_live"] for r in rows], ["yes"])
        self.assertEqual(pair["unique_cells"], "0")

    def test_empty_checkpoint(self):
        pair, rows = core.compare(C, notebook([]), L, notebook([cell()] * 5))
        self.assertEqual(rows, [])
        self.assertEqual([pair[k] for k in ("status", "checkpoint_cells", "live_cells", "unique_cells")],
                         ["differing", "0", "5", "0"])

    def test_one_unique_cell(self):
        pair, rows = core.compare(C, notebook([cell("a"), cell("b"), cell("a")]),
                                  L, notebook([cell("a", "raw")]))
        self.assertEqual([r["in_live"] for r in rows], ["yes", "no", "yes"])
        self.assertEqual(pair["unique_cells"], "1")

    def test_empty_sources(self):
        data = notebook([cell([]), cell("")])
        for live_cells, membership in (([cell([])], "yes"), ([cell("")], "yes"),
                                       ([cell("x")], "no"), ([], "no")):
            with self.subTest(live_cells=live_cells):
                pair, rows = core.compare(C, data, L, notebook(live_cells))
                self.assertEqual(pair["live_cells"], str(len(live_cells)))
                self.assertEqual([row["source_sha256"] for row in rows],
                                 [hashlib.sha256(b"").hexdigest()] * 2)
                self.assertEqual([row["in_live"] for row in rows], [membership] * 2)

    def test_live_empty_source_list(self):
        pair, rows = core.compare(C, notebook([cell("x")]), L, notebook([cell([])]))
        self.assertEqual(pair["live_cells"], "1")
        self.assertEqual([row["in_live"] for row in rows], ["no"])

    def test_source_representation_and_outputs(self):
        a = cell(["x", "\n"], outputs=[])
        b = cell("x\n", outputs=[{"text": "other"}])
        _, rows = core.compare(C, notebook([a, b]), L, notebook([b]))
        self.assertEqual(rows[0]["source_sha256"], rows[1]["source_sha256"])
        self.assertNotEqual(rows[0]["cell_sha256"], rows[1]["cell_sha256"])
        self.assertEqual([r["in_live"] for r in rows], ["yes", "yes"])

    def test_unmatched(self):
        for cells in ([], [cell(), cell()]):
            with self.subTest(count=len(cells)):
                pair, rows = core.compare(C, notebook(cells), L, None)
                self.assertEqual(pair["status"], "unmatched")
                self.assertEqual(pair["live"], L)
                self.assertEqual(pair["live_sha256"], "")
                self.assertEqual(pair["live_cells"], "")
                self.assertEqual(pair["unique_cells"], str(len(cells)))
                self.assertEqual([r["in_live"] for r in rows], ["no"] * len(cells))

    def refuses_both(self, data, index=None):
        good = notebook([])
        for checkpoint, live, path in ((data, good, C), (good, data, L), (data, data, C)):
            with self.subTest(path=path, data=data):
                with self.assertRaises(fdsafe.Refusal) as caught:
                    core.compare(C, checkpoint, L, live)
                self.assertEqual(caught.exception.path, path)
                if index is not None:
                    self.assertIn(f"cells[{index}]", str(caught.exception))

    def test_invalid_encoding_and_json(self):
        for data in (b"\xff", b"{", b""):
            self.refuses_both(data)

    def test_invalid_utf8_inside_json_string(self):
        self.refuses_both(b'{"cells": [], "x": "\xff"}')

    def test_unexpected_json_error_propagates(self):
        error = RuntimeError("x")
        with mock.patch.object(core.json, "loads", side_effect=error):
            with self.assertRaises(RuntimeError) as caught:
                core.compare(C, b'{"cells": []}', L, None)
        self.assertIs(caught.exception, error)

    def test_lone_surrogate_source_string(self):
        self.refuses_both(notebook([cell(), cell("\ud800")]), 1)

    def test_lone_surrogate_source_list(self):
        self.refuses_both(notebook([cell(), cell(["x", "\ud800"])]), 1)

    def test_lone_surrogate_outputs(self):
        self.refuses_both(notebook([cell(), cell(outputs=[{"text": "\ud800"}])]), 1)

    def test_source_encoding_is_strict_independently_of_canonical(self):
        data = notebook([cell("\ud800")])
        # Isolate source encoding so canonical's strict encoding cannot mask it.
        with mock.patch.object(core, "canonical", return_value=b"{}"):
            self.refuses_both(data, 0)

    def test_unexpected_canonical_error_propagates(self):
        data = notebook([cell()])
        good = notebook([])
        error = RuntimeError("x")
        for checkpoint, live in ((data, good), (good, data)):
            with self.subTest(checkpoint=checkpoint):
                with mock.patch.object(core, "canonical", side_effect=error):
                    with self.assertRaises(RuntimeError) as caught:
                        core.compare(C, checkpoint, L, live)
                    self.assertIs(caught.exception, error)

    def test_duplicate_keys(self):
        self.refuses_both(b'{"cells": [], "cells": []}')
        self.refuses_both(b'{"cells": [{"cell_type":"raw","source":""},'
                          b'{"cell_type":"code","source":"x","source":"y"}]}', 1)

    def test_nonfinite_constants(self):
        for token in ("NaN", "Infinity", "-Infinity"):
            self.refuses_both(('{"cells": [], "metadata": ' + token + "}").encode())
            self.refuses_both(('{"cells": [{"cell_type":"code","source":"", "outputs":['
                               + token + "]}]}").encode(), 0)

    def test_notebook_shape(self):
        for value in ([], None, 1, "x", {}, {"cells": {}}, {"cells": None}):
            self.refuses_both(json.dumps(value).encode())

    def test_cell_shape(self):
        for bad in ([], None, 1, {}, {"source": "x"}, cell(kind=1), cell(kind=[]),
                    cell(kind="heading"), {"cell_type": "code"}, cell(1), cell(["x", 1])):
            self.refuses_both(notebook([cell(), bad]), 1)

    def test_purity(self):
        data = notebook([cell()])
        cases = (data, notebook([cell("other")]), None)
        expected = []
        for live in cases:
            pair, rows = core.compare(C, data, L, live)
            expected.append((pair, rows, core.render(PAIR, [pair]), core.render(CELL, rows)))
        with forbid_external_access():
            for live, (expected_pair, expected_rows, expected_result, expected_cells) in zip(cases, expected):
                pair, rows = core.compare(C, data, L, live)
                result = core.render(PAIR, [pair])
                self.assertEqual((pair, rows), (expected_pair, expected_rows))
                self.assertEqual(result, expected_result)
                self.assertEqual(core.render(CELL, rows), expected_cells)
                self.assertEqual(len(rows), 1)
                self.assertTrue(result.startswith(b"checkpoint\tlive\t"))

    def test_duplicate_keys_at_every_level(self):
        first = json.dumps(cell()).encode()
        for fragment, index in (
            (b'{"cells":[],"nbformat":4,"nbformat":4}', None),
            (b'{"cells":[],"metadata":{},"metadata":{}}', None),
            (b'{"cells":[],"metadata":{"x":1,"x":2}}', None),
            (b'{"cell_type":"code","cell_type":"raw","source":"x"}', 1),
            (b'{"cell_type":"code","source":"x","source":"y"}', 1),
            (b'{"cell_type":"code","source":"x","metadata":{},"metadata":{}}', 1),
            (b'{"cell_type":"code","source":"x","metadata":{"x":1,"x":2}}', 1),
            (b'{"cell_type":"code","source":"x","outputs":[{"text":"a","text":"b"}]}', 1),
        ):
            data = fragment if index is None else b'{"cells":[' + first + b',' + fragment + b']}'
            self.refuses_both(data, index)

    def test_exact_source_text_hashes(self):
        for source in ("x\n", " x", "x ", "\tx", "X", ["x", "\n"], ["", "x"], "e\u0301"):
            with self.subTest(source=source):
                item = cell(source)
                text = source if isinstance(source, str) else "".join(source)
                _, rows = core.compare(C, notebook([item]), L, None)
                self.assertEqual(rows[0]["source_sha256"], hashlib.sha256(text.encode("utf-8")).hexdigest())
                self.assertEqual(rows[0]["cell_sha256"], hashlib.sha256(canonical(item)).hexdigest())

    def test_source_whitespace_and_case_membership(self):
        for source in ("x\n", " x", "x ", "\tx", "X"):
            for left, right in ((source, "x"), ("x", source)):
                with self.subTest(left=left, right=right):
                    _, rows = core.compare(C, notebook([cell(left), cell(right)]), L, notebook([cell(right)]))
                    self.assertNotEqual(rows[0]["source_sha256"], rows[1]["source_sha256"])
                    self.assertEqual([row["in_live"] for row in rows], ["no", "yes"])

    def test_unexpected_exception_types_propagate(self):
        data, empty = notebook([cell()]), notebook([])
        for target, name in ((core.json, "loads"), (core, "canonical")):
            for error_type in (ValueError, KeyError, TypeError, RuntimeError):
                for checkpoint, live in ((data, empty), (empty, data)):
                    with self.subTest(function=name, error=error_type.__name__, checkpoint=checkpoint):
                        error = error_type("x")
                        with mock.patch.object(target, name, side_effect=error):
                            with self.assertRaises(error_type) as caught:
                                core.compare(C, checkpoint, L, live)
                        self.assertIs(type(caught.exception), error_type)
                        self.assertIs(caught.exception, error)
                        self.assertNotIsInstance(caught.exception, fdsafe.Refusal)


class Render(unittest.TestCase):
    def test_unexpected_encoding_exception_types_propagate(self):
        for error_type in (ValueError, KeyError, TypeError, RuntimeError):
            with self.subTest(error=error_type.__name__):
                error = error_type("x")

                class BrokenText(str):
                    def encode(self, *args, **kwargs):
                        raise error

                with self.assertRaises(error_type) as caught:
                    core.render(("path",), [{"path": BrokenText("x")}])
                self.assertIs(type(caught.exception), error_type)
                self.assertIs(caught.exception, error)
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)

    def test_tab_in_field_name(self):
        field = "bad\tfield"
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.render((field,), [])
        self.assertEqual(caught.exception.path, field)

    def test_unencodable_field_name(self):
        field = "bad\udcfffield"
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.render((field,), [])
        self.assertEqual(caught.exception.path, field)

    def test_integer_value_is_not_refusal(self):
        with self.assertRaises(AttributeError) as caught:
            core.render(("path",), [{"path": 1}])
        self.assertNotIsInstance(caught.exception, fdsafe.Refusal)

    def test_unencodable_pair_value(self):
        pair, _ = core.compare(C, notebook([]), L, None)
        pair["checkpoint"] = "/checkpoint/\udcff.ipynb"
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.render(PAIR, [pair])
        self.assertEqual(caught.exception.path, "checkpoint")

    def test_exact_bytes_and_empty(self):
        fields = ("checkpoint", "status")
        rows = [{"status": "exact", "checkpoint": C}, {"checkpoint": L, "status": "unmatched"}]
        self.assertEqual(core.render(fields, rows),
                         f"checkpoint\tstatus\n{C}\texact\n{L}\tunmatched\n".encode())
        self.assertEqual(core.render(fields, []), b"checkpoint\tstatus\n")

    def test_control_characters(self):
        for char in "\t\r\n":
            with self.subTest(char=char):
                with self.assertRaises(fdsafe.Refusal) as caught:
                    core.render(("path",), [{"path": "a" + char + "b"}])
                self.assertEqual(caught.exception.path, "path")

    def test_wrong_keys(self):
        for row, field in (({}, "path"), ({"path": "a", "extra": "b"}, "extra")):
            with self.subTest(row=row):
                with self.assertRaises(fdsafe.Refusal) as caught:
                    core.render(("path",), [row])
                self.assertEqual(caught.exception.path, field)


if __name__ == "__main__":
    unittest.main()
