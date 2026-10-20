"""R8: retain outside absolute link text; refuse references to the old unit."""
import os
import tempfile
import unittest
from pathlib import Path

import record_split as R


class AbsoluteLinks(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.unit = self.base / "unit"
        self.unit.mkdir()
        # [LAW:behavior-not-structure] Real links expose per-item decisions in scan order.
        self.prior = (("a", "missing"), ("b", "a"))
        for name, text in self.prior:
            (self.unit / name).symlink_to(text)

    def kept(self, text, root=None):
        (self.unit / "z").symlink_to(text)
        try:
            rows = R.split_unit(self.unit if root is None else root, [])
        except R.Refusal as exc:
            self.fail(f"kept link refused: {exc}")
        expected = tuple(R.Row(name, R.TRACKED, "link", None, None, target)
                         for name, target in (*self.prior, ("z", text)))
        self.assertEqual(rows, expected)
        self.assertEqual(os.readlink(self.unit / "z"), text)

    def refused(self, text, root=None):
        (self.unit / "z").symlink_to(text)
        with self.assertRaises(R.Refusal) as caught:
            R.split_unit(self.unit if root is None else root, [])
        self.assertEqual(str(caught.exception), f"link 'z' -> {text!r} escapes the unit")

    def test_outside_file_keeps_text(self):
        target = self.base / "outside.pt"
        target.write_bytes(b"\x00secret")
        self.kept(str(target))

    def test_outside_directory_is_not_walked(self):
        target = self.base / "outside"
        target.mkdir()
        os.mkfifo(target / "must-not-scan")
        self.kept(str(target))

    def test_outside_dangling_keeps_text(self):
        self.kept(str(self.base / "absent"))

    def test_unit_prefix_sibling_is_outside(self):
        self.kept(str(self.unit) + "-sibling/x")

    def test_normalized_outside_keeps_original_text(self):
        self.kept(str(self.unit) + "/../outside/./x")

    def test_absolute_unit_root_refuses(self):
        self.refused(str(self.unit))

    def test_absolute_descendant_refuses(self):
        self.refused(str(self.unit / "absent"))

    def test_dotdot_into_unit_refuses(self):
        self.refused(str(self.base) + "/other/../unit/absent")

    def test_dotdot_to_unit_root_refuses(self):
        self.refused(str(self.unit) + "/child/..")

    def test_double_slash_into_unit_refuses(self):
        self.refused("/" + str(self.unit / "absent"))

    def test_triple_slash_into_unit_refuses(self):
        self.refused("//" + str(self.unit / "absent"))

    def test_relative_root_is_normalized_before_absolute_decision(self):
        root = Path(os.path.relpath(self.unit)) / ".." / "unit"
        self.refused(str(self.unit / "absent"), root)

    def test_relative_in_unit_keeps_text(self):
        self.kept("sub/../a")

    def test_relative_parent_refuses(self):
        self.refused("..")

    def test_relative_escape_refuses(self):
        self.refused("../outside")

    def test_nested_git_outside_absolute_link_has_git_refusal(self):
        nested = self.unit / "z"
        nested.mkdir()
        (nested / ".git").symlink_to(str(self.base / "outside"))
        with self.assertRaises(R.Refusal) as caught:
            R.split_unit(self.unit, [])
        self.assertEqual(str(caught.exception),
                         "nested .git at 'z/.git' is not a directory "
                         "(a gitlink or a link to another Git dir)")


if __name__ == "__main__":
    unittest.main()
