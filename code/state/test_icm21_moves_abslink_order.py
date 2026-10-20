"""T373: decide later absolute links after two kept absolute links."""
from pathlib import PurePosixPath
import unittest

from icm21_moves import link_boundary_failures


UNIT = PurePosixPath('/fixture/unit')


def link(name, text):
    return {'source': UNIT / name, 'kind': 'symlink', 'link_text': text}


class AbsoluteLinkOrderTest(unittest.TestCase):
    def check(self, extra, failures):
        # [LAW:behavior-not-structure] exact results expose skipped later decisions.
        records = [link('a', '/outside'), link('b', '/elsewhere'), *extra]
        self.assertEqual(link_boundary_failures(records, UNIT), failures)

    def test_third_absolute_link_inside_is_refused(self):
        self.check([link('z', '/fixture/unit/file')],
                   ['link crosses the unit boundary: /fixture/unit/z'])

    def test_third_absolute_link_outside_is_kept(self):
        self.check([link('z', '/outside/file')], [])

    def test_relative_chain_to_later_internal_absolute_link_is_refused(self):
        self.check([link('c', '/fixture/unit/dir'), link('z', 'c/file')],
                   ['link crosses the unit boundary: /fixture/unit/c',
                    'link crosses the unit boundary: /fixture/unit/z'])


if __name__ == '__main__':
    unittest.main()
