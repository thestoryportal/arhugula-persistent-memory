"""Tests for ledger_db_core (Part 2 Step 272): the four ledger_db reports from rows and numbers.

Pure core, so the RED list is the pure-function list: each fixture the step names, malformed input of
each field, boundary values and unexpected types. Every fixture is built from Python values here."""
from __future__ import annotations

import ast
import builtins
import copy
import os
import unittest
from unittest import mock

from ops.migrate import fdsafe
from ops.migrate import ledger_db_core as core

SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64
GiB = 1 << 30

ANNEX = [
    {"requirement_id": "MV-1", "source": "/m/u1", "target": "/v/u1", "action": "HOLD"},
    {"requirement_id": "MV-2", "source": "/m/u2", "target": "/v/u2", "action": "HOLD"},
    {"requirement_id": "MV-3", "source": "/m/u3", "target": "/v/u3", "action": "HOLD"},
    {"requirement_id": "MV-9", "source": "/m/keep", "target": "/m/keep", "action": "KEEP"},
]


def leaf(source, sha=SHA_A, size=10, kind="file"):
    return {"source": source, "kind": kind, "bytes": size, "sha256": sha, "link_text": None,
            "device": 1, "inode": 2, "nlink": 1}


def entry(eid, replaces, moves, leaves):
    return {"id": eid, "replaces": list(replaces), "moves": [{"source": s, "target": t} for s, t in moves],
            "leaves": list(leaves)}


def base():
    """Two entries that are clean: every report is empty."""
    return {
        "entries": [
            entry("E1", ["MV-1"], [("/m/u1", "/d/u1")], [leaf("/m/u1/x.json", SHA_A), leaf("/m/u1/y.json", SHA_B)]),
            entry("E2", ["MV-2"], [("/m/u2", "/d/u2")], [leaf("/m/u2/z.json", SHA_C)]),
        ],
        "annex_rows": copy.deepcopy(ANNEX),
        "toolkit_rows": [("/m/u1/x.json", SHA_A), ("/m/u1/y.json", SHA_B), ("/m/u2/z.json", SHA_C)],
        "existing_targets": [],
        "free_bytes": {"/d": 100 * GiB},
        "floor_bytes": 20 * GiB,
        "same_filesystem": {("/m/u1/x.json", "/d"): True, ("/m/u1/y.json", "/d"): True,
                            ("/m/u2/z.json", "/d"): True},
    }


def run(kw):
    return core.compute(**kw)


class CleanInput(unittest.TestCase):
    def test_clean_plan_has_four_empty_reports(self):
        r = run(base())
        self.assertEqual((r.drift, r.cross_unit_dups, r.targets, r.capacity), ((), (), (), ()))

    def test_inputs_are_not_mutated(self):
        kw = base()
        kw["toolkit_rows"][0] = ("/m/u1/x.json", SHA_D)
        before = copy.deepcopy(kw)
        run(kw)
        self.assertEqual(kw, before)

    def test_column_names(self):
        self.assertEqual(core.DRIFT_COLUMNS, ("status", "entry", "source", "fresh_sha256", "toolkit_sha256"))
        self.assertEqual(core.DUP_COLUMNS, ("sha256", "bytes", "entry", "source"))
        self.assertEqual(core.TARGET_COLUMNS, ("kind", "entry", "source", "target"))
        self.assertEqual(core.CAPACITY_COLUMNS, ("root", "needed_bytes", "free_bytes", "floor_bytes", "budget_bytes"))


class Drift(unittest.TestCase):
    def test_drifted_file(self):
        kw = base()
        kw["toolkit_rows"][0] = ("/m/u1/x.json", SHA_D)
        self.assertEqual(run(kw).drift, (("drift", "E1", "/m/u1/x.json", SHA_A, SHA_D),))

    def test_toolkit_missing_leaf_is_not_drift(self):
        kw = base()
        del kw["toolkit_rows"][1]
        self.assertEqual(run(kw).drift, (("toolkit-missing", "E1", "/m/u1/y.json", SHA_B, ""),))

    def test_toolkit_null_sha_is_not_drift(self):
        kw = base()
        kw["toolkit_rows"][2] = ("/m/u2/z.json", None)
        self.assertEqual(run(kw).drift, (("toolkit-no-hash", "E2", "/m/u2/z.json", SHA_C, ""),))

    def test_toolkit_rows_for_other_paths_are_ignored(self):
        kw = base()
        kw["toolkit_rows"].append(("/elsewhere/f", SHA_D))
        self.assertEqual(run(kw).drift, ())

    def test_drift_is_reported_for_an_unassigned_leaf_too(self):
        kw = base()
        kw["entries"][0]["leaves"].append(leaf("/m/u1b/w", SHA_A))
        kw["toolkit_rows"].append(("/m/u1b/w", SHA_D))
        self.assertIn(("drift", "E1", "/m/u1b/w", SHA_A, SHA_D), run(kw).drift)

    def test_drift_does_not_block_targets_or_capacity(self):
        kw = base()
        kw["toolkit_rows"] = []
        r = run(kw)
        self.assertEqual(len(r.drift), 3)
        self.assertEqual((r.targets, r.capacity), ((), ()))


