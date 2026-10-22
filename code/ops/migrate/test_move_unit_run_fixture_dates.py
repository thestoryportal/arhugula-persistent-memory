"""Standard fixture commits have the same identity across host timezones."""
from datetime import datetime
import os
import tempfile
import unittest
from unittest import mock

from ops.migrate.test_move_unit_run import FIXTURE_COMMIT_DATE, Fixture, git


class FixtureDates(unittest.TestCase):
    def test_every_commit_uses_fixed_author_and_committer_dates(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        fixture = Fixture(tmp.name)
        dates = git(fixture.m, "log", "--all", "--format=%aI%x09%cI").decode().splitlines()
        self.assertTrue(dates)
        expected = datetime.fromisoformat(FIXTURE_COMMIT_DATE)
        # [LAW:behavior-not-structure] Check recorded dates, independent of Git's offset spelling.
        for line in dates:
            self.assertEqual(tuple(datetime.fromisoformat(value) for value in line.split("\t")),
                             (expected, expected))

    def test_head_is_identical_across_timezones(self):
        heads = []
        for timezone in ("UTC", "Asia/Tokyo"):
            tmp = tempfile.TemporaryDirectory()
            self.addCleanup(tmp.cleanup)
            with mock.patch.dict(os.environ, {"TZ": timezone}):
                fixture = Fixture(tmp.name)
                heads.append(git(fixture.m, "rev-parse", "HEAD"))
        # [LAW:behavior-not-structure] Compare real commits, not the helper's environment.
        self.assertEqual(heads[0], heads[1])


if __name__ == "__main__":
    unittest.main()
