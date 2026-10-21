"""T375: compare real manifest and split documents for one idle socket unit."""
import json
import os
import unittest

from ops.migrate import move_run_core as core
from ops.migrate import test_move_run_core as RC
from ops.migrate import unit_manifest as M
import test_record_split_socket as fixtures


class SocketManifestSplit(fixtures.SocketUnit):
    def setUp(self):
        super().setUp()
        source = str(self.unit)
        fd = os.open(self.unit, M.DIR_FLAGS)
        try:
            manifest = M.build_manifest(source, fd)
        finally:
            os.close(fd)
        self.split = self.document()
        spec = RC.U2._replace(name=os.path.basename(source), source=source, leaves=(RC.Leaf("a.txt", b"record\n"),))
        kw, plan, _ = RC.scenario([spec])
        data = M.canonical(manifest)
        digest = RC.sha(data)
        plan["units"][0]["manifest"]["sha256"] = digest
        plan["moves"][0]["source_manifest"]["sha256"] = digest
        plan["moves"][0]["before_sha256"] = digest
        plan["units"][0]["leaves"] = len(manifest["leaves"])
        plan["units"][0]["bytes"] = sum(leaf["bytes"] for leaf in manifest["leaves"])
        plan_bytes = RC.canonical(RC.reseal(plan))
        kw.update(plan=(RC.PLAN_PATH, plan_bytes),
                  approval=(RC.APPROVAL_PATH, RC.canonical(RC.approval_doc(plan_bytes))))
        kw["units"][0].update(manifest=data, split=RC.split_bytes(self.split))
        self.plan = core._plan(kw["plan"])
        core._approval(kw["approval"], self.plan, core._instant(RC.NOW, "now", "now"))
        self.leaves = json.loads(kw["units"][0]["manifest"])["leaves"]
        self.unit_plan = self.plan.units[0]

    def accepted(self):
        try:
            result = core._split(self.unit_plan, RC.split_bytes(self.split), self.leaves)
        except core.Refusal as exc:
            self.fail(f"real socket documents must agree: {exc}")
        self.assertEqual(result, {str(self.unit / "a.txt"): "tracked-record",
                                  str(self.unit / "s.sock"): "governed-payload"})

    def test_real_documents_accept_socket_as_payload(self):
        self.accepted()

    def assert_disagrees(self, field, value):
        # [LAW:behavior-not-structure] A valid baseline proves that the changed field alone decides refusal.
        self.accepted()
        self.split["leaves"][1][field] = value
        with self.assertRaises(core.Refusal) as caught:
            core._split(self.unit_plan, RC.split_bytes(self.split), self.leaves)
        self.assertEqual(str(caught.exception),
                         f"{str(self.unit) + ' split.leaves[1]'!r}: 's.sock' disagrees with its manifest leaf")

    def test_socket_size_zero_refuses(self):
        self.assert_disagrees("size", 0)

    def test_socket_empty_file_digest_refuses(self):
        self.assert_disagrees("sha256", M.EMPTY_SHA)

    def test_socket_file_kind_refuses(self):
        self.assert_disagrees("kind", "file")


if __name__ == "__main__":
    unittest.main()
