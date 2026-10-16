"""ICM v2.1 fixture helpers and FixtureCase, shared by test_icm21 and test_context_audit."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SOURCE_ROOT = Path(os.environ['LLMDB_ROOT'])
SOURCES = Path(__file__).resolve().parents[1] / 'state/icm21'
BASE = 'c4e8ff310a2ccaf48f8661eccdcfd734ccc7a977'
HEADER = b'old\tnew\tdisposition\tunit\n'
ABOUT = 'Derived from sealed path map and approved ICM v2.1 relocations.'
MAP_PATH = 'code/apps/labviz/results_moves.json'
INDEX_PATHS = tuple('_index/' + name + '.md' for name in
                    ('experiments', 'projects', 'evidence', 'checkpoints'))


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
    return (SOURCES / name).read_bytes()


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
        self.temporary = tempfile.TemporaryDirectory(prefix='icm21-', dir=os.path.realpath('/tmp'))
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
