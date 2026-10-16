"""GuardControls workspace admission, hook and bounded-runner cases (mixin for test_icm21)."""
from pathlib import Path
import sys
import unittest

from icm21_fixtures import SOURCE_ROOT, binding, digest, encoded, put, snapshot


class GuardCases:
    def guard_fixture(self):
        self.require_file('code/ops/git/workspace_gate.py', 'workspace admission and bounded runner')
        roots = {name: self.scratch / name for name in
                 ('canonical', 'sources', 'preservation', 'worktrees', 'tools', 'worker')}
        for path in roots.values():
            path.mkdir()
        source = roots['canonical']
        self.git(source, 'init', '-q')
        put(source, 'seed.txt', b'miniature fixture\n')
        self.git(source, 'add', 'seed.txt')
        self.git(source, 'commit', '-qm', 'miniature seed')
        for relative in ('code/state/icm21_check.py', 'code/state/icm21/WIRE-SCHEMAS.json'):
            put(source, relative, (SOURCE_ROOT / relative).read_bytes())
        commit = self.git(source, 'rev-parse', 'HEAD').decode().strip()
        owned = put(self.scratch, 'owned.txt', b'owned fixture\n')
        request = {'schema_version': 1, 'id': 'WS-1', 'kind': 'worktree',
                   'source': str(source), 'destination': str(roots['worktrees'] / 'lane-a'),
                   'lane': 'lane-a', 'base_commit': commit, 'plan': None}
        scopes = put(self.scratch, 'scopes.json', encoded({'schema_version': 1, 'lanes': [
            {'lane': 'lane-a', 'root': request['destination'], 'file_paths': [str(owned)]}]}))
        registry = put(self.scratch, 'registries.json', encoded({'schema_version': 1,
                       'dispatcher': ['checker'], 'reader_registry': [], 'loader_registry': []}))
        empty = put(self.scratch, 'empty.json', encoded({}))
        config = put(self.scratch, 'config.json', encoded({
            'schema_version': 1, 'canonical_root': str(source), 'source_roots': [str(roots['sources'])],
            'preservation_root': str(roots['preservation']), 'worktree_root': str(roots['worktrees']),
            'tool_root': str(roots['tools']), 'ownership_path': binding(scopes),
            'registries': binding(registry), 'references': binding(empty), 'retention': binding(empty),
            'required_checks': ['C-CREATION'], 'nightly_utc': '02:00:00Z', 'migration_holds': []}))
        requests = put(self.scratch, 'requests.json', encoded({'schema_version': 1, 'requests': [request]}))
        gate = put(roots['tools'], 'workspace_gate.py',
                   (SOURCE_ROOT / 'code/ops/git/workspace_gate.py').read_bytes())
        policy = {'schema_version': 1, 'config': binding(config), 'gate': binding(gate),
                  'scopes': binding(scopes), 'approved_requests': binding(requests),
                  'capabilities': [], 'read_tools': ['Read', 'Glob', 'Grep'],
                  'disabled_tool_names': ['write_stdin', 'MCPWriter']}
        return request, policy, roots

    def guard_cli(self, command, request, policy, **kwargs):
        req = put(self.scratch, 'request.json', encoded(request))
        pol = put(self.scratch, 'policy.json', encoded(policy))
        return self.cli(self.scratch, 'code/ops/git/workspace_gate.py', command,
                        '--request', req, '--policy', pol, **kwargs)

    def test_admission_shapes(self):
        request, policy, roots = self.guard_fixture()
        before = snapshot(self.scratch)
        admitted = self.result(self.guard_cli('check', request, policy), 0)
        self.assertEqual(set(admitted), {'decision', 'request', 'request_sha256',
                                        'destination', 'policy_sha256'})
        self.assertEqual(admitted['decision'], 'admit')
        self.assertEqual(admitted['request_sha256'], digest(encoded(request)))
        self.assertEqual(admitted['policy_sha256'], digest(encoded(policy)))
        self.assertFalse(Path(request['destination']).exists())
        for name, data in before.items():
            self.assertEqual(snapshot(self.scratch)[name], data)
        for destination in (roots['canonical'] / 'nested', roots['worktrees'] / 'lane-a' / 'nested'):
            bad = dict(request, destination=str(destination))
            denied = self.result(self.guard_cli('check', bad, policy), 1)
            self.assertEqual(denied['decision'], 'deny')
            self.assertEqual(denied['code'], 'NESTED_DESTINATION')
            self.assertFalse(destination.exists())
        for kind in ('clone', 'repo-copy'):
            denied = self.result(self.guard_cli('check', dict(request, kind=kind), policy), 1)
            self.assertEqual(denied['decision'], 'deny')
        bad = dict(request, schema_version=True)
        self.assertEqual(self.guard_cli('check', bad, policy).returncode, 2)

    def test_create_recheck(self):
        module = self.module('code/ops/git/workspace_gate.py', 'admit_workspace', 'create_workspace')
        request, policy, roots = self.guard_fixture()
        # The CLI's parser owns construction of validated request/policy types.
        admitted = self.result(self.guard_cli('check', request, policy), 0)
        self.assertEqual(admitted['decision'], 'admit')
        approved = Path(policy['approved_requests']['path'])
        approved.write_bytes(encoded({'schema_version': 1, 'requests': []}))
        result = self.guard_cli('create', request, policy)
        self.assertIn(result.returncode, (1, 2))
        self.assertFalse(Path(request['destination']).exists())
        approved.write_bytes(encoded({'schema_version': 1, 'requests': [request]}))
        collision = Path(request['destination'])
        self.assertEqual(self.guard_cli('create', request, policy).returncode, 0)
        self.assertTrue(collision.is_dir())
        self.assertEqual((collision / 'seed.txt').read_bytes(), b'miniature fixture\n')
        sentinel = put(collision, 'sentinel', b'untouched')
        self.assertEqual(self.guard_cli('create', request, policy).returncode, 1)
        self.assertEqual(sentinel.read_bytes(), b'untouched')
        fresh = dict(request, id='WS-2', lane='lane-b', destination=str(roots['worktrees'] / 'lane-b'))
        self.assertIn(self.guard_cli('create', fresh, policy).returncode, (1, 2))
        self.assertFalse(Path(fresh['destination']).exists())
        self.assertTrue(callable(module.create_workspace))

    def test_fault_denial(self):
        request, policy, roots = self.guard_fixture()
        pol = put(self.scratch, 'policy.json', encoded(policy))
        for tool, tool_input in (
                ('Bash', {'command': 'git clone SOURCE ROOT/nested-clone'}),
                ('Bash', {'command': 'git -C SOURCE worktree add ROOT/nested-worktree'}),
                ('Bash', {'command': 'cp -R SOURCE ROOT/nested-copy'}),
                ('Bash', {'command': 'rsync -a SOURCE/ ROOT/nested-rsync/'}),
                ('Bash', {'command': 'python3 -c "import shutil; shutil.copytree(\"s\", \"d\")"'}),
                ('Bash', {'command': '$(renamed-helper)'}),
                ('write_stdin', {'chars': 'clone'}), ('MCPWriter', {'path': request['destination']}),
                ('Write', {'file_path': str(roots['tools'] / 'workspace_gate.py'), 'content': 'changed'}),
                ('Bash', {'unexpected': 'shape'})):
            with self.subTest(tool=tool, input=tool_input):
                event = {'hook_event_name': 'PreToolUse', 'cwd': str(self.scratch),
                         'tool_name': tool, 'tool_input': tool_input,
                         'session_id': 'fixture', 'tool_use_id': 'event-1'}
                result = self.result(self.cli(self.scratch, 'code/ops/git/workspace_gate.py',
                                              'hook', '--policy', pol, input=encoded(event)), 0)
                output = result['hookSpecificOutput']
                self.assertEqual(output['hookEventName'], 'PreToolUse')
                self.assertEqual(output['permissionDecision'], 'deny')
                self.assertTrue(output['permissionDecisionReason'].startswith('ICM-R7:'))
                self.assertFalse(Path(request['destination']).exists())
        for raw in (b'not json', b'{}', encoded({'hook_event_name': 'PostToolUse'})):
            result = self.result(self.cli(self.scratch, 'code/ops/git/workspace_gate.py',
                                          'hook', '--policy', pol, input=raw), 0)
            self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny')
        pol.write_bytes(b'{}')
        result = self.result(self.cli(self.scratch, 'code/ops/git/workspace_gate.py',
                                      'hook', '--policy', pol, input=b'{}'), 0)
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny')

    def runner_fixture(self, body, timeout=2, limit=4096):
        request, policy, roots = self.guard_fixture()
        worker = roots['worker']
        put(worker, 'fixture_worker.py', 'import unittest\nclass Worker(unittest.TestCase):\n'
            '    def test_worker(self):\n' + ''.join('        ' + line + '\n' for line in body.splitlines()))
        profile = put(self.scratch, 'fixture.sb', '(version 1)\n(deny default)\n'
                      '(allow process* file-read* sysctl-read)\n'
                      '(allow file-write* (subpath "' + str(worker) + '"))\n')
        stdout = put(self.scratch, 'worker.stdout', b'')
        stderr = put(self.scratch, 'worker.stderr', b'')
        policy['capabilities'] = [{'id': 'fixture', 'lane': 'lane-a',
            'argv': [sys.executable, '-B', '-m', 'unittest', 'fixture_worker'],
            'interpreter': sys.executable, 'cwd': str(worker), 'profile': binding(profile),
            'output_paths': [str(stdout), str(stderr)], 'fixture_root': str(worker),
            'executable_paths': [sys.executable, '/usr/bin/sandbox-exec'],
            'read_paths': [str(worker), str(Path(sys.prefix))],
            'timeout_seconds': timeout, 'max_output_bytes': limit}]
        return policy, stdout, stderr

    def run_capability(self, policy):
        pol = put(self.scratch, 'policy.json', encoded(policy))
        return self.cli(self.scratch, 'code/ops/git/workspace_gate.py', 'run',
                        '--lane', 'lane-a', '--capability', 'fixture', '--policy', pol)

    @unittest.skipUnless(sys.platform == 'darwin', 'sandbox-exec is macOS-only')
    def test_bounded_runner(self):
        self.module('code/ops/git/workspace_gate.py', 'run_lane')
        policy, stdout, stderr = self.runner_fixture('self.assertEqual(2 + 2, 4)')
        result = self.result(self.run_capability(policy), 0)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['stdout_sha256'], digest(stdout.read_bytes()))
        self.assertEqual(result['stderr_sha256'], digest(stderr.read_bytes()))
        self.assertRegex((stdout.read_bytes() + stderr.read_bytes()).decode(), r'Ran 1 test')
        worker = Path(policy['capabilities'][0]['cwd'])
        for code in ('import time; time.sleep(8)', 'print("x" * 20000)'):
            with self.subTest(code=code):
                put(worker, 'fixture_worker.py', 'import unittest\nclass Worker(unittest.TestCase):\n'
                    '    def test_worker(self):\n        ' + code + '\n')
                failed = self.result(self.run_capability(policy), 1)
                self.assertEqual(failed['status'], 'FAIL')
                self.assertTrue(failed['reason'])

    @unittest.skipUnless(sys.platform == 'darwin', 'sandbox-exec is macOS-only')
    def test_unsupported_sandbox_denial(self):
        module = self.module('code/ops/git/workspace_gate.py', 'run_lane')
        policy, stdout, stderr = self.runner_fixture('self.fail("writer launched")')
        # Fail at the OS boundary, rather than replacing it with a passing fake.
        profile = Path(policy['capabilities'][0]['profile']['path'])
        profile.write_bytes(b'(unsupported fixture profile)')
        policy['capabilities'][0]['profile'] = binding(profile)
        value = self.result(self.run_capability(policy), 1)
        self.assertEqual(value['status'], 'FAIL')
        self.assertNotIn(b'writer launched', stdout.read_bytes() + stderr.read_bytes())
        self.assertTrue(callable(module.run_lane))
