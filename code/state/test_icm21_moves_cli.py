"""Tests for `icm21_check.py moves` (plan Step 204): one JSON result for the pre and post stages.

The subcommand is wiring: validate_move (icm21_moves.py) judges the pre stage and check_retained
(icm21_retained.py) the post stage. Each case builds its inputs as real files in a temporary
directory and runs the real main(). Attacks come from code/tests/fault_kit.py.
"""
import contextlib
import copy
import errno
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
import icm21_check
import icm21_moves  # noqa: F401  imported before any patch, so its schema read is never attacked
import icm21_retained
from ops.migrate import fdsafe

SCRIPT = Path(icm21_check.__file__).resolve()
CODE = SCRIPT.parent.parent
IDS = ['MV-1', 'MV-2', 'MV-3', 'MV-4']
FILES = ('req-a.tsv', 'req-b.tsv', 'phase.tsv', 'plans.json', 'executor.json', 'retention.json',
         'approval.json', 'leaves.json', 'repairs.json', 'routes.tsv', 'observed.json')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dumps(value):
    return json.dumps(value, sort_keys=True).encode()


def named(name):
    """A fault_kit match: the call's first argument is this name or path."""
    return lambda first, *args, **kwargs: first == name


def snapshot(base):
    """Every entry under base: lstat identity and, for a regular file, its bytes."""
    seen = {}
    for directory, dirs, files in os.walk(base):
        for name in sorted(dirs + files):
            path = os.path.join(directory, name)
            st = os.lstat(path)
            data = Path(path).read_bytes() if os.path.isfile(path) and \
                not os.path.islink(path) else None
            seen[path] = (st.st_mode, st.st_ino, st.st_size, st.st_mtime_ns, data)
    return seen


