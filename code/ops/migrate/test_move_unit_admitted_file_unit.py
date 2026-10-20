"""Admitted staging rows include a tracked file unit itself."""
from __future__ import annotations

import unittest

from ops.migrate import move_unit


def action(kind: str, source: str, target: str | None = None) -> dict:
    return {"operation_id": "MV-101", "action": kind, "source": source, "target": target}


class AdmittedFileUnit(unittest.TestCase):
    # [LAW:behavior-not-structure] Assert complete staging bytes from real actions, without mocks.
    def test_git_mv_of_a_tracked_file_unit_is_one_r100_row(self):
        rows = move_unit._admitted(
            "/m", [action("git-mv", "/m/old/model.json", "/m/kept/model.json")],
            ["/m/old/model.json"])
        self.assertEqual(rows, b"R100\told/model.json\tkept/model.json\n")

    def test_git_rm_cached_of_a_tracked_file_unit_is_one_d_row(self):
        rows = move_unit._admitted(
            "/m", [action("mv", "/m/old/model.json", "/v/model.json"),
                   action("git-rm-cached", "/m/old/model.json")],
            ["/m/old/model.json"])
        self.assertEqual(rows, b"D\told/model.json\n")

    def test_prefix_siblings_are_not_counted(self):
        tracked = ["/m/old/model.json.bak", "/m/old/model.json",
                   "/m/old/model.jsonl", "/m/old/model.json-extra/child"]
        for kind, expected in (
                ("git-mv", b"R100\told/model.json\tkept/model.json\n"),
                ("git-rm-cached", b"D\told/model.json\n")):
            with self.subTest(kind=kind):
                rows = move_unit._admitted(
                    "/m", [action(kind, "/m/old/model.json", "/m/kept/model.json")], tracked)
                self.assertEqual(rows, expected)

    def test_directory_unit_rows_are_unchanged(self):
        tracked = ["/m/old/u1/a.json", "/m/old/u1x/b.json", "/m/old/u1/sub/c.json"]
        for kind, expected in (
                ("git-mv", b"R100\told/u1/a.json\tkept/u1/a.json\n"
                           b"R100\told/u1/sub/c.json\tkept/u1/sub/c.json\n"),
                ("git-rm-cached", b"D\told/u1/a.json\nD\told/u1/sub/c.json\n")):
            with self.subTest(kind=kind):
                rows = move_unit._admitted(
                    "/m", [action(kind, "/m/old/u1", "/m/kept/u1")], tracked)
                self.assertEqual(rows, expected)

    def test_untracked_file_unit_has_no_rows(self):
        for kind in ("git-mv", "git-rm-cached"):
            with self.subTest(kind=kind):
                rows = move_unit._admitted(
                    "/m", [action(kind, "/m/old/model.json", "/m/kept/model.json")],
                    ["/m/old/model.json.bak"])
                self.assertEqual(rows, b"")


if __name__ == "__main__":
    unittest.main()
