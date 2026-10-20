"""T371: lexical absolute-link decisions, with no filesystem dependencies."""
from pathlib import PurePosixPath
import unittest

from icm21_moves import link_boundary_failures


UNIT = PurePosixPath('/fixture/unit')


def link(name, text):
    return {'source': UNIT / name, 'kind': 'symlink', 'link_text': text}


class AbsoluteLinkTest(unittest.TestCase):
    def check(self, text, failures=(), extra=()):
        # [LAW:behavior-not-structure] check the entire result after two kept links.
        records = [link('a', 'file'), link('b', 'dir/../file'),
                   *extra, link('z', text)]
        self.assertEqual(link_boundary_failures(records, UNIT), list(failures))

    def test_external_absolute_text_is_kept(self):
        for text in ('/outside', '/elsewhere', '/fixture/unit2/file', '/',
                     '/fixture/unit/../outside', '//outside/./file', '///outside'):
            with self.subTest(text=text):
                self.check(text)

    def test_internal_absolute_text_is_refused(self):
        for text in ('/fixture/unit', '/fixture/unit/file',
                     '/fixture/other/../unit/file', '/fixture/unit/./file',
                     '//fixture/unit/file', '///fixture/unit/file'):
            with self.subTest(text=text):
                self.check(text, ('link crosses the unit boundary: /fixture/unit/z',))

    def test_chain_to_external_absolute_text_is_kept(self):
        self.check('c/file', extra=(link('c', '/outside'),))

    def test_chain_suffix_can_enter_the_unit(self):
        for target in ('/fixture/other', '//fixture/other', '///fixture/other'):
            with self.subTest(target=target):
                self.check('c/../unit/./file',
                           ('link crosses the unit boundary: /fixture/unit/z',),
                           (link('c', target), link('d', 'file')))

    def test_chain_to_internal_absolute_text_is_refused(self):
        self.check('c/file',
                   ('link crosses the unit boundary: /fixture/unit/c',
                    'link crosses the unit boundary: /fixture/unit/z'),
                   (link('c', '/fixture/unit'), link('d', 'file')))

    def test_chain_suffix_can_leave_the_unit(self):
        self.check('c/../../outside',
                   ('link crosses the unit boundary: /fixture/unit/c',),
                   (link('c', '/fixture/unit/dir'), link('d', 'file')))

    def test_relative_escape_and_loop_still_refuse(self):
        self.check('../outside', ('link crosses the unit boundary: /fixture/unit/z',))
        self.check('z', ('ambiguous link (loop): /fixture/unit/z',))

    def test_unit_itself_still_refuses_any_text(self):
        for text in ('/outside', '/fixture/unit', 'file'):
            with self.subTest(text=text):
                self.assertEqual(link_boundary_failures([link('', text)], UNIT),
                                 ['link crosses the unit boundary: /fixture/unit'])


if __name__ == '__main__':
    unittest.main()
