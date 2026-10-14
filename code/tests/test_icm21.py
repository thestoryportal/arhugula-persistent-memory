"""Frozen ICM v2.1 fixture interface (T004; product acceptance is separate).

Sources: sealed COMMAND-DERIVATION.md, SPEC.md and IMPLEMENTATION_PLAN.md D1/D2.
Fixtures contain miniature data only. No operational client, model or loader runs.
"""
import copy
import dataclasses
import hashlib
import importlib.util
import inspect
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SOURCE_ROOT = Path(os.environ['LLMDB_ROOT'])
PACKAGE = Path(os.environ['ICM_PACKAGE'])
BASE = 'c4e8ff310a2ccaf48f8661eccdcfd734ccc7a977'
HEADER = b'old\tnew\tdisposition\tunit\n'
ABOUT = 'Derived from sealed path map and approved ICM v2.1 relocations.'
MAP_PATH = 'code/apps/labviz/results_moves.json'
INDEX_PATHS = tuple('_index/' + name + '.md' for name in
                    ('experiments', 'projects', 'evidence', 'checkpoints'))
SELECTED = {
    'GuardControls': ('test_admission_shapes', 'test_bounded_runner',
                      'test_create_recheck', 'test_fault_denial',
                      'test_unsupported_sandbox_denial'),
    'StagedControls': ('test_ci_bypass', 'test_generator_scope', 'test_real_hook',
                       'test_source_output_closure'),
    'ReaderControls': ('test_candidate_registry_adapter', 'test_current_index_outputs',
                       'test_current_labviz_output', 'test_d2_wire_parser',
                       'test_dispatch_coverage_and_ownership',
                       'test_exact_relocation_and_citations',
                       'test_labviz_adapter_identity', 'test_portable_map_identity',
                       'test_queue_compatibility_and_candidates',
                       'test_relocated_anchor_targets'),
    'ApprovedWireControls': ('test_approved_scope_examples',),
}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def d2_map(inputs, moves):
    return encoded({'about': ABOUT, 'derived_from': {
        key: {'path': path, 'sha256': digest(inputs[path])}
        for key, path in (('sealed', '_index/path-map.tsv'),
                          ('relocations', '_index/icm21-path-map.tsv'))}, 'moves': moves})


D2_POSITIVE = {'inputs': {'_index/path-map.tsv': HEADER,
                          '_index/icm21-path-map.tsv': HEADER}}
D2_POSITIVE['map'] = d2_map(D2_POSITIVE['inputs'], {})


def sealed(name):
    context = json.loads((PACKAGE / 'context.json').read_bytes())
    binding = context['sources'][name]
    data = Path(binding['path'].replace('{package}', str(PACKAGE))).read_bytes()
    if digest(data) != binding['sha256']:
        raise AssertionError('changed sealed source: ' + name)
    return data


def put(root, relative, data):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))
    return path


def binding(path):
    return {'path': str(path), 'sha256': digest(path.read_bytes())}