class Fixture:
    """A miniature M with four units moved to M/dest, and every moves input as a file."""

    def __init__(self, base):
        self.base = base
        self.root, self.specs = base / 'M', base / 'specs'
        self.custody, self.decoy = base / 'custody', base / 'decoy'
        for folder in (self.root, self.specs, self.custody, self.decoy, self.root / 'dest'):
            folder.mkdir()
        (self.decoy / 'file').write_bytes(b'decoy\n')
        self.requirements = {'req-a.tsv': IDS[:2], 'req-b.tsv': IDS[2:]}
        self.extra_requirements = {}
        self.leaves, self.observed_leaves, self.routes, self.moves = [], [], [], []
        for number, identity in enumerate(IDS, 1):
            unit = self.root / ('u%d' % number)
            unit.mkdir()
            data = ('unit %d\n' % number).encode()
            (unit / 'f.txt').write_bytes(data)
            source, target = str(unit / 'f.txt'), str(self.root / 'dest' / unit.name / 'f.txt')
            leaf = {'source': source, 'kind': 'file', 'bytes': len(data), 'sha256': sha(data),
                    'link_text': None, 'device': 1, 'inode': 100 + number, 'nlink': 1}
            self.leaves.append(leaf)
            self.observed_leaves.append(dict(leaf, source=target, inode=200 + number))
            self.routes.append([identity, source, target, 'file', str(len(data)), 'MOVE',
                                'integration', 'record'])
            self.moves.append({'id': 'MOVE-%d' % number, 'prd_ids': ['ICM-R4'], 'action': 'MOVE',
                               'source': str(unit), 'target': str(self.root / 'dest' / unit.name),
                               'kind': 'directory', 'bytes': len(data),
                               'before_sha256': sha(data),
                               'source_manifest': {'path': str(self.custody / 'leaves.json'),
                                                   'sha256': '0' * 64},
                               'lane': 'integration', 'reader_check_ids': []})
        self.entry = {'id': 'E-1', 'replaces': list(IDS), 'roots': [str(self.root)],
                      'run_units': [], 'moves': self.moves}
        self.plans = {'entries': [{'id': 'E-0', 'replaces': ['MV-9']}, self.entry]}
        self.operations = list(IDS)
        self.repairs = {'schema_version': 1, 'repairs': []}
        self.containers = []
        self.executor_path = None  # None: retention binds the --manifest file itself
        self.observed = None  # None: a unit_manifest document of observed_leaves
        self.edits = {}  # file name -> bytes written in place of the generated ones

    def path(self, name):
        return (self.specs if name.endswith('.tsv') and name != 'routes.tsv'
                else self.custody) / name

    def put(self, name, data):
        data = self.edits.get(name, data)
        self.path(name).write_bytes(data)
        return {'path': str(self.path(name)), 'sha256': sha(data)}

    def publish(self):
        header = '\t'.join(icm21_check.MOVES_TABLES['requirements']) + '\n'
        for name, identities in {**self.requirements, **self.extra_requirements}.items():
            rows = ''.join('%s\t%s/src-%s\t%s/dst-%s\tHOLD\t1\tscience\tintegration\tC-MOVE'
                           '\tnone\tICM-R4\n' % (i, self.root, i, self.root, i) for i in identities)
            self.put(name, (header + rows).encode())
        self.put('phase.tsv', b'source_relative\ttarget_relative\tobserved_sha256\n'
                 b'a/x.md\tb/x.md\t' + b'1' * 64 + b'\n')
        plan = self.put('plan.json', b'{"plan_id": "P-1"}\n')
        approval = self.put('approval.json', dumps({
            'approval_id': 'A-1', 'plan_id': 'P-1', 'plan_sha256': plan['sha256'], 'gate': 'G4',
            'approved_by': 'operator', 'approved_at': '2026-10-16T00:00:00Z',
            'expires_at': '2026-12-31T00:00:00Z', 'decision': 'approved'}))
        journal = {'path': str(self.custody / 'operations.jsonl'), 'sha256': '2' * 64}
        executor = self.put('executor.json', dumps({'schema_version': 1, 'operations': [
            {'operation_id': identity, 'prd_ids': ['ICM-R4'], 'plan': plan, 'approval': approval,
             'journal': journal, 'verification': None, 'readers': None, 'acceptance': None,
             'rollback': None} for identity in self.operations]}))
        if self.executor_path is not None:
            executor = {'path': str(self.executor_path), 'sha256': executor['sha256']}
        leaves = self.put('leaves.json', dumps({'schema_version': 1, 'leaves': self.leaves}))
        routes = self.put('routes.tsv', ('\t'.join(icm21_retained.ROUTE_HEADER) + '\n' + ''.join(
            '\t'.join(row) + '\n' for row in self.routes)).encode())
        repairs = self.put('repairs.json', dumps(self.repairs))
        self.put('retention.json', dumps({'schema_version': 1, 'leaves': leaves, 'routes': routes,
                                          'repairs': repairs, 'executor': executor,
                                          'containers': self.containers}))
        self.put('plans.json', dumps(self.plans))
        observed = self.observed if self.observed is not None else {
            'schema_version': 1, 'root': str(self.root / 'dest'), 'leaves': self.observed_leaves,
            'git_roots': []}
        self.put('observed.json', dumps(observed))

    def argv(self, stage, observed=None):
        argv = ['moves', '--root', str(self.root)]
        for name in self.requirements:
            argv += ['--requirements', str(self.path(name))]
        argv += ['--phase-files', str(self.path('phase.tsv')), '--plans',
                 str(self.path('plans.json')), '--entry', 'E-1', '--manifest',
                 str(self.path('executor.json')), '--retention', str(self.path('retention.json')),
                 '--stage', stage]
        if (stage == 'post') if observed is None else observed:
            argv += ['--observed', str(self.path('observed.json'))]
        return argv


