"""Step 275: bind wire Moves to units before producing custody routes."""
import unittest

from ops.migrate import fdsafe, move_run_core as core
import test_move_run_core as fixtures


class WireMoves(unittest.TestCase):
    def refuses(self, edit):
        kw = fixtures.scenario(plan_edit=edit)[0]
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.run_unit(**kw)
        self.assertIn(fixtures.PLAN_PATH, str(caught.exception))
        self.assertIn("moves", str(caught.exception))

    def test_real_build_plan_passes(self):
        result = core.run_unit(**fixtures.scenario()[0])
        self.assertEqual(len(result["documents"]), 6)
        self.assertEqual(result["actions"][1]["source"], fixtures.U1.source)

    def test_changed_bound_fields_refuse(self):
        for field, value in (("id", "MV-999"), ("source", "/other/source"),
                             ("target", "/other/target")):
            with self.subTest(field=field):
                self.refuses(lambda p: p["moves"][0].update({field: value}))

    def test_changed_manifest_refuses(self):
        for field, value in (("path", "/other/manifest.json"), ("sha256", "0" * 64)):
            with self.subTest(field=field):
                self.refuses(lambda p: p["moves"][0].update(source_manifest={
                    **p["moves"][0]["source_manifest"], field: value}))

    def test_missing_fields_refuse(self):
        for field in fixtures.scenario()[1]["moves"][0]:
            with self.subTest(field=field):
                self.refuses(lambda p: p["moves"][0].pop(field))

    def test_two_key_move_refuses(self):
        self.refuses(lambda p: p["moves"].__setitem__(0,
                     {k: p["moves"][0][k] for k in ("source", "target")}))

    def test_non_object_move_refuses(self):
        for value in (None, [], "move", 1):
            with self.subTest(value=value):
                self.refuses(lambda p: p["moves"].__setitem__(0, value))

    def test_invalid_lane_refuses(self):
        for value in ("bad\tlane", "", "bad lane", "/lane", None, 1, []):
            with self.subTest(value=value):
                self.refuses(lambda p: p["moves"][0].update(lane=value))

    def test_moves_cardinality_and_order_refuse(self):
        self.refuses(lambda p: p["moves"].reverse())
        self.refuses(lambda p: p["moves"].pop())
        self.refuses(lambda p: p["moves"].append(p["moves"][0]))
        self.refuses(lambda p: p.update(moves=None))

    def test_each_unit_keeps_its_lane_and_split_role(self):
        def edit(plan):
            plan["moves"][1]["lane"] = "audit-preservation"
        kw = fixtures.scenario(plan_edit=edit)[0]
        routes = fixtures.docs(core.run_unit(**kw))[fixtures.CUSTODY + "/routes.tsv"]
        rows = [line.split("\t") for line in routes.decode().splitlines()[1:]]
        self.assertEqual([(r[0], r[6], r[7]) for r in rows], [
            ("MV-101", "legacy-preservation", "tracked-record"),
            ("MV-101", "legacy-preservation", "governed-payload"),
            ("MV-101", "legacy-preservation", "tracked-record"),
            ("MV-102", "audit-preservation", "tracked-record")])
