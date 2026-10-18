"""Tests for move_plan_core's integer and nesting limits (Step 340).

Manifest bytes and TSV cells are untrusted text. An integer literal over the interpreter's digit limit
(sys.get_int_max_str_digits) or JSON nested past the recursion limit is one fdsafe.Refusal that names
the input, never a ValueError or RecursionError traceback. RED list for a pure function: each field
at, over and far over the limit, a negative literal, the limit switched off, and unexpected
exceptions from the calls around the parse.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from unittest import mock

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as core
from test_move_plan_core import (check_plans, leaf, manifest_bytes, occ, plan, repairs, req_row, risks,
                                 table, unit)

LIMIT = sys.get_int_max_str_digits()
BIG = "9" * 5000
AT_LIMIT = "9" * LIMIT
WHERE = "units[0].manifest_bytes"
DEEP = 100000


def big_manifest(token: str) -> bytes:
    return ('{"git_roots":[],"leaves":[],"root":"/p/u1","schema_version":' + token + "}").encode()


def nested(depth: int) -> bytes:
    """A Step 201 manifest whose git_roots holds one list nested depth deep (git_roots is read after the
    canonical re-encode, so only the parse and the re-encode see the nesting)."""
    return b'{"git_roots":[' + b"[" * depth + b"]" * depth + b'],"leaves":[],"root":"/p/u1","schema_version":1}'


def with_manifest(data: bytes) -> dict:
    u = unit()
    u["manifest_bytes"] = data
    u["comparison"] = None
    return u


class Refuses(unittest.TestCase):
    def refuses(self, call, names, *words):
        with self.assertRaises(fdsafe.Refusal) as caught:
            call()
        self.assertEqual(caught.exception.path, names)
        for word in words:
            self.assertIn(word, str(caught.exception))
        return caught.exception


class ManifestDigits(Refuses):
    def test_5000_digit_int_through_manifest_is_one_refusal(self):
        self.refuses(lambda: core._manifest(big_manifest(BIG), "m"), "m", "5000 digits", str(LIMIT))

    def test_5000_digit_negative_int_through_manifest_is_one_refusal(self):
        self.refuses(lambda: core._manifest(big_manifest("-" + BIG), "m"), "m", "5000 digits")

    def test_5000_digit_whole_document_is_one_refusal(self):
        self.refuses(lambda: core._manifest(BIG.encode(), "m"), "m", "digits")

    def test_5000_digit_int_through_build_plan_is_one_refusal(self):
        self.refuses(lambda: plan([with_manifest(big_manifest(BIG))]), WHERE, "5000 digits")

    def test_5000_digit_leaf_bytes_through_build_plan_is_one_refusal(self):
        data = manifest_bytes("/p/u1", {**leaf("/p/u1", "a.json"), "bytes": 7})
        data = data.replace(b'"bytes":7', b'"bytes":' + BIG.encode())
        self.assertIn(BIG.encode(), data)
        self.refuses(lambda: plan([with_manifest(data)]), WHERE, "digits")

    def test_an_int_at_the_limit_is_parsed(self):
        size = int(AT_LIMIT)
        data = manifest_bytes("/p/u1", {**leaf("/p/u1", "a.json"), "bytes": size})
        root, leaves, git, _ = core._manifest(data, "m")
        self.assertEqual((root, leaves[0][2][1], git), ("/p/u1", size, []))

    def test_a_negative_int_at_the_limit_reaches_the_leaf_check(self):
        lf = {**leaf("/p/u1", "a.json"), "bytes": -int(AT_LIMIT)}
        # the sign is not a digit: the leaf check, not the digit limit, refuses it
        self.refuses(lambda: core._manifest(manifest_bytes("/p/u1", lf), "m"), "/p/u1/a.json", "bytes")

    def test_no_interpreter_limit_parses_5000_digits(self):
        sys.set_int_max_str_digits(0)
        self.addCleanup(sys.set_int_max_str_digits, LIMIT)
        size = int(BIG)
        data = manifest_bytes("/p/u1", {**leaf("/p/u1", "a.json"), "bytes": size})
        self.assertEqual(core._manifest(data, "m")[1][0][2][1], size)


class ManifestNesting(Refuses):
    def test_100000_deep_list_through_manifest_is_one_refusal(self):
        self.refuses(lambda: core._manifest(b"[" * DEEP + b"]" * DEEP, "m"), "m", "nests too deeply")

    def test_100000_deep_git_roots_through_manifest_is_one_refusal(self):
        self.refuses(lambda: core._manifest(nested(DEEP), "m"), "m", "nests too deeply")

    def test_100000_deep_list_through_build_plan_is_one_refusal(self):
        self.refuses(lambda: plan([with_manifest(b"[" * DEEP + b"]" * DEEP)]), WHERE, "nests too deeply")

    def test_100000_deep_git_roots_through_build_plan_is_one_refusal(self):
        self.refuses(lambda: plan([with_manifest(nested(DEEP))]), WHERE, "nests too deeply")

    def test_every_depth_up_to_the_limit_refuses_and_never_raises(self):
        # The re-encode runs a few frames deeper than the parse, so some depth parses and then fails to
        # re-encode; every depth from 1 to the recursion limit must still end in one Refusal.
        real, outcomes = core.canonical, set()
        for depth in range(1, sys.getrecursionlimit() + 1):
            spy = mock.Mock(side_effect=real)
            with self.subTest(depth=depth), mock.patch.object(core, "canonical", spy):
                with self.assertRaises(fdsafe.Refusal) as caught:
                    core._manifest(nested(depth), "m")
                outcomes.add((caught.exception.path, str(caught.exception), spy.called))
        reasons = {(path, text) for path, text, _ in outcomes}
        self.assertEqual(reasons, {("m.git_roots[0]", "'m.git_roots[0]': expected an object, got list"),
                                   ("m", "'m': nests too deeply")})
        # positive control: at some depth the parse passed and the re-encode is what refused
        self.assertIn(("m", "'m': nests too deeply", True), outcomes)

    def test_shallow_nesting_reaches_the_git_roots_check(self):
        self.refuses(lambda: core._manifest(nested(3), "m"), "m.git_roots[0]", "expected an object")


class CellDigits(Refuses):
    TSV = "/m/plans/MOVE-REQUIREMENTS.tsv:2"

    def test_5000_digit_observed_bytes_is_one_refusal(self):
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1", observed=BIG))]
        self.refuses(lambda: plan(tables=tables), self.TSV, "5000 digits")

    def test_observed_bytes_at_the_limit_is_read(self):
        p = plan(tables=[table(req_row("MV-101", "/p/u1", "/v/p/u1", observed=AT_LIMIT))])
        self.assertEqual(p["units"][0]["observed_bytes"], int(AT_LIMIT))
        self.assertEqual(risks(p, "bytes-drift")[0]["items"], [f"annex {int(AT_LIMIT)}", "manifest 3"])

    def test_5000_digit_line_is_one_refusal(self):
        rep = repairs(("code/x.py", BIG, "/p/u1/a.json", "/m/experiments/c10r/runs/u1/a.json", 261))
        self.refuses(lambda: check_plans([occ()], rep), "/m/program/repairs.tsv:2", "5000 digits")

    def test_5000_digit_step_is_one_refusal(self):
        rep = repairs(("code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1/a.json", BIG))
        self.refuses(lambda: check_plans([occ()], rep), "/m/program/repairs.tsv:2", "5000 digits")

    def test_line_and_step_at_the_limit_are_read(self):
        rep = repairs(("code/x.py", AT_LIMIT, "/p/u1/a.json", "/m/x/a.json", 261))
        self.assertEqual([f[0] for f in check_plans([occ()], rep)], ["no-occurrence", "no-row"])
        self.refuses(lambda: check_plans([occ()], repairs(("code/x.py", 3, "/p/u1/a.json", "/m/x/a.json",
                                                             AT_LIMIT))),
                     "/m/program/repairs.tsv:2", "is not one of 261-269")


class OnlyTheParseAndReEncodeAreCovered(unittest.TestCase):
    """RecursionError is refused only from the parse and the re-encode; anything else propagates."""

    def test_recursion_error_between_the_parse_and_the_re_encode_propagates(self):
        with mock.patch.object(core.dup_find_core, "_manifest", side_effect=RecursionError("boom")):
            with self.assertRaises(RecursionError):
                plan([unit(comparison=None)])

    def test_unexpected_exceptions_from_the_parse_and_re_encode_propagate(self):
        for target in ((core.json, "loads"), (core, "canonical")):
            for exc in (ValueError, KeyError, RuntimeError):
                with self.subTest(target=target[1], exc=exc), mock.patch.object(*target, side_effect=exc("boom")):
                    with self.assertRaises(exc) as caught:
                        plan()
                    self.assertNotIsInstance(caught.exception, fdsafe.Refusal)


_AUDIT = {"installed": False, "on": False, "events": []}


def _audit(event, args):
    if _AUDIT["on"] and (event == "open" or event.startswith(("os.", "subprocess.", "shutil."))):
        _AUDIT["events"].append((event, args))


class AuditedLimits(unittest.TestCase):
    """The new refusals make no filesystem or process call (PEP 578 audit events, live positive control)."""

    def test_limit_refusals_make_no_filesystem_or_process_call(self):
        if not _AUDIT["installed"]:
            sys.addaudithook(_audit)  # a hook cannot be removed, so it records only inside the window
            _AUDIT["installed"] = True
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1", observed=BIG))]
        rep = repairs(("code/x.py", BIG, "/p/u1/a.json", "/m/x/a.json", 261))
        calls = [lambda: core._manifest(big_manifest(BIG), "m"), lambda: core._manifest(nested(DEEP), "m"),
                 lambda: plan(tables=tables), lambda: check_plans([occ()], rep)]
        warm = []
        for call in calls:  # warm-up outside the window: lazy imports may open files
            with self.assertRaises(fdsafe.Refusal) as caught:
                call()
            warm.append(str(caught.exception))
        seen = []
        _AUDIT["events"], _AUDIT["on"] = [], True
        try:
            os.listdir(scratch.name)  # positive control: the hook is live inside the window
            for call in calls:
                try:
                    call()
                except fdsafe.Refusal:
                    seen.append("refused")
        finally:
            _AUDIT["on"] = False
        self.assertEqual(_AUDIT["events"], [("os.listdir", (scratch.name,))])
        self.assertEqual(seen, ["refused"] * len(calls))
        self.assertEqual(len(warm), 4)


if __name__ == "__main__":
    unittest.main()