def snapshot(root):
    return {str(p.relative_to(root)): (p.lstat().st_mode, p.lstat().st_mtime_ns,
                                      os.readlink(p) if p.is_symlink() else digest(p.read_bytes()))
            for p in root.rglob('*') if p.is_file() or p.is_symlink()}


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='icm21-', dir='/private/tmp')
        self.addCleanup(self.temporary.cleanup)
        self.scratch = Path(self.temporary.name)

    def require_file(self, relative, behavior):
        path = SOURCE_ROOT / relative
        self.assertTrue(path.is_file(), 'absent behavior: ' + behavior + ' (' + relative + ')')
        return path

    def module(self, relative, *functions):
        path = self.require_file(relative, ', '.join(functions) or relative)
        name = path.stem
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {name: module}), patch.object(
                sys, 'path', [str(SOURCE_ROOT / 'code/state')] + sys.path):
            spec.loader.exec_module(module)
        for function in functions:
            self.assertTrue(callable(getattr(module, function, None)),
                            'absent behavior: ' + relative + ':' + function)
        return module

    def run_argv(self, root, argv, **kwargs):
        environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        environment.update(LLMDB_ROOT=str(root), PYTHONDONTWRITEBYTECODE='1',
                           HOME=str(self.scratch), TMPDIR=str(self.scratch),
                           GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                           GIT_AUTHOR_NAME='ICM fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                           GIT_COMMITTER_NAME='ICM fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        return subprocess.run(argv, cwd=root, env=environment, capture_output=True,
                              timeout=30, **kwargs)

    def git(self, root, *args):
        result = self.run_argv(root, ['git', *args])
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        return result.stdout

    def cli(self, root, relative, *args, input=None):
        script = self.require_file(relative, ' '.join(map(str, args)))
        return self.run_argv(root, [sys.executable, '-B', str(script), *map(str, args)], input=input)

    def result(self, completed, exit_code):
        self.assertEqual(completed.returncode, exit_code,
                         (completed.stdout + completed.stderr).decode('utf-8', 'replace'))
        self.assertTrue(completed.stdout.strip(), 'missing JSON result')
        value = json.loads(completed.stdout)
        self.assertIsInstance(value, dict)
        return value

    def miniature(self, name='repo'):
        root = self.scratch / name
        root.mkdir()
        for folder in ('experiments', 'projects', 'evidence/CORPUS', 'program/checkpoints', '_index'):
            (root / folder).mkdir(parents=True, exist_ok=True)
        self.git(root, 'init', '-q')
        put(root, '_index/path-map.tsv', HEADER)
        put(root, '_index/icm21-path-map.tsv', HEADER)
        put(root, '_index/anchor-map.tsv', b'monolith\tanchor\tpart\tcurrent_anchor\n')
        put(root, 'program/program_state.json', encoded({'work_queue': {'items': []}}))
        return root

    def index_module(self):
        return self.module('code/state/build_index.py', 'generate')

    def generate(self, root):
        """Use the one real generator; permit writes only in this miniature root."""
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            generated = self.index_module().generate(root)
        self.assertIsInstance(generated, dict)
        for name in ('experiments.md', 'projects.md', 'evidence.md', 'checkpoints.md'):
            self.assertIn(name, generated)
        return generated

    def portable_fixture(self, root):
        old = ('results/context_rot_audit_20261012/findings.md',
               'results/skills_pipeline_survey_20261012/skills_pipeline_survey.md',
               'results/autoresearch_reaim/reaim-oct06/iter_01/pass0.json')
        middle = ('audits/context/check/findings.md',
                  'knowledge/research/skills-pipeline/skills_pipeline_survey.md',
                  'experiments/autoresearch/runs/reaim-oct06/iter_01/pass0.json')
        final = ('audits/context/final/findings.md',
                 'knowledge/research/skills-final/skills_pipeline_survey.md',
                 'experiments/autoresearch/runs/final/iter_01/pass0.json')
        sealed_bytes = HEADER + b''.join((a + '\t' + b + '\tmove\tfixture\n').encode()
                                        for a, b in zip(old, middle))
        relocation_bytes = HEADER + b''.join((a + '\t' + b + '\tmove\tfixture\n').encode()
                                            for a, b in zip(middle, final))
        put(root, '_index/path-map.tsv', sealed_bytes)
        put(root, '_index/icm21-path-map.tsv', relocation_bytes)
        leaves = []
        for source, target in zip(old, final):
            raw = encoded({'fixture_source': source})
            put(root, target, raw)
            leaves.append({'source': source, 'target': target, 'sha256': digest(raw)})
        put(root, 'leaves.json', encoded(leaves))
        put(root, 'code/apps/labviz/contexts.json', encoded({}))
        return leaves

    def publish_miniature(self, root):
        generated = self.generate(root)
        for name, raw in generated.items():
            put(root, name if '/' in name else '_index/' + name, raw)
        result = self.cli(root, 'code/state/build_index.py', '--write', '--labviz-map-only')
        self.assertEqual(result.returncode, 0, (result.stdout + result.stderr).decode())
        return (root / MAP_PATH).read_bytes()

    def labviz(self, root):
        module = self.module('code/apps/labviz/context.py', '_moved')
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            return module, module.Program(root)

    def wire(self, root, examples):
        self.require_file('code/state/icm21_check.py', 'approved-scope wire validation')
        schema = put(root, 'schema.json', sealed('WIRE-SCHEMAS.json'))
        path = put(root, 'examples.json', encoded(examples))
        return self.cli(root, 'code/state/icm21_check.py', 'wire', '--root', root,
                        '--schema', schema, '--examples', path)


class ApprovedWireControls(FixtureCase):
    def test_approved_scope_examples(self):
        self.require_file('code/state/icm21_check.py', 'validated common wire types')
        examples = json.loads(sealed('WIRE-EXAMPLES.json'))
        approved = {'Finding', 'CheckResult', 'RegistryEntry', 'Registries', 'Config',
                    'ReferenceRow', 'ReferenceRow[]', 'ReferenceManifest', 'Repair',
                    'ApprovedRequests', 'Admit', 'AuditReport'}
        examples['examples'] = [x for x in examples['examples'] if x['type'] in approved]
        self.assertGreater(len(examples['examples']), 0)
        self.assertNotIn('LabvizMoves', {x['type'] for x in examples['examples']})
        result = self.result(self.wire(self.scratch, examples), 0)
        self.assertEqual(result['status'], 'PASS')
        for type_name, change in (
                ('Finding', lambda v: v.update(extra=True)),
                ('Finding', lambda v: v.update(prd_ids=['ICM-R99'])),
                ('Admit', lambda v: v['request'].update(schema_version=True)),
                ('RegistryEntry', lambda v: v.update(check_ids=['UNKNOWN']))):
            with self.subTest(type=type_name):
                candidate = copy.deepcopy(next(x for x in examples['examples']
                                               if x['type'] == type_name and x['expected'] == 'PASS'))
                change(candidate['value'])
                probe = copy.deepcopy(examples)
                probe['examples'] = [candidate]
                self.assertEqual(self.wire(self.scratch, probe).returncode, 1,
                                 'wire parser accepted invalid ' + type_name)


class GuardControls(FixtureCase):
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


class StagedControls(FixtureCase):
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

    def test_real_hook(self):
        self.checker()
        root = self.miniature()
        self.seed_closure(root)
        hook = put(root, '.git/hooks/pre-commit',
                   (SOURCE_ROOT / 'code/ops/git/hooks/pre-commit').read_bytes())
        hook.chmod(0o755)
        put(root, 'projects/new/CONTEXT.md', b'# New fixture\n')
        self.git(root, 'add', 'projects/new/CONTEXT.md')
        rejected = self.run_argv(root, ['git', 'commit', '-qm', 'stale fixture'])
        self.assertNotEqual(rejected.returncode, 0, 'real hook accepted stale staged index')
        self.assertTrue((rejected.stdout + rejected.stderr).strip())
        for name, raw in self.generate(root).items():
            put(root, name if '/' in name else '_index/' + name, raw)
        self.git(root, 'add', '.')
        accepted = self.run_argv(root, ['git', 'commit', '-qm', 'fresh fixture'])
        self.assertEqual(accepted.returncode, 0, (accepted.stdout + accepted.stderr).decode())
        self.assertFalse((self.scratch / '_audit.out').exists())

    def test_ci_bypass(self):
        self.checker()
        workflow = (SOURCE_ROOT / '.github/workflows/ci.yml').read_text()
        for command in ('code/state/build_index.py --check', 'code/state/render_state.py --check',
                        'code/agents/twins.py --check', 'test_git_automation.py',
                        'lab.runners.test_c10w_p2_gate', 'apps.dashboard.test_dashboard_live',
                        'apps.dashboard.test_dashboard_gpu_detector', 'test_icm21',
                        'test_context_audit', 'staged'):
            self.assertIn(command, workflow)
        root = self.miniature()
        self.seed_closure(root)
        put(root, 'projects/new/CONTEXT.md', b'# Stale CI fixture\n')
        self.git(root, 'add', '.')
        self.git(root, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'bypassed fixture')
        result = self.cli(root, 'code/state/build_index.py', '--check')
        self.assertEqual(result.returncode, 1, 'clean committed stale checkout passed CI command')
        self.assertTrue(any(x['status'] == 'FAIL' for x in self.staged(root)))


class ReaderControls(FixtureCase):
    def test_queue_compatibility_and_candidates(self):
        self.require_file('code/state/icm21_check.py', 'D1 strict queue candidate validation')
        root = self.miniature()
        original = (SOURCE_ROOT / 'program/program_state.json').read_bytes()
        state = json.loads(original)
        items = state['work_queue']['items']
        self.assertEqual(len(items), 16)
        self.assertTrue(all('artifact' not in item for item in items))
        put(root, 'program/program_state.json', original)
        view = self.generate(root)['projects.md'].decode()
        self.assertIn('legacy-unspecified', view)
        self.assertEqual((root / 'program/program_state.json').read_bytes(), original)
        for artifact, label in ((None, 'no-materialized-record'), *(
                ({'kind': kind, 'path': 'records/' + kind}, kind)
                for kind in ('project', 'plan', 'audit', 'research', 'experiment'))):
            with self.subTest(artifact=artifact):
                candidate = copy.deepcopy(state)
                candidate['work_queue']['items'][0]['artifact'] = artifact
                if artifact is not None:
                    (root / artifact['path']).mkdir(parents=True, exist_ok=True)
                data = encoded(candidate)
                put(root, 'program/program_state.json', data)
                self.assertIn(label, self.generate(root)['projects.md'].decode())
                self.assertEqual((root / 'program/program_state.json').read_bytes(), data)
        for artifact in ({}, {'kind': 'unknown', 'path': 'records/project'},
                         {'kind': 'project', 'path': '../escape'},
                         {'kind': 'project', 'path': str(self.scratch)},
                         {'kind': 'project', 'path': 'missing'},
                         {'kind': 'project', 'path': 'records/project', 'extra': 1}):
            candidate = copy.deepcopy(state)
            candidate['work_queue']['items'][0]['artifact'] = artifact
            put(root, 'program/program_state.json', encoded(candidate))
            with self.subTest(invalid=artifact), self.assertRaises(ValueError):
                self.generate(root)
        # The references checker applies strict creation/repair admission separately.
        put(root, 'program/program_state.json', original)
        self.assertEqual(json.loads(original)['updated'], state['updated'])
        self.assertEqual(json.loads(original)['next_actions'][6], state['next_actions'][6])
        self.assertEqual(json.loads(original)['work_queue']['items'][2]['notes'][1],
                         state['work_queue']['items'][2]['notes'][1])

    def test_exact_relocation_and_citations(self):
        resolver = self.module('code/state/resolve_path.py', 'relocate', 'resolve_reference')
        mapping = {'old/file.md': 'middle/file.md', 'middle/file.md': 'final/file.md'}
        self.assertEqual(resolver.relocate('old/file.md', mapping), 'final/file.md')
        self.assertEqual(resolver.relocate('middle/file.md', mapping), 'final/file.md')
        self.assertEqual(resolver.relocate('current/file.md', mapping), 'current/file.md')
        self.assertEqual(resolver.relocate('old/file.md.extra', mapping), 'old/file.md.extra')
        for bad in ({'a': 'a'}, {'a': 'b', 'b': 'a'}, {'z': 'z', **mapping}):
            with self.subTest(mapping=bad), self.assertRaises(ValueError):
                resolver.relocate('current/file.md', bad)
        root = self.miniature()
        rows = []
        for suffix in (':1,3,9-12', ':3–7', '#exact-anchor'):
            for consumer, spelling, intermediate, final in (
                    ('plans/old/verdict.md', 'design.md', 'plans/old/design.md', 'plans/new/decisions_log.md'),
                    ('plans/old/handoff.md', 'verdict.md', 'plans/old/verdict.md', 'plans/new/design.md')):
                rows.append({'schema_version': 1, 'id': 'REF-' + str(len(rows)),
                    'prd_ids': ['ICM-R6'], 'consumer': consumer,
                    'consumer_final': consumer.replace('/old/', '/new/'),
                    'consumer_sha256': digest(b'historical fixture'), 'reference': spelling + suffix,
                    'intermediate': intermediate + suffix, 'final_target': final + suffix,
                    'role': 'historical-source', 'byte_offset': None, 'repair_path': None,
                    'owner': 'integration', 'check_id': 'C-REFERENCES'})
        manifest = self.reference_manifest(root, rows)
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            for row in rows:
                for consumer in (row['consumer'], row['consumer_final']):
                    self.assertEqual(resolver.resolve_reference(consumer, row['reference'], manifest),
                                     row['final_target'])
            with self.assertRaises(ValueError):
                resolver.resolve_reference('unrelated/verdict.md', rows[0]['reference'], manifest)
        duplicate = dict(rows[0], id='REF-AMBIGUOUS', final_target='wrong/file.md:1,3,9-12')
        manifest = self.reference_manifest(root, rows + [duplicate])
        with self.assertRaises(ValueError):
            resolver.resolve_reference(rows[0]['consumer'], rows[0]['reference'], manifest)

    def reference_manifest(self, root, rows):
        references = put(root, 'references.jsonl', b''.join(encoded(row) + b'\n' for row in rows))
        registries = put(root, 'registries.json', encoded({'schema_version': 1,
            'dispatcher': ['checker'], 'reader_registry': [], 'loader_registry': []}))
        executor = put(root, 'executor.json', encoded({'schema_version': 1, 'operations': []}))
        repairs = put(root, 'repairs.json', encoded({'schema_version': 1, 'repairs': []}))
        coverage = put(root, 'coverage.json', encoded({'schema_version': 1, 'scope': 'miniature',
            'coverage': {'inspected': [str(root)], 'excluded': [],
                         'required_registry_ids': [], 'checked_registry_ids': []}, 'sources': []}))
        return {'schema_version': 1, 'references': binding(references), 'registries': binding(registries),
                'executor': binding(executor), 'repairs': binding(repairs), 'coverage': binding(coverage)}

    def test_relocated_anchor_targets(self):
        module = self.index_module()
        self.assertIn('relocations', inspect.signature(module.read_anchor_map).parameters,
                      'absent behavior: sealed anchors validate relocated parts')
        root = self.miniature()
        raw = b'monolith\tanchor\tpart\tcurrent_anchor\nprogram/EXPERIMENT_RUNBOOK.md\told-heading\tprogram/runbook/01.md\texact-heading\n'
        target = put(root, 'program/final/01.md', b'## Exact heading\n')
        mapping = {'program/runbook/01.md': 'program/final/01.md'}
        self.assertEqual(module.read_anchor_map(raw, root, relocations=mapping),
                         {('program/EXPERIMENT_RUNBOOK.md', 'old-heading'):
                          ('program/runbook/01.md', 'exact-heading')})
        with self.assertRaises(ValueError):
            module.read_anchor_map(raw, root)
        with self.assertRaises(ValueError):
            module.read_anchor_map(raw, root, relocations={'program/runbook/01.md': 'missing.md'})
        put(root, '_index/anchor-map.tsv', raw)
        put(root, '_index/path-map.tsv', HEADER + b'RUNBOOK.md\tprogram/EXPERIMENT_RUNBOOK.md\tmove\tfixture\n')
        put(root, '_index/icm21-path-map.tsv', HEADER + b'program/runbook/01.md\tprogram/final/01.md\tmove\tfixture\n')
        resolver = self.module('code/state/resolve_path.py', 'relocate')
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            self.assertEqual(resolver.resolve('RUNBOOK.md#old-heading'), 'program/final/01.md#exact-heading')
            target.write_bytes(b'## Changed heading\n')
            with self.assertRaises(ValueError):
                resolver.resolve('RUNBOOK.md#old-heading')
            target.write_bytes(b'## Exact heading\n## Exact heading\n')
            with self.assertRaises(ValueError):
                resolver.resolve('RUNBOOK.md#old-heading')
        self.assertEqual((root / '_index/anchor-map.tsv').read_bytes(), raw)

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

    def test_d2_wire_parser(self):
        self.require_file('code/state/icm21_check.py', 'D2-only MapBinding parser')
        examples = json.loads(sealed('WIRE-EXAMPLES.json'))
        examples['examples'] = [x for x in examples['examples'] if x['type'] == 'LabvizMoves']
        self.assertEqual(len(examples['examples']), 2)
        positive = copy.deepcopy(examples['examples'][0])
        positive['value'] = json.loads(D2_POSITIVE['map'])
        positive['expected'] = 'PASS'
        examples['examples'] = [positive]
        for name, data in D2_POSITIVE['inputs'].items():
            put(self.scratch, name, data)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        for spelling in ('/foreign/path-map.tsv', '_index/wrong.tsv', '../path-map.tsv'):
            candidate = copy.deepcopy(examples)
            candidate['examples'][0]['value']['derived_from']['sealed']['path'] = spelling
            self.assertEqual(self.wire(self.scratch, candidate).returncode, 1)
        for name in D2_POSITIVE['inputs']:
            original = (self.scratch / name).read_bytes()
            (self.scratch / name).write_bytes(original + b'changed')
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            (self.scratch / name).write_bytes(original)
        for change in (lambda v: v.update(extra=True),
                       lambda v: v.update(about='wrong identity'),
                       lambda v: v.update(moves=[]),
                       lambda v: v['derived_from']['sealed'].update(extra=True),
                       lambda v: v['derived_from']['sealed'].update(sha256='short')):
            candidate = copy.deepcopy(examples)
            change(candidate['examples'][0]['value'])
            self.assertEqual(self.wire(self.scratch, candidate).returncode, 1)
        for name in D2_POSITIVE['inputs']:
            source = self.scratch / name
            parked = source.with_name(source.name + '.parked')
            source.rename(parked)
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            source.symlink_to(parked)
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            source.unlink()
            parked.rename(source)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        # Only LabvizMoves changes: ordinary Binding must remain absolute.
        ordinary = copy.deepcopy(examples)
        ordinary['examples'][0].update(type='Binding', value={'path': '_index/path-map.tsv',
                                                             'sha256': digest(HEADER)})
        self.assertEqual(self.wire(self.scratch, ordinary).returncode, 1)

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

    def test_current_index_outputs(self):
        self.require_file('code/state/icm21_check.py', 'installed D1 current index outputs')
        expected = self.generate(SOURCE_ROOT)
        for relative in INDEX_PATHS:
            self.assertEqual(digest((SOURCE_ROOT / relative).read_bytes()),
                             digest(expected[Path(relative).name]), relative)
        self.assertIn('legacy-unspecified', (SOURCE_ROOT / '_index/projects.md').read_text())

    def test_dispatch_coverage_and_ownership(self):
        self.module('code/state/icm21_check.py', 'check_references')
        # Reuse the sealed representative records and semantic counterexamples.
        examples = json.loads(sealed('WIRE-EXAMPLES.json'))
        examples['examples'] = [x for x in examples['examples'] if x['type'] in
                                ('ReferenceManifest', 'ReferenceRow[]', 'RegistryEntry', 'AuditReport')]
        self.assertGreater(len(examples['examples']), 0)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        registry = json.loads(sealed('REGISTRIES.json'))
        resolver = next(x for x in registry['reader_registry'] if x['id'] == 'state-resolver')
        self.assertEqual(resolver['check_ids'], ['C-REFERENCES'])
        root = self.miniature()
        manifest = self.reference_manifest(root, [])
        registry_path = Path(manifest['registries']['path'])
        registry_path.write_bytes(encoded(registry))
        manifest['registries'] = binding(registry_path)
        path = put(root, 'manifest.json', encoded(manifest))
        value = self.result(self.cli(root, 'code/state/icm21_check.py', 'references',
                                    '--root', root, '--manifest', path), 2)
        ids = [x['registry_id'] for x in value['readers']]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))
        expected = {x['id']: x['check_ids'] for x in registry['reader_registry']}
        for row in value['readers']:
            self.assertIn(row['registry_id'], expected)
            self.assertEqual([x['id'] for x in row['checks']], expected[row['registry_id']])
        self.assertTrue(any(check['status'] == 'UNVERIFIED'
                            for row in value['readers'] for check in row['checks']))

    def test_candidate_registry_adapter(self):
        self.require_file('code/state/icm21_check.py', 'candidate registry adapter integration')
        candidate = self.require_file('plans/icm21/specs/REGISTRIES.json', 'candidate registry')
        registry = json.loads(candidate.read_bytes())
        original = json.loads(sealed('REGISTRIES.json'))
        for collection in ('reader_registry', 'loader_registry'):
            old = {row['id']: row for row in original[collection]}
            new = {row['id']: row for row in registry[collection]}
            self.assertEqual(set(new), set(old))
            self.assertEqual(len(new), len(registry[collection]))
            for key in old:
                self.assertEqual(new[key]['check_ids'], old[key]['check_ids'])
        entry = next(row for row in registry['reader_registry'] if row['id'] == 'labviz-context')
        self.assertEqual(entry['adapter_argv'], ['.venv/bin/python', '-B', '-m', 'unittest',
                                                 'test_icm21.ReaderControls'])
        self.assertNotIn('code.tests', ' '.join(entry['adapter_argv']))
        self.assertEqual(registry['dispatcher'], original['dispatcher'])