# fdsafe reads live paths with macOS F_GETPATH; the CI seam step also runs this file on Linux.
@unittest.skipUnless(hasattr(fcntl, 'F_GETPATH'), 'fdsafe needs fcntl.F_GETPATH (macOS)')
class MovesCase(unittest.TestCase):
    def setUp(self):
        base = Path(os.path.realpath(tempfile.mkdtemp(prefix='moves-cli-')))
        self.addCleanup(shutil.rmtree, base)
        self.fx = Fixture(base)

    def main(self, argv):
        out = io.StringIO()
        with mock.patch.object(sys, 'argv', ['icm21_check.py'] + argv), \
                contextlib.redirect_stdout(out):
            code = icm21_check.main()
        lines = out.getvalue().splitlines()
        self.assertEqual(len(lines), 1, out.getvalue())
        return code, json.loads(lines[0])

    def run_stage(self, stage, publish=True, **kwargs):
        if publish:
            self.fx.publish()
        return self.main(self.fx.argv(stage, **kwargs))

    def assertExit(self, expected, stage, status=None, **kwargs):
        code, result = self.run_stage(stage, **kwargs)
        self.assertEqual(code, expected, result)
        self.assertEqual(result['status'],
                         status or {0: 'PASS', 1: 'FAIL', 2: 'UNVERIFIED'}[expected], result)
        return result

    def assertRefused(self, stage='post', text='', **kwargs):
        code, result = self.run_stage(stage, **kwargs)
        self.assertEqual((code, result['status']), (2, 'UNVERIFIED'), result)
        self.assertEqual(sorted(result), ['reason', 'status'], result)
        self.assertIn(text, result['reason'])
        self.assertNotIn('\n', result['reason'])
        return result['reason']

    def reasons(self, result):
        return [finding['reason'] for finding in result['findings']]


class PassCases(MovesCase):
    def test_post_stage_passes_on_a_complete_move(self):
        result = self.assertExit(0, 'post')
        self.assertEqual(result, {'status': 'PASS', 'stage': 'post', 'entry': 'E-1',
                                  'findings': []})

    def test_pre_stage_passes_before_the_move(self):
        result = self.assertExit(0, 'pre')
        self.assertEqual(result, {'status': 'PASS', 'stage': 'pre', 'entry': 'E-1',
                                  'findings': []})

    def test_observed_unit_manifest_document_is_projected(self):
        # unit_manifest writes root and git_roots, which the strict LeafManifest refuses.
        self.fx.publish()
        document = json.loads(self.fx.path('observed.json').read_bytes())
        self.assertEqual(sorted(document), ['git_roots', 'leaves', 'root', 'schema_version'])
        self.assertEqual(self.run_stage('post', publish=False)[0], 0)

    def test_requirement_rows_load_from_every_requirements_file(self):
        self.fx.requirements = {'req-a.tsv': IDS[:1], 'req-b.tsv': IDS[1:3],
                                'req-c.tsv': IDS[3:]}
        self.assertExit(0, 'post')

    def test_requirements_without_a_final_newline_load(self):
        self.fx.publish()
        path = self.fx.path('req-b.tsv')
        path.write_bytes(path.read_bytes().rstrip(b'\n'))
        self.assertEqual(self.run_stage('post', publish=False)[0], 0)

    def test_relative_input_paths_resolve_against_the_working_directory(self):
        self.fx.publish()
        argv = self.fx.argv('post')
        argv[argv.index('--retention') + 1] = 'retention.json'
        cwd = os.getcwd()
        os.chdir(self.fx.custody)
        self.addCleanup(os.chdir, cwd)
        self.assertEqual(self.main(argv)[0], 0)

    def test_no_input_or_tree_changes_in_either_stage(self):
        self.fx.publish()
        before = snapshot(self.fx.base)
        for stage in ('pre', 'post'):
            self.assertEqual(self.run_stage(stage, publish=False)[0], 0)
            self.assertEqual(snapshot(self.fx.base), before)
        self.fx.operations = IDS[:3]
        self.fx.publish()
        before = snapshot(self.fx.base)
        self.assertEqual(self.run_stage('post', publish=False)[0], 2)
        self.assertEqual(snapshot(self.fx.base), before)


