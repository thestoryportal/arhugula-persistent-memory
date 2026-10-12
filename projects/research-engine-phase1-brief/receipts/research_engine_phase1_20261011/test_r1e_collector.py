"""Nine carried R1C tests plus nine R1D criteria; fake roots and child runners."""
import ast
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
SOURCE = HERE / 'r1e_collector.py'


def load_collector():
    if not SOURCE.exists():
        return None
    spec = importlib.util.spec_from_file_location('r1d', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
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
        self.m['collector']['interpreter'] = {
            'executable': '/fake/python3', 'flags': ['-I', '-B'],
            'minimum_version': [3, 9], 'identity': copy.deepcopy(self.identity)}
        self.m['budget']['components'].append({'id': 'receipts', 'bytes': 40000})
        self.m['budget']['planned_peak_bytes'] = 40030
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
            self.api.SOURCE_MANIFEST_PATH = source_path
            self.m['binding_provenance'] = {
                'v5_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
                'probe_file_sha256': hashlib.sha256(self.api.encoded(self.m['collector']['interpreter']['identity'])).hexdigest(),
                'probe_json': self.api.encoded(self.m['collector']['interpreter']['identity']).decode('utf-8'), 'binder_sha256': hashlib.sha256((HERE / 'r1e_bind_manifest.py').read_bytes()).hexdigest(),
                'collector_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                'identity_probe_sha256': hashlib.sha256((HERE / 'r1e_identity_probe.py').read_bytes()).hexdigest(),
                'utc_time': '2026-10-11T00:00:00Z',
                'bound_core_sha256': self.m['window_seal']['core_sha256']}


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
        c = self.api.Collector(self.m, mode, now=lambda: self.clock[0],
            monotonic=lambda: self.mono[0], runner=kwargs.pop('runner', self.fake_run), **kwargs)
        self.addCleanup(c.close)
        return c

    def observation(self):
        return {'host': copy.deepcopy(self.m['host']), 'tree': copy.deepcopy(self.m['tree']),
            'paths': copy.deepcopy(self.m['paths']), 'preinstalled_ports': [],
            'artifacts': {'a': dict(self.m['artifacts'][0], sha256=self.m['artifacts'][0]['expected_sha256'])},
            'projected_setup_peak_bytes': 40030, 'projected_provisioning_seconds': 17,
            'pools': [{'id': 'pool1', 'free_bytes': 100000, 'projected_peak_bytes': 40030}],
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
        v3 = json.loads((HERE / 'intel_provisioning_manifest_v5.json').read_text())
        for entry in v3['artifacts']:
            if entry['id'] in ['r3-controller', 'r3-workload', 'r3-review']:
                self.assertEqual(entry['route'], 'supplied local artifact')
        self.assertFalse(v3['authorization']['staging'])
        wrapper = (HERE / 'r1e_host_commands.sh').read_text()
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


    def test_r1d_01_core_seal_preserves_window_receipts_and_elapsed(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v5.json').read_text())
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
        self.m['host']['pool_map'] = {'observed': 'pool1'}
        self.m['explanation'] = 'This is outside the sealed core.'
        c = self.api.Collector(self.m, 'inventory', now=lambda: self.clock[0],
            monotonic=lambda: self.mono[0], runner=self.fake_run)
        self.addCleanup(c.close)
        self.assertEqual(c.start, start)
        self.assertEqual(c.elapsed(), 7)
        self.assertEqual(self.snapshot(), before)
        # A usable add-only update entry point preserves every prior receipt and clock.
        update = self.base / 'evidence-update.json'
        update.write_text(json.dumps({'slot': '/evidence/child_contract_receipts', 'value': 'review-pending'}))
        manifest_path = self.base / 'manifest.json'
        manifest_path.write_text(json.dumps(self.m))
        out = io.StringIO()
        with mock.patch.object(self.api, 'Collector', return_value=c), contextlib.redirect_stdout(out):
            self.assertEqual(self.api.entrypoint(['inventory', str(manifest_path), str(update)]), 0)
        self.assertEqual(c.evidence.get('/evidence/child_contract_receipts'), 'review-pending')
        self.assertEqual(len((self.root / 'evidence.jsonl').read_bytes().splitlines()), 2)
        for name, data in before.items():
            if name != 'evidence.jsonl':
                self.assertEqual((self.root / name).read_bytes(), data)
        self.assertEqual(c.start, start)
        self.assertEqual(json.loads(out.getvalue())['status'], 'OBSERVATION-ONLY')
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
                    self.api.Collector(self.m, 'inventory', runner=self.fake_run)
                self.assertEqual(self.snapshot(), before)
        self.m = copy.deepcopy(original)
        other = self.base / 'new-clock-forbidden'
        self.m['collector']['retained_dir'] = str(other)
        self.m['collector']['admitted_write_roots'].append(str(other))
        with self.assertRaises(self.api.Refusal):
            self.api.Collector(self.m, 'inventory', runner=self.fake_run)
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
                    self.api.Collector(self.m, 'inventory', runner=self.fake_run)
                self.assertEqual(self.snapshot(), before)
        ledger.write_bytes(original)
        # Even a manifest-authorized slot may not overlap the core.
        self.m['window_seal']['evidence_slots'].append('/collector/retained_dir')
        self.seal()
        with self.assertRaises(self.api.Refusal):
            self.api.Collector(self.m, 'inventory', runner=self.fake_run)

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
                self.api.Collector(self.m, 'inventory', now=clock, monotonic=clock, runner=self.fake_run)
            self.assertFalse(self.root.exists())
            clock.assert_not_called()
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v5.json').read_text())
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
            self.assertNotEqual(self.api.entrypoint(['inventory', str(manifest_path)]), 0)
        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(json.loads((c.receipts / 'failure.json').read_text())['status'], 'HALTED')
        self.assertEqual(len(list(c.receipts.glob('summary-*.jsonl'))), 1)

    def test_r1d_05_real_cumulative_command_deadline_retains_active_argv(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        c = self.collector()
        c.runner = c._execute
        self.m['collector']['child_contract']['sha256'] = 'a' * 64
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
        result = subprocess.run(['/usr/bin/python3', '-I', '-B', str(HERE / 'r1e_identity_probe.py')],
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
        self.assertIn('r1e_identity_probe.py', SOURCE.read_text())
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
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v5.json').read_text())
        line = next(x for x in (HERE / 'r1e_host_commands.sh').read_text().splitlines() if x.startswith('exec '))
        tokens = shlex.split(line)
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
            lambda: self.m['collector'].update(receipt_limit_bytes=40001),
            lambda: self.m['budget'].update(planned_peak_bytes=40031)]
        for change in changes:
            self.m = copy.deepcopy(original)
            change()
            self.seal()
            with self.assertRaises(self.api.Refusal):
                self.api.Collector(self.m, 'inventory', runner=self.fake_run)
            self.assertFalse(self.root.exists())
        receipts = [x['bytes'] for x in v4['budget']['components'] if x['id'] == 'receipts']
        self.assertEqual(receipts, [v4['collector']['receipt_limit_bytes']])

    def test_r1d_08_each_mode_entrypoint_established_and_open_partition(self):
        self.assertIsNotNone(self.api, 'R1D collector implementation is missing')
        c = self.collector()
        observation = self.base / 'observation.json'
        observation.write_text(json.dumps(self.observation()))
        local = self.base / 'local'
        local.write_bytes(b'abc')
        self.m['artifacts'][0]['source_url'] = str(local)
        # Narrow IO helpers are stubbed; real collect() dispatch and summary persistence run.
        recipes = self.base / 'tree'
        recipes.mkdir()
        recipe = recipes / 'Portfile'
        recipe.write_text('test recipe')
        self.m['tree']['root'] = str(recipes)
        self.m['artifacts'][0]['portfile_path'] = str(recipe)
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
        self.m['artifacts'][0]['route'] = 'supplied local artifact'
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
                    observation.write_text(json.dumps(self.observation()))
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
                    self.assertNotEqual(self.api.entrypoint([mode, str(path), 'a']), 0)
                child.assert_not_called()
                self.assertEqual(stdout.getvalue(), '')
                self.assertFalse(self.root.exists())
                self.assertEqual(sorted(self.base.iterdir()), before)
        # A derived inspect that would download its parent is also gated.
        self.m['artifacts'][0]['source_url'] = 'manifest:parent'
        self.m['artifacts'].append(dict(self.m['artifacts'][0], id='parent', source_url='https://example.invalid/a'))
        self.seal()
        with self.assertRaises(self.api.Refusal):
            self.api.Collector(self.m, 'inspect', entry='a', runner=self.fake_run)
        self.assertFalse(self.root.exists())
        v4 = json.loads((HERE / 'intel_provisioning_manifest_v5.json').read_text())
        self.assertIs(v4['collector']['child_contract']['reviewed'], False)




    def registration(self):
        return Path(self.m['collector']['registration_path'])

    def refused_resume(self):
        before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        clock = mock.Mock(side_effect=AssertionError('new clock during damaged resume'))
        with self.assertRaises(self.api.Refusal):
            self.api.Collector(self.m, 'inventory', now=clock, monotonic=clock, runner=self.fake_run)
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
                        self.api.Collector(self.m, 'inventory', now=lambda: self.clock[0], monotonic=lambda: self.mono[0])
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
        with mock.patch.object(self.api._identity_module.os, 'walk', side_effect=denied):
            with self.assertRaises(PermissionError):
                self.api.stdlib_identity(root)
            with self.assertRaises(PermissionError):
                self.api._identity_module.interpreter_identity()
        self.assertIs(self.api.stdlib_identity, self.api._identity_module.stdlib_identity)

    def binder_fixture(self):
        path = HERE / 'r1e_bind_manifest.py'
        self.assertTrue(path.exists(), 'binder missing')
        spec = importlib.util.spec_from_file_location('r1e_binder', path)
        binder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(binder)
        self.m['collector']['child_contract']['reviewed'] = False
        self.seal()
        probe = self.base / 'probe.json'
        probe.write_bytes(self.api.encoded(self.identity))
        bound = self.base / 'v5_bound.json'
        paths = [self.api.SOURCE_MANIFEST_PATH, SOURCE, HERE / 'r1e_identity_probe.py', probe, bound]
        hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths[:3]]
        return binder, paths, hashes

    def test_r1e_05_binder_checks_all_hashes_before_import_or_write(self):
        binder, paths, hashes = self.binder_fixture()
        for index in range(3):
            bad = hashes[:]
            bad[index] = '0' * 64
            before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
            with mock.patch.object(binder, '_load_verified') as loader:
                with self.assertRaises((ValueError, RuntimeError)):
                    binder.bind_manifest(*paths, *bad)
                loader.assert_not_called()
            self.assertEqual({str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}, before)

    def test_r1e_06_binder_measures_identity_and_records_provenance(self):
        binder, paths, hashes = self.binder_fixture()
        original = copy.deepcopy(self.identity)
        for field in original:
            bad = copy.deepcopy(original)
            bad[field] = 'different'
            paths[3].write_bytes(self.api.encoded(bad))
            with mock.patch.object(binder, '_load_verified', return_value=self.api):
                with self.assertRaises((ValueError, RuntimeError)):
                    binder.bind_manifest(*paths, *hashes)
            self.assertFalse(paths[4].exists())
        paths[3].write_bytes(self.api.encoded(original))
        with mock.patch.object(binder, '_load_verified', return_value=self.api):
            binder.bind_manifest(*paths, *hashes)
        p = json.loads(paths[4].read_bytes())['binding_provenance']
        self.assertEqual(p['v5_sha256'], hashes[0])
        self.assertEqual(p['probe_file_sha256'], hashlib.sha256(paths[3].read_bytes()).hexdigest())
        self.assertEqual(p['binder_sha256'], hashlib.sha256(Path(binder.__file__).read_bytes()).hexdigest())
        self.assertRegex(p['utc_time'], r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$')
        self.assertEqual(json.loads(paths[4].read_bytes())['collector']['interpreter']['identity'], original)

    def test_r1e_07_binder_exclusive_durable_publication_preserves_v5(self):
        binder, paths, hashes = self.binder_fixture()
        original = paths[0].read_bytes()
        real_fsync = os.fsync
        kinds = []
        def sync(fd):
            kinds.append(stat.S_IFMT(os.fstat(fd).st_mode))
            real_fsync(fd)
        out = io.StringIO()
        with mock.patch.object(binder, '_load_verified', return_value=self.api), mock.patch.object(binder.os, 'fsync', side_effect=sync), contextlib.redirect_stdout(out):
            binder.bind_manifest(*paths, *hashes)
        self.assertIn(stat.S_IFREG, kinds)
        self.assertIn(stat.S_IFDIR, kinds)
        data = paths[4].read_bytes()
        self.assertEqual(out.getvalue().strip(), hashlib.sha256(data).hexdigest())
        self.assertEqual(paths[0].read_bytes(), original)
        with mock.patch.object(binder, '_load_verified', return_value=self.api):
            with self.assertRaises((OSError, ValueError, RuntimeError)):
                binder.bind_manifest(*paths, *hashes)
        self.assertEqual(paths[4].read_bytes(), data)
        self.assertEqual(paths[0].read_bytes(), original)
        c = self.collector()
        c.close()
        paths[4].unlink()
        with mock.patch.object(binder, '_load_verified', return_value=self.api):
            with self.assertRaises((OSError, ValueError, RuntimeError)):
                binder.bind_manifest(*paths, *hashes)
        self.assertFalse(paths[4].exists())

    def test_r1e_08_only_bound_reviewed_core_and_provenance_accepted(self):
        self.seal()
        original = copy.deepcopy(self.m)
        mutations = [lambda m: m.pop('binding_provenance'),
            lambda m: m['budget'].update(clock_seconds=38),
            lambda m: m['binding_provenance'].update(v5_sha256='0' * 64),
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
                self.api.Collector(m, 'inventory', now=clock, monotonic=clock)
            clock.assert_not_called()
            self.assertFalse(self.root.exists())
        unbound = json.loads(self.api.SOURCE_MANIFEST_PATH.read_bytes())
        with self.assertRaises(self.api.Refusal):
            self.api.Collector(unbound, 'inventory')
        c = self.api.Collector(original, 'inventory', now=lambda: self.clock[0], monotonic=lambda: self.mono[0])
        c.close()

    def test_r1e_09_report_qualifies_lifecycle_and_host_acceptance(self):
        report = (HERE / 'r1e_report.md').read_text()
        self.assertLessEqual(len(report.splitlines()), 80)
        for line in report.splitlines():
            if 'never restarts' in line.lower():
                self.assertIn('only while the registration survives', line.lower())
        for item in ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'R1', 'R2', 'R3', 'R4']:
            self.assertIn('| ' + item + ' |', report)
        self.assertIn('R1 remains open', report)
        self.assertIn('identity completeness remains open', report)
        self.assertIn('R2 repaired', report)
        self.assertIn('acquisition and native acceptance remain unverified', report)


if __name__ == '__main__':
    unittest.main()
