"""LabViz-map cases: generator scope (StagedControls) and current output (ReaderControls)."""
import inspect
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from icm21_fixtures import (D2_POSITIVE, HEADER, INDEX_PATHS, MAP_PATH, SOURCE_ROOT,
                            d2_map, digest, snapshot)


class GeneratorScopeCase:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_generator_scope(self):
        module = self.index_module()
        self.assertIn('--labviz-map-only', inspect.getsource(module.main),
                      'absent behavior: scoped LabViz generation')
        root = self.miniature()
        self.portable_fixture(root)
        self.publish_miniature(root)
        sealed_paths = (root / '_index/path-map.tsv', root / '_index/anchor-map.tsv')
        for flags in (('--write',), ('--write', '--labviz-map-only'),
                      ('--check',), ('--check', '--labviz-map-only')):
            before = snapshot(root)
            writes = []
            original_open = io.open

            def observing_open(file, mode='r', *args, **kwargs):
                if isinstance(file, (str, os.PathLike)) and any(c in mode for c in 'wax+'):
                    writes.append(Path(file))
                return original_open(file, mode, *args, **kwargs)

            with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}), patch.object(
                    sys, 'argv', ['build_index.py', *flags]), patch('io.open', observing_open):
                self.assertEqual(module.main(), 0)
            self.assertFalse(set(writes) & set(sealed_paths), 'opened sealed map for writing')
            if '--check' in flags:
                self.assertEqual(writes, [])
                self.assertEqual(snapshot(root), before)
            else:
                allowed = {root / MAP_PATH} if '--labviz-map-only' in flags else {
                    root / name for name in (*INDEX_PATHS, MAP_PATH)}
                self.assertTrue(set(writes) <= allowed, writes)


class CurrentLabvizOutputCase:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_current_labviz_output(self):
        for name in ('_index/icm21-path-map.tsv', '_index/path-map.tsv'):
            self.require_file(name, 'installed D2 input identity')
        path = self.require_file(MAP_PATH, 'installed current map output')
        data = json.loads(path.read_bytes())
        self.assertIn('derived_from', data, 'absent behavior: D2 current map provenance')
        inputs = {name: (SOURCE_ROOT / name).read_bytes() for name in D2_POSITIVE['inputs']}
        self.assertEqual(path.read_bytes(), d2_map(inputs, data['moves']))
        self.assertEqual(inputs['_index/icm21-path-map.tsv'], HEADER)
        before = path.read_bytes()
        result = self.cli(SOURCE_ROOT, 'code/state/build_index.py', '--check', '--labviz-map-only')
        self.assertEqual(result.returncode, 0, (result.stdout + result.stderr).decode())
        self.assertEqual(digest(path.read_bytes()), digest(before))
