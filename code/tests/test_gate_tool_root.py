"""The workspace gate runs from a tool-root copy and needs an explicit run policy.

Production runs a copy of workspace_gate.py outside the repository
(_system/governance/workspace-admission.json `gate`). The copy must find the wire
parser and schema in the policy's canonical repository, not beside its own file.
Every case runs the copied gate as a subprocess, never the in-tree module.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SOURCE_ROOT = Path(os.environ['LLMDB_ROOT'])
STATE_FILES = ('code/state/icm21_check.py', 'code/state/icm21/WIRE-SCHEMAS.json')


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def put(root, relative, data):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def binding(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


class GateToolRoot(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='gate-tool-root-',
                                                dir=os.path.realpath('/tmp'))
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(temporary.name)
        roots = {name: self.scratch / name for name in
                 ('canonical', 'sources', 'preservation', 'worktrees', 'llmdb-tools')}
        for root in roots.values():
            root.mkdir()
        canonical = roots['canonical']
        for relative in STATE_FILES:
            put(canonical, relative, (SOURCE_ROOT / relative).read_bytes())
        # parents[2] of the copy is the scratch root, which holds no code/state.
        self.gate = put(roots['llmdb-tools'], 'icm21/workspace_gate.py',
                        (SOURCE_ROOT / 'code/ops/git/workspace_gate.py').read_bytes())
        self.assertFalse((self.gate.parents[2] / 'state').exists())
        self.assertFalse((self.gate.parents[2] / 'code').exists())
        owned = put(self.scratch, 'owned.txt', b'owned fixture\n')
        self.request = {'schema_version': 1, 'id': 'WS-1', 'kind': 'worktree',
                        'source': str(canonical),
                        'destination': str(roots['worktrees'] / 'lane-a'),
                        'lane': 'lane-a', 'base_commit': '0' * 40, 'plan': None}
        scopes = put(self.scratch, 'scopes.json', encoded({'schema_version': 1, 'lanes': [
            {'lane': 'lane-a', 'root': self.request['destination'],
             'file_paths': [str(owned)]}]}))
        registry = put(self.scratch, 'registries.json', encoded({
            'schema_version': 1, 'dispatcher': ['checker'], 'reader_registry': [],
            'loader_registry': []}))
        empty = put(self.scratch, 'empty.json', encoded({}))
        config = put(self.scratch, 'config.json', encoded({
            'schema_version': 1, 'canonical_root': str(canonical),
            'source_roots': [str(roots['sources'])],
            'preservation_root': str(roots['preservation']),
            'worktree_root': str(roots['worktrees']), 'tool_root': str(roots['llmdb-tools']),
            'ownership_path': binding(scopes), 'registries': binding(registry),
            'references': binding(empty), 'retention': binding(empty),
            'required_checks': ['C-CREATION'], 'nightly_utc': '02:00:00Z',
            'migration_holds': []}))
        requests = put(self.scratch, 'requests.json',
                       encoded({'schema_version': 1, 'requests': [self.request]}))
        self.policy = put(self.scratch, 'policy.json', encoded({
            'schema_version': 1, 'config': binding(config), 'gate': binding(self.gate),
            'scopes': binding(scopes), 'approved_requests': binding(requests),
            'capabilities': [], 'read_tools': ['Read', 'Glob', 'Grep'],
            'disabled_tool_names': ['write_stdin', 'MCPWriter']}))
        self.canonical = canonical

    def gate_cli(self, *args, input=None):
        environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        environment.update(LLMDB_ROOT=str(self.scratch), PYTHONDONTWRITEBYTECODE='1',
                           HOME=str(self.scratch), TMPDIR=str(self.scratch))
        return subprocess.run([sys.executable, '-B', str(self.gate), *map(str, args)],
                              cwd=self.scratch, env=environment, input=input,
                              capture_output=True, timeout=30)

    def result(self, completed, exit_code):
        detail = (completed.stdout + completed.stderr).decode('utf-8', 'replace')
        self.assertEqual(completed.returncode, exit_code, detail)
        return json.loads(completed.stdout)

    def check(self):
        request = put(self.scratch, 'request.json', encoded(self.request))
        return self.gate_cli('check', '--policy', self.policy, '--request', request)

    def test_copied_gate_admits(self):
        admitted = self.result(self.check(), 0)
        self.assertEqual(admitted['decision'], 'admit', admitted)
        self.assertFalse(Path(self.request['destination']).exists())

    def test_copied_gate_hook_allows_read(self):
        event = {'hook_event_name': 'PreToolUse', 'cwd': str(self.scratch),
                 'tool_name': 'Read', 'tool_input': {'file_path': str(self.scratch / 'owned.txt')},
                 'session_id': 'fixture', 'tool_use_id': 'event-1'}
        self.assertEqual(self.result(self.gate_cli('hook', '--policy', self.policy,
                                                   input=encoded(event)), 0), {})

    def test_copied_gate_run_reaches_capability_lookup(self):
        value = self.result(self.gate_cli('run', '--policy', self.policy,
                                          '--lane', 'lane-a', '--capability', 'absent'), 1)
        self.assertEqual(value['status'], 'FAIL')
        self.assertTrue(value['reason'].startswith('UNAPPROVED_REQUEST:'), value['reason'])

    def test_schema_comes_from_policy_repo(self):
        (self.canonical / STATE_FILES[1]).unlink()
        denied = self.result(self.check(), 2)
        self.assertEqual(denied['decision'], 'deny')

    def test_run_requires_policy(self):
        completed = self.gate_cli('run', '--lane', 'lane-a', '--capability', 'absent')
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        self.assertIn(b'--policy', completed.stderr)
        self.assertEqual(completed.stdout, b'')


if __name__ == '__main__':
    unittest.main()
