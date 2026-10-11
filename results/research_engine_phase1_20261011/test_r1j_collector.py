"""Nine carried R1C tests plus nine R1D criteria; fake roots and child runners."""
import ast
import base64
import types
import shutil
import contextlib
import io
import shlex
import sys
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
SOURCE = HERE / 'r1j_collector.py'


def load_collector():
    if not SOURCE.exists():
        return None
    probe = types.ModuleType('verified_probe')
    exec(compile((HERE / 'r1j_identity_probe.py').read_bytes(), '<test:identity>', 'exec'), probe.__dict__)
    module = types.ModuleType('verified_collector')
    module.__file__ = str(SOURCE)
    module.VERIFIED_PROBE = probe.__dict__
    module.VERIFIED_MEMBERS = {}
    module.VERIFIED_HASHES = {}
    exec(compile(SOURCE.read_bytes(), '<test:collector>', 'exec'), module.__dict__)
    return module


class R1DCriteria(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='r1d-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'retained'
        self.install = self.base / 'install'
        self.install.mkdir()
        self.clock = [1000.0]
        self.mono = [2000.0]
        self.api = load_collector()
        self.calls = []
        self.identity = {'executable': '/fake/python3', 'realpath': '/fake/python3',
            'executable_sha256': 'a' * 64, 'version_info': [3, 9, 6, 'final', 0],
            'machine': 'fake_arch', 'mac_ver': ['test', ['', '', ''], 'fake_arch'],
            'flags': {'isolated': 1, 'dont_write_bytecode': 1}, 'hostname': 'fake-host',
            'stdlib': {'directory': '/fake/stdlib', 'sha256': 'b' * 64, 'file_count': 2}}
        if self.api is not None:
            patch = mock.patch.object(self.api, 'interpreter_identity', return_value=self.identity, create=True)
            patch.start()
            self.addCleanup(patch.stop)
        self.m = {
            'schema': 'R1D-v3', 'authorization': {
                'staging': True, 'building': True, 'installation': True},
            'host': {'arch': 'fake_arch', 'pool_map': {
                str(self.root): 'pool1', str(self.install): 'pool1'}},
            'tree': {'commit': 'test-pin'}, 'paths': {'root': str(self.install)},
            'selection': {'registered_names': []},
            'artifacts': [{'id': 'a', 'name': 'sample', 'version_revision': '9.7',
                'variants': [], 'source_url': 'https://example.invalid/a',
                'expected_sha256': hashlib.sha256(b'abc').hexdigest(),
                'size_bytes': 3, 'route': 'upstream tarball'}],
            'budget': {'clock_seconds': 37, 'transit_margin_seconds': 5, 'pre_go_cap_seconds': 2, 'max_dispatch_receipt_bytes': 20000, 'm3_receipt_patterns': ['r1j_attempt_*.json', 'r1j_bind_*.json', 'r1j_bind_*.stderr', 'r1j_bind_*.exit', 'r1j_bind_*.final', 'r1j_inventory_*.json', 'r1j_inventory_*.stderr', 'r1j_inventory_*.exit', 'r1j_inventory_*.final', 'r1j_bind_*.final.pending', 'r1j_inventory_*.final.pending'], 'setup_cap_bytes': 200000,
                'free_floor_bytes': 100, 'additional_headroom_bytes': 50,
                'components': [{'id': 'one', 'bytes': 20}, {'id': 'two', 'bytes': 10}],
                'planned_peak_bytes': 30},
            'collector': {'allowed_modes': ['inventory', 'tree', 'guard',
                'compare-installed', 'fetch', 'wheel', 'inspect', 'source-plan',
                'archive-index', 'r3'], 'retained_dir': str(self.root),
                'admitted_write_roots': [str(self.root), str(self.install)],
                'install_roots': [str(self.install)], 'receipt_limit_bytes': 80000,
                'failure_reserve_bytes': 2048, 'staging_bound_bytes': 140000,
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
        self.m['collector']['interpreter'] = {
            'executable': '/fake/python3', 'flags': ['-I', '-B'],
            'minimum_version': [3, 9], 'identity': copy.deepcopy(self.identity)}
        self.m['budget']['components'].append({'id': 'receipts', 'bytes': 80000})
        self.m['budget']['planned_peak_bytes'] = 80030
        self.m['evidence'] = {'child_contract_receipts': 'NEEDS-FETCH'}
        self.m['window_seal'] = {'core_keys': [
            '/window_seal/core_keys', '/window_seal/evidence_slots', '/window_seal/artifact_ids',
            '/budget',
            '/collector', '/preinstall', '/authorization', '/tree', '/paths', '/artifacts', '/host/arch',
            '/postinstall'], 'evidence_slots': ['/host/pool_map', '/evidence/child_contract_receipts'],
            'artifact_ids': ['a'], 'core_sha256': ''}
        self.registration_root = self.base / 'registration'
        self.m['collector']['registration_path'] = str(self.registration_root / 'window.jsonl')
        self.seal()

    def seal(self):
        old = self.registration_root
        self.registration_root = self.base / ('registration-' + self.root.name)
        self.m['collector']['registration_path'] = str(self.registration_root / 'window.jsonl')
        self.m['collector']['admitted_write_roots'] = [x for x in self.m['collector']['admitted_write_roots'] if x != str(old)]
        self.m['collector']['admitted_write_roots'] = list(dict.fromkeys(self.m['collector']['admitted_write_roots'] + [str(self.registration_root)]))
        if str(self.root) in self.m['host']['pool_map']:
            self.m['host']['pool_map'][str(self.registration_root)] = 'pool1'
        self.m['window_seal']['artifact_ids'] = [a['id'] for a in self.m['artifacts']]
        core = {path: self.at(self.m, path) for path in self.m['window_seal']['core_keys']}
        self.m['window_seal']['core_sha256'] = hashlib.sha256(
            (json.dumps(core, sort_keys=True, allow_nan=False) + '\n').encode()).hexdigest()
        if self.api is not None:
            source = copy.deepcopy(self.m)
            source.pop('binding_provenance', None)
            source['collector']['interpreter']['identity'] = {k: 'NEEDS-FETCH' for k in self.identity}
            source['window_seal']['core_sha256'] = 'NEEDS-FETCH'
            source_path = self.base / 'v5.json'
            source_path.write_bytes(self.api.encoded(source))
            self.api.VERIFIED_MEMBERS = {'manifest': source_path.read_bytes(), 'collector': SOURCE.read_bytes(), 'identity': (HERE / 'r1j_identity_probe.py').read_bytes(), 'binder': (HERE / 'r1j_bind_manifest.py').read_bytes()}
            self.api.VERIFIED_HASHES = {k: hashlib.sha256(v).hexdigest() for k, v in self.api.VERIFIED_MEMBERS.items()}
            self.source_path = source_path
            self.m['binding_provenance'] = {
                'v8_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
                'probe_file_sha256': hashlib.sha256(self.api.encoded(self.m['collector']['interpreter']['identity'])).hexdigest(),
                'probe_json': self.api.encoded(self.m['collector']['interpreter']['identity']).decode('utf-8'), 'binder_sha256': hashlib.sha256((HERE / 'r1j_bind_manifest.py').read_bytes()).hexdigest(),
                'collector_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                'identity_probe_sha256': hashlib.sha256((HERE / 'r1j_identity_probe.py').read_bytes()).hexdigest(),
                'utc_time': '2026-10-11T00:00:00Z',
                'bound_core_sha256': self.m['window_seal']['core_sha256']}

            self.capture = self.publication(self.m)
            self.capture_hash = hashlib.sha256(self.capture).hexdigest()
            self.api.VERIFIED_MEMBERS['capture'] = self.capture
            self.api.VERIFIED_MEMBERS['request'] = self.api.encoded({})

    def publication(self, manifest):
        data = self.api.encoded(manifest)
        return self.api.encoded({'bound_manifest_json': data.decode(), 'binding_receipt': {
            'argv': ['fake-runtime', '-I', '-B', '-c', 'verified-stub'],
            'hostname': 'fake-host', 'uname': ['fake'] * 5,
            'bootstrap_start_utc': '1970-01-01T00:16:40Z',
            'input_sha256': dict(self.api.VERIFIED_HASHES),
            'raw_probe_output': self.api.encoded(self.identity).decode(),
            'bound_manifest_sha256': hashlib.sha256(data).hexdigest()}})

    def expected_anchor(self):
        c = getattr(self, 'last_collector', None)
        if c is not None and c.registration == Path(json.loads(json.loads(self.capture)['bound_manifest_json'])['collector']['registration_path']):
            return '%d:%s' % (c.registry_seq, c.registry_head)
        return 'none'

    def construct(self, manifest, mode, **kwargs):
        supplied = self.publication(manifest)
        kwargs.setdefault('expected_anchor', self.expected_anchor())
        kwargs.setdefault('expected_capture_sha256', self.capture_hash)
        kwargs.setdefault('bootstrap_bytes', len(self.capture) + 2)
        budget = json.loads(json.loads(self.capture)['bound_manifest_json'])['budget']
        kwargs.setdefault('remaining_seconds', min(budget['clock_seconds'], budget.get('time_total_s', budget['clock_seconds'])) - max(self.clock[0] - 1000, self.mono[0] - 2000))
        kwargs.setdefault('process_start', self.mono[0])
        c = self.api.Collector(supplied, mode, **kwargs)
        self.last_collector = c
        return c


    @staticmethod
    def at(value, path):
        if not path:
            return value
        for part in path.strip('/').split('/'):
            value = value[int(part)] if isinstance(value, list) else value[part]
        return value

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob('*') if p.is_file()}

    def fake_run(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        if '--output' in argv:
            Path(argv[argv.index('--output') + 1]).write_bytes(b'abc')
        return subprocess.CompletedProcess(argv, 0, b'https://example.invalid/a\n200\n3\n', b'')

    def collector(self, mode='inventory', **kwargs):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        self.seal()
        c = self.construct(self.m, mode, now=lambda: self.clock[0],
            monotonic=lambda: self.mono[0], runner=kwargs.pop('runner', self.fake_run), **kwargs)
        self.addCleanup(c.close)
        return c

    def observation(self, manifest=None):
        m = self.m if manifest is None else manifest
        return {'host': copy.deepcopy(m['host']), 'tree': copy.deepcopy(m['tree']),
            'paths': copy.deepcopy(m['paths']), 'preinstalled_ports': [],
            'artifacts': {'a': dict(m['artifacts'][0], sha256=m['artifacts'][0]['expected_sha256'])},
            'projected_setup_peak_bytes': 80030, 'projected_provisioning_seconds': 17,
            'pools': [{'id': 'pool1', 'free_bytes': 200000, 'projected_peak_bytes': 80030}],
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
        c.p['staging_bound_bytes'] = size + 2
        with self.assertRaisesRegex(self.api.Refusal, 'staging'):
            c.download('https://example.invalid/b', 'b', 3)
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(list((self.root / 'downloads').iterdir()), [p])

    def test_03_durable_timeout_and_command_failure_receipts(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
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
            self.assertTrue(any(Path(path) == r or r in Path(path).parents for r in [self.root, self.install, self.registration_root]))
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
        c.p['receipt_limit_bytes'] = c.usage()['receipt_bytes'] + 10
        with self.assertRaisesRegex(self.api.Refusal, 'receipt'):
            c.inventory()
        self.assertLessEqual(c.usage()['receipt_bytes'], c.p['receipt_limit_bytes'])

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
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
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
        c.p['wheel']['max_platform'] = [26, 0]
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
        v3 = json.loads((HERE / 'intel_provisioning_manifest_v9.json').read_text())
        for entry in v3['artifacts']:
            if entry['id'] in ['r3-controller', 'r3-workload', 'r3-review']:
                self.assertEqual(entry['route'], 'supplied local artifact')
        self.assertFalse(v3['authorization']['staging'])
        wrapper = (HERE / 'r1j_host_commands.sh').read_text()
        self.assertIn('/Library/Developer/CommandLineTools/usr/bin/python3 -I -B', wrapper)
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
        a = c.m['artifacts'][0]
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
        c.p['per_download_bound_bytes'] = parent['size_bytes'] + 1
        c.m['artifacts'].append(parent)
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


    def test_r1d_01_core_seal_preserves_window_receipts_and_elapsed(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v9.json').read_text())
        original_digest = self.api.core_digest(v4)
        original_v4 = copy.deepcopy(v4)
        for slot in v4['window_seal']['evidence_slots']:
            parent, key = slot.rsplit('/', 1)
            self.at(v4, parent)[key] = {'filled': 'test-only'}
        self.assertEqual(self.api.core_digest(v4), original_digest)
        v4 = original_v4
        def unresolved_paths(value, prefix):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield from unresolved_paths(child, prefix + '/' + key)
            elif isinstance(value, list):
                for i, child in enumerate(value):
                    yield from unresolved_paths(child, prefix + '/' + str(i))
            elif isinstance(value, str) and 'NEEDS-FETCH' in value:
                yield prefix
        for required in v4['preinstall']['required_fields']:
            for path in unresolved_paths(self.at(v4, required), required):
                self.assertTrue(any(path == slot or path.startswith(slot + '/')
                    for slot in v4['window_seal']['evidence_slots']), path)
        c = self.collector()
        c.save('prior', {'data': 'immutable'})
        c.append_evidence('/host/pool_map', {'observed': 'pool1'})
        before = self.snapshot()
        start = dict(c.start)
        c.close()
        self.clock[0] += 5
        self.mono[0] += 7
        self.m = json.loads(json.loads(self.capture)['bound_manifest_json'])
        c = self.construct(self.m, 'inventory', now=lambda: self.clock[0],
            monotonic=lambda: self.mono[0], runner=self.fake_run)
        self.addCleanup(c.close)
        self.assertEqual(c.start, start)
        self.assertEqual(c.elapsed(), 7)
        self.assertEqual(self.snapshot(), before)
        # A usable add-only update entry point preserves every prior receipt and clock.
        c.append_evidence('/evidence/child_contract_receipts', 'review-pending')
        self.assertEqual(c.evidence.get('/evidence/child_contract_receipts'), 'review-pending')
        self.assertEqual(len((self.root / 'evidence.jsonl').read_bytes().splitlines()), 2)
        for name, data in before.items():
            if name != 'evidence.jsonl':
                self.assertEqual((self.root / name).read_bytes(), data)
        self.assertEqual(c.start, start)
        self.assertEqual(c.collect('inventory')['status'], 'OBSERVATION-ONLY')
        before = self.snapshot()
        c.close()
        original = copy.deepcopy(self.m)
        for path in self.m['window_seal']['core_keys']:
            with self.subTest(core_path=path):
                self.m = copy.deepcopy(original)
                parent, key = path.rsplit('/', 1)
                container = self.at(self.m, parent)
                container[key] = 'changed core byte'
                with self.assertRaises(self.api.Refusal):
                    self.construct(self.m, 'inventory', runner=self.fake_run)
                self.assertEqual(self.snapshot(), before)
        self.m = copy.deepcopy(original)
        other = self.base / 'new-clock-forbidden'
        self.m['collector']['retained_dir'] = str(other)
        self.m['collector']['admitted_write_roots'].append(str(other))
        with self.assertRaises(self.api.Refusal):
            self.construct(self.m, 'inventory', runner=self.fake_run)
        self.assertFalse(other.exists())
        self.assertEqual(self.snapshot(), before)
        self.m = original

    def test_r1d_02_add_only_evidence_chain_rejects_tampering_and_core_slots(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        c = self.collector()
        ledger = self.root / 'evidence.jsonl'
        c.append_evidence('/host/pool_map', {'observed': 'pool1'})
        first = ledger.read_bytes()
        c.append_evidence('/evidence/child_contract_receipts', {'receipt': 'test-only'})
        lines = ledger.read_bytes().splitlines(keepends=True)
        self.assertTrue(ledger.read_bytes().startswith(first))
        self.assertEqual(json.loads(lines[0])['previous_sha256'], c.start['seal_sha256'])
        self.assertEqual(json.loads(lines[1])['previous_sha256'], hashlib.sha256(lines[0]).hexdigest())
        for line in lines:
            self.assertEqual(json.loads(line)['seal_sha256'], c.start['seal_sha256'])
        before = self.snapshot()
        for slot in ['/not/allowed', '/budget/clock_seconds', '/collector/retained_dir', '/host/pool_map']:
            with self.subTest(slot=slot), self.assertRaises(self.api.Refusal):
                c.append_evidence(slot, 'overwrite')
            self.assertEqual(self.snapshot(), before)
        c.close()
        original = ledger.read_bytes()
        for corrupt in [original[:-1], lines[0].replace(b'pool1', b'pool2') + lines[1], lines[0]]:
            with self.subTest(corrupt=corrupt):
                ledger.write_bytes(corrupt)
                before = self.snapshot()
                with self.assertRaises(self.api.Refusal):
                    self.construct(self.m, 'inventory', runner=self.fake_run)
                self.assertEqual(self.snapshot(), before)
        ledger.write_bytes(original)
        # Even a manifest-authorized slot may not overlap the core.
        self.m['window_seal']['evidence_slots'].append('/collector/retained_dir')
        self.seal()
        with self.assertRaises(self.api.Refusal):
            self.construct(self.m, 'inventory', runner=self.fake_run)

    def test_r1d_03_identity_must_be_bound_and_match_before_any_clock_or_write(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        bound = copy.deepcopy(self.m['collector']['interpreter']['identity'])
        cases = [lambda x: x.update(executable_sha256='NEEDS-FETCH'),
            lambda x: x.update(executable_sha256='c' * 64),
            lambda x: x.update(version_info=[3, 9, 7, 'final', 0]),
            lambda x: x['stdlib'].update(sha256='c' * 64),
            lambda x: x['stdlib'].update(file_count=3),
            lambda x: x.update(realpath='/different/python3'),
            lambda x: x['flags'].update(isolated=0)]
        for mutation in cases:
            self.m['collector']['interpreter']['identity'] = copy.deepcopy(bound)
            mutation(self.m['collector']['interpreter']['identity'])
            self.seal()
            clock = mock.Mock(side_effect=AssertionError('clock started before identity binding'))
            with self.subTest(identity=self.m['collector']['interpreter']['identity']), self.assertRaises(self.api.Refusal):
                self.construct(self.m, 'inventory', now=clock, monotonic=clock, runner=self.fake_run)
            self.assertFalse(self.root.exists())
            clock.assert_not_called()
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v9.json').read_text())
        self.assertIn('NEEDS-FETCH', json.dumps(v4['collector']['interpreter']['identity']))

    def test_r1d_04_final_summary_fsync_deadline_has_no_success_output(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        c = self.collector()
        manifest_path = self.base / 'manifest.json'
        manifest_path.write_text(json.dumps(self.m))
        real_syncdir = c._syncdir
        def cross_deadline(path):
            real_syncdir(path)
            if list(c.receipts.glob('summary-*.jsonl')):
                self.clock[0] += self.m['budget']['clock_seconds'] + 1
                self.mono[0] += self.m['budget']['clock_seconds'] + 1
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), mock.patch.object(c, '_syncdir', side_effect=cross_deadline), \
                mock.patch.object(self.api, 'Collector', return_value=c), contextlib.redirect_stdout(stdout):
            self.assertNotEqual(self.api.entrypoint(['inventory', '--expected-anchor', self.expected_anchor(), '--expected-capture-sha256', self.capture_hash, '--bootstrap-bytes', str(len(self.capture) + 2), '--remaining-seconds', '37', '--m3-receipt-bytes', '0']), 0)
        self.assertFalse(any(x.startswith('{') for x in stdout.getvalue().splitlines()))
        self.assertEqual(json.loads((c.receipts / 'failure.json').read_text())['status'], 'HALTED')
        self.assertEqual(len(list(c.receipts.glob('summary-*.jsonl'))), 1)

    def test_r1d_05_real_cumulative_command_deadline_retains_active_argv(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        c = self.collector()
        c.runner = c._execute
        c.p['child_contract']['sha256'] = 'a' * 64
        child = mock.Mock()
        child.stdout, child.stderr = io.BytesIO(), io.BytesIO()
        child.poll.return_value = None
        selector = mock.MagicMock()
        selector.__enter__.return_value = selector
        selector.get_map.return_value = {'active': True}
        def expire(left):
            self.clock[0] += self.m['budget']['clock_seconds'] + 1
            self.mono[0] += self.m['budget']['clock_seconds'] + 1
            return []
        selector.select.side_effect = expire
        argv = ['/fake/curl', '--version']
        with mock.patch.object(c, 'digest', return_value='a' * 64), \
                mock.patch.object(self.api.subprocess, 'Popen', return_value=child), \
                mock.patch.object(self.api.selectors, 'DefaultSelector', return_value=selector):
            with self.assertRaisesRegex(self.api.Refusal, 'Cumulative'):
                c.run(argv)
        receipt = (c.receipts / 'failure.json').read_bytes()
        self.assertEqual(json.loads(receipt)['argv'], argv)
        self.assertIn('deadline', json.loads(receipt)['error'])
        with self.assertRaises(self.api.Refusal):
            c.halt('outer failure')
        self.assertEqual((c.receipts / 'failure.json').read_bytes(), receipt)
        child.kill.assert_called_once()
        # Also exercise the remaining() call immediately before child.wait().
        c.close()
        self.clock[0], self.mono[0] = 1000.0, 2000.0
        self.root = self.base / 'deadline-before-wait'
        self.m['collector']['retained_dir'] = str(self.root)
        self.m['collector']['admitted_write_roots'] = [str(self.root), str(self.install)]
        self.m['collector']['child_contract']['allowed_write_roots'] = [str(self.root)]
        c = self.collector()
        c.runner = c._execute
        child.stdout, child.stderr = io.BytesIO(), io.BytesIO()
        def empty_map():
            expire(0)
            return {}
        c.p['child_contract']['sha256'] = 'a' * 64
        selector.get_map.side_effect = empty_map
        with mock.patch.object(c, 'digest', return_value='a' * 64), \
                mock.patch.object(self.api.subprocess, 'Popen', return_value=child), \
                mock.patch.object(self.api.selectors, 'DefaultSelector', return_value=selector):
            with self.assertRaisesRegex(self.api.Refusal, 'Cumulative'):
                c.run(argv)
        self.assertEqual(json.loads((c.receipts / 'failure.json').read_bytes())['argv'], argv)

    def test_r1d_06_probe_is_read_only_and_stdlib_function_is_shared(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        cwd = self.base / 'probe-cwd'
        cwd.mkdir()
        result = subprocess.run(['/usr/bin/python3', '-I', '-B', str(HERE / 'r1j_identity_probe.py')],
            cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        self.assertEqual(list(cwd.iterdir()), [])
        identity = json.loads(result.stdout)
        self.assertEqual(set(identity), {'executable', 'realpath', 'executable_sha256',
            'version_info', 'machine', 'mac_ver', 'flags', 'hostname', 'stdlib'})
        self.assertEqual(len(identity['executable_sha256']), 64)
        self.assertEqual(len(identity['version_info']), 5)
        self.assertEqual(identity['flags'], {'isolated': 1, 'dont_write_bytecode': 1})
        self.assertGreater(identity['stdlib']['file_count'], 0)
        self.assertEqual(len(identity['stdlib']['sha256']), 64)
        self.assertIn('r1j_identity_probe.py', SOURCE.read_text())
        self.assertNotIn('def stdlib_identity', SOURCE.read_text())
        stdlib = self.base / 'fake-stdlib'
        stdlib.mkdir()
        (stdlib / 'z.py').write_bytes(b'z')
        (stdlib / 'a.py').write_bytes(b'a')
        (stdlib / 'link').symlink_to(stdlib / 'z.py')
        expected = hashlib.sha256()
        for name in ['a.py', 'link', 'z.py']:
            row = [name, hashlib.sha256((stdlib / name).read_bytes()).hexdigest()] if name != 'link' else [name, 'symlink', os.readlink(str(stdlib / name)), str((stdlib / name).resolve()), 'file', hashlib.sha256((stdlib / name).read_bytes()).hexdigest()]
            expected.update((json.dumps(row,
                separators=(',', ':')) + '\n').encode())
        measured = self.api.stdlib_identity(stdlib)
        self.assertEqual(measured['sha256'], expected.hexdigest())
        self.assertEqual(measured['file_count'], 3)

    def test_r1d_07_single_policy_interpreter_wrapper_and_receipt_equality(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v9.json').read_text())
        line = next(x for x in (HERE / 'r1j_host_commands.sh').read_text().splitlines() if x.startswith('runtime_command='))
        tokens = ['exec'] + shlex.split(shlex.split(line.split('=', 1)[1])[0])
        tool = v4['collector']['interpreter']
        self.assertEqual(tokens[1], tool['executable'])
        self.assertEqual(tokens[2:4], tool['flags'])
        literals = [n.value for n in ast.walk(ast.parse(SOURCE.read_text())) if isinstance(n, ast.Constant)]
        limits = [v for k, v in v4['collector'].items() if k.endswith(('_bytes', '_seconds'))]
        limits += [v for k, v in v4['budget'].items() if k.endswith(('_bytes', '_seconds', '_s'))]
        limits += [v4['collector']['curl']['connect_timeout_seconds']]
        limits += [v for k, v in v4['collector']['wheel'].items() if k.endswith(('_bytes', '_count'))]
        limits += [v4['collector']['archive_index']['bound_bytes']]
        for value in limits:
            self.assertNotIn(value, literals)
        original = copy.deepcopy(self.m)
        changes = [lambda: self.m['collector']['interpreter'].update(executable='/different/python3'),
            lambda: self.m['collector']['interpreter'].update(flags=['-B']),
            lambda: self.m['collector'].update(receipt_limit_bytes=80001),
            lambda: self.m['budget'].update(planned_peak_bytes=80031)]
        for change in changes:
            self.m = copy.deepcopy(original)
            change()
            self.seal()
            with self.assertRaises(self.api.Refusal):
                self.construct(self.m, 'inventory', runner=self.fake_run)
            self.assertFalse(self.root.exists())
        receipts = [x['bytes'] for x in v4['budget']['components'] if x['id'] == 'receipts']
        self.assertEqual(receipts, [v4['collector']['receipt_limit_bytes']])

    def test_r1d_08_each_mode_entrypoint_established_and_open_partition(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        c = self.collector()
        observation = self.base / 'observation.json'
        observation.write_text(json.dumps(self.observation(c.m)))
        local = self.base / 'local'
        local.write_bytes(b'abc')
        c.m['artifacts'][0]['source_url'] = str(local)
        # Narrow IO helpers are stubbed; real collect() dispatch and summary persistence run.
        recipes = self.base / 'tree'
        recipes.mkdir()
        recipe = recipes / 'Portfile'
        recipe.write_text('test recipe')
        c.m['tree']['root'] = str(recipes)
        c.m['artifacts'][0]['portfile_path'] = str(recipe)
        for name in ['ports-tar', 'ports-tar-signature', 'ports-rmd160', 'portindex',
                'portindex-quick', 'portindex-signature', 'macports-key']:
            c.byid[name] = {'id': name, 'source_url': str(local)}
        index = self.base / 'index'
        index.write_text('<a href="sample-9.7.darwin_99.fake_arch.tbz2">sample</a>')
        expected = {'inventory': [], 'guard': ['host', 'paths', 'budget'],
            'compare-installed': ['payloads'], 'tree': ['source_url', 'size_bytes', 'sha256'],
            'wheel': ['source_url', 'size_bytes', 'sha256', 'wheel_lock_membership'],
            'archive-index': ['archive_candidates'], 'source-plan': ['recipe'],
            'r3': ['source_url', 'size_bytes', 'sha256'],
            'fetch': ['source_url', 'size_bytes', 'sha256'],
            'inspect': ['source_url', 'size_bytes', 'sha256']}
        c.m['artifacts'][0]['route'] = 'supplied local artifact'
        for mode in self.m['collector']['allowed_modes']:
            c.mode = mode
            with self.subTest(mode=mode), \
                    mock.patch.object(c, 'inventory', return_value={}), \
                    mock.patch.object(c, 'compare_installed', return_value='receipt'), \
                    mock.patch.object(c, 'check_file', return_value={}), \
                    mock.patch.object(c, 'archive_inventory', return_value='receipt'), \
                    mock.patch.object(c, 'wheel', return_value=expected['wheel']), \
                    mock.patch.object(c, 'download', return_value=index):
                if mode == 'guard':
                    # Guard input was captured before changing artifact/tree fixtures.
                    observation.write_text(json.dumps(self.observation(c.m)))
                result = c.collect(mode, str(observation) if mode == 'guard' else 'a')
                self.assertEqual(result['established'], expected[mode])
                self.assertEqual(set(result['remaining_open']), set(c.p['identity_fields']) - set(expected[mode]))
                self.assertEqual(result['status'], 'OBSERVATION-ONLY')
                self.assertNotIn('verified', result)
        self.assertEqual(len(list(c.receipts.glob('summary-*.jsonl'))), len(expected))

    def test_r1d_09_unreviewed_acquisition_refuses_before_writes_or_children(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        self.m['collector']['child_contract']['reviewed'] = False
        self.seal()
        path = self.base / 'manifest.json'
        path.write_text(json.dumps(self.m))
        for mode in ['fetch', 'wheel', 'archive-index', 'inspect']:
            with self.subTest(mode=mode), mock.patch.object(self.api.subprocess, 'Popen') as child:
                before = sorted(self.base.iterdir())
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
                    self.assertNotEqual(self.api.entrypoint([mode, '--entry', 'a', '--expected-anchor', 'none', '--expected-capture-sha256', self.capture_hash, '--bootstrap-bytes', str(len(self.capture) + 2), '--remaining-seconds', '37', '--m3-receipt-bytes', '0']), 0)
                child.assert_not_called()
                self.assertFalse(any(x.startswith('{') for x in stdout.getvalue().splitlines()))
                self.assertFalse(self.root.exists())
                self.assertEqual(sorted(self.base.iterdir()), before)
        # A derived inspect that would download its parent is also gated.
        self.m['artifacts'][0]['source_url'] = 'manifest:parent'
        self.m['artifacts'].append(dict(self.m['artifacts'][0], id='parent', source_url='https://example.invalid/a'))
        self.seal()
        with self.assertRaises(self.api.Refusal):
            self.construct(self.m, 'inspect', entry='a', runner=self.fake_run)
        self.assertFalse(self.root.exists())
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v9.json').read_text())
        self.assertIs(v4['collector']['child_contract']['reviewed'], False)




    def registration(self):
        return Path(self.m['collector']['registration_path'])

    def refused_resume(self):
        before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        clock = mock.Mock(side_effect=AssertionError('new clock during damaged resume'))
        with self.assertRaises(self.api.Refusal):
            self.construct(self.m, 'inventory', now=clock, monotonic=clock, runner=self.fake_run)
        clock.assert_not_called()
        self.assertEqual({str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}, before)

    def fresh_paths(self, label):
        self.root = self.base / ('retained-' + label)
        self.registration_root = self.base / ('registration-' + label)
        self.m['collector']['retained_dir'] = str(self.root)
        self.m['collector']['registration_path'] = str(self.registration_root / 'window.jsonl')
        self.m['collector']['admitted_write_roots'] = [str(self.root), str(self.install)]
        self.m['collector']['child_contract']['allowed_write_roots'] = [str(self.root)]
        self.m['host']['pool_map'] = {str(self.root): 'pool1', str(self.install): 'pool1'}

    def test_r1e_01_missing_renamed_emptied_replaced_root_refuses_without_clock(self):
        for kind in ['missing', 'renamed', 'empty', 'replaced']:
            with self.subTest(kind=kind):
                self.fresh_paths(kind)
                c = self.collector()
                c.inventory()
                c.close()
                registration = self.registration().read_bytes()
                parked = self.base / ('parked-' + kind)
                self.root.rename(parked)
                if kind in ['empty', 'replaced']:
                    self.root.mkdir(mode=0o700)
                if kind == 'replaced':
                    import shutil
                    for entry in parked.iterdir():
                        dest = self.root / entry.name
                        if entry.is_dir():
                            shutil.copytree(entry, dest)
                        else:
                            dest.write_bytes(entry.read_bytes())
                self.refused_resume()
                self.assertEqual(self.registration().read_bytes(), registration)
                if kind in ['missing', 'renamed']:
                    self.assertFalse(self.root.exists())

    def test_r1e_02_prior_receipt_integrity_and_registered_accounting(self):
        for kind in ['truncated', 'edited', 'deleted', 'added']:
            with self.subTest(kind=kind):
                self.fresh_paths(kind)
                c = self.collector()
                receipt = c.save('prior', {'immutable': 'value'})
                usage = c.usage()
                registered = receipt.read_bytes()
                if kind == 'truncated':
                    receipt.write_bytes(registered[:1])
                elif kind == 'edited':
                    receipt.write_bytes(registered.replace(b'value', b'other'))
                elif kind == 'deleted':
                    receipt.unlink()
                else:
                    (c.receipts / 'extra.json').write_bytes(b'{}')
                # Accounting authority does not shrink or grow with disk tampering.
                self.assertEqual(c.usage(), usage)
                c.close()
                self.refused_resume()

    def test_r1e_03_interrupted_initialization_and_append_boundaries_refuse(self):
        # Cut after every durable append operation and every exclusive receipt write.
        for cut in range(1, 12):
            with self.subTest(initialization_cut=cut):
                self.fresh_paths('init-%d' % cut)
                self.seal()
                original = self.api.Collector._syncdir
                calls = [0]
                def interrupted(c, path):
                    original(c, path)
                    calls[0] += 1
                    if calls[0] == cut:
                        raise OSError('simulated power loss')
                with mock.patch.object(self.api.Collector, '_syncdir', interrupted):
                    with self.assertRaises(OSError):
                        self.construct(self.m, 'inventory', now=lambda: self.clock[0], monotonic=lambda: self.mono[0])
                self.assertTrue(self.registration().exists() or self.registration_root.exists())
                self.refused_resume()
        for cut in range(1, 7):
            with self.subTest(append_cut=cut):
                self.fresh_paths('append-%d' % cut)
                c = self.collector()
                original = c._syncdir
                calls = [0]
                def interrupted(path):
                    original(path)
                    calls[0] += 1
                    if calls[0] == cut:
                        raise OSError('simulated append loss')
                with mock.patch.object(c, '_syncdir', side_effect=interrupted):
                    with self.assertRaises(OSError):
                        c.append_evidence('/evidence/child_contract_receipts', 'receipt')
                c.close()
                self.refused_resume()
        for kind in ['empty-ledger', 'registered-receipt-missing']:
            self.fresh_paths(kind)
            c = self.collector()
            if kind == 'empty-ledger':
                (self.root / 'evidence.jsonl').touch()
            else:
                c.save('missing', {}).unlink()
            c.close()
            self.refused_resume()

    def test_r1e_04_identity_errors_symlink_text_and_target_bytes(self):
        root = self.base / 'stdlib'
        root.mkdir()
        (root / 'regular').write_bytes(b'code')
        outside = self.base / 'outside-file'
        outside.write_bytes(b'first')
        link = root / 'link'
        link.symlink_to(outside)
        initial = self.api.stdlib_identity(root)
        outside.write_bytes(b'other')
        self.assertNotEqual(self.api.stdlib_identity(root)['sha256'], initial['sha256'])
        initial = self.api.stdlib_identity(root)
        link.unlink()
        link.symlink_to('../outside-file')
        self.assertNotEqual(self.api.stdlib_identity(root)['sha256'], initial['sha256'])
        (root / 'inside-dir').mkdir()
        (root / 'inside-dir' / 'child').write_bytes(b'child')
        (root / 'dir-link').symlink_to(root / 'inside-dir')
        self.api.stdlib_identity(root)
        (root / 'outside-dir').symlink_to(self.install)
        with self.assertRaises((OSError, ValueError)):
            self.api.stdlib_identity(root)
        (root / 'outside-dir').unlink()
        (root / 'dangling').symlink_to(self.base / 'absent')
        with self.assertRaises((OSError, ValueError)):
            self.api.stdlib_identity(root)
        (root / 'dangling').unlink()
        def denied(*args, **kwargs):
            kwargs['onerror'](PermissionError('unreadable subtree'))
            return iter(())
        with mock.patch.object(self.api.VERIFIED_PROBE['os'], 'walk', side_effect=denied):
            with self.assertRaises(PermissionError):
                self.api.stdlib_identity(root)
            with self.assertRaises(PermissionError):
                self.api.VERIFIED_PROBE['interpreter_identity']()
        self.assertIs(self.api.stdlib_identity, self.api.VERIFIED_PROBE['stdlib_identity'])

    def bundle(self, mode, *, members=None, request=None):
        if members is None:
            members = dict(self.api.VERIFIED_MEMBERS)
            # A fake identity function is a verified fixture member, never a mocked loader.
            members['identity'] = ('import json\ndef interpreter_identity(): return ' + repr(self.identity) + '\ndef stdlib_identity(directory=None): return interpreter_identity()["stdlib"]\n').encode()
        members = dict(members)
        members.setdefault('probe', self.api.encoded(self.identity))
        members.setdefault('capture', self.capture)
        request = dict(request or {'bootstrap_start_utc': '1970-01-01T00:16:40Z', 'collector_argv': []})
        request['stub_text'] = (HERE / 'r1j_stub.py').read_text()
        request['invoked_argv_prefix'] = [self.m['collector']['interpreter']['executable'], '-I', '-B', '-c', request['stub_text']]
        members['request'] = self.api.encoded(request)
        hashes = {k: hashlib.sha256(v).hexdigest() for k, v in members.items()}
        return members, hashes

    def stub_run(self, mode, members, hashes, cwd=None):
        self.assertTrue((HERE / 'r1j_stub.py').exists(), 'fixed stub missing')
        bundle = json.dumps({k: base64.b64encode(v).decode() for k, v in members.items()}).encode()
        result = subprocess.run(['/usr/bin/python3', '-I', '-B', '-c', (HERE / 'r1j_stub.py').read_text(), mode, json.dumps(hashes)],
            input=bundle+b'\nR1I-GO 30\n', cwd=str(cwd or self.base), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result.stdout = b'\n'.join(x for x in result.stdout.split(b'\n') if not x.startswith((b'R1I-READY ', b'R1I-LIVE')))
        return result

    def test_r1e_05_binder_checks_all_hashes_before_import_or_write(self):
        self.seal()
        members, hashes = self.bundle('bind')
        for name in ['manifest', 'collector', 'identity', 'binder']:
            bad = dict(hashes, **{name: '0' * 64})
            result = self.stub_run('bind', members, bad)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'SHA-256', result.stderr)
            self.assertFalse(self.root.exists())

    def test_r1e_06_binder_measures_identity_and_records_provenance(self):
        self.seal()
        members, hashes = self.bundle('bind')
        for field in self.identity:
            bad = copy.deepcopy(self.identity)
            bad[field] = 'different'
            changed = dict(members, probe=self.api.encoded(bad))
            pins = dict(hashes, probe=hashlib.sha256(changed['probe']).hexdigest())
            result = self.stub_run('bind', changed, pins)
            self.assertNotEqual(result.returncode, 0, field)
            self.assertEqual(result.stdout, b'')
        result = self.stub_run('bind', members, hashes)
        self.assertEqual(result.returncode, 0, result.stderr)
        capture = json.loads(result.stdout)
        m = json.loads(capture['bound_manifest_json'])
        p = m['binding_provenance']
        self.assertEqual(p['v8_sha256'], hashes['manifest'])
        self.assertEqual(p['binder_sha256'], hashes['binder'])
        self.assertEqual(m['collector']['interpreter']['identity'], self.identity)
        self.assertEqual(capture['binding_receipt']['input_sha256'], hashes)
        self.assertEqual(json.loads(capture['binding_receipt']['raw_probe_output']), self.identity)

    def test_r1e_07_binder_exclusive_durable_publication_preserves_v5(self):
        self.seal()
        before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        members, hashes = self.bundle('bind')
        for repeat in range(2):
            result = self.stub_run('bind', members, hashes)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}, before)
        c = self.collector()
        c.close()
        result = self.stub_run('bind', members, hashes)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'already exists', result.stderr)

    def test_r1e_08_only_bound_reviewed_core_and_provenance_accepted(self):
        self.seal()
        original = copy.deepcopy(self.m)
        mutations = [lambda m: m.pop('binding_provenance'),
            lambda m: m['budget'].update(clock_seconds=38),
            lambda m: m['binding_provenance'].update(v8_sha256='0' * 64),
            lambda m: m['binding_provenance'].update(binder_sha256='0' * 64),
            lambda m: m['collector'].update(retained_dir=str(self.base / 'alternate'))]
        for mutate in mutations:
            m = copy.deepcopy(original)
            mutate(m)
            # Forging both digest fields cannot change the reviewed source core.
            try:
                digest = self.api.core_digest(m)
                m['window_seal']['core_sha256'] = digest
                if 'binding_provenance' in m:
                    m['binding_provenance']['bound_core_sha256'] = digest
            except self.api.Refusal:
                pass
            clock = mock.Mock(side_effect=AssertionError('prebinding clock'))
            with self.assertRaises(self.api.Refusal):
                self.construct(m, 'inventory', now=clock, monotonic=clock)
            clock.assert_not_called()
            self.assertFalse(self.root.exists())
        unbound = json.loads(self.source_path.read_bytes())
        with self.assertRaises(self.api.Refusal):
            self.construct(unbound, 'inventory')
        c = self.construct(original, 'inventory', now=lambda: self.clock[0], monotonic=lambda: self.mono[0])
        c.close()

    def test_r1e_09_report_qualifies_lifecycle_and_host_acceptance(self):
        report = (HERE / 'r1j_report.md').read_text()
        self.assertLessEqual(len(report.splitlines()), 90)
        for item in ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'R1', 'R2', 'R3', 'R4', 'R5']:
            self.assertIn('| ' + item + ' |', report)
        for phrase in ['git-committed anchor is intact', 'Intel identity stays open', 'acquisition stays disabled', 'OBSERVATION-ONLY']:
            self.assertIn(phrase, report)

    def test_r1f_01_anchor_refuses_coordinated_rollback_and_rewrite(self):
        for damage in ['prefix', 'rewrite']:
            self.fresh_paths('anchor-' + damage)
            c = self.collector()
            saved_registration = self.registration().read_bytes()
            saved_files = self.snapshot()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                c.save('later', {'data': 'new'})
            expected = self.expected_anchor()
            line = out.getvalue().splitlines()[-1].split()
            self.assertEqual(line, ['R1H-ANCHOR', c.start['seal_sha256'], str(c.registry_seq), c.registry_head])
            c.close()
            if damage == 'prefix':
                self.registration().write_bytes(saved_registration)
                for p in self.root.rglob('*'):
                    if p.is_file() and str(p.relative_to(self.root)) not in saved_files:
                        p.unlink()
            else:
                rows = [json.loads(x) for x in self.registration().read_bytes().splitlines()]
                rows[0]['event']['start']['wall_start'] += 100
                start = self.api.encoded(rows[0]['event']['start'])
                (self.root / 'window.json').write_bytes(start)
                head = c.start['seal_sha256']
                chain = b''
                for row in rows:
                    event = row['event']
                    if event['kind'] == 'commit' and event['path'] == str(self.root / 'window.json'):
                        event.update(size=len(start), sha256=hashlib.sha256(start).hexdigest())
                    row['previous_sha256'] = head
                    data = self.api.encoded(row)
                    chain += data
                    head = hashlib.sha256(data).hexdigest()
                self.registration().write_bytes(chain)
            before = self.snapshot()
            clock = mock.Mock(side_effect=AssertionError('clock before anchor'))
            with self.assertRaisesRegex(self.api.Refusal, 'anchor'):
                self.construct(json.loads(json.loads(self.capture)['bound_manifest_json']), 'inventory', expected_anchor=expected, now=clock, monotonic=clock)
            clock.assert_not_called()
            self.assertEqual(self.snapshot(), before)
        self.fresh_paths('missing-anchor')
        self.seal()
        with self.assertRaisesRegex(self.api.Refusal, 'anchor'):
            self.api.Collector(self.capture, 'inventory', expected_capture_sha256=self.capture_hash, bootstrap_bytes=len(self.capture) + 2)
        self.assertFalse(self.root.exists())

    def test_r1f_02_final_verification_active_edit_and_same_inode_empty(self):
        for damage in ['active-edit', 'same-inode-empty']:
            self.fresh_paths(damage)
            c = self.collector()
            prior = c.save('prior', {'data': 'prior'})
            if damage == 'active-edit':
                original = c.inventory
                def collect_then_edit():
                    result = original()
                    prior.write_bytes(prior.read_bytes().replace(b'prior', b'other'))
                    return result
                with mock.patch.object(c, 'inventory', side_effect=collect_then_edit):
                    with self.assertRaises(self.api.Refusal):
                        c.collect('inventory')
            else:
                inode = self.root.stat().st_ino
                c.close()
                for path in self.root.iterdir():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                self.assertEqual(self.root.stat().st_ino, inode)
                self.refused_resume()

    def test_r1f_03_every_instrumented_write_boundary_refuses_restart(self):
        self.assertTrue(hasattr(self.api.Collector, '_boundary'), 'write boundaries uninstrumented')
        class PowerLoss(BaseException):
            pass
        trace = []
        self.fresh_paths('trace')
        self.seal()
        with mock.patch.object(self.api.Collector, '_boundary', lambda c, label: trace.append(label)):
            c = self.collector()
            c.append_evidence('/evidence/child_contract_receipts', 'receipt')
            c.save('stream', {'value': 'row'})
            with self.assertRaises(self.api.Refusal):
                c.halt('test stop')
            c.close()
        self.assertTrue(trace)
        self.boundaries = sorted(set(trace))
        for cut, label in enumerate(trace, 1):
            with self.subTest(cut=cut, label=label):
                self.fresh_paths('cut-%d' % cut)
                self.seal()
                calls = [0]
                def boundary(c, name):
                    calls[0] += 1
                    if calls[0] == cut:
                        raise PowerLoss(name)
                c = None
                stdout = io.StringIO()
                with mock.patch.object(self.api.Collector, '_boundary', boundary), contextlib.redirect_stdout(stdout):
                    with self.assertRaises(PowerLoss):
                        c = self.collector()
                        c.append_evidence('/evidence/child_contract_receipts', 'receipt')
                        c.save('stream', {'value': 'row'})
                        c.halt('test stop')
                if c is not None:
                    c.close()
                lines = [x.split() for x in stdout.getvalue().splitlines() if x.startswith('R1H-ANCHOR ')]
                anchor = ':'.join(lines[-1][2:]) if lines else 'none'
                before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
                clock = mock.Mock(side_effect=AssertionError('clock restarted'))
                with self.assertRaises(self.api.Refusal):
                    self.construct(self.m, 'inventory', expected_anchor=anchor, now=clock, monotonic=clock)
                clock.assert_not_called()
                self.assertEqual({str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}, before)

    def test_r1f_04_complete_publication_and_ledger_only_evidence(self):
        self.seal()
        original = copy.deepcopy(self.m)
        for mutate in [lambda m: m['authorization'].update(technical_review='manufactured'),
                lambda m: m['host'].update(pool_map={'fake': 'pool'}),
                lambda m: m['binding_provenance'].update(utc_time='2026-10-11T01:02:03Z'),
                lambda m: m['budget'].update(clock_seconds=38)]:
            m = copy.deepcopy(original)
            mutate(m)
            m['window_seal']['core_sha256'] = self.api.core_digest(m)
            m['binding_provenance']['bound_core_sha256'] = m['window_seal']['core_sha256']
            clock = mock.Mock(side_effect=AssertionError('clock before capture'))
            with self.assertRaisesRegex(self.api.Refusal, 'capture'):
                self.construct(m, 'inventory', now=clock, monotonic=clock)
            clock.assert_not_called()
            self.assertFalse(self.root.exists())
        with self.assertRaisesRegex(self.api.Refusal, 'capture'):
            self.api.Collector(self.capture, 'inventory', expected_anchor='none', bootstrap_bytes=0)
        c = self.collector()
        before = self.snapshot()
        c.m['host']['pool_map'] = {'outside': 'ledger'}
        with self.assertRaisesRegex(self.api.Refusal, 'Evidence'):
            c.collect('inventory')
        self.assertEqual(self.snapshot(), before)
        c.m['host']['pool_map'] = original['host']['pool_map']
        c.append_evidence('/host/pool_map', {'observed': 'ledger'})
        self.assertEqual(c.collect('inventory')['status'], 'OBSERVATION-ONLY')

        c.close()
        self.fresh_paths('active-ledger-delete')
        c = self.collector()
        c.append_evidence('/host/pool_map', {'observed': 'old'})
        (self.root / 'evidence.jsonl').unlink()
        for checkpoint in c.receipts.glob('evidence-head-*.json'):
            checkpoint.unlink()
        before = self.snapshot()
        with self.assertRaises(self.api.Refusal):
            c.append_evidence('/evidence/child_contract_receipts', 'new')
        self.assertEqual(self.snapshot(), before)

    def test_r1f_05_real_stub_verifies_before_compile_and_ignores_disk(self):
        self.seal()
        marker = self.base / 'marker'
        members, hashes = self.bundle('probe')
        members['identity'] = ('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\ndef interpreter_identity(): return {"safe": True}\n').encode()
        hashes['identity'] = hashlib.sha256(members['identity']).hexdigest()
        changed = dict(members, manifest=members['manifest'] + b' ')
        result = self.stub_run('probe', changed, hashes)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists(), 'unverified bundle executed a source')
        # Positive control: the same source does execute when every hash matches.
        result = self.stub_run('probe', members, hashes)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(marker.exists())
        marker.unlink()
        safe = b'def interpreter_identity(): return {"safe": True}\n'
        members['identity'] = safe
        hashes['identity'] = hashlib.sha256(safe).hexdigest()
        planted = self.base / 'r1j_identity_probe.py'
        planted.write_bytes(b'raise RuntimeError("planted source")')
        cache = self.base / '__pycache__'
        cache.mkdir()
        import py_compile
        py_compile.compile(str(planted), cfile=str(cache / ('r1j_identity_probe.cpython-%d%d.pyc' % sys.version_info[:2])), doraise=True)
        result = self.stub_run('probe', members, hashes)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'safe': True})
        planted.write_bytes(b'raise RuntimeError("replacement after bundling")')
        result = self.stub_run('probe', members, hashes)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())

    def test_r1f_06_bind_stream_leaves_fake_intel_tree_identical(self):
        self.seal()
        members, hashes = self.bundle('bind')
        def tree():
            return {str(p.relative_to(self.base)): (p.lstat().st_mode, p.read_bytes() if p.is_file() else None)
                for p in self.base.rglob('*')}
        before = tree()
        result = self.stub_run('bind', members, hashes)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(tree(), before)
        receipt = json.loads(result.stdout)['binding_receipt']
        for name in ['argv', 'hostname', 'uname', 'bootstrap_start_utc', 'input_sha256', 'raw_probe_output', 'bound_manifest_sha256']:
            self.assertIn(name, receipt)
        self.assertEqual(receipt['argv'][0], self.m['collector']['interpreter']['executable'])
        self.assertEqual(receipt['argv'][1:4], ['-I', '-B', '-c'])
        self.assertEqual(receipt['argv'][4], (HERE / 'r1j_stub.py').read_text())
        wrapper = (HERE / 'r1j_host_commands.sh').read_text()
        self.assertIn('set -C', wrapper)
        self.assertIn('bootstrap_start_utc=', wrapper)
        self.assertNotIn('scp ', wrapper)

    def test_r1f_07_bootstrap_start_and_bytes_are_charged(self):
        self.m['budget']['time_total_s'] = 36
        self.seal()
        self.clock[0] += self.m['budget'].get('time_total_s', self.m['budget']['clock_seconds']) + 1
        self.mono[0] += self.m['budget'].get('time_total_s', self.m['budget']['clock_seconds']) + 1
        with self.assertRaisesRegex(self.api.Refusal, 'deadline'):
            self.construct(self.m, 'inventory', now=lambda: self.clock[0], monotonic=lambda: self.mono[0])
        self.assertFalse(self.root.exists())
        self.clock[0] = 1005
        self.mono[0] = 2005
        c = self.collector()
        self.assertEqual(c.start['bootstrap_start_utc'], '1970-01-01T00:16:40Z')
        self.assertEqual(c.start['wall_start'], 1000)
        self.assertEqual(c.elapsed(), 5)
        self.assertGreaterEqual(c.usage()['receipt_bytes'], len(self.capture) + 2)
        self.assertEqual(json.loads(self.registration().read_bytes().splitlines()[0])['event']['start']['bootstrap_bytes'], len(self.capture) + 2)
        self.assertIn('bind and inventory must run back to back', (HERE / 'r1j_report.md').read_text())

    def test_r1f_08_direct_runtime_and_strict_realpath(self):
        self.seal()
        m = copy.deepcopy(self.m)
        m['collector']['interpreter']['executable'] = '/launcher-shim'
        # A coherent reseal still cannot pass the invoked/runtime realpath predicate.
        with self.assertRaisesRegex(self.api.Refusal, 'executable'):
            self.api.qualify_interpreter(m)
        v6 = json.loads((HERE / 'intel_provisioning_manifest_v9.json').read_text())
        self.assertEqual(v6['collector']['interpreter']['executable'], '/Library/Developer/CommandLineTools/usr/bin/python3')
        for text in [json.dumps(v6), (HERE / 'r1j_host_commands.sh').read_text()]:
            self.assertNotIn('exec /usr/bin/python3', text)
            self.assertNotIn('/usr/bin/python3 -I -B results/', text)

    def test_r1f_09_report_states_independent_anchor_qualifier(self):
        report = (HERE / 'r1j_report.md').read_text()
        self.assertIn('R1 holds only while the git-committed anchor is intact', report)
        self.assertIn('carried-forward bootstrap', report)
        self.assertIn('independent authority', report)


    def maker(self):
        module = types.ModuleType('m3_maker')
        module.__file__ = str(HERE / 'r1j_make_bundle.py')
        exec(compile((HERE / 'r1j_make_bundle.py').read_bytes(), '<test:maker>', 'exec'), module.__dict__)
        module.HERE = self.base
        for name in ['collector', 'identity_probe', 'bind_manifest', 'stub']:
            shutil.copyfile(HERE/('r1j_' + name + '.py'), self.base/('r1j_' + name + '.py'))
        (self.base/'intel_provisioning_manifest_v9.json').write_bytes(self.source_path.read_bytes())
        module.real_exchange = module.exchange if hasattr(module, 'exchange') else None
        module.exchange = self.legacy_exchange(module)
        return module

    def dispatch_args(self, maker, anchor='none'):
        import argparse
        capture = self.base / 'r1j_bind_fixture.json'
        capture.write_bytes(self.capture)
        capture.with_suffix('.stderr').write_bytes(b'')
        capture.with_suffix('.exit').write_bytes(b'0\n')
        self.final_fixture(capture.with_suffix(''))
        return argparse.Namespace(mode='inventory', probe=None, capture=str(capture),
            expected_capture_sha256=self.capture_hash, expected_anchor=anchor,
            bootstrap_bytes=len(self.capture) + 2 + capture.with_suffix('.final').stat().st_size, bootstrap_start_utc=None,
            remaining_seconds=None, evidence_update=None, capture_prefix=None,
            ssh_argv=['ssh', '-T', 'fixture-host'])

    def git_fixture(self, maker, args, blobs=None):
        blobs = dict(blobs or {})
        for suffix in ('.json','.stderr','.exit','.final'):
            path = Path(args.capture).with_suffix(suffix)
            if path.exists(): blobs[str(path.relative_to(self.base))] = path.read_bytes()
        def call(argv, **kwargs):
            if argv[0] == 'git':
                key = argv[-1].removeprefix('HEAD:./') if hasattr(str, 'removeprefix') else argv[-1][7:]
                if key not in blobs:
                    return subprocess.CompletedProcess(argv, 1, b'', b'missing')
                return subprocess.CompletedProcess(argv, 0, b'' if '-e' in argv else blobs[key], b'')
            core = json.loads(json.loads(self.capture)['bound_manifest_json'])['window_seal']['core_sha256']
            kwargs['stdout'].write(('R1H-ANCHOR ' + core + ' 99 ' + 'b'*64 + '\n').encode())
            return subprocess.CompletedProcess(argv, 0, None, None)
        return call, blobs

    def test_r1h_01_pending_attempt_blocks_lost_output_and_interrupted_append(self):
        for interrupted in (False, True):
            self.fresh_paths('pending-' + str(interrupted))
            c = self.collector()
            anchor = self.expected_anchor()
            old_registration = self.registration().read_bytes()
            old_files = self.snapshot()
            c.close()
            maker = self.maker()
            args = self.dispatch_args(maker, anchor)
            previous = self.base / 'r1j_inventory_previous'
            line = ('R1H-ANCHOR %s %s %s\n' % (c.start['seal_sha256'], *anchor.split(':'))).encode()
            previous.with_suffix('.json').write_bytes(line)
            previous.with_suffix('.stderr').write_bytes(b'')
            previous.with_suffix('.exit').write_bytes(b'0\n')
            self.final_fixture(previous)
            prior = self.base / 'r1j_attempt_prior.json'
            prior.write_text(json.dumps({'capture_prefix':str(previous)}))
            git, blobs = self.git_fixture(maker, args, {str(x.relative_to(self.base)):x.read_bytes() for x in [prior, previous.with_suffix('.json'), previous.with_suffix('.stderr'), previous.with_suffix('.exit'), previous.with_suffix('.final')]})
            ssh_calls = []
            def transport(argv, **kwargs):
                if argv[0] == 'git':
                    return git(argv, **kwargs)
                ssh_calls.append(argv)
                active = self.collector()
                if interrupted:
                    real_open = Path.open
                    class InterruptedWriter:
                        def __init__(self, stream):
                            self.stream = stream
                        def __enter__(self):
                            self.stream.__enter__()
                            return self
                        def __exit__(self, *values):
                            return self.stream.__exit__(*values)
                        def write(self, data):
                            self.stream.write(data[:len(data)//2])
                            raise RuntimeError('interrupted mid-append')
                    def open_with_partial_write(path, *values, **options):
                        stream = real_open(path, *values, **options)
                        if path.name.startswith('unacknowledged-') and values and values[0] == 'xb':
                            return InterruptedWriter(stream)
                        return stream
                    with mock.patch.object(Path, 'open', new=open_with_partial_write):
                        with self.assertRaisesRegex(RuntimeError, 'mid-append'):
                            active.save('unacknowledged', {'append':'partial'})
                    partial = next(active.receipts.glob('unacknowledged-*')).read_bytes()
                    self.assertTrue(partial)
                    self.assertFalse(partial.endswith(b'\n'))
                else:
                    active.save('unacknowledged', {'append':'complete'})
                active.close()
                raise subprocess.TimeoutExpired(argv, 1)
            with mock.patch.object(maker.subprocess, 'run', side_effect=transport):
                self.assertNotEqual(maker.dispatch(args, now=lambda:1001), 0)
            self.assertEqual(len(ssh_calls), 1)
            records = [x for x in self.base.glob('r1j_attempt_*.json') if x != prior and json.loads(x.read_text()).get('anchor') == anchor]
            self.assertEqual(len(records), 1)
            # Lose transport output and restore the exact old Intel state A.
            prefix = Path(json.loads(records[0].read_text())['capture_prefix'])
            for suffix in ('.json', '.stderr', '.exit'):
                prefix.with_suffix(suffix).unlink()
            self.registration().write_bytes(old_registration)
            for path in self.root.rglob('*'):
                if path.is_file():
                    key = str(path.relative_to(self.root))
                    if key in old_files:
                        path.write_bytes(old_files[key])
                    else:
                        path.unlink()
            with mock.patch.object(maker.subprocess, 'run', side_effect=git) as calls:
                with self.assertRaisesRegex(ValueError, 'consumed|recovery'):
                    maker.dispatch(args, now=lambda:1002)
                self.assertFalse(any(x.args[0][0] == 'ssh' for x in calls.call_args_list))
            with self.assertRaises(FileExistsError):
                maker.exclusive_record(records[0], b'{}\n')

    def test_r1h_02_single_m3_clock_and_monotonic_remote_budget(self):
        budgets = []
        for skew in (-300, 300):
            self.fresh_paths('skew-' + str(skew))
            self.m['budget']['clock_seconds'] = 870
            self.seal()
            maker = self.maker()
            args = self.dispatch_args(maker)
            git, _ = self.git_fixture(maker, args)
            with mock.patch.object(maker.subprocess, 'run', side_effect=git) as calls:
                self.assertEqual(maker.dispatch(args, now=lambda:1600), 0)
            call = next(x for x in calls.call_args_list if x.args[0][0] == 'ssh')
            request = json.loads(base64.b64decode(json.loads(call.kwargs['input'])['request']))
            argv = request['collector_argv']
            self.assertEqual(float(argv[argv.index('--remaining-seconds') + 1]), args.remaining_seconds)
            budgets.append(args.remaining_seconds)
            self.assertLessEqual(args.remaining_seconds, 870 - 600 - 5)
            self.clock[0] = 1600 + skew
            self.mono[0] = 2000
            c = self.construct(self.m, 'inventory', now=lambda:self.clock[0], monotonic=lambda:self.mono[0],
                remaining_seconds=args.remaining_seconds, process_start=2000)
            self.assertEqual(c.remaining(), args.remaining_seconds)
            self.mono[0] += args.remaining_seconds + 1
            before = len(self.calls)
            with self.assertRaises(self.api.Refusal):
                c.download('https://example.invalid/a', 'a', 3)
            self.assertEqual(len(self.calls), before)
            with self.assertRaises(self.api.Refusal):
                c.save('late', {'too':'late'})
            self.assertFalse(list(c.receipts.glob('late-*')))
            c.close()
        self.assertEqual(budgets[0], budgets[1])
        self.fresh_paths('dispatch-expired')
        self.seal()
        maker = self.maker()
        args = self.dispatch_args(maker)
        git, _ = self.git_fixture(maker, args)
        with mock.patch.object(maker.subprocess, 'run', side_effect=git) as calls:
            with self.assertRaisesRegex(ValueError, 'deadline'):
                maker.dispatch(args, now=lambda:1870)
            self.assertFalse(any(x.args[0][0] == 'ssh' for x in calls.call_args_list))
        self.fresh_paths('m3-late')
        self.seal()
        maker = self.maker()
        args = self.dispatch_args(maker)
        git, _ = self.git_fixture(maker, args)
        times = iter([1001, 1002, 1871])
        with mock.patch.object(maker.subprocess, 'run', side_effect=git) as calls:
            self.assertNotEqual(maker.dispatch(args, now=lambda:next(times,1871)), 0)
        ssh = next(x for x in calls.call_args_list if x.args[0][0] == 'ssh')
        self.assertLessEqual(ssh.kwargs['timeout'], 868)
        self.assertNotEqual(Path(args.capture_prefix).with_suffix('.exit').read_bytes(), b'0\n')
        self.assertIn(b'deadline', Path(args.capture_prefix).with_suffix('.stderr').read_bytes())
        self.fresh_paths('m3-sync-late')
        self.seal()
        maker = self.maker()
        args = self.dispatch_args(maker)
        git, _ = self.git_fixture(maker, args)
        m3_now = [1001]
        real_syncdir = maker.syncdir
        def final_sync(path):
            real_syncdir(path)
            if args.capture_prefix is not None:
                status = Path(args.capture_prefix).with_suffix('.exit')
                if status.exists() and status.read_bytes() == b'0\n':
                    m3_now[0] = 1871
        with mock.patch.object(maker, 'syncdir', side_effect=final_sync), mock.patch.object(maker.subprocess, 'run', side_effect=git):
            self.assertNotEqual(maker.dispatch(args, now=lambda:m3_now[0]), 0)
        self.assertEqual(Path(args.capture_prefix).with_suffix('.exit').read_bytes(), b'0\n')
        self.assertFalse(Path(args.capture_prefix).with_suffix('.final').exists())

    def test_r1h_03_bind_capture_requires_committed_matching_bytes(self):
        for missing in (True, False):
            maker = self.maker()
            args = self.dispatch_args(maker)
            git, blobs = self.git_fixture(maker, args)
            key = str(Path(args.capture).relative_to(self.base))
            if missing:
                blobs.pop(key)
            else:
                blobs[key] = self.capture + b' '
            with mock.patch.object(maker.subprocess, 'run', side_effect=git) as calls:
                with self.assertRaisesRegex(ValueError, 'committed|Committed'):
                    maker.dispatch(args, now=lambda:1001)
                self.assertFalse(any(x.args[0][0] == 'ssh' for x in calls.call_args_list))
            self.assertFalse(list(self.base.glob('r1j_attempt_[0-9]*.json')))

    def test_r1h_04_v7_commands_have_full_arguments_and_direct_runtime(self):
        import shlex
        manifest = json.loads((HERE / 'intel_provisioning_manifest_v9.json').read_bytes())
        command = manifest['window_seal']['update_command']
        self.assertEqual(subprocess.run(['bash','-n'], input=command.encode(), capture_output=True).returncode, 0)
        words = shlex.split(command)
        i = words.index('inventory')
        self.assertEqual(len(words[i+1:]), 5)
        self.assertIn('r1j_host_commands.sh', words[1])
        self.assertEqual(manifest['budget']['transit_margin_seconds'], 5)
        def commands(value):
            if isinstance(value, dict):
                for k,v in value.items():
                    if 'command' in k and isinstance(v,str) and not v.startswith(('BLOCKED:', 'NEEDS-FETCH')):
                        yield v
                    else:
                        yield from commands(v)
            elif isinstance(value,list):
                for v in value:
                    yield from commands(v)
        for text in commands(manifest):
            if text.startswith('bash '):
                self.assertIn('r1j_', text)
            if 'python3 ' in text:
                self.assertIn('/Library/Developer/CommandLineTools/usr/bin/python3 -I -B', text)
        self.assertNotIn('r1f_', json.dumps(manifest))

    def test_r1h_05_every_wrapper_ssh_uses_explicit_identity(self):
        lines = [line for line in (HERE/'r1j_host_commands.sh').read_text().splitlines() if 'ssh -T' in line]
        self.assertTrue(lines)
        for line in lines:
            self.assertIn('-i ~/.ssh/intel_mac_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes', line)
        wrapper = (HERE/'r1j_host_commands.sh').read_text()
        self.assertIn('--dispatch-m3', wrapper)
        self.assertNotIn('| ssh ', wrapper)

    def test_r1h_06_report_states_intact_and_unconsumed_boundary(self):
        report = (HERE/'r1j_report.md').read_text()
        self.assertIn('intact and unconsumed', report)
        self.assertIn('exit-status file is outside the capture hash', report)
        self.assertIn('historical observation before the bootstrap start', report)
        self.assertIn('operator-reviewed recovery', report)

    def final_fixture(self, prefix, deadline=1870, qualified_at=1001):
        data = (json.dumps({'exit':0, 'qualified':True, 'm3_deadline':deadline,
            'm3_qualified_at':qualified_at}, sort_keys=True, allow_nan=False)+'\n').encode()
        prefix.with_suffix('.final').write_bytes(data)
        return data

    def legacy_exchange(self, maker):
        def exchange(args, remote, bundle, request_hash, deadline, margin, out, err, output_limit, now):
            args.remaining_seconds = deadline - now() - margin
            if args.remaining_seconds <= 0:
                return 124
            # Preserve carried transport instrumentation; never substitute a loader/stub.
            payload = json.loads(bundle)
            request = json.loads(base64.b64decode(payload['request']))
            request['collector_argv'] += ['--remaining-seconds', str(args.remaining_seconds)]
            payload['request'] = base64.b64encode(self.api.encoded(request)).decode()
            try:
                return maker.subprocess.run(args.ssh_argv+[remote], input=json.dumps(payload).encode(),
                    stdout=out, stderr=err, timeout=deadline-now()).returncode
            except subprocess.TimeoutExpired:
                err.write(b'REFUSED: M3 hard timeout\n')
                return 124
        return exchange

    @contextlib.contextmanager
    def local_transport(self, maker, git, *, extra=b'', ready=True, ready_delay=0):
        real_popen = subprocess.Popen
        processes = []
        script = ('import sys,json,base64,hashlib,time\n'
            'b=json.loads(sys.stdin.buffer.readline()); r=base64.b64decode(b["request"])\n'
            'time.sleep('+repr(ready_delay)+')\n'
            + ('print("R1I-READY "+hashlib.sha256(r).hexdigest(),flush=True)\n' if ready else '')
            + 'go=sys.stdin.buffer.readline()\n'
            'print("R1H-ANCHOR '+json.loads(json.loads(self.capture)['bound_manifest_json'])['window_seal']['core_sha256']+' 99 '+'b'*64+'",flush=True)\n'
            'sys.stdout.buffer.write('+repr(extra)+'); sys.stdout.buffer.flush()\n')
        def spawn(argv, **kwargs):
            self.assertEqual(argv[0], 'ssh')
            process = real_popen(['/usr/bin/python3','-I','-B','-c',script], **kwargs)
            processes.append(process)
            return process
        maker.exchange = maker.real_exchange
        with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker.subprocess,'Popen',side_effect=spawn):
            yield processes

    def test_r1i_01_zero_exit_without_final_refuses_consumption(self):
        for data in (None, b'{', b'{}\n'):
            self.fresh_paths('final-'+str(data))
            maker = self.maker(); args = self.dispatch_args(maker)
            path = Path(args.capture).with_suffix('.final')
            if data is None: path.unlink()
            else: path.write_bytes(data)
            git, _ = self.git_fixture(maker,args)
            with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker.subprocess,'Popen') as ssh:
                with self.assertRaises((ValueError,OSError)): maker.dispatch(args,now=lambda:1001)
                ssh.assert_not_called()

    def test_r1i_01_final_errors_and_post_sync_expiry_have_no_authority(self):
        for boundary in ('write','fsync','late','crash'):
            self.fresh_paths('terminal-'+boundary); self.seal()
            maker=self.maker(); args=self.dispatch_args(maker); git,blobs=self.git_fixture(maker,args)
            clock=[1001]; real_record=maker.exclusive_record; real_sync=maker.syncdir
            def record(path,data):
                if path.name.endswith('.final.pending') and boundary=='write':
                    path.write_bytes(data[:10]); raise OSError('final write failed')
                if path.name.endswith('.final.pending') and boundary=='fsync':
                    with mock.patch.object(maker.os,'fsync',side_effect=OSError('final fsync failed')):
                        real_record(path,data)
                else: real_record(path,data)
            def sync(path):
                real_sync(path)
                if boundary in ('late','crash') and args.capture_prefix and Path(args.capture_prefix).with_suffix('.exit').exists() and Path(args.capture_prefix).with_suffix('.exit').read_bytes()==b'0\n':
                    if boundary=='crash': raise RuntimeError('crash after durable exit')
                    clock[0]=1871
            with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker,'exclusive_record',side_effect=record), mock.patch.object(maker,'syncdir',side_effect=sync):
                if boundary=='late': self.assertNotEqual(maker.dispatch(args,now=lambda:clock[0]),0)
                elif boundary=='crash':
                    with self.assertRaisesRegex(RuntimeError,'durable exit'): maker.dispatch(args,now=lambda:clock[0])
                else:
                    with self.assertRaises(OSError): maker.dispatch(args,now=lambda:clock[0])
            prefix=Path(args.capture_prefix)
            self.assertEqual(prefix.with_suffix('.exit').read_bytes(),b'0\n')
            # Failed/partial final bytes are never committed authority.
            for path in self.base.glob('r1j_*'):
                if path.suffix in ('.json','.stderr','.exit','.final'): blobs[str(path.relative_to(self.base))]=path.read_bytes()
            with mock.patch.object(maker.subprocess,'run',side_effect=git):
                with self.assertRaises((ValueError,OSError)): maker.require_anchor('99:'+'b'*64,json.loads(json.loads(self.capture)['bound_manifest_json'])['window_seal']['core_sha256'])

    def test_r1i_01_attempt_durable_before_reservation_crash(self):
        maker=self.maker(); args=self.dispatch_args(maker); git,_=self.git_fixture(maker,args)
        real_record=maker.exclusive_record
        def crash(path,data):
            real_record(path,data)
            if 'attempt' in path.name: raise RuntimeError('crash after durable attempt')
        with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker,'exclusive_record',side_effect=crash), mock.patch.object(maker.subprocess,'Popen') as ssh:
            with self.assertRaisesRegex(RuntimeError,'durable attempt'): maker.dispatch(args,now=lambda:1001)
            ssh.assert_not_called()
        self.assertFalse(list(self.base.glob('r1j_inventory_*')))
        with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker.subprocess,'Popen') as ssh:
            with self.assertRaisesRegex(ValueError,'consumed'): maker.dispatch(args,now=lambda:1001)
            ssh.assert_not_called()

    def test_r1i_01_success_final_is_accepted_only_after_commit(self):
        maker=self.maker(); args=self.dispatch_args(maker); git,blobs=self.git_fixture(maker,args)
        with self.local_transport(maker,git): self.assertEqual(maker.dispatch(args,now=lambda:1001),0)
        prefix=Path(args.capture_prefix); final=json.loads(prefix.with_suffix('.final').read_bytes())
        self.assertEqual(set(final),{'exit','qualified','m3_deadline','m3_qualified_at'})
        self.assertEqual(final['exit'],0); self.assertIs(final['qualified'],True)
        self.assertLessEqual(final['m3_qualified_at'],final['m3_deadline'])
        with mock.patch.object(maker.subprocess,'run',side_effect=git):
            with self.assertRaises(ValueError): maker.require_anchor('99:'+'b'*64,json.loads(json.loads(self.capture)['bound_manifest_json'])['window_seal']['core_sha256'])
            for path in self.base.glob('r1j_*'):
                if path.suffix in ('.json','.stderr','.exit','.final'): blobs[str(path.relative_to(self.base))]=path.read_bytes()
            maker.require_anchor('99:'+'b'*64,json.loads(json.loads(self.capture)['bound_manifest_json'])['window_seal']['core_sha256'])
        self.assertTrue(prefix.with_suffix('.json').read_bytes().startswith(b'R1I-READY '))

    def test_r1i_02_delays_and_wall_skews_obey_round_trip_bound(self):
        for start_delay,go_delay in ((60,0),(0,60)):
            budgets=[]
            for skew in (-300,300):
                self.fresh_paths(str((start_delay,go_delay,skew))); self.m['budget']['clock_seconds']=870; self.seal()
                maker=self.maker(); args=self.dispatch_args(maker); git,_=self.git_fixture(maker,args)
                times=iter([1001,1001+start_delay+go_delay,1001+start_delay+go_delay,1001+start_delay+go_delay])
                with self.local_transport(maker,git): self.assertEqual(maker.dispatch(args,now=lambda:next(times,1001+start_delay+go_delay)),0)
                t0=1001+start_delay
                self.assertLessEqual(t0+args.remaining_seconds,1870-5)
                budgets.append(args.remaining_seconds)
                mono=[t0+go_delay]
                c=self.construct(self.m,'inventory',now=lambda:1001+skew,
                    monotonic=lambda:mono[0],remaining_seconds=args.remaining_seconds,process_start=t0)
                self.assertEqual(c.remaining(),args.remaining_seconds-go_delay)
                mono[0]=t0+args.remaining_seconds
                before=len(self.calls)
                with self.assertRaises(self.api.Refusal): c.download('https://example.invalid/a','a',3)
                self.assertEqual(len(self.calls),before)
                with self.assertRaises(self.api.Refusal): c.save('past-go-budget',{})
                self.assertFalse(list(c.receipts.glob('past-go-budget-*')))
                c.close()
            self.assertEqual(budgets[0],budgets[1])

    def start_real_stub(self):
        self.seal()
        members,hashes=self.bundle('inventory',request={'bootstrap_start_utc':'1970-01-01T00:16:40Z','collector_argv':['inventory','--expected-anchor','none','--expected-capture-sha256',self.capture_hash,'--bootstrap-bytes',str(len(self.capture)+2),'--m3-receipt-bytes','0']})
        # Retain a valid bound capture for the verified fake identity member, so
        # disconnection tests cannot pass on an unrelated provenance refusal.
        bound=copy.deepcopy(self.m)
        bound['binding_provenance']['identity_probe_sha256']=hashes['identity']
        members['capture']=self.publication(bound)
        hashes['capture']=hashlib.sha256(members['capture']).hexdigest()
        request=json.loads(members['request'])
        argv=request['collector_argv']
        argv[argv.index('--expected-capture-sha256')+1]=hashes['capture']
        argv[argv.index('--bootstrap-bytes')+1]=str(len(members['capture'])+2)
        members['request']=self.api.encoded(request)
        hashes['request']=hashlib.sha256(members['request']).hexdigest()
        proc=subprocess.Popen(['/usr/bin/python3','-I','-B','-c',(HERE/'r1j_stub.py').read_text(),'inventory',json.dumps(hashes)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(self.base))
        self.addCleanup(lambda: proc.poll() is None and proc.kill())
        proc.stdin.write(json.dumps({k:base64.b64encode(v).decode() for k,v in members.items()}).encode()+b'\n'); proc.stdin.flush()
        import select
        self.assertTrue(select.select([proc.stdout],[],[],3)[0], 'READY absent within fixture cap')
        line=proc.stdout.readline()
        self.assertEqual(line,b'R1I-READY '+hashes['request'].encode()+b'\n')
        return proc

    def test_r1i_02_real_stub_no_go_eof_malformed_cap_and_disconnect(self):
        for action in ('eof','malformed','cap','stdout','stdin-after-go'):
            self.fresh_paths('stub-'+action)
            proc=self.start_real_stub()
            if action=='stdout':
                proc.stdout.close(); proc.stdin.write(b'R1I-GO 30\n'); proc.stdin.flush()
            elif action=='stdin-after-go':
                proc.stdin.write(b'R1I-GO 30\n'); proc.stdin.flush(); proc.stdin.close()
            elif action=='malformed': proc.stdin.write(b'R1I-GO nope\n'); proc.stdin.flush()
            elif action=='eof': proc.stdin.close()
            # Cap uses the real two-second fake-manifest limit, no GO.
            proc.wait(timeout=5)
            self.assertNotEqual(proc.returncode,0)
            self.assertFalse(self.root.exists()); self.assertFalse(self.registration_root.exists())
            if not proc.stdin.closed: proc.stdin.close()
            if not proc.stdout.closed: proc.stdout.close()
            error=proc.stderr.read()
            if action in ('stdout','stdin-after-go'): self.assertIn(b'disconnected',error)
            proc.stderr.close()

    def test_r1i_02_expired_go_kills_transport(self):
        maker=self.maker(); args=self.dispatch_args(maker); git,_=self.git_fixture(maker,args)
        times=iter([1001,1870,1870,1870])
        with self.local_transport(maker,git) as processes: self.assertNotEqual(maker.dispatch(args,now=lambda:next(times,1871)),0)
        self.assertNotEqual(processes[0].returncode,0)
        self.assertFalse(Path(args.capture_prefix).with_suffix('.final').exists())

    def test_r1i_03_disk_accounting_failed_receipts_and_admission(self):
        maker=self.maker(); args=self.dispatch_args(maker); git,_=self.git_fixture(maker,args)
        failed=self.base/'r1j_inventory_failed.stderr'; failed.write_bytes(b'x'*60000)
        source=json.loads(self.source_path.read_bytes())
        expected=sum(x.stat().st_size for x in self.base.iterdir() if x.name.startswith(('r1j_bind_','r1j_inventory_','r1j_attempt_')) and x.suffix in ('.json','.stderr','.exit','.final'))
        self.assertEqual(maker.receipt_usage(source),expected)
        with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker.subprocess,'Popen') as ssh:
            with self.assertRaisesRegex(ValueError,'receipt'): maker.dispatch(args,now=lambda:1001)
            ssh.assert_not_called()
        self.assertEqual(failed.stat().st_size,60000)

    def test_r1i_03_output_bound_retains_failed_capture(self):
        maker=self.maker(); args=self.dispatch_args(maker); git,_=self.git_fixture(maker,args)
        with self.local_transport(maker,git,extra=b'x'*30000): self.assertNotEqual(maker.dispatch(args,now=lambda:1001),0)
        prefix=Path(args.capture_prefix)
        for suffix in ('.json','.stderr','.exit'): self.assertTrue(prefix.with_suffix(suffix).exists())
        self.assertFalse(prefix.with_suffix('.final').exists())
        self.assertNotEqual(prefix.with_suffix('.exit').read_bytes(),b'0\n')
        self.assertLessEqual(sum(x.stat().st_size for x in self.base.glob('r1j_inventory_*'))+sum(x.stat().st_size for x in self.base.glob('r1j_attempt_*')),20000)
        self.assertGreater(maker.receipt_usage(json.loads(self.source_path.read_bytes())),args.bootstrap_bytes)

    def test_r1i_04_sealed_margin_changes_go_budget_exactly(self):
        budgets=[]
        for margin in (5,11):
            self.fresh_paths('margin-'+str(margin)); self.m['budget']['transit_margin_seconds']=margin; self.seal()
            maker=self.maker(); args=self.dispatch_args(maker); git,_=self.git_fixture(maker,args)
            with self.local_transport(maker,git): self.assertEqual(maker.dispatch(args,now=lambda:1001),0)
            budgets.append(args.remaining_seconds)
        self.assertEqual(budgets[0]-budgets[1],6)
        tree=ast.parse((HERE/'r1j_make_bundle.py').read_text())
        self.assertFalse(any(isinstance(x,ast.Constant) and type(x.value) in (int,float) and x.value==5 for x in ast.walk(tree)))

    def test_r1i_05_probe_bytes_identical(self):
        self.assertEqual(hashlib.sha256((HERE/'r1j_identity_probe.py').read_bytes()).hexdigest(),hashlib.sha256((HERE/'r1h_identity_probe.py').read_bytes()).hexdigest())

    def test_r1i_06_report_round_trip_bound_and_same_window(self):
        report=(HERE/'r1j_report.md').read_text()
        for text in ('T0 + budget <= GO-send time + budget = deadline - margin','clock-rate drift','100 ppm','original 870 s window','separately reviewed recovery','.final','F1','F6','R1','R4'):
            self.assertIn(text,report)


    def r1j_commit_survivors(self, blobs):
        for path in self.base.glob('r1j_*'):
            if path.is_file():
                blobs[str(path.relative_to(self.base))] = path.read_bytes()

    def test_r1j_01_pending_failure_bytes_refuse_all_consumers(self):
        class Crash(BaseException):
            pass
        for mode in ('bind', 'inventory'):
            for boundary in ('crash-before-fsync', 'file-fsync', 'dir-before-link', 'late', 'marker-fails'):
                with self.subTest(mode=mode, boundary=boundary):
                    self.fresh_paths(mode + boundary); self.seal()
                    maker=self.maker(); args=self.dispatch_args(maker); git,blobs=self.git_fixture(maker,args)
                    core=json.loads(json.loads(self.capture)['bound_manifest_json'])['window_seal']['core_sha256']
                    if mode=='bind':
                        args.mode='bind'; args.capture=None; args.expected_anchor=None
                        args.bootstrap_start_utc='1970-01-01T00:16:40Z'
                        args.probe=str(self.base/'probe.json'); Path(args.probe).write_bytes(self.api.encoded(self.identity))
                        args.capture_prefix=str(self.base/('r1j_bind_failure_'+boundary))
                    def transport(a,remote,bundle,pin,deadline,margin,out,err,limit,now):
                        out.write(self.capture if mode=='bind' else ('R1H-ANCHOR '+core+' 99 '+'b'*64+'\n').encode())
                        return 0
                    maker.exchange=transport
                    real_record=maker.exclusive_record; real_sync=maker.syncdir; real_fdopen=maker.os.fdopen
                    clock=[1001]
                    def record(path,data):
                        if path.name.endswith('.final.pending'):
                            if boundary=='crash-before-fsync':
                                fd=os.open(str(path),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
                                with real_fdopen(fd,'wb') as stream: stream.write(data); stream.flush()
                                raise Crash('complete pending before fsync')
                            if boundary in ('file-fsync','marker-fails'):
                                with mock.patch.object(maker.os,'fsync',side_effect=OSError('pending fsync')):
                                    return real_record(path,data)
                        return real_record(path,data)
                    def sync(path):
                        pending=Path(args.capture_prefix).with_suffix('.final.pending') if args.capture_prefix else None
                        if pending is not None and pending.exists() and not pending.with_suffix('').exists():
                            if boundary=='dir-before-link': raise OSError('directory before link')
                            if boundary=='late': clock[0]=1871
                        return real_sync(path)
                    class Stream:
                        def __init__(self, stream): self.stream=stream
                        def __getattr__(self, name): return getattr(self.stream,name)
                        def __enter__(self): return self
                        def __exit__(self,*args): return self.stream.__exit__(*args)
                        def write(self,data):
                            if b'final receipt persistence failed' in data: raise OSError('marker write failed')
                            return self.stream.write(data)
                    def fdopen(*a,**kw):
                        stream=real_fdopen(*a,**kw)
                        return Stream(stream) if boundary=='marker-fails' else stream
                    with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker,'exclusive_record',side_effect=record), mock.patch.object(maker,'syncdir',side_effect=sync), mock.patch.object(maker.os,'fdopen',side_effect=fdopen):
                        if boundary=='late': self.assertNotEqual(maker.dispatch(args,now=lambda:clock[0]),0)
                        else:
                            with self.assertRaises(Crash if boundary=='crash-before-fsync' else OSError):
                                maker.dispatch(args,now=lambda:clock[0])
                    prefix=Path(args.capture_prefix)
                    self.assertTrue(prefix.with_suffix('.final.pending').exists())
                    self.assertFalse(prefix.with_suffix('.final').exists())
                    self.assertEqual(prefix.with_suffix('.exit').read_bytes(),b'0\n')
                    self.r1j_commit_survivors(blobs)
                    before={str(p):p.read_bytes() for p in self.base.glob('r1j_*') if p.is_file()}
                    with mock.patch.object(maker.subprocess,'run',side_effect=git), mock.patch.object(maker.subprocess,'Popen') as ssh:
                        with self.assertRaises((ValueError,OSError)): maker.qualified(prefix,committed=True)
                        with self.assertRaises((ValueError,OSError)): maker.require_anchor('99:'+'b'*64,core)
                        args.mode='inventory'
                        if mode=='bind':
                            args.capture=str(prefix.with_suffix('.json')); args.expected_capture_sha256=hashlib.sha256(Path(args.capture).read_bytes()).hexdigest()
                            args.expected_anchor='none'; args.bootstrap_bytes=1
                        else: args.expected_anchor='99:'+'b'*64
                        with self.assertRaises((ValueError,OSError)): maker.dispatch(args,now=lambda:1001)
                        ssh.assert_not_called()
                    self.assertEqual(before,{str(p):p.read_bytes() for p in self.base.glob('r1j_*') if p.is_file()})

    def test_r1j_01_durable_pending_link_order_success_and_post_link_failure(self):
        for fail in (False,True):
            self.fresh_paths('link-'+str(fail)); self.seal()
            maker=self.maker(); args=self.dispatch_args(maker); git,blobs=self.git_fixture(maker,args)
            real_record=maker.exclusive_record; real_sync=maker.syncdir; real_link=maker.os.link
            events=[]; saved={}
            def record(path,data):
                real_record(path,data)
                if path.name.endswith('.final.pending'): events.append('pending-durable'); saved['pending']=data
            def link(src,dst):
                self.assertEqual(events,['pending-durable','fresh-clock'])
                self.assertEqual(Path(src).read_bytes(),saved['pending'])
                self.assertFalse(Path(dst).exists()); real_link(src,dst); events.append('link')
            def sync(path):
                if events and events[-1]=='link':
                    if fail: raise OSError('directory after link')
                    events.append('published-directory-durable')
                real_sync(path)
            def now():
                if events==['pending-durable']: events.append('fresh-clock')
                return 1001
            with mock.patch.object(maker,'exclusive_record',side_effect=record), mock.patch.object(maker.os,'link',side_effect=link), mock.patch.object(maker,'syncdir',side_effect=sync), self.local_transport(maker,git):
                if fail:
                    with self.assertRaisesRegex(OSError,'after link'): maker.dispatch(args,now=now)
                else: self.assertEqual(maker.dispatch(args,now=now),0)
            prefix=Path(args.capture_prefix)
            self.assertEqual(prefix.with_suffix('.exit').read_bytes(),b'0\n')
            self.assertEqual(prefix.with_suffix('.final').read_bytes(),saved['pending'])
            self.assertEqual(prefix.with_suffix('.final.pending').read_bytes(),saved['pending'])
            self.assertEqual(prefix.with_suffix('.final').stat().st_ino,prefix.with_suffix('.final.pending').stat().st_ino)
            self.r1j_commit_survivors(blobs)
            # Post-link directory error deliberately narrows the guarantee: durable
            # content can qualify if an operator commits it; publication exited nonzero.
            with mock.patch.object(maker.subprocess,'run',side_effect=git):
                maker.require_anchor('99:'+'b'*64,json.loads(json.loads(self.capture)['bound_manifest_json'])['window_seal']['core_sha256'])

    def r1j_real_bind(self, small_budget):
        import datetime, time
        self.m['budget']['clock_seconds']=870; self.m['budget']['time_total_s']=870
        start=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        deadline=datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp()+870
        self.m['budget']['transit_margin_seconds']=deadline-time.time()-0.3 if small_budget else 5
        self.seal(); maker=self.maker(); maker.RUNTIME=self.identity['executable']; args=self.dispatch_args(maker)
        args.mode='bind'; args.capture=None; args.expected_anchor=None; args.bootstrap_start_utc=start
        args.capture_prefix=str(self.base/'r1j_bind_real')
        args.probe=str(self.base/'probe.json'); Path(args.probe).write_bytes(self.api.encoded(self.identity))
        # Verified fixture identity uses real elapsed time and CPU work. The actual
        # stub, compiler, binder and collector are unmodified, unmocked members.
        identity=('import time,hashlib\n'
            'def stdlib_identity(directory=None):\n'
            '    end=time.monotonic()+0.6\n'
            '    while time.monotonic()<end:\n'
            '        hashlib.sha256(b"entry"*100).digest()\n'
            '    return '+repr(self.identity['stdlib'])+'\n'
            'def interpreter_identity():\n'
            '    value='+repr(self.identity)+'\n'
            '    value["stdlib"]=stdlib_identity()\n'
            '    return value\n').encode()
        (self.base/'r1j_identity_probe.py').write_bytes(identity)
        real_popen=subprocess.Popen
        def spawn(argv,**kw):
            self.assertEqual(argv[0],'ssh')
            words=shlex.split(argv[-1]); self.assertEqual(words[1:4],['-I','-B','-c'])
            return real_popen(['/usr/bin/python3']+words[1:],cwd=str(self.base),**kw)
        maker.exchange=maker.real_exchange
        with mock.patch.object(maker.subprocess,'Popen',side_effect=spawn): rc=maker.dispatch(args)
        self.assertLess(time.time(),deadline, 'M3 deadline reached; wrong failure boundary')
        return maker,args,rc

    def test_r1j_02_real_stub_bind_crosses_cutoff_during_identity(self):
        maker,args,rc=self.r1j_real_bind(True)
        self.assertNotEqual(rc,0)
        prefix=Path(args.capture_prefix)
        self.assertIn(b'cutoff',prefix.with_suffix('.stderr').read_bytes())
        self.assertNotIn(b'bound_manifest_json',prefix.with_suffix('.json').read_bytes())
        self.assertFalse(prefix.with_suffix('.final').exists())
        self.assertFalse(self.root.exists()); self.assertFalse(self.registration_root.exists())

    def test_r1j_02_real_stub_bind_ample_budget_success(self):
        maker,args,rc=self.r1j_real_bind(False)
        self.assertEqual(rc,0,Path(args.capture_prefix).with_suffix('.stderr').read_bytes())
        raw=maker.publication(Path(args.capture_prefix).with_suffix('.json').read_bytes())
        self.assertEqual(json.loads(raw['bound_manifest_json'])['collector']['interpreter']['identity'],self.identity)
        maker.qualified(Path(args.capture_prefix))
        self.assertFalse(self.root.exists()); self.assertFalse(self.registration_root.exists())

    def test_r1j_02_cutoff_immediately_before_success_publish(self):
        self.seal(); members,hashes=self.bundle('bind')
        probe={}; exec(compile(members['identity'],'<fixture:identity>','exec'),probe)
        collector={'VERIFIED_PROBE':probe}; exec(compile(members['collector'],'<fixture:collector>','exec'),collector)
        binder={'VERIFIED_COLLECTOR':collector,'VERIFIED_PROBE':probe,'VERIFIED_MEMBERS':members,
            'VERIFIED_HASHES':hashes,'STUB_TEXT':json.loads(members['request'])['stub_text'],'INTEL_CUTOFF':30}
        exec(compile(members['binder'],'<fixture:binder>','exec'),binder)
        clock=[1]; binder['time']=types.SimpleNamespace(monotonic=lambda:clock[0])
        real_dumps=json.dumps
        def dumps(value,*a,**kw):
            result=real_dumps(value,*a,**kw)
            if isinstance(value,dict) and 'bound_manifest_json' in value: clock[0]=31
            return result
        out=io.StringIO(); err=io.StringIO()
        with mock.patch.object(json,'dumps',side_effect=dumps), contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
            rc=binder['entrypoint']()
        self.assertNotEqual(rc,0); self.assertEqual(out.getvalue(),''); self.assertIn('cutoff',err.getvalue())

    def test_r1j_03_pending_bytes_and_v9_commands_and_probe_pin(self):
        self.seal(); maker=self.maker(); manifest=json.loads((HERE/'intel_provisioning_manifest_v9.json').read_bytes())
        for label in ('bind','inventory'):
            path=self.base/('r1j_'+label+'_failed.final.pending'); path.write_bytes(b'x'*1234)
        fixture=json.loads(self.source_path.read_bytes())
        fixture['budget']['m3_receipt_patterns']=manifest['budget']['m3_receipt_patterns']
        self.assertEqual(maker.receipt_usage(fixture),2468)
        self.assertEqual(hashlib.sha256((HERE/'r1j_identity_probe.py').read_bytes()).digest(),hashlib.sha256((HERE/'r1i_identity_probe.py').read_bytes()).digest())
        self.assertNotIn('r1i_',json.dumps(manifest))
        self.assertIn('/Library/Developer/CommandLineTools/usr/bin/python3 -I -B',json.dumps(manifest))
        result=subprocess.run(['bash','-n',str(HERE/'r1j_host_commands.sh')],capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_r1j_04_report_publish_cutoff_same_window_and_coverage(self):
        report=(HERE/'r1j_report.md').read_text()
        for text in ('durable pending bytes','os.link','in-binding cutoff','original 870 s window',
                'post-link directory-fsync','S:36','blocking I/O','remote process lifetime',
                'assertions, not proof a run passed','Could it pass with a relevant defect remaining?',
                'capture + .final + hash committed','attempt','OBSERVATION-ONLY'):
            self.assertIn(text,report)
        self.assertNotIn('HANDOFF',report)

if __name__ == '__main__':
    unittest.main()
