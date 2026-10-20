"""File-unit tests for move_run_core.run_unit (T215 A3 seam, ticket T359).

A file unit's Step 212 split names its one leaf by the relpath "."; the core joins it to the manifest leaf whose
source is the unit source, and routes that leaf to the unit target itself.
"""
from __future__ import annotations

import json
import unittest

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as plan_core
from ops.migrate import move_run_core as core
from test_move_run_core import (APPROVAL_PATH, CUSTODY, HEADER, M, NOW, PLAN_PATH, WORKTREE, act, approval_doc,
                                canonical, sha, split_bytes)

DATA = b'{"model": 1}\n'


def file_scenario(source: str, target: str, base: str, tracked: bool, split_path: str = ".") -> dict:
    """run_unit kwargs for one file unit whose plan, approval and observations agree."""
    leaf = {"source": source, "kind": "file", "bytes": len(DATA), "sha256": sha(DATA), "link_text": None,
            "device": 16777230, "inode": 4242, "nlink": 1}
    manifest = canonical({"schema_version": 1, "root": source, "leaves": [leaf], "git_roots": []})
    row = "\t".join(["MV-101", source, target, "HOLD", str(len(DATA)), "legacy-science-unit",
                     "legacy-preservation", "C-HOLD", "G4+G5; reader hold", "ICM-R4"])
    plan = plan_core.build_plan(
        entry_id="S220", root=M, requirement_tables=[("/m/MOVE-REQUIREMENTS.tsv", f"{HEADER}\n{row}\n")],
        units=[{"requirement_id": "MV-101", "manifest_path": "/m/program/units/model.json",
                "manifest_bytes": manifest,
                "registry": {"unit": "model.json", "result": "none", "experiment_id": None, "candidates": [],
                             "unknown": [], "evidence": []},
                "candidate": None, "readers": {"stale": [], "unverified": []}, "comparison": None}],
        existing_targets=[])
    plan_bytes = canonical(plan)
    split = {"root": source, "leaves": [{"path": split_path, "class": "tracked-record", "kind": "file",
                                         "size": len(DATA), "sha256": sha(DATA), "link": None}]}
    return dict(root=M, plan=(PLAN_PATH, plan_bytes), approval=(APPROVAL_PATH, canonical(approval_doc(plan_bytes))),
                now=NOW, units=[{"source": source, "manifest": manifest, "split": split_bytes(split)}],
                tracked=[source] if tracked else [], worktree=dict(WORKTREE),
                targets=[{"target": target, "exists": False, "base": base}], run_units=[], custody_dir=CUSTODY)


class FileUnitRun(unittest.TestCase):
    def run_file(self, kw):
        # [LAW:behavior-not-structure] A valid file unit must produce actions, not a refusal.
        try:
            return core.run_unit(**kw)
        except fdsafe.Refusal as exc:
            self.fail(f"valid file unit was refused: {exc}")

    def test_tracked_file_unit_staying_in_m_is_one_git_mv(self):
        kw = file_scenario("/m/old/model.json", "/m/kept/model.json", "/m/kept", tracked=True)
        self.assertEqual(self.run_file(kw)["actions"],
                         [act("MV-101", "git-mv", "/m/old/model.json", "/m/kept/model.json")])

    def test_untracked_record_file_unit_entering_m_is_mv_then_git_add_of_the_target(self):
        kw = file_scenario("/v/p/model.json", "/m/kept/model.json", "/m", tracked=False)
        self.assertEqual(self.run_file(kw)["actions"], [
            act("MV-101", "mkdir", target="/m/kept"),
            act("MV-101", "mv", "/v/p/model.json", "/m/kept/model.json"),
            act("MV-101", "git-add", target="/m/kept/model.json"),
        ])

    def test_file_unit_route_and_leaf_documents_name_the_file_itself(self):
        kw = file_scenario("/m/old/model.json", "/v/preserved/model.json", "/v/preserved", tracked=True)
        result = self.run_file(kw)
        self.assertEqual([a["action"] for a in result["actions"]], ["mv", "git-rm-cached"])
        docs = {d["path"].rsplit("/", 1)[1]: d["bytes"] for d in result["documents"]}
        rows = docs["routes.tsv"].decode().splitlines()
        self.assertEqual(rows[1].split("\t"), ["MV-101", "/m/old/model.json", "/v/preserved/model.json", "file",
                                               str(len(DATA)), "MOVE", "legacy-preservation", "tracked-record"])
        self.assertEqual([leaf["source"] for leaf in json.loads(docs["leaves.json"])["leaves"]],
                         ["/m/old/model.json"])

    def test_file_unit_empty_split_path_refuses(self):
        kw = file_scenario("/m/old/model.json", "/m/kept/model.json", "/m/kept", tracked=True,
                           split_path="")
        with self.assertRaisesRegex(fdsafe.Refusal, "is not a relative path inside the unit"):
            core.run_unit(**kw)

    def test_file_unit_split_naming_the_file_by_name_refuses(self):
        kw = file_scenario("/m/old/model.json", "/m/kept/model.json", "/m/kept", tracked=True,
                           split_path="model.json")
        with self.assertRaisesRegex(fdsafe.Refusal, "is not a manifest leaf"):
            core.run_unit(**kw)


if __name__ == "__main__":
    unittest.main()
