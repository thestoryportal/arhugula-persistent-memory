"""An entry must have leaves before it can contribute ledger reports."""
import unittest

from ops.migrate import fdsafe, ledger_db_core as core


def entry(eid, leaves):
    return {"id": eid, "replaces": ["MV-1"],
            "moves": [{"source": "/src", "target": "/dst/unit"}], "leaves": leaves}


def leaf():
    return {"source": "/src/a", "kind": "file", "bytes": 7, "sha256": "a" * 64}


def compute(entries):
    return core.compute(entries=entries,
                        annex_rows=[{"requirement_id": "MV-1", "source": "/src", "action": "HOLD"}],
                        toolkit_rows=[], existing_targets=["/dst/unit/a"],
                        free_bytes={"/dst": 5}, floor_bytes=0,
                        same_filesystem={("/src/a", "/dst"): False})


class EntryLeaves(unittest.TestCase):
    def test_empty_leaves_refuse(self):
        with self.assertRaisesRegex(fdsafe.Refusal, r"entries\[0\]\.leaves"):
            compute([entry("E1", [])])

    def test_one_leaf_keeps_its_rows(self):
        self.assertEqual(compute([entry("E1", [leaf()])]), core.Reports(
            drift=(("toolkit-missing", "E1", "/src/a", "a" * 64, ""),),
            cross_unit_dups=(),
            targets=(("target-exists", "E1", "/src/a", "/dst/unit/a"),),
            capacity=(("/dst", 7, 5, 0, 5),)))

    def test_second_entry_empty_leaves_refuse_with_its_index(self):
        with self.assertRaisesRegex(fdsafe.Refusal, r"entries\[1\]\.leaves"):
            compute([entry("E1", [leaf()]), entry("E2", [])])
