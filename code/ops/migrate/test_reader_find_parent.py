"""T356: reader bytes stay bound to a held parent inside the admitted root."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
import reader_find


class Parent(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='reader-find-parent-')
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.root = self.base / 'unit'
        self.parent = self.root / 'parent'
        self.parent.mkdir(parents=True)
        self.outside = self.base / 'outside'
        self.outside.mkdir()

    def readers(self, kind):
        for parent, text in ((self.parent, 'original'), (self.outside, 'impostor')):
            path = parent / 'reader'
            if kind == 'link':
                path.symlink_to(text)
            else:
                path.write_text(text + '\n')

    def cli(self, name='parent/reader'):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, LLMDB_ROOT=str(self.root)), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = reader_find.main(['--paths', name, '--old', 'original', 'impostor'])
        return rc, out.getvalue(), err.getvalue()

    @contextlib.contextmanager
    def swap(self, when):
        real_open = os.open
        fired = []

        def change():
            self.parent.rename(self.root / 'parked')
            self.parent.symlink_to(self.outside, target_is_directory=True)
            fired.append(True)

        def opened(path, *args, **kwargs):
            matched = path == self.parent and kwargs.get('dir_fd') is None and not fired
            if matched and when == 'before':
                change()
            fd = real_open(path, *args, **kwargs)
            if matched and when == 'after':
                change()
            return fd

        # [LAW:behavior-not-structure] Rebind the real folder at the open boundary.
        with mock.patch.object(reader_find.os, 'open', side_effect=opened):
            yield
        self.assertEqual(fired, [True])

    def refused(self, result):
        rc, out, err = result
        self.assertEqual(rc, 2, result)
        self.assertEqual(out, '')
        self.assertIn('a parent symlink leaves', err)
        self.assertNotIn('impostor', out + err)
        self.assertNotIn('Traceback', err)

    def original(self, result):
        rc, out, err = result
        self.assertEqual(rc, 0, result)
        self.assertEqual(err, '')
        report = json.loads(out)
        self.assertEqual([row['old_text'] for row in report['stale']], ['original'])
        self.assertEqual(report['unverified'], [])
        self.assertNotIn('impostor', out)

    def test_link_parent_swapped_before_open_refuses(self):
        self.readers('link')
        with self.swap('before'):
            result = self.cli()
        self.refused(result)

    def test_file_parent_swapped_before_open_refuses(self):
        self.readers('file')
        with self.swap('before'):
            result = self.cli()
        self.refused(result)

    def test_prefix_sibling_parent_swap_refuses(self):
        sibling = self.base / 'unit-evil'
        sibling.mkdir()
        # [LAW:behavior-not-structure] Sharing the root's prefix does not make a folder contained.
        with mock.patch.object(self, 'outside', sibling):
            self.readers('file')
            with self.swap('before'):
                result = self.cli()
        self.refused(result)

    def test_static_prefix_sibling_name_escapes(self):
        parent = self.base / 'unit-evil/parent'
        parent.mkdir(parents=True)
        (parent / 'reader').write_text('impostor\n')
        rc, out, err = self.cli('../unit-evil/parent/reader')
        self.assertEqual(rc, 2, (out, err))
        self.assertEqual(out, '')
        self.assertIn('escapes', err)
        self.assertNotIn('impostor', out + err)

    def test_symlink_root_parent_swap_refuses(self):
        (self.outside / 'reader').write_text('impostor\n')
        for spelling in ('relative', 'absolute-real'):
            with self.subTest(spelling=spelling):
                root = self.base / spelling / 'unit'
                parent = root / 'parent'
                parent.mkdir(parents=True)
                (parent / 'reader').write_text('original\n')
                link = root.parent / 'root-link'
                link.symlink_to(root, target_is_directory=True)
                name = 'parent/reader' if spelling == 'relative' else str(parent / 'reader')
                opened_parent = link / 'parent' if spelling == 'relative' else parent
                # [LAW:behavior-not-structure] Both spellings must retain containment after resolve.
                with mock.patch.object(self, 'root', link), \
                        mock.patch.object(self, 'parent', opened_parent), self.swap('before'):
                    result = self.cli(name)
                self.refused(result)

    def test_absent_reader_has_resolve_diagnostic(self):
        rc, out, err = self.cli('parent/missing')
        self.assertEqual(rc, 2, (out, err))
        self.assertEqual(out, '')
        self.assertIn('parent/missing: absent', err)

    def test_file_parent_swapped_after_open_reads_original(self):
        self.readers('file')
        with self.swap('after'):
            result = self.cli()
        self.original(result)

    def test_link_parent_swapped_after_open_reads_original(self):
        self.readers('link')
        with self.swap('after'):
            result = self.cli()
        self.original(result)

    def test_outside_absolute_path_is_read(self):
        path = self.outside / 'launch.plist'
        path.write_text('original\n')
        self.original(self.cli(str(path)))

    def test_in_root_parent_link_is_read(self):
        self.readers('file')
        (self.root / 'alias').symlink_to(self.parent, target_is_directory=True)
        self.original(self.cli('alias/reader'))

    def test_stable_non_regular_reader_is_unverified(self):
        for kind in ('directory', 'fifo'):
            with self.subTest(kind=kind):
                tmp = tempfile.TemporaryDirectory(prefix='reader-find-kind-')
                self.addCleanup(tmp.cleanup)
                root = Path(tmp.name).resolve()
                (root / 'parent').mkdir()
                path = root / 'parent/reader'
                if kind == 'directory':
                    path.mkdir()
                else:
                    os.mkfifo(path)
                # [LAW:behavior-not-structure] The stable kind is reported without opening a FIFO.
                try:
                    with mock.patch.object(self, 'root', root), \
                            FK._deadline(0.5) as clock, clock.body():
                        rc, out, err = self.cli()
                except FK.AttackTimeout as exc:
                    self.fail('stable reader scan blocked: ' + str(exc))
                self.assertEqual(rc, 0, (out, err))
                self.assertEqual(err, '')
                self.assertEqual(json.loads(out), {
                    'stale': [], 'unverified': [
                        {'file': 'parent/reader', 'reason': 'not a regular file'}]})

    def test_symlink_root_reads_original(self):
        self.readers('file')
        link = self.base / 'root-link'
        link.symlink_to(self.root, target_is_directory=True)
        # [LAW:behavior-not-structure] The lexical root may differ from the held folder's live path.
        with mock.patch.object(self, 'root', link):
            self.original(self.cli())

    def test_stable_and_refused_reads_close_parent(self):
        self.readers('file')
        # [LAW:verifiable-goals] Check closure on both exits through the public CLI.
        before = len(os.listdir('/dev/fd'))
        self.original(self.cli())
        self.assertEqual(len(os.listdir('/dev/fd')), before)
        with self.swap('before'):
            result = self.cli()
        self.refused(result)
        self.assertEqual(len(os.listdir('/dev/fd')), before)

    def test_regular_leaf_replaced_by_link_is_not_followed(self):
        self.readers('file')
        with FK.swap_for_symlink(
                'open', 1, self.parent / 'reader', self.outside / 'reader',
                match=lambda name, *a, **kw:
                name == self.parent / 'reader' or
                (name == 'reader' and kw.get('dir_fd') is not None)) as fault:
            rc, out, err = self.cli()
        self.assertEqual(fault.fired, 1)
        self.assertEqual(rc, 2, (out, err))
        self.assertEqual(out, '')
        self.assertIn('reader_find: refused:', err)
        self.assertNotIn('impostor', out + err)

    def test_regular_leaf_replaced_by_fifo_does_not_block(self):
        self.readers('file')
        # [LAW:behavior-not-structure] A real FIFO without a writer exposes a blocking open.
        try:
            with FK.fifo_in_place(
                    self.parent / 'reader', name='open', timeout=0.5,
                    match=lambda name, *a, **kw:
                    name == self.parent / 'reader' or
                    (name == 'reader' and kw.get('dir_fd') is not None)) as fault:
                rc, out, err = self.cli()
            self.assertEqual(fault.fired, 1)
            self.assertEqual(rc, 2, (out, err))
            self.assertEqual(out, '')
            self.assertIn(str(self.parent / 'reader'), err)
            self.assertIn('changed between scan and open', err)
        except FK.AttackTimeout as exc:
            self.fail('regular leaf open blocked on a swapped FIFO: ' + str(exc))

    def test_regular_leaf_replaced_by_regular_file_refuses(self):
        self.readers('file')
        real_open = os.open
        fired = []

        def opened(name, *args, **kwargs):
            if name == 'reader' and kwargs.get('dir_fd') is not None and not fired:
                # [LAW:behavior-not-structure] A same-kind replacement must not supply the scanned bytes.
                os.replace(self.outside / 'reader', self.parent / 'reader')
                fired.append(True)
            return real_open(name, *args, **kwargs)

        with mock.patch.object(fdsafe.os, 'open', side_effect=opened):
            rc, out, err = self.cli()
        self.assertEqual(fired, [True])
        self.assertEqual(rc, 2, (out, err))
        self.assertEqual(out, '')
        self.assertIn(str(self.parent / 'reader'), err)
        self.assertIn('changed between scan and open', err)
        self.assertNotIn('impostor', out + err)


if __name__ == '__main__':
    unittest.main()
