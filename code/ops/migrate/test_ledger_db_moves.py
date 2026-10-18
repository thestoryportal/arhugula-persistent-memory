"""T277: real build_plan records bind each move to its own manifest."""
import copy
import json
import os
import unittest
from pathlib import Path

from ops.migrate import fdsafe, ledger_db, move_plan_core
import fault_kit as FK
from test_ledger_db import Fixture, REQ_HEADER, readb


class MoveManifests(unittest.TestCase):
    def setUp(self):
        self.fx = fx = Fixture(self)  # Fixture registers every directory with addCleanup.
        rows, units = [], []
        for rid, name, target, manifest in (("MV-901", "u1", "x", fx.m1),
                                             ("MV-902", "u2", "y", fx.m2)):
            rows.append("\t".join((rid, fx.u(name), f"{fx.dst}/{target}", "HOLD", "0",
                                   "legacy-science-unit", "legacy-preservation", "C-HOLD", "none", "ICM-R4")))
            units.append({"requirement_id": rid, "manifest_path": manifest[0],
                          "manifest_bytes": readb(manifest[0]),
                          "registry": {"unit": name, "result": "none", "experiment_id": None,
                                       "candidates": [], "unknown": [], "evidence": []},
                          "candidate": None, "readers": {"stale": [], "unverified": []}, "comparison": None})
        self.entry = move_plan_core.build_plan(entry_id="E277", root=fx.base,
            requirement_tables=[(fx.req, REQ_HEADER + "\n".join(rows) + "\n")],
            units=units, existing_targets=[])
        fx.write_plans([self.entry])

    def parsed(self, entry):
        self.fx.write_plans([entry])
        return ledger_db._plans(self.fx.plans, "")

    def refused(self, entry, index, reason=None):
        with self.assertRaises(fdsafe.Refusal) as caught:
            self.parsed(entry)
        self.assertIn(f"entries[0].moves[{index}].source_manifest", str(caught.exception))
        if reason is not None:
            self.assertIn(reason, str(caught.exception))
        self.assertFalse(os.path.exists(self.fx.out))

    def test_build_plan_two_manifests_yield_both_units_in_order(self):
        entries = self.parsed(self.entry)
        expected = [leaf for path, _ in (self.fx.m1, self.fx.m2)
                    for leaf in json.loads(readb(path))["leaves"]]
        self.assertEqual(entries[0]["leaves"], expected)
        self.assertEqual(entries[0]["moves"], [{k: m[k] for k in ("source", "target")}
                                               for m in self.entry["moves"]])
        self.entry["moves"].reverse()
        self.assertEqual([leaf["source"] for leaf in self.parsed(self.entry)[0]["leaves"]],
                         [leaf["source"] for leaf in expected[2:] + expected[:2]])

    def test_real_plan_reports_include_second_unit(self):
        code, _, err = self.fx.run()
        self.assertEqual((code, err), (0, ""))
        drift = self.fx.report("drift.tsv")
        self.assertEqual({row[2] for row in drift[1:]},
                         {self.fx.u(p) for p in ("u1/a.txt", "u1/sub/b.bin", "u2/e.txt")})
        self.assertEqual(len(self.fx.report("targets.tsv")), 1)
        self.assertEqual(len(self.fx.report("capacity.tsv")), 1)

    def test_entry_level_binding_is_ignored(self):
        self.entry.update(manifest="/invalid\0entry", manifest_sha256=None)
        self.assertEqual(len(self.parsed(self.entry)[0]["leaves"]), 4)

    def test_missing_binding_has_no_entry_fallback(self):
        for index in range(2):
            entry = copy.deepcopy(self.entry)
            entry.update(manifest=self.fx.m1[0], manifest_sha256=self.fx.m1[1])
            del entry["moves"][index]["source_manifest"]
            self.refused(entry, index)

    def test_binding_shape(self):
        good = self.entry["moves"][0]["source_manifest"]
        for index in range(2):
            for bad in (None, False, 1, "manifest", [], {}, {"path": good["path"]},
                        {"sha256": good["sha256"]}, {**good, "extra": True}):
                with self.subTest(index=index, binding=bad):
                    entry = copy.deepcopy(self.entry)
                    entry["moves"][index]["source_manifest"] = bad
                    self.refused(entry, index)

    def test_bad_path(self):
        for bad in (None, 1, [], "relative", "/bad\0path", "/bad/../path"):
            entry = copy.deepcopy(self.entry)
            entry["moves"][1]["source_manifest"]["path"] = bad
            self.refused(entry, 1)

    def test_bad_digest_refuses_before_read(self):
        for bad in (None, 1, [], "", "a" * 63, "a" * 65, "g" * 64, "A" * 64):
            with self.subTest(digest=bad):
                entry = copy.deepcopy(self.entry)
                entry["moves"][1]["source_manifest"] = {"path": self.fx.inp + "/absent", "sha256": bad}
                self.refused(entry, 1, "string" if not isinstance(bad, str) else "lowercase hex sha256")

    def test_digest_mismatch(self):
        for index in range(2):
            entry = copy.deepcopy(self.entry)
            entry["moves"][index]["source_manifest"]["sha256"] = "0" * 64
            self.refused(entry, index, "is not the plan")

    def test_unexpected_manifest_open_errors_propagate(self):
        for error in (ValueError, KeyError, RuntimeError):
            with self.subTest(error=error):
                with FK.raise_unexpected("open", 1, error, match=lambda name, *a, **kw: name == "m2.json"):
                    with self.assertRaises(error):
                        self.parsed(self.entry)

    def test_second_manifest_changed_bytes_refuse(self):
        path = Path(self.fx.m2[0])
        path.write_bytes(path.read_bytes() + b" ")
        self.refused(self.entry, 1, "is not the plan")




if __name__ == "__main__":
    unittest.main()
