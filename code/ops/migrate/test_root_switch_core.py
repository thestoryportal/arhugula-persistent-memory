"""Step 411: value fixtures, including malformed observations and atomic refusal."""
import ast
import builtins
import copy
from dataclasses import replace
from hashlib import sha256
import os
import unittest
from unittest import mock

from ops.migrate import fdsafe, root_readers_core as rows
from ops.migrate import root_switch_core as core


def file(data=b'old\xff old', mode=0o755, preimage='/run/pre/1'):
    return core.FileState(data, sha256(data).hexdigest(), mode, preimage)


def fixture():
    registry = (
        rows.Replace('bin/tool', 'old', 'new', 2),
        rows.Install('bin/tool', '/deploy/tool'),
        rows.Rename('/projects/old', '/projects/new'),
        rows.Rename('/backup/old', '/backup/new'),
        rows.Check('reader', 'readers'), rows.Stop('writer'),
        rows.Record('/history'),
    )
    state = core.PreState(
        m='/old/root', r='/new/root', m_device=7, r_parent_device=7,
        r_exists=False, tracked_clean=True, head='a' * 40, pinned_sha='a' * 40,
        processes={'writer': ()}, locks=(), markers=(), launchd='loaded',
        targets={'bin/tool': file(), '/deploy/tool': core.Absent()},
        sources={'bin/tool': core.Source(b'old\xff old', 0o755)},
        pairs=(core.BackupPair('ssd', '/old', '/backup', '/p.excludes'),
               core.BackupPair('gdrive', '/new/root', 'gdrive:backup', '/r.excludes'),
               core.BackupPair('ssd', '/new/root', '/backup/new', '/r.excludes')))
    return registry, state