class CrossUnitDuplicates(unittest.TestCase):
    def test_sha_group_across_two_entries(self):
        kw = base()
        kw["entries"][1]["leaves"].append(leaf("/m/u2/copy.json", SHA_A, size=10))
        kw["toolkit_rows"].append(("/m/u2/copy.json", SHA_A))
        kw["same_filesystem"][("/m/u2/copy.json", "/d")] = True
        self.assertEqual(run(kw).cross_unit_dups, ((SHA_A, 10, "E1", "/m/u1/x.json"), (SHA_A, 10, "E2", "/m/u2/copy.json")))

    def test_sha_group_inside_one_entry_is_not_cross_unit(self):
        kw = base()
        kw["entries"][0]["leaves"].append(leaf("/m/u1/x2.json", SHA_A))
        kw["toolkit_rows"].append(("/m/u1/x2.json", SHA_A))
        kw["same_filesystem"][("/m/u1/x2.json", "/d")] = True
        self.assertEqual(run(kw).cross_unit_dups, ())

    def test_only_regular_files_group(self):
        kw = base()
        kw["entries"][0]["leaves"].append(leaf("/m/u1/sock", SHA_D, 0, kind="socket"))
        kw["entries"][1]["leaves"].append(leaf("/m/u2/sock", SHA_D, 0, kind="socket"))
        kw["entries"][0]["leaves"].append(leaf("/m/u1/ln", SHA_B, 3, kind="symlink"))
        kw["entries"][1]["leaves"].append(leaf("/m/u2/ln", SHA_B, 3, kind="symlink"))
        for s in ("/m/u1/sock", "/m/u2/sock", "/m/u1/ln", "/m/u2/ln"):
            kw["same_filesystem"][(s, "/d")] = True
        self.assertEqual(run(kw).cross_unit_dups, ())


