"""T273: the producer's approved moves cross the wire/reader seam unchanged."""
import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest

from ops.migrate import fdsafe, move_plan_core as core
from ops.migrate import test_move_plan_core as fx
from icm21_moves import validate_move, wire_record


class PlanMoves(unittest.TestCase):
    def setUp(self):
        self.units = [fx.unit('u2', 'MV-102', data=b'hello', git_roots=[
            {'path': '/p/u2/nested', 'head': None, 'branch': None, 'dirty': []}]),
            fx.unit(git_roots=[{'path': '/p/u1', 'head': 'abc', 'branch': 'main', 'dirty': []}])]
        self.rows = [fx.req_row('MV-101', '/p/u1', '/v/p/u1').split('\t'),
                     fx.req_row('MV-102', '/p/u2', '/v/p/u2', observed=8).split('\t')]
        self.rows[0][6:7] = ['lane-one']
        self.rows[0][9] = 'ICM-R4,ICM-R6'
        self.rows[1][6] = 'lane-two'

    def build(self):
        return fx.plan(self.units, tables=[fx.table(*('\t'.join(row) for row in self.rows))])

    def check(self, plan):
        return core.check_plans(root='/m', entries=[plan], occurrences=[fx.occ()], historical=fx.historical(),
            repairs=fx.repairs(('code/x.py', 3, '/p/u1/a.json',
                               '/m/experiments/c10r/runs/u1/a.json', 261)))

    def test_fields_and_full_validation(self):
        plan = self.build()
        expected = []
        for unit, row, kind in zip(reversed(self.units), self.rows, ['git-root', 'directory']):
            digest = hashlib.sha256(unit['manifest_bytes']).hexdigest()
            expected.append({'id': row[0], 'prd_ids': row[9].split(','), 'action': 'MOVE',
                'source': row[1], 'target': unit['candidate'], 'kind': kind,
                'bytes': sum(x['bytes'] for x in json.loads(unit['manifest_bytes'])['leaves']),
                'before_sha256': digest,
                'source_manifest': {'path': unit['manifest_path'], 'sha256': digest},
                'lane': row[6], 'reader_check_ids': []})
        self.assertEqual(plan['moves'], expected)
        for i, move in enumerate(plan['moves']):
            with self.subTest(move=move['id']):
                wire_record('Move', move)
                leaves = json.loads(self.units[1-i]['manifest_bytes'])['leaves']
                # [LAW:behavior-not-structure] Move bytes follow leaves despite annex drift.
                self.assertEqual(move['bytes'], sum(leaf['bytes'] for leaf in leaves))
                self.assertEqual(validate_move(move, ['/p', '/m', '/v'],
                    other_moves=plan['moves'][:i] + plan['moves'][i+1:],
                    existing_paths=[x['source'] for x in leaves],
                    run_units=['/p/u1', '/p/u2'], leaves=leaves), ())
        self.assertEqual(self.check(plan), ())
        self.assertEqual(plan['rollback'], [
            {'source': '/m/experiments/c10r/runs/u2', 'target': '/p/u2'},
            {'source': '/m/experiments/c10r/runs/u1', 'target': '/p/u1'}])
        body = {k: v for k, v in plan.items() if k not in ('digest', 'approval')}
        digest = hashlib.sha256(fx.canonical(body)).hexdigest()
        self.assertEqual(plan['digest'], digest)
        self.assertEqual(plan['approval'], 'G4 approve S220 sha256:' + digest)

    def test_annex_shape_refusals_name_row(self):
        for column, value in [(6, ''), (6, 'bad lane'), (6, '/lane'),
                              (9, ''), (9, ',ICM-R4'), (9, 'ICM-R4,'),
                              (9, 'ICM-R4,,ICM-R6'), (9, 'ICM-R4,ICM-R4')]:
            with self.subTest(column=column, value=value):
                old = self.rows[0][column]
                self.rows[0][column] = value
                try:
                    with self.assertRaises(fdsafe.Refusal) as caught:
                        self.build()
                    self.assertIn('MOVE-REQUIREMENTS.tsv:2', str(caught.exception))
                finally:
                    self.rows[0][column] = old

    def test_prd_values_are_enforced_by_wire_schema(self):
        for value in ['UNKNOWN', ' ICM-R4', 'ICM-R4 ']:
            with self.subTest(value=value):
                self.rows[0][9] = value
                move = self.build()['moves'][0]
                self.assertEqual(move['prd_ids'], [value])
                with self.assertRaises(ValueError):
                    wire_record('Move', move)

    def test_every_missing_key_and_extra_key_refused(self):
        plan = self.build()
        keys = ['id', 'prd_ids', 'action', 'source', 'target', 'kind', 'bytes',
                'before_sha256', 'source_manifest', 'lane', 'reader_check_ids']
        for key in keys + ['extra']:
            with self.subTest(key=key):
                bad = copy.deepcopy(plan)
                if key == 'extra':
                    bad['moves'][0][key] = None
                else:
                    bad['moves'][0].pop(key, None)
                with self.assertRaises(fdsafe.Refusal) as caught:
                    self.check(bad)
                self.assertIn(key, str(caught.exception))
        bad = copy.deepcopy(plan)
        bad['moves'][0] = {'source': '/p/u1', 'target': '/m/experiments/c10r/runs/u1'}
        with self.assertRaises(fdsafe.Refusal) as caught:
            self.check(bad)
        for key in set(keys) - {'source', 'target'}:
            self.assertIn(key, str(caught.exception))

    def test_malformed_wire_fields(self):
        plan = self.build()
        malformed = {'id': '', 'prd_ids': [], 'action': 'BOGUS', 'source': 'relative',
            'target': None, 'kind': 'unknown', 'bytes': -1, 'before_sha256': 'bad',
            'source_manifest': {}, 'lane': None, 'reader_check_ids': [None]}
        for key, value in malformed.items():
            with self.subTest(key=key):
                move = dict(plan['moves'][0], **{key: value})
                with self.assertRaises(ValueError):
                    wire_record('Move', move)
                self.assertTrue(validate_move(move, ['/p', '/m'], other_moves=[],
                    existing_paths=[], run_units=[], leaves=[]))

    def test_pure_with_live_audit_control(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        events, active = [], [False]
        def audit(event, args):
            if active[0] and (event == 'open' or event.startswith(('os.', 'subprocess.', 'shutil.'))):
                events.append(event)
        sys.addaudithook(audit)
        warm = self.build()
        self.check(warm)
        active[0] = True
        try:
            os.listdir(scratch.name)
            result = self.build()
            found = self.check(result)
        finally:
            active[0] = False
        self.assertEqual(events, ['os.listdir'])
        self.assertEqual(result, warm)
        self.assertEqual(found, ())


if __name__ == '__main__':
    unittest.main()
