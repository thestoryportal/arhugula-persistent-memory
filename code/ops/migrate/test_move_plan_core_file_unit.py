"""File-unit tests for move_plan_core.build_plan (T215 A3 seam, ticket T358).

A file unit's manifest root is the requirement source and its one leaf; the plan's Move kind is that leaf's
kind, which icm21_moves.validate_move compares with the LeafRecord at the source.
"""
from __future__ import annotations

import os
import sys
import unittest

from test_move_plan_core import leaf, manifest_bytes, match, plan, req_row, table, unit, sha

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "state"))
import icm21_moves  # noqa: E402

SOURCE = "/p/old/model.json"


def file_unit(data: bytes = b"abc") -> dict:
    lf = dict(leaf(SOURCE, "x", data), source=SOURCE)
    return {"requirement_id": "MV-101", "manifest_path": "/m/program/units/model.json",
            "manifest_bytes": manifest_bytes(SOURCE, lf), "registry": match("model.json"), "candidate": None,
            "readers": {"stale": [], "unverified": []},
            "comparison": [{"source": SOURCE, "relpath": ".", "class": "unique", "equal_to": [],
                            "differing_from": [], "same_inode": [], "hint": None}]}


class FileUnitPlan(unittest.TestCase):
    def setUp(self):
        self.tables = [table(req_row("MV-101", SOURCE, "/v/p/old/model.json"))]

    def test_file_unit_move_kind_is_file(self):
        p = plan([file_unit()], tables=self.tables)
        move = p["moves"][0]
        self.assertEqual((move["source"], move["target"], move["kind"]),
                         (SOURCE, "/v/p/old/model.json", "file"))
        self.assertEqual((p["units"][0]["leaves"], p["units"][0]["bytes"]), (1, 3))
        self.assertEqual([r["kind"] for r in p["risks"]], ["registry-none"])

    def test_file_unit_validates_against_its_leaf_record(self):
        u = file_unit()
        p = plan([u], tables=self.tables)
        import json
        lf = json.loads(u["manifest_bytes"])["leaves"][0]
        found = icm21_moves.validate_move(p["moves"][0], ["/p", "/v"], other_moves=[], existing_paths=[],
                                          run_units=[], leaves=[lf])
        self.assertEqual([f["reason"] for f in found], [])

    def test_directory_unit_kind_is_unchanged(self):
        # [LAW:behavior-not-structure] Pin the whole wire row, including its manifest binding.
        u = unit()
        binding = {"path": u["manifest_path"], "sha256": sha(u["manifest_bytes"])}
        self.assertEqual(plan([u])["moves"], [{
            "id": "MV-101", "prd_ids": ["ICM-R4"], "action": "MOVE",
            "source": "/p/u1", "target": "/m/experiments/c10r/runs/u1", "kind": "directory",
            "bytes": 3, "before_sha256": binding["sha256"], "source_manifest": binding,
            "lane": "legacy-preservation", "reader_check_ids": []}])

    def test_git_root_kind_is_unchanged(self):
        git = [{"path": "/p/u1", "head": None, "branch": None, "dirty": []}]
        self.assertEqual(plan([unit(git_roots=git)])["moves"][0]["kind"], "git-root")

    def test_empty_directory_kind_is_unchanged(self):
        u = unit(comparison=[])
        u["manifest_bytes"] = manifest_bytes("/p/u1")
        self.assertEqual(plan([u])["moves"][0]["kind"], "directory")


if __name__ == "__main__":
    unittest.main()