class CoverageCases(MovesCase):
    def test_four_row_entry_with_three_row_evidence_is_incomplete_not_pass(self):
        self.fx.operations = IDS[:3]
        for stage in ('post', 'pre'):
            result = self.assertExit(2, stage)
            self.assertEqual(self.reasons(result), [
                'the entry replaces MV-4 and the executor evidence names no operation for it'])
            self.assertEqual(result['findings'][0]['status'], 'UNVERIFIED')

    def test_missing_evidence_row_exits_2_even_beside_a_failure(self):
        self.fx.operations = IDS[:3]
        self.fx.observed_leaves[0]['sha256'] = '9' * 64
        result = self.assertExit(2, 'post')
        self.assertIn('FAIL', {finding['status'] for finding in result['findings']})

    def test_evidence_row_outside_the_entry_fails(self):
        self.fx.operations = IDS + ['MV-5']
        result = self.assertExit(1, 'post')
        self.assertEqual(self.reasons(result), [
            'the executor evidence names MV-5, which the entry does not replace'])

    def test_required_set_comes_from_the_entry_not_the_evidence(self):
        self.fx.entry['replaces'] = IDS[:2]
        self.fx.routes = self.fx.routes[:2]
        self.fx.leaves, self.fx.observed_leaves = self.fx.leaves[:2], self.fx.observed_leaves[:2]
        result = self.assertExit(1, 'post')
        self.assertEqual(self.reasons(result), [
            'the executor evidence names MV-3, which the entry does not replace',
            'the executor evidence names MV-4, which the entry does not replace'])

    def test_evidence_naming_one_row_twice_fails(self):
        self.fx.operations = IDS + ['MV-2']
        result = self.assertExit(1, 'post')
        self.assertEqual(self.reasons(result), ['the executor evidence names MV-2 twice'])

    def test_route_row_outside_the_entry_fails(self):
        self.fx.routes[0][0] = 'MV-9'
        for stage in ('post', 'pre'):
            result = self.assertExit(1, stage)
            self.assertIn('route row names MV-9, which the entry does not replace',
                          self.reasons(result))

    def test_split_files_move_is_unverified(self):
        self.fx.moves[0]['action'] = 'SPLIT_FILES'
        for stage in ('post', 'pre'):
            result = self.assertExit(2, stage)
            self.assertIn('C-PHASE (SPLIT_FILES) is not checked by moves', self.reasons(result))


class PostCases(MovesCase):
    def test_changed_byte_at_the_target_fails(self):
        self.fx.observed_leaves[0]['sha256'] = '9' * 64
        result = self.assertExit(1, 'post')
        self.assertEqual(self.reasons(result),
                         ['C-MOVE: target differs from the admitted leaf in sha256'])

    def test_hold_route_is_unverified(self):
        self.fx.routes[0][5] = 'HOLD'
        self.fx.observed_leaves[0] = self.fx.leaves[0]
        result = self.assertExit(2, 'post')
        self.assertEqual([f['status'] for f in result['findings']], ['UNVERIFIED'])
        self.assertIn('route action HOLD', self.reasons(result)[0])

    def test_changed_bound_document_fails(self):
        self.fx.publish()
        path = self.fx.path('leaves.json')
        path.write_bytes(path.read_bytes() + b' ')
        for stage in ('post', 'pre'):
            code, result = self.run_stage(stage, publish=False)
            self.assertEqual(code, 1, result)
            self.assertIn('binding digest differs from the supplied bytes', self.reasons(result))

    def test_executor_binding_must_be_the_manifest_file(self):
        # A copy with identical bytes elsewhere: reading the binding's own path would PASS.
        other = self.fx.custody / 'other.json'
        self.fx.executor_path = other
        self.fx.publish()
        shutil.copyfile(self.fx.path('executor.json'), other)
        for stage in ('post', 'pre'):
            code, result = self.run_stage(stage, publish=False)
            self.assertEqual(code, 2, result)
            self.assertIn('bound document was not supplied', self.reasons(result))

    def test_post_needs_observed_and_pre_refuses_it(self):
        self.assertRefused('post', '--observed is required', observed=False)
        self.assertRefused('pre', '--observed is required', observed=True)

    def test_observed_document_without_leaves_is_refused(self):
        for observed in ([], {'schema_version': 1}, {'leaves': []}):
            with self.subTest(observed=observed):
                self.fx.observed = observed
                self.assertRefused('post', 'is not a unit manifest document')


