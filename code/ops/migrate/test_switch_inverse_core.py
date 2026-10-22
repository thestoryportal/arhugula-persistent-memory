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
