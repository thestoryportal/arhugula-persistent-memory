"""Local fixtures only; acceptance uses the unchanged R1L collector harness."""
import copy
import base64
import contextlib
import io
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(root):
    result = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        for name in ['.'] + dirs + files:
            path = Path(parent) if name == '.' else Path(parent) / name
            s = path.lstat()
            result[str(path)] = (s.st_size, s.st_mtime_ns, s.st_mode)
    return result


class SizingTests(unittest.TestCase):
    def setUp(self):
        self.probe = load('r1m_size_probe')
        self.evaluate = load('r1m_evaluate')
        self.harness = load('test_r1l_collector').R1DCriteria('test_04_scoped_streaming_inventory_separates_baseline')
        with mock.patch.object(tempfile, 'tempdir', '/private/tmp'):
            self.harness.setUp()
        self.addCleanup(self.harness.doCleanups)
        self.manifest = json.loads((HERE / 'intel_provisioning_manifest_v10.json').read_bytes())

    def measured(self):
        h = self.harness
        return self.probe.measure(h.m, h.api, old_roots=[str(h.base / 'old'), str(h.base / 'old-registration')])

    def test_01_every_type_sound_bound_and_no_writes(self):
        h = self.harness
        c = h.collector()
        (h.install / 'unicode-é-"').write_bytes(b'x' * 257)
        (h.install / 'dir').mkdir()
        (h.install / 'link').symlink_to('/outside-must-not-be-read')
        os.mkfifo(h.install / 'fifo')
        socket_path = h.install / 'socket'
        socket_path.touch()
        (h.install / 'denied').mkdir()
        special = h.install / 'special'
        special.touch()
        refused = h.base / 'refused-root'
        refused.symlink_to(h.install, target_is_directory=True)
        h.m['collector']['admitted_write_roots'].append(str(refused))
        real_scandir, real_stat, real_lstat = os.scandir, os.stat, Path.lstat
        def denied(path):
            if isinstance(path, int):
                s = os.fstat(path)
                if s.st_ino == (h.install / 'denied').lstat().st_ino:
                    raise PermissionError('fixture unreadable directory')
            elif str(path) == str(h.install / 'denied'):
                raise PermissionError('fixture unreadable directory')
            return real_scandir(path)
        # Synthetic device metadata, matching the predecessor's socket-stat fixture.
        special_identity = special.lstat()
        socket_identity = socket_path.lstat()
        def typed_stat(path, *args, **kwargs):
            value = real_stat(path, *args, **kwargs)
            if value.st_ino in [special_identity.st_ino, socket_identity.st_ino]:
                proxy = mock.Mock(wraps=value)
                for attr in ['st_uid', 'st_gid', 'st_size', 'st_blocks', 'st_dev', 'st_ino', 'st_mtime_ns', 'st_ctime_ns']:
                    setattr(proxy, attr, getattr(value, attr))
                proxy.st_mode = 0o020600 if value.st_ino == special_identity.st_ino else 0o140600
                return proxy
            return value
        def typed_lstat(path):
            return typed_stat(path, follow_symlinks=False)
        before = snapshot(h.base)
        with mock.patch.object(os, 'scandir', side_effect=denied), mock.patch.object(os, 'stat', side_effect=typed_stat), mock.patch.object(Path, 'lstat', typed_lstat):
            before = snapshot(h.base)
            summary = self.measured()
            self.assertEqual(before, snapshot(h.base))
            result = c.inventory()
        kinds = summary['by_kind']
        self.assertTrue({'file', 'directory', 'symlink', 'symlink-root-refused', 'unreadable', 'fifo', 'socket', 'special'} <= set(kinds))
        self.assertGreater(kinds['symlink-root-refused']['encoded_target_bytes'], 0)
        actual = Path(result['receipt']).stat().st_size
        self.assertGreaterEqual(summary['inventory_row_bound_bytes'], actual)
        actual_rows = [json.loads(x) for x in Path(result['receipt']).read_text().splitlines()]
        baseline_bytes = sum(len(h.api.encoded(x)) for x in actual_rows if x['origin'] == 'baseline')
        observed_baseline = sum(x['row_bytes'] for x in summary['roots'] if x['root'] in [str(h.install), str(refused)])
        self.assertGreaterEqual(observed_baseline, baseline_bytes)
        self.assertEqual(summary['hash_chunks'], 3)
        print('R1M-ROWS ' + json.dumps({'bound': summary['inventory_row_bound_bytes'], 'actual': actual, 'kinds': sorted(kinds)}))
        # A separate probe observes the post-collector tree without changing it.
        before = snapshot(h.base)
        self.measured()
        self.assertEqual(before, snapshot(h.base))

    def test_02_old_state_measured_without_mutation(self):
        h = self.harness
        old = h.base / 'old'
        old.mkdir()
        (old / 'partial.jsonl').write_bytes(b'x' * 12345)
        reg = h.base / 'old-registration'
        reg.mkdir()
        (reg / 'window.jsonl').write_bytes(b'y' * 234)
        before = snapshot(h.base)
        summary = self.measured()
        self.assertEqual(summary['old_state']['total_bytes'], 12579)
        self.assertEqual(len(summary['old_state']['files']), 2)
        self.assertEqual(before, snapshot(h.base))
        terms = self.evaluate.evaluate(summary, h.m, measured_m3_bytes=0, fixture=True)
        self.assertEqual(terms['terms']['old_intel_state_bytes'], 12579)
        self.assertEqual(terms['required_setup_bytes'], terms['nonreceipt_setup_bytes']+terms['required_receipt_bytes'])

    def test_03_evaluator_small_pass_and_large_fixture_fail(self):
        # The evaluator consumes exact manifest bytes matching the probe.
        manifest = copy.deepcopy(self.harness.m)
        manifest['budget'] = copy.deepcopy(self.manifest['budget'])
        manifest['collector']['receipt_limit_bytes'] = 18000000
        manifest['collector']['failure_reserve_bytes'] = 16384
        summary = self.probe.measure(manifest, self.harness.api, old_roots=[str(self.harness.base/'old'), str(self.harness.base/'old-registration')])
        out = self.evaluate.evaluate(summary, manifest, measured_m3_bytes=0, fixture=True)
        self.assertEqual(out['verdict'], 'PASS')
        def cli(sizing):
            capture = self.harness.base / 'sizing.json'
            policy = self.harness.base / 'manifest.json'
            capture.write_bytes(self.probe.output_bytes(sizing))
            policy.write_bytes(self.harness.api.encoded(manifest))
            output = io.StringIO()
            with mock.patch.object(sys, 'argv', ['r1m_evaluate.py', str(capture), str(policy)]), \
                    mock.patch.object(self.evaluate, 'MANIFEST_SHA256', sizing['manifest_sha256']), \
                    mock.patch.object(self.evaluate, 'OLD_ROOTS', sizing['old_state']['roots']), \
                    contextlib.redirect_stdout(output):
                rc = self.evaluate.main()
            value = json.loads(output.getvalue())
            print('R1M-CLI ' + output.getvalue().strip())
            return rc, value
        rc, output = cli(summary)
        self.assertEqual((rc, output['verdict']), (0, 'PASS'))
        # Long, escaped local paths make exact serialized rows exceed 18 MB.
        directory = self.harness.install
        for i in range(4):
            directory = directory / ('"' * 160 + str(i))
            directory.mkdir()
        for i in range(13000):
            (directory / ('f%05d-' % i + 'z' * 100)).touch()
        big = self.probe.measure(manifest, self.harness.api, old_roots=[str(self.harness.base/'old'), str(self.harness.base/'old-registration')])
        self.assertGreater(big['inventory_row_bound_bytes'], 18000000)
        out = self.evaluate.evaluate(big, manifest, measured_m3_bytes=0, fixture=True)
        self.assertEqual(out['verdict'], 'FAIL')
        rc, output = cli(big)
        self.assertEqual((rc, output['verdict']), (1, 'FAIL'))
        print('R1M-EVALUATOR ' + json.dumps(out, sort_keys=True))

    def test_04_live_output_fails_independently(self):
        summary = self.measured()
        summary['hash_chunks'] = 300000
        summary['roots'][0]['hash_chunks'] = 300000
        out = self.evaluate.evaluate(summary, self.harness.m, measured_m3_bytes=0, fixture=True)
        self.assertFalse(out['live_pass'])

    def test_05_bounded_output_and_incomplete_old_list_refuse(self):
        h = self.harness
        old = h.base / 'old'
        old.mkdir()
        for i in range(self.probe.MAX_OLD_FILES + 1):
            (old / str(i)).touch()
        with self.assertRaisesRegex(ValueError, 'old-state file list'):
            self.measured()
        with self.assertRaisesRegex(ValueError, 'summary bound'):
            self.probe.output_bytes({'too_big': 'x' * self.probe.MAX_SUMMARY_BYTES})

    def test_06_ancestor_symlink_and_old_symlink_refuse(self):
        h = self.harness
        alias = h.base / 'alias'
        alias.symlink_to(h.install, target_is_directory=True)
        h.m['collector']['admitted_write_roots'] = [str(alias / 'nested')]
        with self.assertRaises(OSError):
            self.measured()
        h.m['collector']['admitted_write_roots'] = [str(h.install)]
        (h.base / 'old').symlink_to(h.install, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'old-state'):
            self.measured()

    def test_07_production_pins_and_cli_fail_closed(self):
        api = self.probe.load_collector((HERE/'r1j_collector.py').read_bytes())
        self.assertEqual(api.encoded({'é': 'x'}), self.harness.api.encoded({'é': 'x'}))
        with self.assertRaisesRegex(ValueError, 'collector pin'):
            self.probe.load_collector(b'print("bad")')
        summary = self.measured()
        summary['sizing_probe_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'sizing probe pin'):
            self.evaluate.evaluate(summary, self.harness.m, measured_m3_bytes=0, fixture=True)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'probe.json'
            path.write_text('{}')
            process = subprocess.run(['/usr/bin/python3', '-B', str(HERE/'r1m_evaluate.py'), str(path), str(HERE/'intel_provisioning_manifest_v10.json')], capture_output=True)
        self.assertEqual(process.returncode, 1)
        self.assertIn(b'FAIL', process.stdout)

    def test_08_stability_witness_detects_change(self):
        h = self.harness
        real = self.probe.scan_inventory
        calls = [0]
        def changed(*args, **kwargs):
            result = real(*args, **kwargs)
            calls[0] += 1
            if calls[0] == 1:
                (h.install / 'new-entry').touch()
            return result
        with mock.patch.object(self.probe, 'scan_inventory', side_effect=changed):
            with self.assertRaisesRegex(ValueError, 'tree changed'):
                self.measured()

    def test_09_pinned_stub_sizing_is_read_only_and_framing_evaluates(self):
        h = self.harness
        members, hashes = h.bundle('probe')
        raw = (HERE/'r1m_size_probe.py').read_bytes()
        # Only disposable fixture roots/policy pin differ; traversal/encoding unchanged.
        old = [str(h.base/'old'), str(h.base/'old-registration')]
        raw += ('\nMANIFEST_SHA256 = ' + repr(hashlib.sha256(members['manifest']).hexdigest()) +
                '\nOLD_ROOTS = ' + repr(old) + '\n').encode()
        members['identity'] = raw
        hashes = {k: hashlib.sha256(v).hexdigest() for k, v in members.items()}
        bundle = json.dumps({k: base64.b64encode(v).decode() for k, v in members.items()}).encode()
        before = snapshot(h.base)
        process = subprocess.run(['/usr/bin/python3', '-I', '-B', '-c', (HERE/'r1j_stub.py').read_text(), 'probe', json.dumps(hashes)],
            input=bundle+b'\nR1I-GO 30\n', capture_output=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, b'')
        self.assertEqual(before, snapshot(h.base))
        self.assertLessEqual(len(process.stdout), self.probe.MAX_SUMMARY_BYTES+75)
        summary = self.evaluate.parse_capture(process.stdout)
        self.assertEqual(summary['dispatch_request_sha256'], hashes['request'])
        print('R1M-STUB ' + json.dumps({'exit': process.returncode, 'stdout_bytes': len(process.stdout)}))

    def test_10_live_and_overhead_bound_with_extra_traversal_row(self):
        h = self.harness
        c = h.collector()
        directory = h.install / 'late-denied'
        directory.mkdir()
        (h.install / 'file').write_bytes(b'z' * 20000)
        real_scandir = os.scandir
        counters = {}
        def denied(path):
            identity = os.fstat(path).st_ino if isinstance(path, int) else Path(path).lstat().st_ino
            if identity == directory.lstat().st_ino:
                counters[identity] = counters.get(identity, 0) + 1
                if counters[identity] % 2 == 0:
                    raise PermissionError('fixture traversal error')
            return real_scandir(path)
        calls = [0]
        def live():
            calls[0] += 1
        with mock.patch.object(os, 'scandir', side_effect=denied):
            sizing = self.measured()
            h.api.TRANSPORT_CHECK = live
            c.collect('inventory')
        observed_rows = [json.loads(x) for p in c.receipts.glob('inventory-*.jsonl')
                         if not p.name.startswith('inventory-accounting-') for x in p.read_text().splitlines()]
        self.assertEqual(sizing['rows']-sizing['walk_remaining_calls'], 1)
        bound = self.evaluate.evaluate(sizing, h.m, measured_m3_bytes=0, fixture=True)
        self.assertGreaterEqual(bound['live_calls_bound'], calls[0])
        self.assertGreaterEqual(sizing['inventory_row_bound_bytes'], sum(len(h.api.encoded(x)) for x in observed_rows))
        self.assertLessEqual(c.registration.stat().st_size, self.evaluate.OVERHEAD['registration_bytes'])
        self.assertLessEqual((c.root/'window.json').stat().st_size, self.evaluate.OVERHEAD['window_bytes'])
        self.assertLessEqual(sum(p.stat().st_size for p in c.receipts.glob('summary-*.jsonl')), self.evaluate.OVERHEAD['summary_bytes'])
        print('R1M-LIVE ' + json.dumps({'actual_calls': calls[0], 'bound_calls': bound['live_calls_bound']}))


if __name__ == '__main__':
    unittest.main()
