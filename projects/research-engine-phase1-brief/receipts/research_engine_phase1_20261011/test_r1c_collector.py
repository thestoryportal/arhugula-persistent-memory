"""Nine preregistered R1C criteria; fake roots and command runner only."""
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'r1c_collector.py'


def load_collector():
    if not SOURCE.exists():
        return None
    spec = importlib.util.spec_from_file_location('r1c', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class R1CCriteria(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='r1c-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'retained'
        self.install = self.base / 'install'
        self.install.mkdir()
        self.clock = [1000.0]
        self.mono = [2000.0]
        self.api = load_collector()
        self.calls = []
        self.m = {
            'schema': 'R1C-v3', 'authorization': {
                'staging': True, 'building': True, 'installation': True},
            'host': {'arch': 'fake_arch', 'pool_map': {
                str(self.root): 'pool1', str(self.install): 'pool1'}},
            'tree': {'commit': 'test-pin'}, 'paths': {'root': str(self.install)},
            'selection': {'registered_names': []},
            'artifacts': [{'id': 'a', 'name': 'sample', 'version_revision': '9.7',
                'variants': [], 'source_url': 'https://example.invalid/a',
                'expected_sha256': hashlib.sha256(b'abc').hexdigest(),
                'size_bytes': 3, 'route': 'upstream tarball'}],
            'budget': {'clock_seconds': 37, 'setup_cap_bytes': 100000,
                'free_floor_bytes': 100, 'additional_headroom_bytes': 50,
                'components': [{'id': 'one', 'bytes': 20}, {'id': 'two', 'bytes': 10}],
                'planned_peak_bytes': 30},
            'collector': {'allowed_modes': ['inventory', 'tree', 'guard',
                'compare-installed', 'fetch', 'wheel', 'inspect', 'source-plan',
                'archive-index', 'r3'], 'retained_dir': str(self.root),
                'admitted_write_roots': [str(self.root), str(self.install)],
                'install_roots': [str(self.install)], 'receipt_limit_bytes': 40000,
                'failure_reserve_bytes': 2048, 'staging_bound_bytes': 70000,
                'per_download_bound_bytes': 5000, 'command_timeout_seconds': 11,
                'command_output_limit_bytes': 5000, 'io_chunk_bytes': 128,
                'child_contract': {'reviewed': True, 'executable': '/fake/curl',
                    'sha256': 'test-only', 'environment': {},
                    'allowed_write_roots': [str(self.root)]},
                'curl': {'argv_prefix': ['/fake/curl'], 'connect_timeout_seconds': 2,
                    'allowed_schemes': ['https'], 'success_http_codes': ['200']},
                'wheel': {'entry_id': 'a', 'lock_entry_id': 'lock',
                    'distribution': 'sample', 'python_tag': 'cp399', 'abi_tag': 'cp399',
                    'platform_arch': 'fakearch', 'max_platform': [27, 4],
                    'lock_hash_count': 1, 'compressed_allowance_bytes': 11,
                    'unpacked_allowance_bytes': 29, 'metadata_bound_bytes': 1000},
                'archive_index': {'url_template': 'https://example.invalid/{name}/',
                    'bound_bytes': 1000, 'platform_tag': 'darwin_99',
                    'architectures': ['fake_arch']},
                'identity_fields': ['source_url', 'size_bytes', 'sha256',
                    'signature_trust', 'recipe', 'build_closure', 'abi', 'linkage',
                    'installer_interface', 'compiler', 'sdk', 'tree_content',
                    'host', 'paths', 'budget', 'payloads', 'review_binding',
                    'archive_candidates', 'wheel_lock_membership']},
            'preinstall': {'required_fields': ['/tree/commit'], 'host_fields': ['arch', 'pool_map']},
            'postinstall': {'observed_active_ports': 'NEEDS-FETCH',
                'expected_payloads': {}, 'generated_file_allowlist': {}},
            'needs_fetch_commands': {'note': 'BLOCKED: future native work'}
        }

    def fake_run(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        if '--output' in argv:
            Path(argv[argv.index('--output') + 1]).write_bytes(b'abc')
        return subprocess.CompletedProcess(argv, 0, b'https://example.invalid/a\n200\n3\n', b'')

    def collector(self, mode='inventory', **kwargs):
        self.assertIsNotNone(self.api, 'R1C collector implementation is missing')
        c = self.api.Collector(self.m, mode, now=lambda: self.clock[0],
            monotonic=lambda: self.mono[0], runner=kwargs.pop('runner', self.fake_run), **kwargs)
        self.addCleanup(c.close)
        return c

    def observation(self):
        return {'host': copy.deepcopy(self.m['host']), 'tree': copy.deepcopy(self.m['tree']),
            'paths': copy.deepcopy(self.m['paths']), 'preinstalled_ports': [],
            'artifacts': {'a': dict(self.m['artifacts'][0], sha256=self.m['artifacts'][0]['expected_sha256'])},
            'projected_setup_peak_bytes': 30, 'projected_provisioning_seconds': 17,
            'pools': [{'id': 'pool1', 'free_bytes': 1000, 'projected_peak_bytes': 30}],
            'writer_reservation_matches': True, 'no_queued_external_writers': True}

    def test_01_cumulative_clock_across_invocations(self):
        c = self.collector()
        state = (self.root / 'window.json').read_bytes()
        c.close()
        self.clock[0] += 31
        self.mono[0] += 31
        later = self.collector()
        self.assertEqual(later.remaining(), 6)
        self.assertEqual((self.root / 'window.json').read_bytes(), state)
        later.close()
        self.clock[0] += 7
        self.mono[0] += 7
        with self.assertRaisesRegex(self.api.Refusal, 'deadline'):
            self.collector()
        self.assertEqual((self.root / 'window.json').read_bytes(), state)

    def test_02_prewrite_byte_admission_and_cached_accounting(self):
        c = self.collector('fetch')
        p = c.download('https://example.invalid/a', 'a', 3)
        size = c.usage()['staging_bytes']
        self.assertGreaterEqual(size, 3)
        self.assertEqual(c.download('https://example.invalid/a', 'a', 3), p)
        self.assertEqual(len(self.calls), 1)
        c.close()
        c = self.collector('fetch')
        self.assertEqual(c.download('https://example.invalid/a', 'a', 3), p)
        self.assertEqual(len(self.calls), 1)
        self.assertGreaterEqual(c.usage()['staging_bytes'], size)
        size = c.usage()['staging_bytes']
        self.m['collector']['staging_bound_bytes'] = size + 2
        with self.assertRaisesRegex(self.api.Refusal, 'staging'):
            c.download('https://example.invalid/b', 'b', 3)
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(list((self.root / 'downloads').iterdir()), [p])

    def test_03_durable_timeout_and_command_failure_receipts(self):
        self.assertIsNotNone(self.api, 'R1C collector implementation is missing')
        for kind in ['timeout', 'nonzero', 'spawn', 'large-error']:
            with self.subTest(kind=kind):
                self.root = self.base / kind
                self.m['collector']['retained_dir'] = str(self.root)
                self.m['collector']['admitted_write_roots'] = [str(self.root), str(self.install)]
                self.m['collector']['child_contract']['allowed_write_roots'] = [str(self.root)]
                def failed(argv, **kwargs):
                    if kind == 'timeout':
                        raise subprocess.TimeoutExpired(argv, kwargs['timeout'], output=b'partial')
                    if kind == 'spawn':
                        raise OSError('exec failed')
                    return subprocess.CompletedProcess(argv, 7, b'partial',
                        b'bad' if kind == 'nonzero' else b'x' * 6000)
                if kind == 'large-error':
                    self.m['collector']['io_chunk_bytes'] = 8192
                c = self.collector(runner=failed)
                with self.assertRaises(self.api.Refusal):
                    c.run(['/fake/curl', '--version'])
                receipt = json.loads((self.root / 'receipts' / 'failure.json').read_text())
                self.assertEqual(receipt['argv'], ['/fake/curl', '--version'])
                self.assertGreaterEqual(receipt['elapsed_seconds'], 0)
                self.assertTrue(receipt['error'])
                self.assertEqual(receipt['status'], 'HALTED')
                with self.assertRaises(self.api.Refusal):
                    c.halt('outer stop')
                self.assertEqual(json.loads((self.root / 'receipts' / 'failure.json').read_text()), receipt)
                c.close()
                with self.assertRaisesRegex(self.api.Refusal, 'retained failure'):
                    self.collector()

    def test_04_scoped_streaming_inventory_separates_baseline(self):
        outside = self.base / 'unadmitted'
        outside.mkdir()
        (outside / 'secret').write_bytes(b'never visited')
        for i in range(80):
            (self.install / ('f%d' % i)).write_bytes(b'baseline')
        c = self.collector()
        real_scandir = os.scandir
        visited = []
        def scoped(path):
            visited.append(str(path))
            self.assertTrue(any(Path(path) == r or r in Path(path).parents for r in [self.root, self.install]))
            return real_scandir(path)
        with mock.patch.object(self.api.os, 'scandir', side_effect=scoped):
            result = c.inventory()
        rows = [json.loads(x) for x in Path(result['receipt']).read_text().splitlines()]
        self.assertEqual(sum(x['logical_bytes'] for x in rows if x.get('kind') == 'file' and x['origin'] == 'baseline'), 640)
        self.assertTrue(any(x['origin'] == 'collector' for x in rows))
        self.assertEqual(next(x['origin'] for x in rows if x['path'] == str(self.root)), 'collector')
        self.assertNotIn(str(outside), visited)
        source = SOURCE.read_text()
        self.assertNotIn('.rglob(', source)
        self.assertNotIn('list(self.walk', source)
        self.m['collector']['receipt_limit_bytes'] = c.usage()['receipt_bytes'] + 10
        with self.assertRaisesRegex(self.api.Refusal, 'receipt'):
            c.inventory()
        self.assertLessEqual(c.usage()['receipt_bytes'], self.m['collector']['receipt_limit_bytes'])

    def test_05_special_unreadable_and_changing_entries_are_observations(self):
        c = self.collector()
        fifo = self.install / 'fifo'
        os.mkfifo(str(fifo))
        socket_path = self.install / 'socket'
        socket_path.write_bytes(b'')
        bad = self.install / 'unreadable'
        bad.write_bytes(b'x')
        changed = self.install / 'changed'
        changed.write_bytes(b'x')
        real = c.digest
        def digest(path):
            if Path(path) == bad:
                raise PermissionError('fixture unreadable')
            value = real(path)
            if Path(path) == changed:
                changed.write_bytes(b'changed')
            return value
        real_lstat = Path.lstat
        def typed_lstat(path):
            value = real_lstat(path)
            if path == socket_path:
                fields = list(value)
                fields[0] = stat.S_IFSOCK | 0o600
                # A fake stat carries the real metadata plus a socket file type.
                proxy = mock.Mock(wraps=value)
                for attr in ['st_uid', 'st_gid', 'st_size', 'st_blocks', 'st_dev', 'st_ino', 'st_mtime_ns', 'st_ctime_ns']:
                    setattr(proxy, attr, getattr(value, attr))
                proxy.st_mode = fields[0]
                return proxy
            return value
        with mock.patch.object(c, 'digest', side_effect=digest), mock.patch.object(Path, 'lstat', typed_lstat):
            rows = list(c.walk([str(self.install)]))
        kinds = {Path(x['path']).name: x['kind'] for x in rows}
        self.assertEqual(kinds['fifo'], 'fifo')
        self.assertEqual(kinds['socket'], 'socket')
        self.assertEqual(kinds['unreadable'], 'unreadable')
        self.assertEqual(kinds['changed'], 'changed')
        real_scandir = os.scandir
        directory_reads = [0]
        def denied_walk(path):
            if str(path) == str(self.install):
                directory_reads[0] += 1
                if directory_reads[0] > 1:
                    raise PermissionError('directory changed to unreadable')
            return real_scandir(path)
        with mock.patch.object(self.api.os, 'scandir', side_effect=denied_walk):
            walked = list(c.walk([str(self.install)]))
        self.assertTrue(any(x['kind'] == 'unreadable' and x['path'] == str(self.install) for x in walked))

    def test_06_phase_specific_guard_and_strict_observation_types(self):
        self.assertIsNotNone(self.api, 'R1C collector implementation is missing')
        self.api.admission(self.m, self.observation())
        for mutation in [lambda o: o.update(pools=[]),
                lambda o: o['pools'][0].update(id='wrong'),
                lambda o: o['pools'][0].update(free_bytes=-1),
                lambda o: o.update(projected_provisioning_seconds=float('inf')),
                lambda o: o.update(projected_setup_peak_bytes=float('nan')),
                lambda o: o.update(projected_setup_peak_bytes=-1),
                lambda o: o.update(writer_reservation_matches=1),
                lambda o: o.update(no_queued_external_writers='true'),
                lambda o: o.update(projected_setup_peak_bytes=29)]:
            o = self.observation()
            mutation(o)
            with self.subTest(observation=o), self.assertRaises(self.api.Refusal):
                self.api.admission(self.m, o)
        for value in [-1, float('inf'), float('nan'), True]:
            m = copy.deepcopy(self.m)
            m['budget']['components'][0]['bytes'] = value
            with self.subTest(component=value), self.assertRaises(self.api.Refusal):
                self.api.admission(m, self.observation())
        m = copy.deepcopy(self.m)
        m['tree']['commit'] = 'NEEDS-FETCH'
        with self.assertRaises(self.api.Refusal):
            self.api.admission(m, self.observation())

    def test_07_actual_install_walk_rejects_unregistered_extra(self):
        wanted = self.install / 'wanted'
        wanted.write_bytes(b'abc')
        self.m['postinstall']['expected_payloads'] = {
            str(self.install): {'kind': 'directory', 'mode': self.install.stat().st_mode & 0o7777},
            str(wanted): {'kind': 'file', 'mode': wanted.stat().st_mode & 0o7777,
                'sha256': hashlib.sha256(b'abc').hexdigest()}}
        c = self.collector('compare-installed')
        c.compare_installed()
        (self.install / 'unregistered').write_bytes(b'extra')
        with self.assertRaisesRegex(self.api.Refusal, 'Unexpected'):
            c.compare_installed()
        self.assertEqual(self.calls, [])

    def test_08_manifest_policy_artifact_types_lock_and_modes(self):
        c = self.collector()
        literals = [n.value for n in ast.walk(ast.parse(SOURCE.read_text())) if isinstance(n, ast.Constant)]
        for forbidden in [900, 600000000, 10000000, '1.5.5', 'cp312', 'x86_64', 'darwin_23']:
            self.assertNotIn(forbidden, literals)
            self.assertNotIn(str(forbidden), SOURCE.read_text())
        self.assertEqual(c.remaining(), self.m['budget']['clock_seconds'])
        a = self.m['artifacts'][0]
        meta = {'info': {'version': '9.7'}, 'urls': [{'filename': 'sample-9.7-cp399-cp399-macosx_27_4_fakearch.whl',
            'packagetype': 'bdist_wheel', 'yanked': False, 'size': 3, 'url': a['source_url'],
            'digests': {'sha256': a['expected_sha256']}}]}
        self.assertEqual(c.wheel_candidate(a, meta)['size'], 3)
        self.m['collector']['wheel']['max_platform'] = [26, 0]
        with self.assertRaises(self.api.Refusal):
            c.wheel_candidate(a, meta)
        missing = self.base / 'missing.lock'
        fallback = self.base / 'fallback.lock'
        fallback.write_text('sample==9.7 --hash=sha256:' + a['expected_sha256'])
        self.m['artifacts'].append({'id': 'lock', 'source_url': str(missing)})
        c.byid['lock'] = self.m['artifacts'][-1]
        self.m['paths']['duckdb_lock'] = str(fallback)
        with self.assertRaisesRegex(self.api.Refusal, 'lock'):
            c.wheel(a)
        self.assertEqual(self.calls, [])
        c.close()
        self.m['collector']['retained_dir'] = str(self.base / 'untouched')
        with self.assertRaisesRegex(self.api.Refusal, 'mode'):
            self.collector('install')
        self.assertFalse((self.base / 'untouched').exists())
        v3 = json.loads((HERE / 'intel_provisioning_manifest_v3.json').read_text())
        for entry in v3['artifacts']:
            if entry['id'] in ['r3-controller', 'r3-workload', 'r3-review']:
                self.assertEqual(entry['route'], 'supplied local artifact')
        self.assertFalse(v3['authorization']['staging'])
        wrapper = (HERE / 'r1c_host_commands.sh').read_text()
        self.assertIn('exec /usr/bin/python3 -I -B', wrapper)
        self.assertNotIn('R1B_READ_PYTHON', wrapper)

    def test_09_mode_results_partition_identity_without_verification(self):
        c = self.collector()
        for mode in self.m['collector']['allowed_modes']:
            with self.subTest(mode=mode):
                result = c.result(mode, None, ['sha256'])
                self.assertEqual(result['status'], 'OBSERVATION-ONLY')
                self.assertEqual(result['established'], ['sha256'])
                self.assertEqual(set(result['remaining_open']), set(self.m['collector']['identity_fields']) - {'sha256'})
                self.assertNotIn('verified', result)
        a = self.m['artifacts'][0]
        local = self.base / 'supplied'
        local.write_bytes(b'abc')
        a['source_url'] = str(local)
        result = c.collect('inspect', 'a')
        self.assertNotIn('abi', result['established'])
        self.assertIn('abi', result['remaining_open'])
        self.assertIn('signature_trust', result['remaining_open'])
        parent_archive = self.base / 'parent.tar'
        with tarfile.open(str(parent_archive), 'w') as archive:
            archive.add(str(local), arcname='member')
        parent = dict(a, id='parent', source_url='https://example.invalid/parent',
            size_bytes=parent_archive.stat().st_size, expected_sha256=hashlib.sha256(parent_archive.read_bytes()).hexdigest())
        self.m['collector']['per_download_bound_bytes'] = parent['size_bytes'] + 1
        self.m['artifacts'].append(parent)
        c.byid['parent'] = parent
        a['source_url'] = 'manifest:parent'
        def archive_runner(argv, **kwargs):
            Path(argv[argv.index('--output') + 1]).write_bytes(parent_archive.read_bytes())
            return subprocess.CompletedProcess(argv, 0,
                ('https://example.invalid/parent\n200\n%d\n' % parent['size_bytes']).encode(), b'')
        c.runner = archive_runner
        derived = c.collect('inspect', 'a')
        self.assertEqual(derived['established'], [])
        self.assertIn('installer_interface', derived['remaining_open'])
        self.assertIn('abi', derived['remaining_open'])


if __name__ == '__main__':
    unittest.main()
