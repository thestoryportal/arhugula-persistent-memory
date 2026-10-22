"""Standard fixture commits have the same identity across host timezones."""
import os
import tempfile
import unittest
from unittest import mock

from ops.migrate.test_move_unit_run import Fixture, git


class FixtureDates(unittest.TestCase):
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
