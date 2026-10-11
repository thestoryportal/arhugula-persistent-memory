"""R1N acceptance; local captures and disposable fixtures, never a host dispatch."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
CAP = HERE / 'r1j_probe_r1m_20261011T154940Z.json'


def load(name):
    return importlib.import_module(name)


class ReplanTests(unittest.TestCase):
    def test_01_generator_exact_diff_and_determinism(self):
        g = load('r1n_make_manifest_v11')
        old = json.loads((HERE / g.SOURCE).read_bytes())
        new = json.loads(g.generated_bytes())
        changes = g.changed_paths(old, new)
        expected = {
            '/budget/components/11/bytes', '/budget/components/11/basis',
            '/budget/components/11/evidence', '/budget/components/12/bytes',
            '/budget/planned_peak_bytes', '/budget/margin_bytes',
            '/collector/receipt_limit_bytes', '/paths/probe_tmp',
            '/collector/retained_dir', '/collector/admitted_write_roots/3',
            '/collector/admitted_write_roots/4',
            '/collector/child_contract/allowed_write_roots/0',
            '/collector/registration_path'}
        self.assertEqual(set(changes), expected)
        self.assertEqual(new['budget']['setup_cap_bytes'], 2_000_000_000)
        non = sum(x['bytes'] for x in new['budget']['components'] if x['id'] != 'receipts')
        self.assertEqual(new['budget']['planned_peak_bytes'], non + 38_000_000)
        self.assertLessEqual(new['budget']['planned_peak_bytes'], 2_000_000_000)
        with tempfile.TemporaryDirectory() as tmp:
            outputs = [Path(tmp) / n for n in ('one.json', 'two.json')]
            for output in outputs:
                p = subprocess.run(['/usr/bin/python3', '-B', str(HERE / 'r1n_make_manifest_v11.py'), str(output)], capture_output=True)
                self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            self.assertEqual(outputs[0].read_bytes(), (HERE / g.TARGET).read_bytes())

    def test_02_cap_replay_pass_prints_all_terms_old_still_fails(self):
        e = load('r1n_evaluate')
        p = subprocess.run(['/usr/bin/python3', '-B', str(HERE / 'r1n_evaluate.py'), str(CAP), str(HERE / 'intel_provisioning_manifest_v11.json'), '--replay-cap'], capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
        result = json.loads(p.stdout)
        self.assertEqual(result['verdict'], 'PASS')
        self.assertTrue(result['replay_only'])
        self.assertEqual(result['terms']['inventory_rows_bytes'], 20_114_046)
        self.assertEqual(result['terms']['old_intel_state_bytes'], 7_386_341)
        self.assertEqual(result['terms']['drift_receipt_bytes'], 4_009_702)
        self.assertGreater(result['terms']['omitted_m3_bytes'], 0)
        self.assertEqual(sum(result['terms'].values()), result['required_receipt_bytes'])
        self.assertEqual(result['required_setup_bytes'], result['nonreceipt_setup_bytes'] + result['required_receipt_bytes'])
        old = load('r1m_evaluate')
        probe = old.parse_capture(CAP.read_bytes())
        # Re-run unchanged E's CLI at CAP's measurement time, never change CAP.
        with mock.patch.object(sys, 'argv', ['r1m_evaluate.py', str(CAP), str(HERE / 'intel_provisioning_manifest_v10.json')]), mock.patch('time.time_ns', return_value=probe['measured_at_unix_ns']):
            self.assertEqual(old.main(), 1)

    def test_03_row_growth_over_reserve_fails(self):
        e = load('r1n_evaluate')
        g = load('r1n_make_manifest_v11')
        probe = load('r1m_evaluate').parse_capture(CAP.read_bytes())
        probe['manifest_sha256'] = e.MANIFEST_SHA256
        probe['sizing_probe_sha256'] = e.probe_pin()
        manifest = json.loads(g.generated_bytes())
        for root, name in zip(probe['roots'], manifest['collector']['admitted_write_roots']):
            root['root'] = name
        delta = e.drift_reserve(e.CAP_ROW_BYTES) + 1
        for key in ('observed_row_bytes', 'inventory_row_bound_bytes'):
            probe[key] += delta
        probe['roots'][0]['row_bytes'] += delta
        probe['rows'] += 12350
        probe['roots'][0]['rows'] += 12350
        result = e.evaluate(probe, manifest, 851702, 10000)
        print('R1N-GROWTH ' + json.dumps(result, sort_keys=True))
        self.assertEqual(result['verdict'], 'FAIL')
        self.assertFalse(result['receipt_pass'])

    def test_04_complete_evidence_union_and_sizing_envelope(self):
        e = load('r1n_evaluate')
        manifest = json.loads(load('r1n_make_manifest_v11').generated_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'r1j_bind_a.json').write_bytes(b'123')
            (root / 'r1m_evaluate_a.out').write_bytes(b'12345')
            prefix = root / 'r1j_probe_r1n_a'
            for suffix, data in [('.json', b'{}'), ('.stderr', b'warning'), ('.exit', b'0\n'), ('.final', b'{}'), ('.final.pending', b'{}')]:
                prefix.with_suffix(suffix).write_bytes(data)
            info = e.local_accounting(manifest, root)
            self.assertEqual(info['matched_bytes'], 3)
            self.assertEqual(info['omitted_bytes'], 20)
            current = e.local_accounting(manifest, root, sizing_prefix=prefix)
            self.assertEqual(current['omitted_bytes'], 5)
            self.assertEqual(current['sizing_set_bytes'], 15)
            prefix.with_suffix('.stderr').write_bytes(b'x' * e.SIZING_ENVELOPE)
            with self.assertRaisesRegex(ValueError, 'sizing.*envelope'):
                e.local_accounting(manifest, root, sizing_prefix=prefix)
            prefix.with_suffix('.stderr').unlink()
            (root / 'r1j_unknown.json').symlink_to(root / 'r1j_bind_a.json')
            with self.assertRaisesRegex(ValueError, 'receipt'):
                e.local_accounting(manifest, root)

    def test_05_freshness_pins_and_no_replay_authority(self):
        e = load('r1n_evaluate')
        old = load('r1m_evaluate').parse_capture(CAP.read_bytes())
        e.check_age(old, old['measured_at_unix_ns'] + 3600 * 10**9)
        for now in (old['measured_at_unix_ns'] - 1, old['measured_at_unix_ns'] + 3600 * 10**9 + 1):
            with self.assertRaisesRegex(ValueError, 'one hour|future'):
                e.check_age(old, now)
        manifest = json.loads(load('r1n_make_manifest_v11').generated_bytes())
        with self.assertRaisesRegex(ValueError, 'pins'):
            e.evaluate(old, manifest, 0, 0)
        p = subprocess.run(['/usr/bin/python3', '-B', str(HERE / 'r1n_evaluate.py'), str(CAP), str(HERE / 'intel_provisioning_manifest_v11.json')], capture_output=True)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stdout)['verdict'], 'FAIL')

    def test_06_adapter_builds_v11_and_probe_only(self):
        a = load('r1n_sizing_dispatch')
        a.verify_pins()
        maker = a.load_maker(sizing=True)
        args = type('Args', (), dict(mode='probe', probe=None, capture=None, bootstrap_start_utc=None, m3_receipt_bytes=0))()
        members = maker.build(args)
        self.assertEqual(hashlib.sha256(members['manifest']).hexdigest(), a.MANIFEST_SHA256)
        self.assertEqual(members['identity'], a.probe_member())
        args.mode = 'bind'
        with self.assertRaisesRegex(ValueError, 'probe-only'):
            maker.build(args)
        normal = a.load_maker(sizing=False)
        args.mode = 'probe'
        self.assertEqual(normal.build(args)['identity'], (HERE / 'r1j_identity_probe.py').read_bytes())
        self.assertEqual(normal.build(args)['manifest'], members['manifest'])
        # The original M3 dispatch also loads the v11 budget, without calling it.
        self.assertIn('intel_provisioning_manifest_v11.json', a.maker_source().decode())
        self.assertNotIn('intel_provisioning_manifest_v10.json', a.maker_source().decode())

    def test_07_budget_tamper_and_unknown_terms_fail_closed(self):
        e = load('r1n_evaluate')
        manifest = json.loads(load('r1n_make_manifest_v11').generated_bytes())
        probe = load('r1m_evaluate').parse_capture(CAP.read_bytes())
        for key in ('setup_cap_bytes', 'planned_peak_bytes'):
            bad = copy.deepcopy(manifest)
            bad['budget'][key] += 1
            with self.assertRaisesRegex(ValueError, 'manifest'):
                e.evaluate(probe, bad, 0, 0, replay=True)
        with self.assertRaisesRegex(ValueError, 'nonnegative'):
            e.evaluate(probe, manifest, 0, -1, replay=True)


if __name__ == '__main__':
    unittest.main()
