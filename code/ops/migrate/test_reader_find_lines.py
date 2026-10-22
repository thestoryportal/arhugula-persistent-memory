"""CLI diagnostics keep untrusted names inside one stderr line."""
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ops.migrate import reader_find

TOOL = Path(reader_find.__file__).resolve()


class Lines(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()

    def cli(self, *args):
        env = dict(os.environ, LLMDB_ROOT=str(self.root), PYTHONPATH=str(TOOL.parents[2]))
        return subprocess.run([sys.executable, '-B', str(TOOL), *map(str, args)],
                              cwd=self.root, env=env, capture_output=True, timeout=60)

    def report(self, rows):
        return (json.dumps({'stale': rows, 'unverified': []}, indent=1,
                           sort_keys=True, ensure_ascii=False) + '\n').encode()

    def names(self, name, escaped, *scope, old='old/place', inputs=()):
        (self.root / name).write_bytes(old.encode())
        result = self.cli('--check', *scope, *(inputs or ('--old', old)))
        row = {'file': name, 'line': 1, 'old': old, 'old_text': old}
        self.assertEqual((result.returncode, result.stderr, result.stdout),
                         (1, f'reader_find: {escaped}\n'.encode(), self.report([row])))

    def test_untracked_lf(self):
        subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-c',
                        'core.fsmonitor=false', 'init', '-q'], cwd=self.root,
                       check=True, capture_output=True, timeout=60)
        name = 'x\nreader_find: forged:1 names FORGED'
        self.names(name, r'x\nreader_find: forged:1 names FORGED:1 names old/place',
                   '--untracked')

    def test_paths_lf(self):
        name = 'x\nreader_find: forged:1 names FORGED'
        self.names(name, r'x\nreader_find: forged:1 names FORGED:1 names old/place',
                   '--paths', name)

    def test_old_lf(self):
        old = 'old/pla\nce'
        mapping = self.root / 'map.tsv'
        with mapping.open('w', newline='') as handle:
            writer = csv.writer(handle, delimiter='\t')
            writer.writerow(['old', 'new', 'disposition', 'unit'])
            writer.writerow([old, 'new/place', 'moved', 'S1'])
        self.names('note', r'note:1 names old/pla\nce', '--paths', 'note',
                   old=old, inputs=('--relocations', mapping))

    def test_report_lf(self):
        name = 'report\nforged.json'
        (self.root / name).write_bytes(b'{}\n')
        (self.root / 'note').write_bytes(b'clean')
        result = self.cli('--check', '--paths', 'note', '--old', 'old/place',
                          '--report', name)
        expected = f'reader_find: {self.root}/report\\nforged.json differs from this scan\n'
        self.assertEqual((result.returncode, result.stderr, result.stdout),
                         (1, expected.encode(), self.report([])))

    def test_name_esc(self):
        self.names('x\x1b', r'x\x1b:1 names old/place', '--paths', 'x\x1b')

    def test_name_del(self):
        self.names('x\x7f', r'x\x7f:1 names old/place', '--paths', 'x\x7f')

    def test_plain_name(self):
        self.names('note', 'note:1 names old/place', '--paths', 'note')

    def test_refused_lf(self):
        result = self.cli('--check', '--paths', 'absent\nforged', '--old', 'old/place')
        self.assertEqual((result.returncode, result.stderr, result.stdout),
                         (2, b'reader_find: refused: absent\\nforged: absent\n', b''))


if __name__ == '__main__':
    unittest.main()