class Planning(unittest.TestCase):
    def test_complete_batches_and_operands(self):
        registry, state = fixture()
        result = core.plan(registry, state)
        self.assertEqual(result.failures, ())
        self.assertEqual(tuple(b.name for b in result.batches),
                         ('PAUSE', 'MOVE', 'REPAIR', 'CHECK', 'BACKUP', 'RESUME'))
        actions = [b.actions for b in result.batches]
        self.assertEqual(actions[0], (core.Launchd('loaded', 'unloaded'), core.Quiesce()))
        self.assertEqual(actions[1], (core.Rename('/old/root', '/new/root'),
                                     core.Rename('/projects/old', '/projects/new'),
                                     core.Rename('/backup/old', '/backup/new')))
        self.assertEqual(actions[2], (
            core.Replace('/new/root/bin/tool', state.targets['bin/tool'], b'new\xff new', 0o755),
            core.Install('/deploy/tool', core.Absent(), b'new\xff new', 0o755)))
        self.assertEqual(actions[2][1].pre.kind, 'absent')
        self.assertEqual(actions[3], (core.Check('readers'),))
        self.assertEqual(actions[4], (core.BackupRun((state.pairs[0], state.pairs[2])),))
        self.assertEqual(actions[5], (core.Launchd('unloaded', 'loaded'),))
        self.assertEqual(tuple(a.kind for batch in actions for a in batch),
                         ('LAUNCHD', 'QUIESCE', 'RENAME', 'RENAME', 'RENAME',
                          'REPLACE', 'INSTALL', 'CHECK', 'BACKUP_RUN', 'LAUNCHD'))

    def test_start_unloaded_and_existing_install_mode(self):
        registry, state = fixture()
        state.targets['/deploy/tool'] = file(b'existing', 0o640, '/run/pre/2')
        result = core.plan(registry, replace(state, launchd='unloaded'))
        self.assertEqual(result.batches[0].actions[0], core.Launchd('unloaded', 'unloaded'))
        action = result.batches[2].actions[1]
        self.assertEqual((action.pre, action.post_bytes, action.post_mode),
                         (state.targets['/deploy/tool'], b'new\xff new', 0o640))

    def test_all_preconditions_reported_without_actions(self):
        registry, state = fixture()
        state = replace(state, r_exists=True, r_parent_device=8, tracked_clean=False,
                        head='b' * 40, processes={'writer': (21, 22)},
                        locks=('ship.lock',), markers=('T400',))
        result = core.plan(registry, state)
        self.assertEqual(result.batches, ())
        self.assertEqual(result.failures, ('R exists: /new/root', 'st_dev differs',
                         'tracked tree dirty', 'HEAD differs from pinned sha',
                         'STOP writer: (21, 22)', 'L/tools lock: ship.lock', 'ready marker: T400'))

    def test_each_precondition_alone_blocks(self):
        registry, state = fixture()
        for changes in ({'r_exists': True}, {'r_parent_device': 8}, {'tracked_clean': False},
                        {'head': 'b' * 40}, {'processes': {'writer': (1,)}},
                        {'locks': ('x',)}, {'markers': ('x',)}):
            with self.subTest(changes=changes):
                result = core.plan(registry, replace(state, **changes))
                self.assertEqual(result.batches, ())
                self.assertEqual(len(result.failures), 1)

    def test_counts_exact_measured_zero_and_atomicity(self):
        registry, state = fixture()
        for count, succeeds in ((2, True), ('measured', True), (1, False), (3, False), (0, False)):
            with self.subTest(count=count):
                result = core.plan((replace(registry[0], count=count),) + registry[1:], state)
                self.assertEqual(bool(result.batches), succeeds)
                if not succeeds:
                    self.assertIn('row 0 bin/tool', result.failures[0])
        state.targets['bin/tool'] = file(b'no match')
        state.sources['bin/tool'] = core.Source(b'no match', 0o755)
        for count, succeeds in ((0, True), ('measured', False), (1, False)):
            result = core.plan((replace(registry[0], count=count),) + registry[1:], state)
            self.assertEqual(bool(result.batches), succeeds)

    def test_multiple_counts_and_precondition_failures_accumulate(self):
        registry, state = fixture()
        state.targets['/outside'] = file(b'none', preimage='/run/pre/3')
        registry += (rows.Replace('/outside', 'missing', 'next', 1),)
        state.targets['bin/tool'] = file(b'bad')
        result = core.plan(registry, replace(state, tracked_clean=False))
        self.assertEqual(result.batches, ())
        self.assertEqual(len(result.failures), 3)
        self.assertIn('row 0 bin/tool', result.failures[1])
        self.assertIn('row 7 /outside', result.failures[2])

    def test_grouped_replacements_count_original_bytes_no_cascade(self):
        registry, state = fixture()
        registry = (rows.Replace('bin/tool', 'old', 'new', 2),
                    rows.Replace('bin/tool', 'new', 'final', 1)) + registry[1:]
        state.targets['bin/tool'] = file(b'old new old')
        state.sources['bin/tool'] = core.Source(b'old new old', 0o755)
        result = core.plan(registry, state)
        self.assertEqual(len(result.batches[2].actions), 2)
        self.assertEqual(result.batches[2].actions[0].post_bytes, b'new final new')
        self.assertEqual(result.batches[2].actions[1].post_bytes, b'new final new')

    def test_replacement_preserves_prefix_suffix_and_non_utf8_bytes(self):
        registry, state = fixture()
        data = b'\xff before old old after\x00'
        state.targets['bin/tool'] = file(data)
        state.sources['bin/tool'] = core.Source(data, 0o755)
        self.assertEqual(core.plan(registry, state).batches[2].actions[0].post_bytes,
                         b'\xff before new new after\x00')

    def test_overlap_refuses(self):
        registry, state = fixture()
        state.targets['bin/tool'] = file(b'old')
        registry = (rows.Replace('bin/tool', 'old', 'x', 1),
                    rows.Replace('bin/tool', 'ld', 'y', 1)) + registry[1:]
        result = core.plan(registry, state)
        self.assertEqual(result.batches, ())
        self.assertIn('overlapping replacements', result.failures[0])

    def test_outside_paths_component_boundary_and_install_order(self):
        registry, state = fixture()
        registry = (rows.Install('plain', '/old/root/config'),
                    rows.Replace('/old/rootish/x', 'old', 'new', 2),
                    rows.Replace('/old/root/in', 'old', 'new', 2)) + registry
        state.targets.update({'/old/root/config': core.Absent(),
                              '/old/rootish/x': file(preimage='/run/pre/3'),
                              '/old/root/in': file(preimage='/run/pre/4')})
        state.sources['plain'] = core.Source(b'unchanged', 0o600)
        repairs = core.plan(registry, state).batches[2].actions
        self.assertEqual(repairs[0], core.Install('/new/root/config', core.Absent(), b'unchanged', 0o600))
        self.assertEqual(repairs[1].path, '/old/rootish/x')
        self.assertEqual(repairs[2].path, '/new/root/in')

    def test_missing_observations_refuse(self):
        registry, state = fixture()
        for field, key in (('targets', 'bin/tool'), ('targets', '/deploy/tool'),
                           ('sources', 'bin/tool'), ('processes', 'writer')):
            changed = copy.deepcopy(state)
            del getattr(changed, field)[key]
            with self.subTest(field=field, key=key), self.assertRaises(fdsafe.Refusal):
                core.plan(registry, changed)

    def test_absent_replace_and_conflicting_sources_refuse(self):
        registry, state = fixture()
        state.targets['bin/tool'] = core.Absent()
        with self.assertRaises(fdsafe.Refusal):
            core.plan(registry, state)
        registry, state = fixture()
        state.sources['bin/tool'] = core.Source(b'other', 0o755)
        with self.assertRaises(fdsafe.Refusal):
            core.plan(registry, state)

    def test_install_source_mode_must_match_replacement_prestate(self):
        registry, state = fixture()
        state.sources['bin/tool'] = core.Source(b'old\xff old', 0o600)
        with self.assertRaises(fdsafe.Refusal):
            core.plan(registry, state)

    def test_unencodable_edits_are_not_silently_replaced(self):
        registry, state = fixture()
        for field in ('old', 'new'):
            changed = (replace(registry[0], **{field: '\ud800'}),) + registry[1:]
            with self.subTest(field=field), self.assertRaises(UnicodeEncodeError):
                core.plan(changed, state)
    def test_inputs_unchanged_and_unregistered_process_allowed(self):
        registry, state = fixture()
        state.processes['unrelated'] = (90,)
        before = copy.deepcopy((registry, state))
        self.assertTrue(core.plan(registry, state).batches)
        self.assertEqual((registry, state), before)