class PreCases(MovesCase):
    def test_existing_target_fails(self):
        (self.fx.root / 'dest' / 'u2').mkdir()
        result = self.assertExit(1, 'pre')
        self.assertEqual(self.reasons(result),
                         ['target already exists: ' + str(self.fx.root / 'dest' / 'u2')])

    def test_absent_run_units_are_unverified(self):
        del self.fx.entry['run_units']
        result = self.assertExit(2, 'pre')
        self.assertEqual(set(self.reasons(result)),
                         {'run_units not supplied: run splitting unchecked'})

    def test_run_unit_around_a_source_fails(self):
        self.fx.entry['run_units'] = [str(self.fx.root / 'u1')]
        self.fx.moves[0]['source'] = str(self.fx.root / 'u1' / 'inner')
        self.fx.leaves[0]['source'] = str(self.fx.root / 'u1' / 'inner' / 'f.txt')
        result = self.assertExit(1, 'pre')
        self.assertIn('move splits run unit ' + str(self.fx.root / 'u1'), self.reasons(result))

    def test_target_outside_the_entry_roots_fails(self):
        self.fx.entry['roots'] = [str(self.fx.root / 'u1'), str(self.fx.root / 'u2'),
                                  str(self.fx.root / 'u3'), str(self.fx.root / 'u4')]
        result = self.assertExit(1, 'pre')
        self.assertIn('target escapes every admitted root: ' + str(self.fx.root / 'dest' / 'u1'),
                      self.reasons(result))

    def test_other_moves_reach_validate_move(self):
        self.fx.moves[1]['target'] = self.fx.moves[0]['target']
        result = self.assertExit(1, 'pre')
        self.assertIn("target collides with another move's target: MOVE-1", self.reasons(result))

    def test_leaves_under_each_source_reach_validate_move(self):
        link = str(self.fx.root / 'u1' / 'out')
        self.fx.leaves.append({'source': link, 'kind': 'symlink', 'bytes': 9,
                               'sha256': sha(b'../../decoy'), 'link_text': '../../decoy',
                               'device': 1, 'inode': 99, 'nlink': 1})
        result = self.assertExit(1, 'pre')
        self.assertEqual(self.reasons(result), ['link crosses the unit boundary: ' + link])

    def test_refused_retention_leaves_leave_validate_move_unverified(self):
        self.fx.edits['leaves.json'] = b'{"schema_version": 1, "leaves": [], "root": "/x"}'
        result = self.assertExit(2, 'pre')
        self.assertIn('leaves not supplied: link boundary unchecked', self.reasons(result))

    def test_target_lstat_error_is_a_refusal_naming_the_target(self):
        target = self.fx.moves[0]['target']
        real = os.lstat

        def failing(path, *args, **kwargs):
            if path == target:
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *args, **kwargs)
        self.fx.publish()
        with mock.patch.object(os, 'lstat', failing):
            reason = self.assertRefused('pre', publish=False)
        self.assertEqual(reason, '%r: Input/output error [EIO]' % target)

    def test_unexpected_lstat_error_propagates(self):
        target = self.fx.moves[0]['target']
        real = os.lstat

        def failing(path, *args, **kwargs):
            if path == target:
                raise RuntimeError('unexpected')
            return real(path, *args, **kwargs)
        self.fx.publish()
        with mock.patch.object(os, 'lstat', failing), self.assertRaises(RuntimeError):
            self.main(self.fx.argv('pre', observed=False))


