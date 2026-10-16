"""Staged source/output closure case (StagedControls)."""

from icm21_fixtures import put


class SourceOutputClosureCase:
    def test_source_output_closure(self):
        self.checker()
        root = self.miniature()
        self.seed_closure(root)
        self.assertFalse(any(x['status'] == 'FAIL' for x in self.staged(root)))
        paths = ('program/program_state.json', 'code/state/resolve_path.py',
                 '_index/experiments.md', 'program/STATUS.md', 'map/CLAUDE.md',
                 'code/gates/closeout_fingerprints.json',
                 '_system/governance/workspace-admission.json')
        for relative in paths:
            with self.subTest(path=relative):
                original = (root / relative).read_bytes()
                (root / relative).write_bytes(original + b'\n')
                findings = self.staged(root)
                self.assertTrue(any(x['status'] == 'FAIL' for x in findings), relative)
                (root / relative).write_bytes(original)
        put(root, 'experiments/new/CONTEXT.md', b'---\nstatus: designed\n---\n')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)))
        self.git(root, 'add', 'experiments/new/CONTEXT.md')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)), 'stale staged index')
        for name, raw in self.generate(root).items():
            put(root, name if '/' in name else '_index/' + name, raw)
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)), 'fresh unstaged outputs')
        self.git(root, 'add', '.')
        self.assertFalse(any(x['status'] == 'FAIL' for x in self.staged(root)))
