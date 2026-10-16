"""Step 270: the repo environment pins duckdb 1.5.6.

1.5.6 is the version that produced the Part 2 OUT/sql measurements.
The lock may differ from origin/master only by the added duckdb package.
"""
import importlib.metadata
import subprocess
import tomllib
from pathlib import Path
import unittest

PIN = ('duckdb', '1.5.6')
ROOT = Path(__file__).resolve().parents[2]


def lock_pairs(text):
    return sorted((p['name'], p['version']) for p in tomllib.loads(text)['package'])


class DuckdbPin(unittest.TestCase):
    def test_interpreter_imports_pinned_duckdb(self):
        import duckdb
        self.assertEqual(duckdb.__version__, PIN[1])
        self.assertEqual(importlib.metadata.version('duckdb'), PIN[1])

    def test_pyproject_lists_exact_pin(self):
        project = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']
        deps = [d.replace(' ', '') for d in project['dependencies']]
        self.assertEqual([d for d in deps if d.lower().startswith('duckdb')],
                         ['duckdb==1.5.6'])

    def test_lock_adds_only_duckdb(self):
        base = subprocess.run(['git', '-C', str(ROOT), 'show', 'origin/master:uv.lock'],
                              capture_output=True, text=True, check=True).stdout
        # Set union, so the check still holds once origin/master carries the pin.
        expected = sorted(set(lock_pairs(base)) | {PIN})
        self.assertEqual(lock_pairs((ROOT / 'uv.lock').read_text()), expected)


if __name__ == '__main__':
    unittest.main()