class Targets(unittest.TestCase):
    def test_two_leaves_with_one_target(self):
        kw = base()
        kw["entries"][1]["moves"][0]["target"] = "/d/u1"
        kw["entries"][1]["leaves"][0]["source"] = "/m/u2/x.json"
        kw["toolkit_rows"][2] = ("/m/u2/x.json", SHA_C)
        kw["same_filesystem"] = {("/m/u1/x.json", "/d"): True, ("/m/u1/y.json", "/d"): True,
                                 ("/m/u2/x.json", "/d"): True}
        self.assertEqual(run(kw).targets, (("collision", "E1", "/m/u1/x.json", "/d/u1/x.json"),
                                           ("collision", "E2", "/m/u2/x.json", "/d/u1/x.json")))

    def test_existing_leaf_target(self):
        kw = base()
        kw["existing_targets"] = ["/d/u1/y.json"]
        self.assertEqual(run(kw).targets, (("target-exists", "E1", "/m/u1/y.json", "/d/u1/y.json"),))

    def test_existing_move_target(self):
        kw = base()
        kw["existing_targets"] = ("/d/u2",)
        self.assertEqual(run(kw).targets, (("target-exists", "E2", "/m/u2", "/d/u2"),))

    def test_exact_file_move_existing_reports_one_row(self):
        kw = base()
        kw["entries"][0]["moves"].append({"source": "/m/u1/x.json", "target": "/d/other/x.json"})
        kw["existing_targets"] = {"/d/other/x.json"}
        self.assertEqual(run(kw).targets, (("target-exists", "E1", "/m/u1/x.json", "/d/other/x.json"),))

    def test_existing_paths_that_are_no_target_are_ignored(self):
        kw = base()
        kw["existing_targets"] = frozenset({"/d", "/d/u3"})
        self.assertEqual(run(kw).targets, ())

    def test_unassigned_leaf(self):
        kw = base()
        kw["entries"][0]["leaves"].append(leaf("/m/u1b/w", SHA_D))
        kw["toolkit_rows"].append(("/m/u1b/w", SHA_D))
        self.assertEqual(run(kw).targets, (("unassigned", "E1", "/m/u1b/w", ""),))

    def test_sibling_prefix_is_not_inside_a_move(self):
        kw = base()
        kw["entries"][0]["leaves"].append(leaf("/m/u10/w", SHA_D))
        kw["toolkit_rows"].append(("/m/u10/w", SHA_D))
        kw["annex_rows"].append({"requirement_id": "MV-10", "source": "/m/u10", "target": "/v", "action": "HOLD"})
        self.assertEqual(run(kw).targets, (("unassigned", "E1", "/m/u10/w", ""),))

    def test_doubly_assigned_leaf(self):
        kw = base()
        kw["entries"][1]["replaces"].append("MV-1")
        kw["entries"][1]["moves"].append({"source": "/m/u1/y.json", "target": "/d/u2/y.json"})
        kw["same_filesystem"][("/m/u1/y.json", "/d")] = True
        self.assertEqual(run(kw).targets, (("multi-assigned", "E1", "/m/u1/y.json", "/d/u1/y.json"),
                                           ("multi-assigned", "E2", "/m/u1/y.json", "/d/u2/y.json")))

    def test_longest_move_source_wins_inside_an_entry(self):
        kw = base()
        kw["entries"][0]["moves"].append({"source": "/m/u1/y.json", "target": "/d/u2/z.json"})
        r = run(kw)
        self.assertEqual(r.targets, (("collision", "E1", "/m/u1/y.json", "/d/u2/z.json"),
                                     ("collision", "E2", "/m/u2/z.json", "/d/u2/z.json")))

    def test_rows_sort_by_kind_then_target(self):
        kw = base()
        kw["entries"][0]["leaves"].append(leaf("/m/u1b/w", SHA_D))
        kw["toolkit_rows"].append(("/m/u1b/w", SHA_D))
        kw["existing_targets"] = ["/d/u2/z.json", "/d/u1/x.json"]
        self.assertEqual([row[0] for row in run(kw).targets], ["target-exists", "target-exists", "unassigned"])
        self.assertEqual(run(kw).targets[0][3], "/d/u1/x.json")


