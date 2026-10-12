"""P1/P7 fixture acceptance. No network, real SRC scan, or science launch."""
import ast
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import runpy
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
CLT = '/Library/Developer/CommandLineTools/usr/bin/python3'
EXCLUDES = REPO / 'tools/backup_mirror.excludes'


class Fixture(unittest.TestCase):
    def setUp(self):
        self.assertTrue((REPO / 'tools/memit_intel_copy.py').is_file(), 'P1 controller absent')
        self.assertTrue((REPO / 'tools/memit_intel_receive.py').is_file(), 'P1 receiver absent')
        self.C = importlib.import_module('tools.memit_intel_copy')
        self.R = importlib.import_module('tools.memit_intel_receive')
        # Intentionally keep fixtures: builder has no deletion authority.
        self.base = Path(tempfile.mkdtemp(prefix='ic1-', dir=str(REPO / 'results/intel_memit_copy_20261012')))
        self.src = self.base / 'source'
        self.src.mkdir()
        self.home = self.base / 'intel'
        self.home.mkdir()
        self.root = self.home / 'memit_copy'
        self.records = self.base / 'records'
        self.events = []
        self.runner = self.C.NativeRunner(gate=lambda: {'ok': True}, policy=[], poll=0.01, stop_timeout=0.05, log=self.events.append)
        remote = self.base / 'remote.sh'
        remote.write_text('#!/bin/sh\nexport HOME=' + str(self.home) + '\ncd "$HOME" || exit 3\nshift\nexec /bin/sh -c "$*"\n')
        remote.chmod(0o755)
        self.controller = self.C.Controller(self.src, self.records, 'g1', [str(remote), 'fixture'], self.runner)
        real_inventory = self.controller.remote_inventory
        def fixture_inventory():
            result = real_inventory()
            result['free_bytes'] = 500_000_000_000
            return result
        self.controller.remote_inventory = fixture_inventory
        self.now = time.time_ns()

    def file(self, path, data=b'fixture', age=601):
        p = self.src / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        ns = self.now - int(age * 10**9)
        os.utime(p, ns=(ns, ns))
        return p

    def build(self, paths=None):
        return self.controller.manifest(paths_from=paths, started_ns=self.now)

    def test_population_every_exclude(self):
        excluded = ['.deleted/a', '.last_success', '.DS_Store', 'deep/.DS_Store',
                    '.cache/a', 'deep/.cache/a', '.ipynb_checkpoints/a', '__pycache__/a',
                    'tmp/a', 'graft/a', 'arhugula-persistent-memory/.claude/worktrees/x/a',
                    'arhugula-persistent-memory/graft/a', '.intel_copy_state/a',
                    '.hf_token', 'deep/.hf_token', 'x/.git/objects/tmp_obj_1',
                    'x/.git/objects/pack/tmp_obj_2', 'x/.git/objects/aa/bb/tmp_obj_3']
        for name in excluded:
            self.file(name)
        self.file('keep/a')
        manifest = self.build()
        self.assertEqual([r['path'] for r in manifest['entries']], ['keep/a'])
        self.assertIn('deep/.hf_token', manifest['credentials'])

    def test_recent_boundary(self):
        for name, age in [('at', 600), ('inside', 599.999999999), ('outside', 600.000000001)]:
            self.file(name, age=age)
        entries = self.build()['entries']
        self.assertEqual({r['path'] for r in entries}, {'at', 'outside'})

    def test_symlinks_are_recorded_without_following(self):
        self.file('a')
        p = self.src / 'link'
        p.symlink_to('../outside/missing')
        os.utime(p, ns=(self.now - 601 * 10**9,) * 2, follow_symlinks=False)
        m = self.build()
        row = next(r for r in m['entries'] if r['path'] == 'link')
        self.assertEqual(row['target'], '../outside/missing')
        self.assertEqual(row['kind'], 'symlink')
        receipt = self.controller.run()
        self.assertEqual(receipt['status'], 'COMPLETE')
        self.assertEqual(os.readlink(self.root / 'generations/g1/tree/link'), '../outside/missing')

    def test_credential_names_quarantined_and_reported(self):
        for name in ['id_ed25519', 'nested/.env', 'credentials.json', 'token.txt', 'secret.pem']:
            self.file(name)
        m = self.build()
        self.assertEqual(m['entries'], [])
        self.assertEqual(len(m['credentials']), 5)

    def test_paths_from_subset_and_escape_refused(self):
        self.file('a'); self.file('b')
        selected = self.base / 'paths'
        selected.write_text('a\n')
        self.assertEqual([r['path'] for r in self.build(selected)['entries']], ['a'])
        selected.write_text('../outside\n')
        with self.assertRaises(ValueError):
            self.build(selected)

    def test_manifest_json_round_trip(self):
        self.file('strange\nname', b'abc')
        m = self.build()
        loaded = self.C.read_manifest(self.controller.manifest_path)
        self.assertEqual(loaded, m['entries'])
        self.assertEqual(m['manifest_sha256'], hashlib.sha256(self.controller.manifest_path.read_bytes()).hexdigest())
        self.assertEqual(m['bytes'], 3)

    def test_duplicate_digest_sent_once_and_hardlinked(self):
        self.file('a', b'same'); self.file('dir/b', b'same')
        receipt = self.controller.run(started_ns=self.now)
        tree = self.root / 'generations/g1/tree'
        self.assertEqual(receipt['status'], 'COMPLETE')
        self.assertEqual(receipt['paths'], 2)
        self.assertEqual(receipt['sent_objects'], 1)
        self.assertEqual((tree / 'a').stat().st_ino, (tree / 'dir/b').stat().st_ino)
        self.assertEqual(len(list((self.root / 'objects/sha256').iterdir())), 1)
        self.assertEqual(stat.S_IMODE((tree / 'a').stat().st_mode), 0o444)
        self.assertEqual(json.loads(self.controller.receipt_path.read_text()), receipt)

    def test_held_digest_not_sent_again(self):
        self.file('a')
        self.controller.run(started_ns=self.now)
        second = self.C.Controller(self.src, self.records, 'g2', self.controller.remote, self.runner)
        real_inventory = second.remote_inventory
        second.remote_inventory = lambda: dict(real_inventory(), free_bytes=500_000_000_000)
        self.assertEqual(second.run(started_ns=self.now)['sent_objects'], 0)

    def test_killed_hash_resumes_from_completed_cache(self):
        self.file('a'); self.file('b', b'other')
        original = self.runner.run
        def die_on_b(cmd, **kwargs):
            if cmd[0] == '/sbin/sha256sum' and cmd[-1].endswith('/b'):
                raise KeyboardInterrupt('killed hash')
            return original(cmd, **kwargs)
        with mock.patch.object(self.runner, 'run', side_effect=die_on_b):
            with self.assertRaises(KeyboardInterrupt):
                self.build()
        calls = []
        def track(cmd, **kwargs):
            calls.append(cmd)
            return original(cmd, **kwargs)
        with mock.patch.object(self.runner, 'run', side_effect=track):
            self.build()
        self.assertEqual([Path(c[-1]).name for c in calls if c[0] == '/sbin/sha256sum'], ['b'])

    def test_killed_transfer_resumes_same_generation_with_partial_dir(self):
        self.file('a', b'x' * 100000)
        original = self.runner.run
        seen = []
        def kill(cmd, **kwargs):
            if cmd[0] == '/opt/homebrew/bin/rsync' and str(self.src) + '/' in cmd:
                partial = self.root / 'incoming/g1/data/.partials/a'
                partial.parent.mkdir(parents=True, exist_ok=True)
                partial.write_bytes(b'x' * 1000)
                seen.append(cmd)
                raise KeyboardInterrupt('killed transfer')
            return original(cmd, **kwargs)
        with mock.patch.object(self.runner, 'run', side_effect=kill):
            with self.assertRaises(KeyboardInterrupt):
                self.controller.run(started_ns=self.now)
        self.assertIn('--partial-dir=.partials', seen[0])
        self.assertFalse((self.root / 'objects/sha256').exists())
        self.assertEqual(self.controller.run()['status'], 'COMPLETE')

    def test_source_changed_after_hash_is_incomplete(self):
        self.file('a'); self.build()
        (self.src / 'a').write_bytes(b'changed')
        receipt = self.controller.run()
        self.assertEqual(receipt['status'], 'INCOMPLETE')
        self.assertEqual(receipt['changed_paths'], ['a'])
        self.assertFalse((self.root / 'generations/g1/tree/a').exists())

    def test_corrupt_incoming_is_never_published(self):
        self.file('a'); self.build()
        self.controller.prepare_transfer()
        incoming = self.root / 'incoming/g1/data/a'
        incoming.parent.mkdir(parents=True, exist_ok=True)
        incoming.write_bytes(b'corrupt')
        with self.assertRaises(ValueError):
            self.R.verify(self.root, 'g1', self.controller.manifest_info['manifest_sha256'])
        self.assertFalse((self.root / 'objects/sha256' / hashlib.sha256(b'fixture').hexdigest()).exists())
        self.assertFalse((self.root / 'generations/g1/tree').exists())

    def test_manifest_digest_mismatch_refuses(self):
        self.file('a'); self.build(); self.controller.prepare_transfer()
        with self.assertRaises(ValueError):
            self.R.verify(self.root, 'g1', '0' * 64)

    def test_receiver_rejects_path_escape_and_symlink_ancestor(self):
        self.file('a'); self.build(); self.controller.prepare_transfer()
        folder = self.root / 'incoming/g1'
        rows = self.C.read_manifest(self.controller.manifest_path)
        for path in ['../escape', '/absolute', 'x/../escape']:
            rows[0]['path'] = path
            with gzip.open(folder / 'manifest.jsonl.gz', 'wt') as f:
                f.write(json.dumps(rows[0]) + '\n')
            digest = hashlib.sha256((folder / 'manifest.jsonl.gz').read_bytes()).hexdigest()
            with self.assertRaises(ValueError):
                self.R.verify(self.root, 'g1', digest)
        # A pre-existing recovery-area symlink cannot redirect a write.
        (folder / 'data').rename(folder / 'data_saved')
        (folder / 'data').symlink_to(self.src, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.R.verify(self.root, 'g1', digest)

    def test_budget_recovery_cap_boundaries(self):
        for delta, allowed in [(-1, True), (0, True), (1, False)]:
            measure = self.C.budget(250_000_000_000 - 7 + delta, 200_000_000_000, 7)
            self.assertEqual(measure['ok'], allowed)

    def test_budget_free_floor_boundaries(self):
        floor = 80_000_000_000 + 20 * 1024**3
        for delta, allowed in [(-1, False), (0, True), (1, True)]:
            self.assertEqual(self.C.budget(0, floor + 7 + delta, 7)['ok'], allowed)

    def test_refusal_sends_zero_payload_and_records_measurements(self):
        self.file('a')
        with mock.patch.object(self.controller, 'remote_inventory', return_value={'digests': [], 'recovery_bytes': 250_000_000_000, 'free_bytes': 0}):
            with self.assertRaises(ValueError):
                self.controller.run(started_ns=self.now)
        self.assertFalse(self.root.exists())
        receipt = json.loads(self.controller.receipt_path.read_text())
        self.assertEqual(receipt['phase'], 'budget')
        self.assertIn('traceback', receipt)
        self.assertFalse(receipt['budget']['ok'])
        self.assertTrue(self.controller.manifest_path.exists())

    def test_empty_inventory_fails_closed(self):
        self.file('a')
        with mock.patch.object(self.controller, 'remote_inventory', return_value={}):
            with self.assertRaises((ValueError, KeyError)):
                self.controller.run(started_ns=self.now)
        self.assertFalse(self.root.exists())

    def test_source_mutation_during_verify_marks_both_receipts_incomplete(self):
        self.file('a')
        original = self.controller.remote_script
        def mutate(mode, *args):
            receipt = original(mode, *args)
            if mode == 'verify' and receipt['status'] == 'COMPLETE':
                (self.src / 'a').write_bytes(b'late mutation')
            return receipt
        with mock.patch.object(self.controller, 'remote_script', side_effect=mutate):
            receipt = self.controller.run(started_ns=self.now)
        self.assertEqual(receipt['status'], 'INCOMPLETE')
        self.assertEqual(receipt['changed_paths'], ['a'])
        self.assertEqual(json.loads((self.root / 'generations/g1/receipt.json').read_text())['status'], 'INCOMPLETE')

    def test_unreachable_verify_is_not_retried_even_with_source_mutation(self):
        self.file('a')
        original = self.controller.remote_script
        calls = []
        def unreachable(mode, *args):
            if mode == 'verify':
                calls.append(mode)
                (self.src / 'a').write_bytes(b'changed')
                raise subprocess.CalledProcessError(255, ['fixture'], output=b'', stderr=b'unreachable')
            return original(mode, *args)
        with mock.patch.object(self.controller, 'remote_script', side_effect=unreachable):
            with self.assertRaises(subprocess.CalledProcessError):
                self.controller.run(started_ns=self.now)
        self.assertEqual(calls, ['verify'])

    def test_changed_digest_representative_does_not_halt_unchanged_duplicate(self):
        self.file('a', b'same'); self.file('b', b'same')
        self.build()
        original = self.controller.rsync
        def mutate(sources, destination, files_from=None):
            result = original(sources, destination, files_from)
            if files_from is not None:
                (self.src / 'a').write_bytes(b'changed')
                (self.root / 'incoming/g1/data/a').write_bytes(b'changed')
            return result
        with mock.patch.object(self.controller, 'rsync', side_effect=mutate):
            receipt = self.controller.run()
        self.assertEqual(receipt['status'], 'INCOMPLETE')
        self.assertEqual(receipt['changed_paths'], ['a'])
        self.assertIn('b', receipt['missing_paths'])

    def test_state_symlink_refused_before_write(self):
        other = self.base / 'other_source'
        other.mkdir()
        (other / '.intel_copy_state').symlink_to(self.src, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.C.Controller(other, self.records, 'bad', self.controller.remote, self.runner)

    def test_manifest_halt_saves_partial_cache_and_traceback(self):
        self.file('a'); self.file('b', b'other')
        original = self.runner.run
        def kill(cmd, **kwargs):
            if cmd[0] == '/sbin/sha256sum' and cmd[-1].endswith('/b'):
                raise KeyboardInterrupt('hash interrupted')
            return original(cmd, **kwargs)
        with mock.patch.object(self.runner, 'run', side_effect=kill):
            with self.assertRaises(KeyboardInterrupt):
                self.controller.manifest(started_ns=self.now)
        receipt = json.loads(self.controller.receipt_path.read_text())
        self.assertEqual(receipt['phase'], 'manifest')
        self.assertIn('KeyboardInterrupt', receipt['traceback'])

    def test_excess_records_refused_with_limit_measurements(self):
        self.file('a')
        with mock.patch.object(self.C, 'RECORD_CAP', 65536):
            with self.assertRaises(ValueError):
                self.controller.run(started_ns=self.now)
        receipt = json.loads(self.controller.receipt_path.read_text())
        self.assertIn('record_budget', receipt)
        self.assertGreater(receipt['record_budget']['projected_bytes'], receipt['record_budget']['cap_bytes'])

    def test_inventory_counts_hardlinks_once_and_df_fail_closed(self):
        self.root.mkdir()
        p = self.root / 'a'; p.write_bytes(b'a' * 1000)
        os.link(p, self.root / 'b')
        first = self.R.inventory(self.root)
        (self.root / 'b').rename(self.root / 'b_saved')
        self.assertEqual(first['recovery_bytes'], self.R.inventory(self.root)['recovery_bytes'])
        with mock.patch.object(self.R.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout='', stderr='')):
            with self.assertRaises(ValueError):
                self.R.inventory(self.root)

    def test_py39_syntax_and_executable_modes(self):
        for name in ['memit_intel_copy.py', 'memit_intel_receive.py']:
            p = REPO / 'tools' / name
            ast.parse(p.read_text(), feature_version=(3, 9))
            self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o755)

    def test_controller_suppresses_gate_import_bytecode_without_cli_flags(self):
        fake_repo = self.base / 'fake_repo'
        (fake_repo / 'tools').mkdir(parents=True)
        (fake_repo / 'tools/c10w_p2_gate.py').write_text('def check_gpu():\n    return {"ok": True}\n')
        previous = sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode = False
            namespace = runpy.run_path(str(REPO / 'tools/memit_intel_copy.py'))
            self.assertTrue(sys.dont_write_bytecode)
            namespace['check_gpu'].__globals__['REPO'] = fake_repo
            self.assertEqual(namespace['check_gpu'](), {'ok': True})
            self.assertFalse((fake_repo / 'tools/__pycache__').exists())
        finally:
            sys.dont_write_bytecode = previous


