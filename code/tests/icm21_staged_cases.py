"""StagedControls helpers; composes the closure, hook and CI case leaves (mixin for test_icm21)."""
import dataclasses
import json
import os
from unittest.mock import patch

from icm21_case_ci import CiBypassCase
from icm21_case_closure import SourceOutputClosureCase
from icm21_case_hook import RealHookCase
from icm21_fixtures import SOURCE_ROOT, encoded, put


class StagedCases(SourceOutputClosureCase, RealHookCase, CiBypassCase):
    def checker(self):
        return self.module('code/state/icm21_check.py', 'check_staged')

    def seed_closure(self, root):
        for relative in ('code/state/build_index.py', 'code/state/resolve_path.py',
                         'code/state/icm21_check.py', 'code/state/render_state.py',
                         'code/state/llmdb_records.py', 'code/agents/twins.py',
                         'code/gates/closeout_check.py', 'code/gates/closeout_fingerprints.json',
                         'code/ops/git/hooks/pre-commit'):
            put(root, relative, self.require_file(relative, 'staged source closure').read_bytes())
        for relative in ('CLAUDE.md', 'AGENTS.md', 'routing.md',
                         'map/CLAUDE.md', 'map/AGENTS.md', 'map/routing.md'):
            put(root, relative, b'# Miniature authority\n')
        put(root, 'code/gates/closeout_fingerprints.json', b'{}')
        put(root, '_system/governance/workspace-admission.json', b'{}')
        self.publish_miniature(root)
        state = json.loads((SOURCE_ROOT / 'program/program_state.json').read_bytes())
        state['work_queue']['items'] = []
        put(root, 'program/program_state.json', encoded(state))
        for script in ('code/state/render_state.py', 'code/agents/twins.py'):
            value = self.cli(root, script, '--write')
            self.assertEqual(value.returncode, 0, (value.stdout + value.stderr).decode())
        for name, raw in self.generate(root).items():
            put(root, name if '/' in name else '_index/' + name, raw)
        self.git(root, 'add', '.')

    def staged(self, root):
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            result = self.checker().check_staged(root)
        self.assertIsInstance(result, tuple)
        return [dataclasses.asdict(x) if dataclasses.is_dataclass(x) else x for x in result]
