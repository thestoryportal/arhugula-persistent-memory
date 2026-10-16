"""LabViz reader cases: portable map identity and adapter identity (ReaderControls)."""
import inspect
import json
import unittest

from icm21_fixtures import D2_POSITIVE, INDEX_PATHS, MAP_PATH, digest, encoded, put, snapshot


class LabvizReaderCase:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_portable_map_identity(self):
        module = self.index_module()
        self.assertIn('--labviz-map-only', inspect.getsource(module.main),
                      'absent behavior: portable derived map generation')
        first, second = self.miniature('A'), self.miniature('B')
        for root in (first, second):
            self.portable_fixture(root)
        original = self.publish_miniature(first)
        for name in (*INDEX_PATHS, MAP_PATH):
            put(second, name, (first / name).read_bytes())
        self.assertNotIn(str(first).encode(), original)
        for root in (first, second):
            before = snapshot(root)
            for flags in (('--check',), ('--check', '--labviz-map-only')):
                result = self.cli(root, 'code/state/build_index.py', *flags)
                self.assertEqual(result.returncode, 0, (result.stdout + result.stderr).decode())
            self.labviz(root)
            self.assertEqual(snapshot(root), before)
        for name in D2_POSITIVE['inputs']:
            initial = (second / name).read_bytes()
            (second / name).write_bytes(initial + b'changed\tinput\tmove\tfixture\n')
            for flags in (('--check',), ('--check', '--labviz-map-only')):
                self.assertEqual(self.cli(second, 'code/state/build_index.py', *flags).returncode, 1)
            with self.assertRaises(ValueError):
                self.labviz(second)
            (second / name).write_bytes(initial)
            self.assertEqual(self.cli(second, 'code/state/build_index.py', '--check').returncode, 0)
            self.labviz(second)
            self.assertEqual((second / MAP_PATH).read_bytes(), original)

    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_labviz_adapter_identity(self):
        self.module('code/state/resolve_path.py', 'relocate')
        root = self.miniature()
        leaves = self.portable_fixture(root)
        self.publish_miniature(root)
        module, program = self.labviz(root)
        accepted = json.loads((root / 'leaves.json').read_bytes())
        self.assertEqual(accepted, leaves)
        before = snapshot(root)
        for leaf in accepted:
            self.assertEqual(digest((root / leaf['target']).read_bytes()), leaf['sha256'])
            self.assertEqual(module._moved(leaf['source'], program.moves), [leaf['target']])
            self.assertTrue(program._cites(leaf['source'], leaf['target']))
            self.assertFalse(program._cites(leaf['source'], leaf['target'] + '.wrong'))
        self.assertEqual(module._moved('results/absent/file.md', program.moves), [])
        self.assertTrue(all(isinstance(x, str) for x in module._moved('results/context_rot_audit_20261012/', program.moves)))
        with self.assertRaises(ValueError):
            module._moved('a', {'a': 'b', 'b': 'a'})
        self.assertEqual(snapshot(root), before)
        original = (root / MAP_PATH).read_bytes()
        for field, value in (('path', '/foreign/path-map.tsv'),
                             ('path', '_index/wrong.tsv'), ('path', '../path-map.tsv'),
                             ('sha256', '0' * 64)):
            candidate = json.loads(original)
            candidate['derived_from']['sealed'][field] = value
            put(root, MAP_PATH, encoded(candidate))
            before = snapshot(root)
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.labviz(root)
            self.assertEqual(snapshot(root), before)
        put(root, MAP_PATH, original)
        for name in D2_POSITIVE['inputs']:
            source = root / name
            parked = source.with_name(source.name + '.parked')
            source.rename(parked)
            with self.subTest(missing=name), self.assertRaises(ValueError):
                self.labviz(root)
            source.symlink_to(parked)
            with self.subTest(linked=name), self.assertRaises(ValueError):
                self.labviz(root)
            source.unlink()
            parked.rename(source)
            self.labviz(root)
        self.assertEqual((root / MAP_PATH).read_bytes(), original)