class Capacity(unittest.TestCase):
    def cross_fs(self, kw):
        for key in kw["same_filesystem"]:
            kw["same_filesystem"][key] = False

    def test_over_capacity_copy(self):
        kw = base()
        self.cross_fs(kw)
        kw["entries"][0]["leaves"][0]["bytes"] = 81 * GiB
        need = 81 * GiB + 10 + 10
        self.assertEqual(run(kw).capacity, (("/d", need, 100 * GiB, 20 * GiB, 80 * GiB),))

    def test_two_entries_fit_alone_but_not_together(self):
        kw = base()
        self.cross_fs(kw)
        kw["entries"][0]["leaves"][0]["bytes"] = 50 * GiB
        kw["entries"][1]["leaves"][0]["bytes"] = 40 * GiB
        for alone in (0, 1):
            one = copy.deepcopy(kw)
            del one["entries"][1 - alone]
            self.assertEqual(run(one).capacity, ())
        self.assertEqual(run(kw).capacity, (("/d", 90 * GiB + 10, 100 * GiB, 20 * GiB, 80 * GiB),))

    def test_same_filesystem_rename_costs_no_bytes(self):
        kw = base()
        kw["entries"][0]["leaves"][0]["bytes"] = 500 * GiB
        self.assertEqual(run(kw).capacity, ())

    def test_budget_boundary(self):
        kw = base()
        self.cross_fs(kw)
        kw["free_bytes"] = {"/d": 50}
        kw["floor_bytes"] = 20
        self.assertEqual(run(kw).capacity, ())  # 30 needed, budget 30
        kw["entries"][1]["leaves"][0]["bytes"] = 11
        self.assertEqual(run(kw).capacity, (("/d", 31, 50, 20, 30),))

    def test_zero_free_and_zero_floor(self):
        kw = base()
        kw["free_bytes"] = {"/d": 0}
        kw["floor_bytes"] = 0
        self.assertEqual(run(kw).capacity, ())
        self.cross_fs(kw)
        self.assertEqual(run(kw).capacity, (("/d", 30, 0, 0, 0),))

    def test_floor_above_free_reports_any_copy(self):
        kw = base()
        kw["free_bytes"] = {"/d": 5}
        self.assertEqual(run(kw).capacity, (("/d", 0, 5, 20 * GiB, 5 - 20 * GiB),))
        kw["same_filesystem"][("/m/u2/z.json", "/d")] = False
        self.assertEqual(run(kw).capacity, (("/d", 10, 5, 20 * GiB, 5 - 20 * GiB),))

    def test_renames_at_or_above_floor_report_nothing(self):
        kw = base()
        kw["free_bytes"] = {"/d": 20 * GiB}
        self.assertEqual(run(kw).capacity, ())  # 0 needed, budget 0
        kw["free_bytes"] = {"/d": 20 * GiB - 1}
        self.assertEqual(run(kw).capacity, (("/d", 0, 20 * GiB - 1, 20 * GiB, -1),))

    def test_longest_root_takes_the_bytes(self):
        kw = base()
        kw["free_bytes"] = {"/d": 100 * GiB, "/d/u2": 0}
        kw["same_filesystem"] = {("/m/u1/x.json", "/d"): True, ("/m/u1/y.json", "/d"): True,
                                 ("/m/u2/z.json", "/d/u2"): False}
        kw["floor_bytes"] = 0
        self.assertEqual(run(kw).capacity, (("/d/u2", 10, 0, 0, 0),))

    def test_doubly_assigned_leaf_counts_for_each_entry(self):
        kw = base()
        self.cross_fs(kw)
        kw["free_bytes"] = {"/d": 45}
        kw["floor_bytes"] = 0
        self.assertEqual(run(kw).capacity, ())
        kw["entries"][1]["replaces"].append("MV-1")
        kw["entries"][1]["moves"].append({"source": "/m/u1/y.json", "target": "/d/u2/y.json"})
        self.assertEqual(run(kw).capacity, ())  # 40 needed, budget 45
        kw["free_bytes"] = {"/d": 39}
        self.assertEqual(run(kw).capacity, (("/d", 40, 39, 0, 39),))

    def test_unassigned_leaf_costs_nothing(self):
        kw = base()
        self.cross_fs(kw)
        kw["free_bytes"] = {"/d": 30}
        kw["floor_bytes"] = 0
        kw["entries"][0]["leaves"].append(leaf("/m/u1b/w", SHA_D, size=1000))
        self.assertEqual(run(kw).capacity, ())


