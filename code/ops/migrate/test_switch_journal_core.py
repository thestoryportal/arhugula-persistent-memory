"""T412 journal recovery, using values only; no real roots or tools."""
import ast
import builtins
import copy
import _io
import io
import json
import os
import subprocess
import time
import unittest
from contextlib import ExitStack
from dataclasses import FrozenInstanceError, replace
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from ops.migrate import switch_journal_core as c
from ops.migrate import root_switch_core as a
from ops.migrate.fdsafe import Refusal


H = sha256(b'old').hexdigest()
J = sha256(b'new').hexdigest()


def cases():
    file = a.FileState(b'old', H, 0o755, '/run/pre/1')
    pair = a.BackupPair('ssd', '/m', '/backup', '/exclude')
    return (
        (a.Replace('/file', file, b'new', 0o755), c.FileIdentity(H, 0o755), c.FileIdentity(J, 0o755)),
        (a.Install('/file', a.Absent(), b'new', 0o755), a.Absent(), c.FileIdentity(J, 0o755)),
        (a.Rename('/src', '/dst'), c.RenameIdentity(c.Inode(7, 9), None), c.RenameIdentity(None, c.Inode(7, 9))),
        (a.Launchd('loaded', 'unloaded'), c.AgentIdentity('loaded'), c.AgentIdentity('unloaded')),
        (a.Check('readers'), c.NoIdentity(), c.NoIdentity()),
        (a.Quiesce(), c.NoIdentity(), c.NoIdentity()),
        (a.BackupRun((pair,)), c.NoIdentity(), c.NoIdentity()),
        (c.BackupCompare((pair,)), c.NoIdentity(), c.NoIdentity()),
        (c.ResyncP((pair,)), c.NoIdentity(), c.NoIdentity()),
    )


def intent(index=0, seq=1, direction='forward', key='item'):
    action, pre, _ = cases()[index]
    if index in (7, 8):
        direction = 'inverse'
    return c.Intent(seq, direction, key, action, pre)


def journal(*records):
    return ''.join(c.encode(record) for record in records)


def recover(text, observation=None, preimages=None):
    return c.recover(c.parse(text), observation,
                     {'/run/pre/1': H} if preimages is None else preimages)