class InputCases(MovesCase):
    def test_root_must_be_absolute_and_real(self):
        self.fx.publish()
        argv = self.fx.argv('post')
        for root, text in (('M', 'is not an absolute path'),
                           (str(self.fx.base / 'absent'), '[ENOENT]')):
            with self.subTest(root=root):
                argv[2] = root
                code, result = self.main(argv)
                self.assertEqual(code, 2)
                self.assertIn(text, result['reason'])
        os.symlink(self.fx.root, self.fx.base / 'link')
        argv[2] = str(self.fx.base / 'link')
        self.assertEqual(self.main(argv)[0], 2)

    def test_missing_arguments_are_parse_errors(self):
        self.fx.publish()
        argv = self.fx.argv('post')
        for flag in ('--root', '--plans', '--entry', '--manifest', '--retention', '--stage',
                     '--requirements', '--phase-files'):
            with self.subTest(flag=flag):
                kept = [item for at, item in enumerate(argv)
                        if flag not in argv[max(at - 1, 0):at + 1]]
                with contextlib.redirect_stderr(io.StringIO()), \
                        mock.patch.object(sys, 'argv', ['x'] + kept), \
                        self.assertRaises(SystemExit) as raised:
                    icm21_check.main()
                self.assertEqual(raised.exception.code, 2)

    def test_requirements_rows_are_checked(self):
        header = '\t'.join(icm21_check.MOVES_TABLES['requirements']).encode()
        for data, text in ((b'', 'header'), (b'id\tsource\n', 'header'),
                           (header + b'\nMV-1\tx\n', 'has a row without 10 fields'),
                           (header + b'\n\n', 'has a row without 10 fields'),
                           (header + b'\n\xff\n', 'is not UTF-8')):
            with self.subTest(data=data):
                self.fx.edits['req-a.tsv'] = data
                self.assertRefused('post', str(self.fx.path('req-a.tsv')))
                self.assertRefused('post', text)

    def test_requirement_repeated_across_files_is_refused(self):
        self.fx.requirements['req-b.tsv'] = IDS[1:]
        self.assertRefused('post', 'repeats MV-2')

    def test_entry_row_absent_from_every_requirements_file_is_refused(self):
        del self.fx.requirements['req-b.tsv']
        reason = self.assertRefused('post', "that no --requirements file has: ['MV-3', 'MV-4']")
        self.assertIn(str(self.fx.path('plans.json')), reason)

    def test_phase_files_header_is_checked(self):
        self.fx.edits['phase.tsv'] = b'source\ttarget\n'
        self.assertRefused('post', 'does not start with the phase-files header')

    def test_plans_must_name_the_entry_once(self):
        cases = (({'entries': []}, "names entry 'E-1' 0 times"),
                 ({'entries': [self.fx.entry, self.fx.entry]}, "names entry 'E-1' 2 times"),
                 ({'entries': {}}, 'has no entries list of objects'),
                 ({'entries': [self.fx.entry, 'E-2']}, 'has no entries list of objects'),
                 ([self.fx.entry], 'has no entries list of objects'))
        for plans, text in cases:
            with self.subTest(plans=plans):
                self.fx.plans = plans
                self.assertRefused('post', text)

    def test_entry_fields_are_checked(self):
        cases = {'no replaces': lambda e: e.pop('replaces'),
                 'no roots': lambda e: e.pop('roots'),
                 'no moves': lambda e: e.pop('moves'),
                 'moves not a list': lambda e: e.update(moves={}),
                 'replaces not a list': lambda e: e.update(replaces='MV-1'),
                 'replaces empty': lambda e: e.update(replaces=[]),
                 'replaces not strings': lambda e: e.update(replaces=IDS + [5]),
                 'replaces repeated': lambda e: e.update(replaces=IDS + ['MV-1'])}
        for label, edit in cases.items():
            with self.subTest(label):
                entry = copy.deepcopy(self.fx.entry)
                edit(entry)
                self.fx.plans = {'entries': [entry]}
                self.assertRefused('post', "entry 'E-1' lacks unique replaces, roots or a moves")

    def test_inputs_must_be_utf8_json(self):
        for data, text in ((b'{', 'is not JSON'), (b'{"a": NaN}', 'invalid JSON constant'),
                           (b'"\xff"', 'is not UTF-8')):
            with self.subTest(data=data):
                self.fx.edits['plans.json'] = data
                self.assertRefused('post', text)

    def test_deeply_nested_json_propagates(self):
        self.fx.edits['plans.json'] = b'[' * 100000
        self.fx.publish()
        with self.assertRaises(RecursionError):
            self.main(self.fx.argv('post'))

    def test_manifest_must_be_executor_evidence(self):
        self.fx.edits['executor.json'] = b'{"schema_version": 1}'
        self.assertRefused('post', 'is not ExecutorEvidence: missing field')

    def test_unexpected_wire_error_propagates(self):
        self.fx.publish()
        with mock.patch.object(icm21_check, 'validate_wire', side_effect=RuntimeError('wire')), \
                self.assertRaises(RuntimeError):
            self.main(self.fx.argv('post'))

    def test_unexpected_custody_parser_error_propagates(self):
        self.fx.publish()
        for stage in ('post', 'pre'):
            with self.subTest(stage=stage), \
                    mock.patch.object(icm21_retained, 'route_table',
                                      side_effect=RuntimeError('route')), \
                    self.assertRaises(RuntimeError):
                self.main(self.fx.argv(stage, observed=stage == 'post'))

    def test_retention_must_be_an_object_with_bindings(self):
        self.fx.edits['retention.json'] = b'[]'
        self.assertRefused('post', 'is not a RetentionManifest object')
        del self.fx.edits['retention.json']
        for key, value in (('leaves', None), ('routes', {'path': 'routes.tsv'}),
                           ('repairs', 'x')):
            with self.subTest(key=key):
                self.fx.publish()
                path = self.fx.path('retention.json')
                document = json.loads(path.read_bytes())
                document[key] = value
                self.fx.edits['retention.json'] = dumps(document)
                self.assertRefused('post', key + ' is not a Binding with an absolute path')
                del self.fx.edits['retention.json']