class Refusals(unittest.TestCase):
    def refuses(self, kw, where):
        with self.assertRaises(fdsafe.Refusal) as ctx:
            run(kw)
        self.assertIsNone(ctx.exception.errno)
        self.assertEqual(ctx.exception.path, where)
        return ctx.exception

    def test_refusal_is_the_one_refusal_type(self):
        self.assertIs(core.Refusal, fdsafe.Refusal)

    def test_zero_entries(self):
        for empty in ([], ()):
            kw = base()
            kw["entries"] = empty
            self.refuses(kw, "entries")

    def test_entries_wrong_type(self):
        for bad in (None, "E1", {"id": "E1"}, 3, b"x"):
            kw = base()
            kw["entries"] = bad
            self.refuses(kw, "entries")

    def test_entry_wrong_type(self):
        for bad in (None, ["E1"], "E1"):
            kw = base()
            kw["entries"][1] = bad
            self.refuses(kw, "entries[1]")

    def test_entry_missing_key(self):
        for key in ("id", "replaces", "moves", "leaves"):
            kw = base()
            del kw["entries"][0][key]
            self.refuses(kw, f"entries[0].{key}")

    def test_entry_id(self):
        for bad in ("", 7, None, True):
            kw = base()
            kw["entries"][0]["id"] = bad
            self.refuses(kw, "entries[0].id")

    def test_duplicate_entry_id(self):
        kw = base()
        kw["entries"][1]["id"] = "E1"
        self.refuses(kw, "entries[1].id")

    def test_replaces(self):
        for bad in ([], "MV-1", None, [1]):
            kw = base()
            kw["entries"][0]["replaces"] = bad
            where = "entries[0].replaces[0]" if bad == [1] else "entries[0].replaces"
            self.refuses(kw, where)

    def test_replaces_unknown_row(self):
        kw = base()
        kw["entries"][0]["replaces"] = ["MV-404"]
        self.refuses(kw, "entries[0].replaces[0]")

    def test_replaces_a_row_that_is_not_hold(self):
        kw = base()
        kw["entries"][0]["replaces"] = ["MV-1", "MV-9"]
        self.refuses(kw, "entries[0].replaces[1]")

    def test_moves(self):
        for bad in ([], None, {"source": "/m/u1", "target": "/d/u1"}):
            kw = base()
            kw["entries"][0]["moves"] = bad
            self.refuses(kw, "entries[0].moves")

    def test_move_wrong_type_or_key(self):
        kw = base()
        kw["entries"][0]["moves"][0] = ("/m/u1", "/d/u1")
        self.refuses(kw, "entries[0].moves[0]")
        kw = base()
        del kw["entries"][0]["moves"][0]["target"]
        self.refuses(kw, "entries[0].moves[0].target")

    def test_move_paths(self):
        for key in ("source", "target"):
            for bad in ("m/u1", "/m/u1/", "/m//u1", "/m/./u1", "/m/x/../u1", "/", "", None, 5, "/m/u1\0"):
                kw = base()
                kw["entries"][0]["moves"][0][key] = bad
                self.refuses(kw, f"entries[0].moves[0].{key}")

    def test_move_source_outside_its_replaced_rows(self):
        kw = base()
        kw["entries"][0]["moves"][0]["source"] = "/m/u2"
        self.refuses(kw, "entries[0].moves[0].source")
        kw = base()
        kw["entries"][0]["moves"][0]["source"] = "/m"
        self.refuses(kw, "entries[0].moves[0].source")
        kw = base()
        kw["annex_rows"].append({"requirement_id": "MV-10", "source": "/m/u10", "target": "/v", "action": "HOLD"})
        kw["entries"][0]["moves"][0]["source"] = "/m/u10"
        self.refuses(kw, "entries[0].moves[0].source")

    def test_duplicate_move_source_in_one_entry(self):
        kw = base()
        kw["entries"][0]["moves"].append({"source": "/m/u1", "target": "/d/elsewhere"})
        self.refuses(kw, "entries[0].moves[1].source")

    def test_leaves(self):
        for bad in (None, "x", {"source": "/m/u1/x.json"}):
            kw = base()
            kw["entries"][0]["leaves"] = bad
            self.refuses(kw, "entries[0].leaves")
        kw = base()
        kw["entries"][0]["leaves"][1] = ["/m/u1/y.json"]
        self.refuses(kw, "entries[0].leaves[1]")

    def test_leaf_fields(self):
        cases = {
            "source": ("rel/x", "/m/u1/x.json/", "/m/u1/x\0.json", None, 1),
            "kind": ("dir", "File", None, 0, ["file"]),
            "bytes": (-1, True, 1.0, "10", None),
            "sha256": ("A" * 64, "a" * 63, "a" * 65, "g" * 64, None, 0),
        }
        for key, bads in cases.items():
            for bad in bads:
                kw = base()
                kw["entries"][0]["leaves"][0][key] = bad
                self.refuses(kw, f"entries[0].leaves[0].{key}")
            kw = base()
            del kw["entries"][0]["leaves"][0][key]
            self.refuses(kw, f"entries[0].leaves[0].{key}")

    def test_leaf_listed_by_two_manifests(self):
        kw = base()
        kw["entries"][1]["leaves"].append(leaf("/m/u1/x.json", SHA_A))
        self.refuses(kw, "entries[1].leaves[1].source")

    def test_annex_rows(self):
        for bad in (None, "MV-1", {"MV-1": {}}):
            kw = base()
            kw["annex_rows"] = bad
            self.refuses(kw, "annex_rows")
        kw = base()
        kw["annex_rows"][2] = ["MV-3"]
        self.refuses(kw, "annex_rows[2]")
        for key in ("requirement_id", "source", "action"):
            kw = base()
            del kw["annex_rows"][1][key]
            self.refuses(kw, f"annex_rows[1].{key}")
            kw = base()
            kw["annex_rows"][1][key] = 3
            self.refuses(kw, f"annex_rows[1].{key}")
        kw = base()
        kw["annex_rows"][1]["source"] = "m/u2"
        self.refuses(kw, "annex_rows[1].source")
        kw = base()
        kw["annex_rows"][3]["requirement_id"] = "MV-1"
        self.refuses(kw, "annex_rows[3].requirement_id")

    def test_toolkit_rows(self):
        for bad in (None, "x", {"/m/u1/x.json": SHA_A}):
            kw = base()
            kw["toolkit_rows"] = bad
            self.refuses(kw, "toolkit_rows")
        for bad in ("/m/u1/x.json", ("/m/u1/x.json",), ("/m/u1/x.json", SHA_A, 1), None):
            kw = base()
            kw["toolkit_rows"][0] = bad
            self.refuses(kw, "toolkit_rows[0]")
        for bad in ("A" * 64, "a" * 63, 0, ""):
            kw = base()
            kw["toolkit_rows"][0] = ("/m/u1/x.json", bad)
            self.refuses(kw, "toolkit_rows[0].sha256")
        for bad in (None, "rel", 3):
            kw = base()
            kw["toolkit_rows"][0] = (bad, SHA_A)
            self.refuses(kw, "toolkit_rows[0].source")

    def test_toolkit_duplicate_source(self):
        kw = base()
        kw["toolkit_rows"].append(("/m/u1/x.json", SHA_A))
        self.refuses(kw, "toolkit_rows[3].source")

    def test_existing_targets(self):
        for bad in (None, "/d/u1", b"/d", {"/d/u1": True}, 0):
            kw = base()
            kw["existing_targets"] = bad
            self.refuses(kw, "existing_targets")
        for bad in ("d/u1", None, "/d/u1/", "/d/u1\0"):
            kw = base()
            kw["existing_targets"] = [bad]
            self.refuses(kw, "existing_targets[0]")

    def test_free_bytes(self):
        for bad in (None, [("/d", 1)], 100):
            kw = base()
            kw["free_bytes"] = bad
            self.refuses(kw, "free_bytes")
        for bad in (-1, True, 1.5, "1", None):
            kw = base()
            kw["free_bytes"] = {"/d": bad}
            self.refuses(kw, "free_bytes['/d']")
        kw = base()
        kw["free_bytes"] = {"d": 1}
        self.refuses(kw, "free_bytes['d']")

    def test_floor_bytes(self):
        for bad in (-1, True, False, 1.0, "20", None):
            kw = base()
            kw["floor_bytes"] = bad
            self.refuses(kw, "floor_bytes")

    def test_target_under_no_destination_root(self):
        kw = base()
        kw["free_bytes"] = {"/d/u1": 100 * GiB}
        kw["same_filesystem"] = {("/m/u1/x.json", "/d/u1"): True, ("/m/u1/y.json", "/d/u1"): True}
        self.refuses(kw, "entries[1].moves[0].target")

    def test_same_filesystem(self):
        for bad in (None, [], True):
            kw = base()
            kw["same_filesystem"] = bad
            self.refuses(kw, "same_filesystem")
        kw = base()
        del kw["same_filesystem"][("/m/u2/z.json", "/d")]
        self.refuses(kw, "same_filesystem[('/m/u2/z.json', '/d')]")
        for bad in (1, 0, None, "yes"):
            kw = base()
            kw["same_filesystem"][("/m/u2/z.json", "/d")] = bad
            self.refuses(kw, "same_filesystem[('/m/u2/z.json', '/d')]")
        for bad in (("rel", "/d"), ("/m/u2/z.json",), ("/m/u2/z.json", "/d", "/e"), "/m/u2/z.json", ("/m/x", None)):
            kw = base()
            kw["same_filesystem"][bad] = True
            self.refuses(kw, f"same_filesystem[{bad!r}]")

    def test_refusal_message_names_the_field(self):
        kw = base()
        kw["floor_bytes"] = -1
        exc = self.refuses(kw, "floor_bytes")
        self.assertTrue(str(exc).startswith("'floor_bytes': "))


class Purity(unittest.TestCase):
    def test_no_filesystem_clock_or_environment_call(self):
        def forbidden(*args, **kwargs):
            raise AssertionError("ledger_db_core made a filesystem, clock or environment call")

        names = ("open", "stat", "lstat", "fstat", "scandir", "listdir", "walk", "readlink", "statvfs", "getcwd",
                 "getenv", "access")
        with mock.patch.object(builtins, "open", forbidden), \
                mock.patch.multiple(os, **{n: forbidden for n in names}), \
                mock.patch("time.time", forbidden), mock.patch("time.monotonic", forbidden):
            kw = base()
            kw["toolkit_rows"][0] = ("/m/u1/x.json", SHA_D)
            self.assertEqual(len(run(kw).drift), 1)

    def test_imports_are_stdlib_value_modules_only(self):
        with open(core.__file__, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module)
        self.assertTrue(names <= {"__future__", "collections.abc", "dataclasses", "ops.migrate", "re", "typing"},
                        names)
        self.assertIn("ops.migrate", names)


if __name__ == "__main__":
    unittest.main()