class Recovery(unittest.TestCase):
    def test_classified_not_applied_intent_allows_rollback_and_retry(self):
        pause = intent(3, key='pause')
        move = intent(2, seq=2, key='move')
        inverse = replace(intent(2, seq=3, key='undo-move'), direction='inverse')
        records = (pause, c.Done(1, cases()[3][2]), move,
                   c.Done(2, cases()[2][1], 'not-applied'), inverse,
                   c.Done(3, cases()[2][1], 'not-applied'))
        retry = replace(inverse, seq=4)
        state = recover(journal(*records, retry), cases()[2][2])
        self.assertEqual(state.done, (pause, retry))
        self.assertEqual(state.inverse_done, ('undo-move',))
        self.assertIsNone(state.pending)

    def test_classified_backup_uncertainty_survives_interrupted_rollback(self):
        backup = intent(6, key='backup')
        drain = replace(intent(5, seq=2, key='drain'), direction='inverse')
        resync = intent(8, seq=3, key='resync')
        prefix = journal(backup, c.Done(1, c.NoIdentity(), 'uncertain'),
                         drain, c.Done(2, c.NoIdentity()))
        state = recover(prefix)
        self.assertEqual(state.pending, backup)
        state = recover(prefix + journal(resync), c.NoIdentity())
        self.assertEqual(state.pending, resync)
        state = recover(prefix + journal(resync, c.Done(3, c.NoIdentity(), 'uncertain')))
        self.assertEqual(state.pending, resync)
        retry = replace(resync, seq=4)
        state = recover(prefix + journal(resync, c.Done(3, c.NoIdentity(), 'uncertain'), retry),
                        c.NoIdentity())
        self.assertEqual(state.pending, retry)
        self.assertEqual(state.inverse_done, ('drain',))
        state = recover(prefix + journal(resync, c.Done(3, c.NoIdentity(), 'uncertain'),
                                          retry, c.Done(4, c.NoIdentity())))
        self.assertIsNone(state.pending)
        self.assertEqual(state.inverse_done, ('drain', 'resync'))
        state = recover(prefix + journal(resync, c.Done(3, c.NoIdentity())))
        self.assertEqual(state.pending, backup)
        self.assertEqual(state.inverse_done, ('drain', 'resync'))

    def test_classification_must_match_rule(self):
        for index, outcome, observed in ((2, 'not-applied', cases()[2][2]),
                                          (2, 'uncertain', cases()[2][1]),
                                          (6, 'not-applied', c.NoIdentity()),
                                          (2, 'unknown', cases()[2][2])):
            with self.assertRaises(Refusal):
                recover(journal(intent(index), c.Done(1, observed, outcome)))
        first = intent(6)
        second = intent(6, seq=2, key='other')
        with self.assertRaisesRegex(Refusal, 'multiple uncertain'):
            recover(journal(first, c.Done(1, c.NoIdentity(), 'uncertain'),
                            second, c.Done(2, c.NoIdentity(), 'uncertain')))
        with self.assertRaisesRegex(Refusal, 'multiple uncertain'):
            recover(journal(first, c.Done(1, c.NoIdentity(), 'uncertain'), second), c.NoIdentity())

    def test_uncertain_retry_binds_operands_and_backup_coverage(self):
        first = intent(8)
        other_pair = replace(first.action.pairs[0], dst='/unrelated')
        second = replace(first, seq=2, action=c.ResyncP((other_pair,)))
        with self.assertRaisesRegex(Refusal, 'operation operands changed'):
            recover(journal(first, c.Done(1, c.NoIdentity(), 'uncertain'),
                            second, c.Done(2, c.NoIdentity())))
        with self.assertRaisesRegex(Refusal, 'retry key changed'):
            recover(journal(first, c.Done(1, c.NoIdentity(), 'uncertain'),
                            replace(first, seq=2, key='new-key')), c.NoIdentity())
        first = intent(6)
        second = replace(second, key='resync')
        with self.assertRaisesRegex(Refusal, 'backup coverage'):
            recover(journal(first, c.Done(1, c.NoIdentity(), 'uncertain'), second), c.NoIdentity())

    def test_backup_coverage_maps_back_through_completed_renames(self):
        move = c.Intent(1, 'forward', 'move', a.Rename('/m', '/r'),
                        c.RenameIdentity(c.Inode(1, 2), None))
        pair = a.BackupPair('ssd', '/r', '/backup', '/r/excludes')
        backup = c.Intent(2, 'forward', 'backup', a.BackupRun((pair,)), c.NoIdentity())
        resync = c.Intent(3, 'inverse', 'resync', c.ResyncP((replace(pair, src='/m', excludes='/m/excludes'),)),
                          c.NoIdentity())
        prefix = journal(move, c.Done(1, c.RenameIdentity(None, c.Inode(1, 2))),
                         backup, c.Done(2, c.NoIdentity(), 'uncertain'))
        self.assertEqual(recover(prefix + journal(resync), c.NoIdentity()).pending, resync)
        wrong = replace(resync, action=c.ResyncP((replace(pair, src='/mish'),)))
        with self.assertRaisesRegex(Refusal, 'backup coverage'):
            recover(prefix + journal(wrong), c.NoIdentity())

    def test_single_parent_pair_covers_both_forward_pairs(self):
        pre = c.RenameIdentity(c.Inode(1, 2), None)
        post = c.RenameIdentity(None, c.Inode(1, 2))
        move = c.Intent(1, 'forward', 'move', a.Rename('/p/repo', '/r'), pre)
        backup_move = c.Intent(2, 'forward', 'backup-move', a.Rename('/b/p/repo', '/b/r'), pre)
        parent = a.BackupPair('ssd', '/p', '/b/p', '/eP')
        child = a.BackupPair('ssd', '/r', '/b/r', '/eR')
        backup = c.Intent(3, 'forward', 'backup', a.BackupRun((parent, child)), c.NoIdentity())
        resync = c.Intent(4, 'inverse', 'backup', c.ResyncP((parent,)), c.NoIdentity())
        prefix = journal(move, c.Done(1, post), backup_move, c.Done(2, post),
                         backup, c.Done(3, c.NoIdentity(), 'uncertain'))
        self.assertEqual(recover(prefix + journal(resync), c.NoIdentity()).pending, resync)
        self.assertEqual(recover(prefix + journal(resync, c.Done(4, c.NoIdentity()))).pending, backup)
        for pair in (replace(parent, dst='/unrelated'), replace(parent, excludes='/wrong'),
                     replace(parent, src='/pi')):
            with self.assertRaisesRegex(Refusal, 'backup coverage'):
                recover(prefix + journal(replace(resync, action=c.ResyncP((pair,)))), c.NoIdentity())
        mismatched = replace(backup, action=a.BackupRun((parent, replace(child, dst='/b/rish'))))
        bad_prefix = journal(move, c.Done(1, post), backup_move, c.Done(2, post),
                             mismatched, c.Done(3, c.NoIdentity(), 'uncertain'))
        with self.assertRaisesRegex(Refusal, 'backup coverage'):
            recover(bad_prefix + journal(resync), c.NoIdentity())

    def test_observation_fields_are_exact_types(self):
        item = replace(intent(2), pre=c.RenameIdentity(c.Inode(1, 1), None))
        for observed in (c.Inode(True, 1), c.Inode(1, True)):
            with self.assertRaisesRegex(Refusal, 'item'):
                recover(journal(item), c.RenameIdentity(None, observed))
        for index, observation in (
                (0, c.FileIdentity(J, True)), (0, c.FileIdentity(J, -1)),
                (0, c.FileIdentity('bad', 0o755)),
                (2, c.RenameIdentity(None, c.Inode(True, 9))),
                (2, c.RenameIdentity(None, c.Inode(7, True))),
                (2, c.RenameIdentity(3, None)), (2, c.RenameIdentity(None, 'inode')),
                (3, c.AgentIdentity('unknown'))):
            with self.subTest(index=index, observation=observation), self.assertRaisesRegex(Refusal, 'item'):
                recover(journal(intent(index)), observation)

    def test_invalid_public_inputs_and_named_observation_refusal(self):
        with self.assertRaisesRegex(Refusal, 'item.*unexpected observation'):
            recover(journal(intent()), object())
        for bad in (None, SimpleNamespace(records=())):
            with self.assertRaisesRegex(Refusal, 'expected parsed Journal'):
                c.recover(bad, None, {})
        with self.assertRaisesRegex(Refusal, 'expected observations'):
            c.recover(c.parse(''), None, [])
        with self.assertRaisesRegex(Refusal, 'neither pre nor post'):
            recover(journal(intent()), c.FileIdentity('f' * 64, 0o755))
        bad = replace(intent(4), action=SimpleNamespace(kind='UNKNOWN'))
        with self.assertRaisesRegex(Refusal, 'unknown action kind'):
            c.recover(c.Journal((bad,), ''), c.NoIdentity(), {})
        with self.assertRaisesRegex(Refusal, 'invalid sha256'):
            recover(journal(intent()), cases()[0][2], {'/run/pre/1': 'bad'})

    def test_sequence_checks_without_masking_by_observation(self):
        item = intent(4)
        second = intent(4, seq=2, key='second')
        for text, observation, message in (
                (journal(item, second), c.NoIdentity(), 'unclosed intent'),
                (journal(item, c.Done(1, c.NoIdentity()), replace(second, seq=1)),
                 c.NoIdentity(), 'sequence is not increasing'),
                (journal(item, c.Done(2, c.NoIdentity())), None, 'done sequence mismatch'),
                (journal(item, c.Done(1, c.FileIdentity(J, 0o755))), None, 'done post-identity mismatch')):
            with self.subTest(message=message), self.assertRaisesRegex(Refusal, message):
                recover(text, observation)

    def test_each_kind_pre_post_other(self):
        for index, (action, pre, post) in enumerate(cases()):
            item = intent(index)
            for observation, is_post in ((pre, False), (post, True)):
                with self.subTest(kind=action.kind, post=is_post):
                    state = recover(journal(item), observation)
                    if index in (6, 8):
                        self.assertEqual(state.pending, item)
                        self.assertEqual(state.done, ())
                    else:
                        expected = (item,) if is_post and index < 4 else ()
                        self.assertEqual(state.done, expected)
                        self.assertIsNone(state.pending)
                    self.assertEqual(state.status, 0)
            with self.subTest(kind=action.kind), self.assertRaisesRegex(Refusal, 'item'):
                recover(journal(item), c.FileIdentity('f' * 64, 0o600))

    def test_file_identity_requires_mode_and_hash(self):
        for index in (0, 1):
            for digest, mode in ((J, 0o600), (H, 0o600), ('f' * 64, 0o755)):
                with self.subTest(index=index, digest=digest, mode=mode), self.assertRaises(Refusal):
                    recover(journal(intent(index)), c.FileIdentity(digest, mode))

    def test_rename_identity_binds_device_inode_and_both_paths(self):
        for observation in (c.RenameIdentity(None, c.Inode(8, 9)),
                            c.RenameIdentity(None, c.Inode(7, 10)),
                            c.RenameIdentity(c.Inode(7, 9), c.Inode(7, 9)),
                            c.RenameIdentity(None, None)):
            with self.subTest(observation=observation), self.assertRaises(Refusal):
                recover(journal(intent(2)), observation)

    def test_done_records_and_interrupted_inverse(self):
        forward = intent(2)
        inverse = c.Intent(2, 'inverse', 'undo-item', a.Rename('/dst', '/src'),
                           c.RenameIdentity(c.Inode(7, 9), None))
        post = cases()[2][2]
        prefix = journal(forward, c.Done(1, post), inverse)
        state = recover(prefix, post)
        self.assertEqual(state.done, (forward, inverse))
        self.assertEqual(state.inverse_done, ('undo-item',))
        self.assertIsNone(state.pending)
        state2 = recover(prefix + c.encode(c.Done(2, post)))
        self.assertEqual(state, state2)
        retry = replace(inverse, seq=3)
        with self.assertRaisesRegex(Refusal, 'undo-item'):
            recover(prefix + c.encode(c.Done(2, post)) + c.encode(retry), post)

    def test_partial_inverse_backup_runs_again(self):
        first = intent(7, 1, key='compare')
        second = intent(8, 2, key='resync')
        state = recover(journal(first, c.Done(1, c.NoIdentity()), second), c.NoIdentity())
        self.assertEqual(state.inverse_done, ('compare',))
        self.assertEqual(state.pending, second)

    def test_preimage_missing_and_changed_stop_with_three(self):
        item = intent()
        for value in (None, 'e' * 64):
            for text, obs in ((journal(item), cases()[0][2]),
                              (journal(item, c.Done(1, cases()[0][2])), None)):
                state = recover(text, obs, {'/run/pre/1': value})
                self.assertEqual(state.status, 3)
                self.assertEqual(len(state.stopped), 1)
                self.assertIn('item', state.stopped[0])
                self.assertIn('/run/pre/1', state.stopped[0])
        with self.assertRaisesRegex(Refusal, 'preimage observation'):
            recover(journal(item), cases()[0][2], {})

    def test_existing_install_preimage_and_noop_post(self):
        original = intent()
        item = replace(original, action=a.Install('/file', original.action.pre, b'new', 0o755))
        self.assertEqual(recover(journal(item), cases()[0][2]).done, (item,))
        no_op = c.Intent(1, 'forward', 'pause', a.Launchd('unloaded', 'unloaded'),
                         c.AgentIdentity('unloaded'))
        self.assertEqual(recover(journal(no_op), c.AgentIdentity('unloaded')).done, (no_op,))

    def test_empty_and_unexpected_observation(self):
        self.assertEqual(recover('').done, ())
        with self.assertRaises(Refusal):
            recover('', c.NoIdentity())
        with self.assertRaises(Refusal):
            recover(journal(intent(4)))