class FilesystemCases(MovesCase):
    """fault_kit attacks: every bound file and folder, every call class the tool makes."""

    def folders(self):
        return {'root': self.fx.root, 'specs': self.fx.specs, 'custody': self.fx.custody}

    def test_each_input_file_swapped_for_a_symlink_refuses(self):
        for name in FILES:
            with self.subTest(name=name):
                self.setUp()
                self.fx.publish()
                path = self.fx.path(name)
                with FK.swap_for_symlink('open', 1, path, self.fx.decoy / 'file',
                                         match=named(name)):
                    reason = self.assertRefused('post', publish=False)
                self.assertEqual(reason, '%r: Too many levels of symbolic links [ELOOP]'
                                 % str(path))

    def test_each_folder_swapped_for_a_symlink_refuses(self):
        for label, folder in self.folders().items():
            with self.subTest(folder=label):
                self.setUp()
                folder = self.folders()[label]
                self.fx.publish()
                with FK.swap_for_symlink('open', 1, folder, self.fx.decoy,
                                         match=named(str(folder))):
                    reason = self.assertRefused('post', publish=False)
                # macOS: O_DIRECTORY | O_NOFOLLOW on a symlink fails ENOTDIR, not ELOOP.
                self.assertEqual(reason, '%r: Not a directory [ENOTDIR]' % str(folder))

    def test_each_folder_replaced_by_a_fifo_refuses(self):
        for label in self.folders():
            with self.subTest(folder=label):
                self.setUp()
                folder = self.folders()[label]
                self.fx.publish()
                with FK.fifo_in_place(folder):
                    reason = self.assertRefused('post', publish=False)
                self.assertEqual(reason, '%r: Not a directory [ENOTDIR]' % str(folder))

    def test_each_input_file_replaced_by_a_fifo_refuses(self):
        for name in FILES:
            with self.subTest(name=name):
                self.setUp()
                self.fx.publish()
                path = self.fx.path(name)
                with FK.fifo_in_place(path):
                    reason = self.assertRefused('post', publish=False)
                self.assertEqual(reason, '%r: is not a regular file' % str(path))

    def test_injected_eio_at_each_call_class_names_the_path_and_errno(self):
        first = str(self.fx.path('req-a.tsv'))
        cases = (('open', named('retention.json'), str(self.fx.path('retention.json'))),
                 ('read', None, first), ('fstat', None, first), ('close', None, first),
                 (FK.GETPATH, None, str(self.fx.root)))
        for call, match, path in cases:
            with self.subTest(call=call):
                self.fx.publish()
                with FK.inject_oserror(call, 1, errno.EIO, match=match):
                    reason = self.assertRefused('post', publish=False)
                self.assertEqual(reason, '%r: Input/output error [EIO]' % path)

    def test_eio_on_the_folder_check_after_a_read_names_the_folder(self):
        self.fx.publish()
        # F_GETPATH calls: root hold, then for req-a.tsv: its folder hold, read_named, our check.
        with FK.inject_oserror(FK.GETPATH, 4, errno.EIO):
            reason = self.assertRefused('post', publish=False)
        self.assertEqual(reason, '%r: Input/output error [EIO]' % str(self.fx.specs))

    def test_root_renamed_and_rebound_during_the_run_refuses(self):
        for stage in ('post', 'pre'):
            with self.subTest(stage=stage):
                self.setUp()
                self.fx.publish()
                with FK.rename_and_rebind('open', 1, self.fx.root, match=named('plans.json')):
                    reason = self.assertRefused(stage, publish=False, observed=stage == 'post')
                self.assertEqual(reason, '%r: moved while the check ran' % str(self.fx.root))

    def test_input_folder_renamed_and_rebound_during_a_read_refuses(self):
        for label, name in (('specs', 'req-a.tsv'), ('custody', 'retention.json')):
            with self.subTest(folder=label):
                self.setUp()
                self.fx.publish()
                folder = self.folders()[label]
                with FK.rename_and_rebind('open', 1, folder, when='after', match=named(name)):
                    reason = self.assertRefused('post', publish=False)
                self.assertEqual(reason, '%r: its folder moved while it was read'
                                 % str(self.fx.path(name)))

    def test_unexpected_exceptions_propagate(self):
        self.fx.publish()
        for kind in FK.UNEXPECTED:
            with self.subTest(kind=kind.__name__):
                with FK.raise_unexpected('read', 1, kind), self.assertRaises(kind) as raised:
                    self.main(self.fx.argv('post'))
                self.assertNotIsInstance(raised.exception, fdsafe.Refusal)


