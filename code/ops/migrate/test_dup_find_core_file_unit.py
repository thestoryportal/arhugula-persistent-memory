"""T357: file roots classify at '.', with exclusive root leaves."""
import unittest

from ops.migrate import dup_find_core as core
from ops.migrate import fdsafe
from test_dup_find_core import R1, leaf, manifest

F = "/v/old/model.json"


def root_leaf(root, data=b"x"):
    return dict(leaf(root, "x", data), source=root)


class LeafRelpath(unittest.TestCase):
    def test_path_cases(self):
        # [LAW:behavior-not-structure] Assert the public path contract, including '/' boundaries.
        self.assertTrue(callable(getattr(core, "leaf_relpath", None)), "leaf_relpath must be public")
        for source, root, expected in (
            (F, F, "."), ("/", "/", "."),
            ("/v/unit/a/b.json", "/v/unit", "a/b.json"), ("/a", "/", "a"),
            ("/v/unit2/x", "/v/unit", None), ("/v", "/v/unit", None),
            ("/v/other", "/v/unit", None),
        ):
            with self.subTest(source=source, root=root):
                self.assertEqual(core.leaf_relpath(source, root), expected)


class FileUnitManifest(unittest.TestCase):
    def test_file_unit_classifies_at_dot(self):
        rows = core.classify(manifest(F, root_leaf(F, b"same"), git_roots=[]),
                             [manifest(R1, leaf(R1, "copy.json", b"same"))])
        self.assertEqual(rows, [{"source": F, "relpath": ".", "class": "equal",
                                 "equal_to": [f"{R1}/copy.json"], "differing_from": [],
                                 "same_inode": [], "hint": None}])

    def test_file_reference_differs_at_dot(self):
        ref = "/p/ref/model.json"
        rows = core.classify(manifest(F, root_leaf(F, b"new")),
                             [manifest(ref, root_leaf(ref, b"old"))])
        self.assertEqual((rows[0]["relpath"], rows[0]["class"], rows[0]["differing_from"]),
                         (".", "differing", [ref]))

    def test_root_leaf_beside_another_refuses(self):
        for leaves in ((root_leaf(F), leaf(F, "child")), (leaf(F, "child"), root_leaf(F))):
            with self.subTest(order=[row["source"] for row in leaves]):
                with self.assertRaisesRegex(fdsafe.Refusal, "only leaf") as caught:
                    core.classify(manifest(F, *leaves), [manifest(R1)])
                self.assertEqual(caught.exception.path, F)

    def test_reference_root_leaf_beside_another_refuses(self):
        with self.assertRaisesRegex(fdsafe.Refusal, "only leaf") as caught:
            core.classify(manifest(R1, leaf(R1, "x")),
                          [manifest(F, root_leaf(F), leaf(F, "child"))])
        self.assertEqual(caught.exception.path, F)

    def test_root_leaf_beside_two_descendants_refuses(self):
        # [LAW:behavior-not-structure] Exclusivity also forbids more than two leaves.
        with self.assertRaisesRegex(fdsafe.Refusal, "only leaf") as caught:
            core.classify(manifest(F, root_leaf(F), leaf(F, "child1"), leaf(F, "child2")),
                          [manifest(R1)])
        self.assertEqual(caught.exception.path, F)

    def test_reference_root_leaf_beside_two_descendants_refuses(self):
        with self.assertRaisesRegex(fdsafe.Refusal, "only leaf") as caught:
            core.classify(manifest(R1, leaf(R1, "x")),
                          [manifest(F, root_leaf(F), leaf(F, "child1"), leaf(F, "child2"))])
        self.assertEqual(caught.exception.path, F)

    def test_outside_leaf_keeps_existing_refusal(self):
        with self.assertRaisesRegex(fdsafe.Refusal, "source is not inside the manifest root"):
            core.classify(manifest(F, root_leaf(F + "2")), [manifest(R1)])

    def test_file_root_overlap_still_refuses(self):
        with self.assertRaisesRegex(fdsafe.Refusal, "overlaps"):
            core.classify(manifest(F, root_leaf(F)), [manifest("/v/old")])


if __name__ == "__main__":
    unittest.main()
