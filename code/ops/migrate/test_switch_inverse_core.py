"""Step 421: exact rollback descriptions from journal recovery values."""
import ast
import builtins
import _io
import io
import os
import subprocess
import time
from contextlib import ExitStack
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from ops.migrate import root_switch_core as a
from ops.migrate import switch_journal_core as j
from ops.migrate import switch_inverse_core as core
from ops.migrate.fdsafe import Refusal


def file(data, mode, path):
    return a.FileState(data, sha256(data).hexdigest(), mode, path)


class Inverses(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.run = temp.name
        self.pre = file(b'old\x00\xff', 0o755, self.run + '/pre/6')
        self.pair = a.BackupPair('ssd', '/parent', '/backup/parent', '/outside/excludes')
        self.rpair = a.BackupPair('ssd', '/root', '/backup/root', '/root/excludes')
        self.actions = (
            a.Launchd('loaded', 'unloaded'), a.Quiesce(),
            a.Rename('/parent/repo', '/root'),
            a.Rename('/projects/old', '/projects/new'),
            a.Rename('/backup/parent/repo', '/backup/root'),
            a.Replace('/root/config', self.pre, b'new', 0o600),
            a.Install('/outside/existing', self.pre, b'new', 0o644),
            a.Install('/outside/new', a.Absent(), b'created', 0o700),
            a.Check('readers'), a.BackupRun((self.pair, self.rpair)),
            a.Launchd('unloaded', 'loaded'))
        self.intents = tuple(self.intent(n, action) for n, action in enumerate(self.actions, 1))

    def intent(self, seq, action, direction='forward', key=None):
        if type(action) in (a.Replace, a.Install):
            pre = (j.FileIdentity(action.pre.sha256, action.pre.mode)
                   if type(action.pre) is a.FileState else a.Absent())
        elif type(action) is a.Rename:
            pre = j.RenameIdentity(j.Inode(1, seq), None)
        elif type(action) is a.Launchd:
            pre = j.AgentIdentity(action.from_state)
        else:
            pre = j.NoIdentity()
        return j.Intent(seq, direction, key or f'op-{seq}', action, pre)

    def state(self, count, pending=None, observation=None, inverses=()):
        records = []
        for item in self.intents[:count] + inverses:
            records.extend((item, j.Done(item.seq, j._post(item))))
        if pending is not None:
            records.append(pending)
        return j.recover(j.Journal(tuple(records), ''), observation,
                         {self.pre.preimage: self.pre.sha256})

    def expected(self, count):
        tail = (a.Launchd('unloaded', 'loaded'),) if count else ()
        moves = (a.Rename('/backup/root', '/backup/parent/repo'),
                 a.Rename('/projects/new', '/projects/old'),
                 a.Rename('/root', '/parent/repo'))
        repairs = (
            a.Rename('/outside/new', self.run + '/undone/8'),
            a.Install('/outside/existing', file(b'new', 0o644, self.pre.preimage + '.inverse-7'),
                      self.pre.data, self.pre.mode),
            a.Replace('/root/config', file(b'new', 0o600, self.pre.preimage + '.inverse-6'),
                      self.pre.data, self.pre.mode))
        middle = repairs[max(0, 8-count):] if count >= 6 else ()
        middle += moves[max(0, 5-count):] if count >= 3 else ()
        backups = (j.ResyncP((self.pair,)), j.BackupCompare((self.pair,))) if count >= 10 else ()
        head = (a.Launchd('loaded', 'unloaded'),) if count == 11 else ()
        return head + (a.Quiesce(),) + middle + backups + tail

    def test_every_batch_cut(self):
        for count in (0, 2, 5, 8, 9, 10, 11):
            with self.subTest(count=count):
                self.assertEqual(core.plan(self.state(count), self.run), self.expected(count))

    def test_each_kind_pending_pre_and_post(self):
        for index, item in enumerate(self.intents):
            with self.subTest(seq=item.seq, observation='pre'):
                state = self.state(index, item, item.pre)
                count = index + 1 if type(item.action) is a.BackupRun else index
                self.assertEqual(core.plan(state, self.run), self.expected(count))
            if type(item.action) not in (a.Check, a.Quiesce, a.BackupRun):
                with self.subTest(seq=item.seq, observation='post'):
                    self.assertEqual(core.plan(self.state(index, item, j._post(item)), self.run),
                                     self.expected(index + 1))

    def test_w14_run_folder_changes_only_undone(self):
        state = self.state(11)
        other = self.run + '/other'
        expected = tuple(a.Rename(x.src, other + '/undone/8')
                         if x == a.Rename('/outside/new', self.run + '/undone/8')
                         else x for x in core.plan(state, self.run))
        self.assertEqual(core.plan(state, other), expected)

    def test_noncanonical_run_refuses_and_names_value(self):
        for path in ('relative', '/a/../b', '/a/./b', '/a//b', '/a/', '/', '', '/a\n'):
            with self.subTest(path=path), self.assertRaises(Refusal) as caught:
                core.plan(self.state(2), path)
            self.assertIn(repr(path), str(caught.exception))

    def test_no_m_operand_before_root_inverse(self):
        result = core.plan(self.state(11), self.run)
        boundary = result.index(a.Rename('/root', '/parent/repo'))
        for action in result[:boundary]:
            for value in vars(action).values():
                if isinstance(value, str):
                    self.assertFalse(value == '/parent/repo' or value.startswith('/parent/repo/'))

    def test_initially_unloaded_pause_restores_unloaded(self):
        item = self.intent(1, a.Launchd('unloaded', 'unloaded'))
        state = j.recover(j.Journal((item,), ''), j.AgentIdentity('unloaded'), {})
        self.assertEqual(core.plan(state, self.run), (a.Quiesce(), a.Launchd('unloaded', 'unloaded')))

    def test_completed_inverse_is_not_repeated(self):
        undo = self.intent(20, a.Rename('/outside/new', self.run + '/undone/8'),
                           'inverse', 'undo:8')
        self.assertEqual(core.plan(self.state(8, inverses=(undo,)), self.run),
                         tuple(x for x in self.expected(8) if x != undo.action))

    def test_resync_pending_restarts_but_done_does_not(self):
        action = j.ResyncP((self.pair,))
        item = self.intent(20, action, 'inverse', 'resync:10')
        pending = self.state(10, item, j.NoIdentity())
        done = self.state(10, inverses=(item,))
        self.assertEqual(core.plan(pending, self.run), self.expected(10))
        self.assertEqual(core.plan(done, self.run), tuple(x for x in self.expected(10) if x != action))

    def test_invalid_state_refuses(self):
        state = self.state(2)
        for bad in (None, {}, replace(state, done=[]), replace(state, inverse_done=[]),
                    replace(state, status=3, stopped=('missing preimage',)),
                    replace(state, pending=self.intents[5])):
            with self.subTest(bad=bad), self.assertRaises(Refusal):
                core.plan(bad, self.run)


    # [LAW:behavior-not-structure] Refusals are checked through the public planner.
    def test_non_intent_refuses(self):
        bad = replace(self.state(0), done=(None,))
        with self.assertRaisesRegex(Refusal, 'state.*expected Intent'):
            core.plan(bad, self.run)

    def test_non_round_trip_intent_refuses(self):
        item = self.intent(10, a.BackupRun([self.pair]))
        bad = replace(self.state(0), done=(item,))
        with self.assertRaisesRegex(Refusal, 'op-10.*invalid intent'):
            core.plan(bad, self.run)

    def test_duplicate_sequence_refuses(self):
        state = self.state(2)
        bad = replace(state, done=(state.done[0], replace(state.done[1], seq=1)))
        with self.assertRaisesRegex(Refusal, 'op-2.*duplicate sequence'):
            core.plan(bad, self.run)

    def test_inverse_keys_mismatch_refuses(self):
        bad = replace(self.state(2), inverse_done=('undo:1',))
        with self.assertRaisesRegex(Refusal, 'state.*inverse keys differ'):
            core.plan(bad, self.run)

    def test_non_unique_covering_pair_refuses(self):
        state = self.state(10)
        for pairs in ((self.pair, self.pair),
                      (self.pair, a.BackupPair('ssd', '/other', '/backup/other',
                                              '/outside/excludes'))):
            item = replace(state.done[-1], action=a.BackupRun(pairs))
            bad = replace(state, done=state.done[:-1] + (item,))
            with self.subTest(pairs=pairs), self.assertRaisesRegex(
                    Refusal, 'BACKUP_RUN.*no unique covering P pair'):
                core.plan(bad, self.run)

    def test_nonfirst_launchd_requires_resume(self):
        state = self.state(11)
        item = self.intent(11, a.Launchd('loaded', 'unloaded'))
        bad = replace(state, done=state.done[:-1] + (item,))
        with self.assertRaisesRegex(Refusal, 'op-11.*expected RESUME'):
            core.plan(bad, self.run)

    def test_pending_resync_must_match_backup(self):
        item = self.intent(20, j.ResyncP((self.pair,)), 'inverse', 'resync:10')
        state = self.state(10, item, j.NoIdentity())
        bad = replace(state, pending=replace(item, action=j.ResyncP((self.rpair,))))
        with self.assertRaisesRegex(Refusal, 'resync:10.*pending RESYNC_P differs'):
            core.plan(bad, self.run)


    def recovery_retry(self, completed, compared=False):
        records = []
        preimages = {self.pre.preimage: self.pre.sha256}
        for item in self.intents[:9]:
            records.extend((item, j.Done(item.seq, j._post(item))))
        records.extend((self.intents[9], j.Done(10, j.NoIdentity(), 'uncertain')))
        keys = ('quiesce:retry', 'undo:8', 'undo:7', 'undo:6', 'undo:5', 'undo:4', 'undo:3')
        for seq, (key, action) in enumerate(zip(keys, self.expected(9)[:-1]), 11):
            item = self.intent(seq, action, 'inverse', key)
            if type(action) in (a.Replace, a.Install):
                preimages[action.pre.preimage] = action.pre.sha256
            records.extend((item, j.Done(seq, j._post(item))))
        if compared:
            compare = self.intent(18, j.BackupCompare((self.pair,)), 'inverse', 'compare:10')
            records.extend((compare, j.Done(18, j.NoIdentity())))
        resync = self.intent(19, j.ResyncP((self.pair,)), 'inverse', 'resync:10')
        records.append(resync)
        observation = j.NoIdentity()
        if completed:
            records.append(j.Done(19, j.NoIdentity(), 'uncertain'))
            retry = self.intent(20, resync.action, 'inverse', resync.key)
            records.extend((retry, j.Done(20, j.NoIdentity())))
            observation = None
        state = j.recover(j.parse(''.join(j.encode(r) for r in records)), observation, preimages)
        self.assertEqual(state.status, 0)
        self.assertNotIn(self.intents[9], state.done)
        self.assertEqual(state.pending, None if completed else resync)
        return state

    def test_superseded_backup_pending_resync(self):
        self.assertEqual(core.plan(self.recovery_retry(False), self.run),
                         (a.Quiesce(), j.ResyncP((self.pair,)),
                          j.BackupCompare((self.pair,)), a.Launchd('unloaded', 'loaded')))

    def test_superseded_backup_completed_resync(self):
        self.assertEqual(core.plan(self.recovery_retry(True), self.run),
                         (a.Quiesce(), j.BackupCompare((self.pair,)),
                          a.Launchd('unloaded', 'loaded')))

    def test_superseded_backup_pending_resync_compared(self):
        self.assertEqual(core.plan(self.recovery_retry(False, True), self.run),
                         (a.Quiesce(), j.ResyncP((self.pair,)), a.Launchd('unloaded', 'loaded')))

    def test_superseded_backup_completed_resync_compared(self):
        self.assertEqual(core.plan(self.recovery_retry(True, True), self.run),
                         (a.Quiesce(), a.Launchd('unloaded', 'loaded')))

    def test_bad_resync_key_refuses(self):
        for key in ('wrong::10', 'resync:', 'resync:0', 'resync:-1', 'resync:1x', 'resync:01'):
            for completed in (False, True):
                item = self.intent(20, j.ResyncP((self.pair,)), 'inverse', key)
                state = (self.state(0, inverses=(item,)) if completed
                         else self.state(0, item, j.NoIdentity()))
                with self.subTest(key=key, completed=completed), self.assertRaises(Refusal) as caught:
                    core.plan(state, self.run)
                self.assertIn(repr(key), str(caught.exception))

    def test_completed_resync_must_match_backup(self):
        item = self.intent(20, j.ResyncP((self.rpair,)), 'inverse', 'resync:10')
        with self.assertRaisesRegex(Refusal, 'resync:10.*pending RESYNC_P differs from backup'):
            core.plan(self.state(10, inverses=(item,)), self.run)

    def test_backup_obligations_reverse_order(self):
        other = replace(self.pair, dst='/other-backup')
        records = []
        for seq, pair in ((1, self.pair), (2, other)):
            item = self.intent(seq, a.BackupRun((pair,)))
            records.extend((item, j.Done(seq, j.NoIdentity())))
        state = j.recover(j.parse(''.join(j.encode(r) for r in records)), None, {})
        self.assertEqual(core.plan(state, self.run),
                         (a.Quiesce(), j.ResyncP((other,)), j.BackupCompare((other,)),
                          j.ResyncP((self.pair,)), j.BackupCompare((self.pair,))))

    def test_stopped_boundary_values_refuse(self):
        state = self.state(0)
        for bad in (replace(state, stopped=[]), replace(state, status=False),
                    replace(state, status=3), replace(state, stopped=('stopped item',))):
            with self.subTest(state=bad), self.assertRaises(Refusal):
                core.plan(bad, self.run)

    def test_completed_compare_is_not_repeated(self):
        resync = self.intent(20, j.ResyncP((self.pair,)), 'inverse', 'resync:10')
        compare = self.intent(21, j.BackupCompare((self.pair,)), 'inverse', 'compare:10')
        self.assertEqual(core.plan(self.state(10, inverses=(resync, compare)), self.run),
                         self.expected(9))

    def backup_state(self, pairs):
        records = []
        for item in self.intents[:10]:
            if type(item.action) is a.BackupRun:
                item = replace(item, action=a.BackupRun(pairs))
            records.extend((item, j.Done(item.seq, j._post(item))))
        return j.recover(j.parse(''.join(j.encode(r) for r in records)), None,
                         {self.pre.preimage: self.pre.sha256})

    def test_restored_excludes_and_prefix_boundary(self):
        for before, after in (('/root/excludes', '/parent/repo/excludes'),
                              ('/root-other/excludes', '/root-other/excludes')):
            pair = replace(self.pair, excludes=before)
            restored = replace(pair, excludes=after)
            state = self.backup_state((pair, self.rpair))
            with self.subTest(excludes=before):
                self.assertEqual(core.plan(state, self.run), self.expected(9)[:-1] +
                                 (j.ResyncP((restored,)), j.BackupCompare((restored,)),
                                  a.Launchd('unloaded', 'loaded')))

    def test_covering_pair_destination_and_boundary(self):
        for pairs in ((self.pair, replace(self.pair, dst='/wrong'), self.rpair),
                      (self.pair, replace(self.rpair, dst='/wrong/root')),
                      (self.pair, a.BackupPair('ssd', '/parent-other', '/backup/parent-other',
                                              '/outside/excludes'))):
            with self.subTest(pairs=pairs), self.assertRaisesRegex(
                    Refusal, 'BACKUP_RUN.*no unique covering P pair'):
                core.plan(self.backup_state(pairs), self.run)


    # [LAW:behavior-not-structure] Parsed witnesses pin public refusal and rollback behavior.
    def parsed_completed_state(self, items):
        records = tuple(record for item in items
                        for record in (item, j.Done(item.seq, j._post(item))))
        state = j.recover(j.parse(''.join(j.encode(record) for record in records)), None,
                          {self.pre.preimage: self.pre.sha256})
        self.assertEqual(state.status, 0)
        return state

    def test_nonfirst_loaded_to_loaded_refuses(self):
        items = self.intents[:10] + (self.intent(11, a.Launchd('loaded', 'loaded')),)
        state = self.parsed_completed_state(items)
        with self.assertRaisesRegex(Refusal, 'op-11.*expected RESUME'):
            core.plan(state, self.run)

    def test_nonfirst_unloaded_to_unloaded_refuses(self):
        items = self.intents[:10] + (self.intent(11, a.Launchd('unloaded', 'unloaded')),)
        state = self.parsed_completed_state(items)
        with self.assertRaisesRegex(Refusal, 'op-11.*expected RESUME'):
            core.plan(state, self.run)

    def test_alien_source_sharing_parent_destination_refuses(self):
        child = replace(self.pair, src='/parent/repo', dst='/backup/parent/repo')
        alien = replace(self.pair, src='/alien')
        state = self.parsed_completed_state((
            self.intent(1, a.BackupRun((self.pair, child, alien))),))
        with self.assertRaisesRegex(Refusal, 'BACKUP_RUN.*no unique covering P pair'):
            core.plan(state, self.run)

    def test_composed_renames_restore_backup_source_and_excludes(self):
        state = self.parsed_completed_state((
            self.intent(1, a.Launchd('loaded', 'unloaded')),
            self.intent(2, a.Rename('/a', '/b')),
            self.intent(3, a.Rename('/b', '/c')),
            self.intent(4, a.BackupRun((
                a.BackupPair('ssd', '/c', '/backup', '/c/excludes'),)))))
        restored = a.BackupPair('ssd', '/a', '/backup', '/a/excludes')
        self.assertEqual(core.plan(state, self.run),
                         (a.Quiesce(), a.Rename('/c', '/b'), a.Rename('/b', '/a'),
                          j.ResyncP((restored,)), j.BackupCompare((restored,)),
                          a.Launchd('unloaded', 'loaded')))


    def test_inverse_done_tuple_subclass_refuses(self):
        class CompletedKeys(tuple):
            pass
        state = replace(self.state(0), inverse_done=CompletedKeys())
        with self.assertRaisesRegex(Refusal, 'state.*expected frozen sequences'):
            core.plan(state, self.run)


def effects():
    names = {'open', 'fdopen', 'stat', 'lstat', 'fstat', 'scandir', 'listdir', 'walk',
             'readlink', 'statvfs', 'getcwd', 'getenv', 'access', 'system', 'popen'}
    names.update(n for n in dir(os) if n.startswith(('exec', 'spawn', 'posix_spawn', 'open')))
    return ([(os, n) for n in sorted(names)] + [(builtins, 'open'), (Path, 'open')]
            + [(m, n) for m in (io, _io) for n in ('open', 'open_code', 'FileIO')]
            + [(subprocess, n) for n in ('Popen', 'run', 'call', 'check_call', 'check_output',
                                        'getoutput', 'getstatusoutput')]
            + [(time, 'time'), (time, 'monotonic')])


class Purity(unittest.TestCase):
    def test_ast_allowlist(self):
        tree = ast.parse(Path(core.__file__).read_text())
        imports = {'__future__': {'annotations'}, 'hashlib': {'sha256'},
                   'ops.migrate.fdsafe': {'Refusal'},
                   'ops.migrate.root_switch_core': {'Absent', 'BackupPair', 'BackupRun', 'Check',
                       'FileState', 'Install', 'Launchd', 'Quiesce', 'Rename', 'Replace'},
                   'ops.migrate.switch_journal_core': {'Action', 'RecoveryState', 'Intent',
                       'ResyncP', 'BackupCompare', '_path', 'encode', 'parse'}}
        calls = {'type', 'tuple', 'len', 'all', 'any', 'repr', 'reversed', 'enumerate',
                 'set', 'sha256', 'Refusal', '_require', '_validate', '_inverse', '_restore',
                 '_pairs', 'plan'} | set().union(*imports.values())
        methods = {'append', 'extend', 'startswith', 'hexdigest', 'add'}
        imported = set().union(*imports.values())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.fail(ast.unparse(node))
            if isinstance(node, ast.ImportFrom):
                self.assertEqual(node.level, 0)
                self.assertIn(node.module, imports)
                for name in node.names:
                    self.assertIn(name.name, imports[node.module])
                    self.assertIsNone(name.asname)
            if isinstance(node, ast.Name):
                self.assertNotIn(node.id, ('getattr', '__dict__', 'importlib', 'sys', 'globals', 'locals'))
            if isinstance(node, ast.Attribute):
                self.assertFalse(node.attr.startswith('__'))
                if isinstance(node.value, ast.Name):
                    self.assertNotIn(node.value.id, imported)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertIn(node.func.id, calls)
                else:
                    self.assertIsInstance(node.func, ast.Attribute)
                    self.assertIn(node.func.attr, methods)

    def test_effect_interceptions_and_each_mutant(self):
        state = j.RecoveryState((), (), None, (), 0)
        def forbidden(*args, **kwargs):
            raise AssertionError('inverse performed an effect')
        for owner, name in effects():
            with self.subTest(effect=f'{owner.__name__}.{name}'):
                with mock.patch.object(owner, name, forbidden):
                    with self.assertRaisesRegex(AssertionError, 'inverse performed an effect'):
                        getattr(owner, name)()
        with ExitStack() as stack:
            for owner, name in effects():
                stack.enter_context(mock.patch.object(owner, name, forbidden))
            self.assertEqual(core.plan(state, '/run/fixture'), (a.Quiesce(),))