class Parsing(unittest.TestCase):
    def test_narrow_json_exception_and_encoder_refusals(self):
        with self.assertRaisesRegex(Refusal, 'line 1'):
            c.parse('[' * 2000 + ']' * 2000)
        for record in (object(), SimpleNamespace(seq=1, post=c.NoIdentity())):
            with self.assertRaisesRegex(Refusal, 'unknown record type'):
                c.encode(record)
        with self.assertRaisesRegex(Refusal, 'unknown identity type'):
            c.encode(c.Done(1, object()))
        with self.assertRaisesRegex(Refusal, 'unknown action type'):
            c.encode(replace(intent(4), action=SimpleNamespace(kind='UNKNOWN', pairs=())))

    def test_large_json_integer_does_not_escape_as_value_error(self):
        parsed = c.parse('["done",' + '9' * 5000 + ',["none"]]\n')
        self.assertEqual(parsed.records[0].seq, 10 ** 5000 - 1)

    def test_independent_schema_guards(self):
        variants = []
        raw = json.loads(c.encode(intent(4)))
        changed = copy.deepcopy(raw)
        changed[0] = 'unknown'
        variants.append(changed)
        changed = copy.deepcopy(raw)
        changed[4] = ['UNKNOWN']
        variants.append(changed)
        changed = copy.deepcopy(raw)
        changed[5] = ['unknown']
        variants.append(changed)
        raw = json.loads(c.encode(intent()))
        changed = copy.deepcopy(raw)
        changed[4][2][0] = 'unknown'
        variants.append(changed)
        changed = copy.deepcopy(raw)
        changed[4][2] = ['absent']
        changed[5] = ['absent']
        variants.append(changed)
        raw = json.loads(c.encode(intent(2)))
        raw[5][1].append(10)
        variants.append(raw)
        variants.append(['done', 1, ['none'], 'extra'])
        variants.append(['done', 1, ['none'], 'uncertain', 'extra'])
        variants.append(['done', 1, ['file', 'g' * 64, 0]])
        for value in variants:
            with self.subTest(value=value), self.assertRaisesRegex(Refusal, 'line 1'):
                c.parse(json.dumps(value) + '\n')

    def test_action_and_identity_field_boundaries(self):
        raw = json.loads(c.encode(intent()))
        changes = {
            (4,): (None, [], ['UNKNOWN']),
            (4, 1): ('relative', '/', '/a/', '/a//b', '/a/./b', '/a/../b', '/a\x00b', 0),
            (4, 2): (None, [], ['absent'], ['unknown', '00', H, 493, '/pre']),
            (4, 2, 1): (None, '0', 'gg', ' 0', '00'),
            (4, 2, 2): (None, '', 'a' * 63, 'a' * 65, 'g' * 64, 'A' * 64, 'f' * 64),
            (4, 2, 3): (None, True, -1, 4096, '755'),
            (4, 2, 4): ('relative', '/', '/a/../b', None),
            (4, 3): (None, '0', 'gg'),
            (4, 4): (None, True, -1, 4096),
            (5,): (None, [], ['unknown'], ['none'], ['file', H]),
            (5, 1): (None, 'f' * 64),
            (5, 2): (None, True, -1, 4096, 0),
        }
        for path, values in changes.items():
            for value in values:
                changed = copy.deepcopy(raw)
                parent = changed
                for key in path[:-1]:
                    parent = parent[key]
                parent[path[-1]] = value
                with self.subTest(path=path, value=value), self.assertRaisesRegex(Refusal, 'line 1'):
                    c.parse(json.dumps(changed) + '\n')

    def test_other_action_fields_and_record_lengths(self):
        for index, (_, _, post) in enumerate(cases()):
            raw = json.loads(c.encode(intent(index)))
            for path in ((), (4,), (5,)):
                for extra in (False, True):
                    changed = copy.deepcopy(raw)
                    target = changed if not path else changed[path[0]]
                    if extra:
                        target.append('extra')
                    else:
                        target.pop()
                    with self.subTest(index=index, path=path, extra=extra), self.assertRaises(Refusal):
                        c.parse(json.dumps(changed) + '\n')
            done = json.loads(c.encode(c.Done(1, post)))
            for value in (0, -1, True, None):
                done[1] = value
                with self.assertRaises(Refusal):
                    c.parse(json.dumps(done) + '\n')
        for index, field, value in ((2, 1, '/dst'), (3, 1, 'unknown'),
                                    (3, 2, 'unknown'), (4, 1, ''),
                                    (6, 1, []), (6, 1, None),
                                    (6, 1, [['gdrive', '/m', '/b', '/e']]),
                                    (6, 1, [['ssd', '/m', '/b']])):
            raw = json.loads(c.encode(intent(index)))
            raw[4][field] = value
            with self.subTest(index=index, field=field), self.assertRaises(Refusal):
                c.parse(json.dumps(raw) + '\n')
        for index in (7, 8):
            raw = json.loads(c.encode(intent(index)))
            raw[2] = 'forward'
            with self.assertRaises(Refusal):
                c.parse(json.dumps(raw) + '\n')

    def test_rename_and_agent_pre_identity_must_bind_action(self):
        for pre in (c.NoIdentity(), c.RenameIdentity(None, None),
                    c.RenameIdentity(c.Inode(1, 2), c.Inode(1, 2)),
                    c.RenameIdentity(c.Inode(True, 2), None),
                    c.RenameIdentity(c.Inode(1, -1), None)):
            with self.assertRaises(Refusal):
                c.parse(journal(replace(intent(2), pre=pre)))
        with self.assertRaises(Refusal):
            c.parse(journal(replace(intent(3), pre=c.AgentIdentity('unloaded'))))
        with self.assertRaises(Refusal):
            c.parse(journal(replace(intent(4), pre=a.Absent())))

    def test_forward_after_inverse_and_independent_keys(self):
        first = replace(intent(4), direction='inverse')
        text = journal(first, c.Done(1, c.NoIdentity()), intent(4, seq=2, key='later'))
        with self.assertRaisesRegex(Refusal, 'forward after inverse'):
            recover(text, c.NoIdentity())
        first = intent(4)
        second = replace(first, seq=2, direction='inverse')
        state = recover(journal(first, c.Done(1, c.NoIdentity()), second), c.NoIdentity())
        self.assertEqual(state.done, (first,))
        self.assertEqual(state.inverse_done, ())

    def test_round_trip_and_frozen_records(self):
        for index, (_, _, post) in enumerate(cases()):
            item = intent(index)
            records = (item, c.Done(1, post))
            self.assertEqual(c.parse(journal(*records)).records, records)
            with self.assertRaises(FrozenInstanceError):
                item.seq = 4
        with self.assertRaises(FrozenInstanceError):
            recover('').status = 3

    def test_truncated_last_line_retained(self):
        prefix = journal(intent(2))
        parsed = c.parse(prefix + '["done",1,')
        self.assertEqual(parsed.truncated, '["done",1,')
        self.assertEqual(recover(prefix + '["done",1,', cases()[2][2]).done, (intent(2),))
        self.assertEqual(c.parse('["intent",').records, ())
        self.assertEqual(c.parse(journal(intent(4)).rstrip('\n')).records, (intent(4),))

    def test_malformed_lines_not_hidden(self):
        for text in ('bad\n', 'bad\n' + journal(intent(4)), '\n', '[]', '{}',
                     '["unknown"]', journal(intent(4)) + '[]\n'):
            with self.subTest(text=text), self.assertRaisesRegex(Refusal, 'line'):
                c.parse(text)

    def test_sequence_refusals(self):
        item = intent(4)
        for text in (journal(c.Done(1, c.NoIdentity())),
                     journal(item, item), journal(replace(item, seq=0)),
                     journal(item, c.Done(2, c.NoIdentity())),
                     journal(item, c.Done(1, c.FileIdentity(J, 0o755))),
                     journal(item, c.Done(1, c.NoIdentity()), replace(item, seq=1))):
            with self.subTest(text=text), self.assertRaises(Refusal):
                recover(text, c.NoIdentity())

    def test_malformed_fields(self):
        raw = json.loads(c.encode(intent()))
        for pos, values in ((1, (0, -1, True, '1', None)),
                            (2, ('wrong', None, 1)), (3, ('', None, 1))):
            for value in values:
                changed = list(raw)
                changed[pos] = value
                with self.subTest(pos=pos, value=value), self.assertRaises(Refusal):
                    c.parse(json.dumps(changed) + '\n')
        for text in (None, b'', 4):
            with self.assertRaises(Refusal):
                c.parse(text)