class ProcessCases(MovesCase):
    def cli(self, argv):
        environment = dict(os.environ, PYTHONPATH=str(CODE), PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run([sys.executable, '-B', str(SCRIPT)] + argv, capture_output=True,
                              env=environment, timeout=120)

    def test_script_emits_one_json_line_and_exit_code(self):
        self.fx.publish()
        done = self.cli(self.fx.argv('post'))
        self.assertEqual((done.returncode, done.stderr), (0, b''))
        self.assertEqual(json.loads(done.stdout)['status'], 'PASS')
        self.assertEqual(done.stdout.count(b'\n'), 1)

    def test_script_refusal_is_one_line_without_traceback(self):
        self.fx.publish()
        os.symlink(self.fx.decoy, self.fx.base / 'link')
        argv = self.fx.argv('post')
        argv[argv.index('--plans') + 1] = str(self.fx.base / 'link' / 'plans.json')
        done = self.cli(argv)
        self.assertEqual((done.returncode, done.stderr), (2, b''))
        self.assertEqual(done.stdout.count(b'\n'), 1)
        self.assertEqual(json.loads(done.stdout)['reason'],
                         '%r: Not a directory [ENOTDIR]' % str(self.fx.base / 'link'))


class ImportClosureCases(unittest.TestCase):
    """Ruling F1: the staged-hook miniature copies icm21_check.py without the moves closure."""

    def test_other_subcommands_never_import_the_moves_closure(self):
        probe = ('import sys; import icm21_check; print(sorted(set(sys.modules) & '
                 "{'icm21_moves', 'icm21_retained', 'ops.migrate.fdsafe', 'ops'}))")
        environment = dict(os.environ, PYTHONPATH=os.pathsep.join([str(SCRIPT.parent),
                                                                   str(CODE)]))
        done = subprocess.run([sys.executable, '-B', '-c', probe], capture_output=True,
                              env=environment, timeout=120)
        self.assertEqual((done.returncode, done.stdout), (0, b'[]\n'), done.stderr)


if __name__ == '__main__':
    unittest.main()