class Pause(unittest.TestCase):
    setUp = Fixture.setUp
    def test_two_clear_polls_required_and_failures_count_as_science(self):
        replies = iter([{'ok': False}, {'ok': True}, RuntimeError('failed check'), {'ok': True}, {'ok': True}])
        def gate():
            value = next(replies, {'ok': True})
            if isinstance(value, Exception):
                raise value
            return value
        runner = self.C.NativeRunner(gate=gate, policy=[], poll=0.001, log=self.events.append)
        self.assertEqual(runner.run(['/usr/bin/true']), b'')
        self.assertEqual([e['event'] for e in self.events], ['PAUSED', 'RESUMED'])
        self.assertEqual(self.events[-1]['clear_polls'], 2)

    def test_active_child_group_stops_on_first_science_poll_and_restarts(self):
        marker = self.base / 'marker'
        pidfile = self.base / 'child.pid'
        script = self.base / 'child.sh'
        script.write_text('#!/bin/sh\nif [ ! -f "' + str(marker) + '" ]; then\n  touch "' + str(marker) + '"\n  sleep 60 &\n  echo $! > "' + str(pidfile) + '"\n  wait\nfi\necho done\n')
        script.chmod(0o755)
        checks = []
        def gate():
            # Positive control: interrupt only once the native child is running.
            seen = pidfile.exists() and pidfile.stat().st_size > 0
            science = seen and not checks
            if science:
                checks.append(time.monotonic())
            return {'ok': not science}
        runner = self.C.NativeRunner(gate=gate, policy=[], poll=0.03, stop_timeout=0.1, log=self.events.append)
        start = time.monotonic()
        self.assertEqual(runner.run([str(script)]).strip(), b'done')
        self.assertLess(time.monotonic() - start, 1)
        pid = int(pidfile.read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)
        self.assertEqual([e['event'] for e in self.events], ['PAUSED', 'RESUMED'])

    def test_nonzero_native_failure_is_not_retried(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.runner.run(['/usr/bin/false'])


if __name__ == '__main__':
    unittest.main()