def effects():
    names = {'open', 'fdopen', 'stat', 'lstat', 'fstat', 'scandir', 'listdir', 'walk',
             'readlink', 'statvfs', 'getcwd', 'getenv', 'access', 'system', 'popen'}
    names.update(n for n in dir(os) if n.startswith(('exec', 'spawn', 'posix_spawn', 'open')))
    return ([(os, n) for n in sorted(names)] + [(builtins, 'open'), (Path, 'open')] +
            [(m, n) for m in (io, _io) for n in ('open', 'open_code', 'FileIO')] +
            [(subprocess, n) for n in ('Popen', 'run', 'call', 'check_call', 'check_output',
                                       'getoutput', 'getstatusoutput')] +
            [(time, 'time'), (time, 'monotonic')])


class Purity(unittest.TestCase):
    def test_import_and_call_allowlist(self):
        with open(c.__file__, encoding='utf-8') as stream:
            tree = ast.parse(stream.read())
        imports = {
            '__future__': {'annotations': 'annotations'},
            'dataclasses': {'dataclass': 'dataclass', 'field': 'field'},
            'hashlib': {'sha256': 'sha256'},
            'json': {'JSONDecodeError': 'JSONDecodeError', 'dumps': 'dumps', 'loads': 'loads'},
            'typing': {'Literal': 'Literal'},
            'ops.migrate.fdsafe': {'Refusal': 'Refusal'},
            'ops.migrate': {'root_switch_core': 'a'},
        }
        attributes = {name: set() for names in imports.values() for name in names.values()}
        attributes['a'] = {'Absent', 'Action', 'BackupPair', 'BackupRun', 'Check', 'FileState',
                           'Install', 'Launchd', 'Quiesce', 'Rename', 'Replace'}
        calls = {'AgentIdentity', 'BackupCompare', 'Done', 'FileIdentity', 'Inode', 'Intent',
                 'Journal', 'NoIdentity', 'RecoveryState', 'RenameIdentity', 'ResyncP', 'Refusal',
                 '_action', '_agent', '_array', '_decision', '_file_identity', '_hash', '_hex',
                 '_identity', '_inode', '_json_integer', '_mode', '_number', '_pairs', '_path', '_post', '_pre',
                 '_record', '_require', '_supersede', '_covers', '_restore_path', '_text', '_wire_action', '_wire_identity', '_wire_inode',
                 '_wire_pre', 'all', 'bool', 'dataclass', 'dumps', 'enumerate', 'field', 'len',
                 'loads', 'ord', 'set', 'sha256', 'tuple', 'type', 'reversed', 'any'}
        methods = {'fromhex', 'hexdigest', 'startswith', 'split', 'append', 'hex', 'add'}
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.fail(ast.unparse(node))
            elif isinstance(node, ast.ImportFrom):
                self.assertEqual(node.level, 0)
                self.assertIn(node.module, imports)
                for alias in node.names:
                    self.assertIn(alias.name, imports[node.module])
                    self.assertEqual(alias.asname or alias.name, imports[node.module][alias.name])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertIn(node.func.id, calls, ast.unparse(node))
                else:
                    self.assertIsInstance(node.func, ast.Attribute)
                    self.assertTrue(node.func.attr in methods or
                                    isinstance(node.func.value, ast.Name) and node.func.value.id == 'a',
                                    ast.unparse(node))
            elif isinstance(node, ast.ExceptHandler):
                self.assertIsInstance(node.type, ast.Name)
                self.assertIn(node.type.id, {'JSONDecodeError', 'RecursionError'})
            elif isinstance(node, ast.Name) and node.id == 'a':
                self.assertIsInstance(parents[node], ast.Attribute)
            elif isinstance(node, ast.Attribute):
                self.assertFalse(node.attr.startswith('__'), ast.unparse(node))
                root = node.value
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name) and root.id in attributes:
                    self.assertIsInstance(node.value, ast.Name)
                    self.assertIn(node.attr, attributes[root.id], ast.unparse(node))

    def test_no_effects_and_each_interceptor_kills_a_call_mutant(self):
        text = journal(intent(2))
        observation = cases()[2][2]
        def forbidden(*args, **kwargs):
            raise AssertionError('journal performed IO')
        with ExitStack() as stack:
            for owner, name in effects():
                stack.enter_context(mock.patch.object(owner, name, forbidden))
            self.assertEqual(recover(text, observation).done, (intent(2),))
            for owner, name in effects():
                with self.subTest(owner=owner, name=name), self.assertRaisesRegex(AssertionError, 'performed IO'):
                    # A mutant core calling this effect fails before it can touch the host.
                    getattr(owner, name)()


if __name__ == '__main__':
    unittest.main()