class Malformed(unittest.TestCase):
    def test_extra_observations_are_validated_without_downstream_masking(self):
        registry, state = fixture()
        cases = (
            ('processes', '', ()), ('targets', 'bad/../path', core.Absent()),
            ('targets', '/extra', object()),
            ('targets', '/extra', file(b'x', -1)),
            ('targets', '/extra', file(b'x', True)),
            ('targets', '/extra', file(b'x', 0o10000)),
            ('sources', 'bad/../path', core.Source(b'x', 0)),
            ('sources', '/absolute', core.Source(b'x', 0)),
            ('sources', 'extra', core.Source('text', 0)),
            ('sources', 'extra', core.Source(b'x', -1)),
        )
        for field, key, value in cases:
            changed = copy.deepcopy(state)
            getattr(changed, field)[key] = value
            with self.subTest(field=field, key=key, value=value), self.assertRaises(fdsafe.Refusal):
                core.plan(registry, changed)
        with self.assertRaises(fdsafe.Refusal):
            core.plan(registry, replace(state, pairs=state.pairs +
                      (core.BackupPair('', '/a', '/b', '/e'),)))

    def test_bad_state_fields(self):
        registry, state = fixture()
        bads = {'m': ('relative', '/', '/x/../y', None), 'r': ('relative', '/', None),
                'm_device': (-1, True, '7'), 'r_parent_device': (-1, False, None),
                'r_exists': (1, None), 'tracked_clean': (0, None),
                'head': ('', 'z' * 40, None), 'pinned_sha': ('a', None),
                'launchd': ('unknown', True), 'processes': (None, [], {'writer': None}, {'writer': (0,)}),
                'locks': (None, 'x', ('',)), 'markers': (None, 1, ('',)),
                'targets': (None, [], {'bin/tool': None}), 'sources': (None, [], {'bin/tool': None}),
                'pairs': (None, (), ('ssd',))}
        for name, values in bads.items():
            for value in values:
                with self.subTest(name=name, value=value), self.assertRaises(fdsafe.Refusal):
                    core.plan(registry, replace(state, **{name: value}))

    def test_bad_files_sources_and_pairs(self):
        registry, state = fixture()
        for changes in ({'data': 'text'}, {'sha256': 'f' * 64}, {'sha256': None},
                        {'mode': -1}, {'mode': 0o10000}, {'mode': True},
                        {'preimage': 'relative'}, {'preimage': '/old/root/pre'}):
            changed = copy.deepcopy(state)
            changed.targets['bin/tool'] = replace(file(), **changes)
            with self.subTest(changes=changes), self.assertRaises(fdsafe.Refusal):
                core.plan(registry, changed)
        for source in (core.Source('text', 0o755), core.Source(b'x', -1)):
            changed = copy.deepcopy(state)
            changed.sources['bin/tool'] = source
            with self.assertRaises(fdsafe.Refusal):
                core.plan(registry, changed)
        for pair in (core.BackupPair('', '/a', '/b', '/e'),
                     core.BackupPair('ssd', 'relative', '/b', '/e'),
                     core.BackupPair('ssd', '/a', '', '/e'),
                     core.BackupPair('ssd', '/a', '/b', 'relative')):
            with self.assertRaises(fdsafe.Refusal):
                core.plan(registry, replace(state, pairs=(pair,)))

    def test_invalid_rows_roots_and_duplicate_writers(self):
        registry, state = fixture()
        for value in (None, 'rows', (object(),)):
            with self.assertRaises(fdsafe.Refusal):
                core.plan(value, state)
        with self.assertRaises(fdsafe.Refusal):
            core.plan(registry, None)
        for root in (state.m, state.m + '/child', '/old'):
            with self.assertRaises(fdsafe.Refusal):
                core.plan(registry, replace(state, r=root))
        with self.assertRaises(fdsafe.Refusal):
            core.plan(registry + (registry[1],), state)