class FixtureContractControls(unittest.TestCase):
    def test_saved_behavioral_baselines(self):
        # These exact base subjects stop at named absence assertions, before effects.
        with tempfile.TemporaryDirectory(prefix='icm21-base-', dir='/private/tmp') as temporary:
            baseline = Path(temporary)
            inputs = ('code/state/build_index.py', 'code/state/resolve_path.py', MAP_PATH)
            for relative in inputs:
                result = subprocess.run(['git', 'show', BASE + ':' + relative],
                                        cwd=SOURCE_ROOT, capture_output=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                self.assertTrue(result.stdout, 'empty baseline source: ' + relative)
                put(baseline, relative, result.stdout)
                if relative != MAP_PATH:
                    self.assertEqual(result.stdout, sealed('base/' + relative))
            self.assertFalse((baseline / 'code/state/icm21_check.py').exists())
            self.assertFalse((baseline / 'code/ops/git/workspace_gate.py').exists())
            source_root = SOURCE_ROOT
            try:
                globals()['SOURCE_ROOT'] = baseline
                for name, methods in SELECTED.items():
                    for method in methods:
                        stream = io.StringIO()
                        with patch.dict(sys.modules), patch.dict(
                                os.environ, {'LLMDB_ROOT': str(baseline)}):
                            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
                                unittest.TestSuite([globals()[name](method)]))
                        output = stream.getvalue()
                        observation = {'control': name + '.' + method, 'base': BASE,
                                       'tests': result.testsRun, 'failures': len(result.failures),
                                       'errors': len(result.errors), 'output': output}
                        print('BEHAVIORAL_BASELINE ' + json.dumps(observation, sort_keys=True))
                        self.assertEqual(result.testsRun, 1, output)
                        self.assertEqual(len(result.failures), 1, output)
                        self.assertEqual(result.errors, [], output)
                        self.assertEqual(result.skipped, [], output)
                        self.assertEqual(result.expectedFailures, [], output)
                        self.assertEqual(result.unexpectedSuccesses, [], output)
                        self.assertIn('AssertionError', output)
                        self.assertIn('absent behavior:', output)
            finally:
                globals()['SOURCE_ROOT'] = source_root

    def test_complete_collection(self):
        loader = unittest.TestLoader()
        for name, methods in SELECTED.items():
            cls = globals()[name]
            self.assertTrue(issubclass(cls, unittest.TestCase))
            self.assertEqual(set(loader.getTestCaseNames(cls)), set(methods))
            self.assertEqual(loader.loadTestsFromTestCase(cls).countTestCases(), len(methods))

    def test_d2_complete_input_identity(self):
        self.assertEqual(set(D2_POSITIVE), {'inputs', 'map'})
        self.assertEqual(set(D2_POSITIVE['inputs']), {'_index/path-map.tsv', '_index/icm21-path-map.tsv'})
        self.assertTrue(all(isinstance(value, bytes) for value in D2_POSITIVE['inputs'].values()))
        self.assertEqual(D2_POSITIVE['map'], d2_map(D2_POSITIVE['inputs'], {}))
        self.assertFalse(D2_POSITIVE['map'].endswith(b'\n'))
        for key in ('sealed', 'relocations'):
            self.assertFalse(Path(json.loads(D2_POSITIVE['map'])['derived_from'][key]['path']).is_absolute())

    def test_sealed_interface_definition(self):
        definitions = json.loads(sealed('foundation-specs'))['T004']
        self.assertEqual(definitions['subject'], 'code/tests/test_icm21.py')
        self.assertEqual(definitions['contract'], type(self).__name__)
        for name, methods in definitions['required'].items():
            self.assertTrue(set(methods) <= set(SELECTED[name]))


if __name__ == '__main__':
    unittest.main()