class Purity(unittest.TestCase):
    def test_import_allowlist(self):
        with open(core.__file__, encoding='utf-8') as stream:
            tree = ast.parse(stream.read())
        # [LAW:effects-at-boundaries] Imports must not expose an I/O escape.
        imports = {
            '__future__': {'annotations': 'annotations'},
            'collections.abc': {'Mapping': 'Mapping'},
            'dataclasses': {'dataclass': 'dataclass', 'field': 'field'},
            'hashlib': {'sha256': 'sha256'},
            'typing': {'Literal': 'Literal'},
            'ops.migrate': {'fdsafe': 'fdsafe', 'root_readers_core': 'registry'},
        }
        attributes = {
            name: set() for bindings in imports.values() for name in bindings.values()
        }
        attributes.update({
            'fdsafe': {'Refusal'},
            'registry': {'Row', 'Replace', 'Rename', 'Install', 'Check', 'Stop',
                         'Record', '_count', '_mapping', '_path', '_text'},
        })
        calls = {
            'BackupRun', 'Batch', 'Check', 'Install', 'Launchd', 'Quiesce',
            'Rename', 'Replace', 'Result', '_absolute', '_mode', '_post',
            '_repair', '_require', '_sequence', '_under', '_validate',
            'all', 'any', 'dataclass', 'enumerate', 'field', 'getattr',
            'isinstance', 'len', 'set', 'sha256', 'tuple', 'type', 'zip',
        }
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.fail(f'unapproved import: {ast.unparse(node)}')
            elif isinstance(node, ast.ImportFrom):
                self.assertEqual(node.level, 0)
                self.assertIn(node.module, imports)
                names.add(node.module)
                for alias in node.names:
                    self.assertIn(alias.name, imports[node.module])
                    self.assertEqual(alias.asname or alias.name,
                                     imports[node.module][alias.name])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertIn(node.func.id, calls, ast.unparse(node))
            elif isinstance(node, ast.Attribute):
                root = node.value
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name) and root.id in attributes:
                    self.assertIsInstance(node.value, ast.Name, ast.unparse(node))
                    self.assertIn(node.attr, attributes[root.id], ast.unparse(node))
        self.assertIn('ops.migrate', names)

    def test_no_effects(self):
        registry, state = fixture()
        def forbidden(*args, **kwargs):
            raise AssertionError('planner performed IO')
        names = ('open', 'stat', 'lstat', 'fstat', 'scandir', 'listdir', 'walk',
                 'readlink', 'statvfs', 'getcwd', 'getenv', 'access')
        with mock.patch.object(builtins, 'open', forbidden), \
                mock.patch.multiple(os, **{n: forbidden for n in names}), \
                mock.patch('time.time', forbidden), mock.patch('time.monotonic', forbidden):
            self.assertTrue(core.plan(registry, state).batches)
