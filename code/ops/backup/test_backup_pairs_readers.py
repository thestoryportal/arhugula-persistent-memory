"""T405: real readers, confined native-tool fixtures, no remote services."""
import contextlib
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from ops.intel import memit_intel_copy as intel

ROOT = Path(__file__).resolve().parents[3]
DRIVE = ROOT / 'code/ops/backup/backup_gdrive.sh'


class Readers(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(dir='/tmp')).resolve()
        self.addCleanup(shutil.rmtree, self.base)
        self.sources = [self.base / 'one', self.base / 'two']
        self.dests = [self.base / 'first', self.base / 'second']
        for i, source in enumerate(self.sources):
            source.mkdir()
            (source / 'payload').write_text(str(i))
            os.utime(source / 'payload', (1, 1))
        self.table = self.base / 'pairs.tsv'
        self.excludes = self.base / 'excludes'
        self.excludes.write_text('# fixture\n')
        self.calls = self.base / 'calls.jsonl'
        self.repo = self.base / 'repo'
        (self.repo / 'code/ops/backup').mkdir(parents=True)
        (self.repo / 'code/ops/intel').mkdir(parents=True)
        shutil.copy2(ROOT / 'code/ops/intel/memit_intel_receive.py', self.repo / 'code/ops/intel/memit_intel_receive.py')
        shutil.copy2(self.excludes, self.repo / 'code/ops/backup/backup_mirror.excludes')
        self.tool = self.base / 'native'
        self.tool.write_text('#!' + sys.executable + '\n' + NATIVE)
        self.tool.chmod(0o700)
        self.mount = self.base / 'mount'
        self.mount.write_text('#!/bin/sh\nprintf "fixture on /fixture (local)\\n"\n')
        self.mount.chmod(0o700)
        self.env = dict(os.environ)
        for name in list(self.env):
            if name.startswith(('BACKUP_', 'RCLONE_')):
                del self.env[name]
        self.env.update(BACKUP_PAIRS=str(self.table), BACKUP_SRC=str(self.sources[0]),
                        BACKUP_DEST=str(self.dests[0]), BACKUP_EXCLUDES=str(self.excludes),
                        BACKUP_RCLONE=str(self.tool), BACKUP_PYTHON=sys.executable,
                        BACKUP_MOUNT=str(self.mount), BACKUP_MOUNT_POINT='/fixture',
                        BACKUP_LOG=str(self.base / 'log'), BACKUP_LOCK_DIR=str(self.base / 'lock'),
                        BACKUP_HEARTBEAT=str(self.base / 'heartbeat'),
                        RCLONE_CONFIG=str(self.base / 'config'), HOME=str(self.base),
                        FIXTURE_ROOT=str(self.base))

    def pairs(self, reader, hold=False):
        destinations = [str(p) for p in self.dests]
        if reader == 'intel':
            destinations = ['fixture:' + p for p in destinations]
        if hold:
            destinations[1] = 'HOLD'
        self.table.write_text('reader\tsource\tdestination\texcludes\n' + ''.join(
            f'{reader}\t{s}\t{d}\texcludes\n' for s, d in zip(self.sources, destinations)))

    def preflight(self, path, seams):
        text = path.read_text()
        for seam in seams:
            self.assertTrue(seam in text, 'W7: reader missing fixture seam ' + seam)

    def recorded(self):
        return [json.loads(line) for line in self.calls.read_text().splitlines()] if self.calls.exists() else []

    def drive(self):
        self.preflight(DRIVE, [name for name in self.env if name.startswith('BACKUP_')])
        process = subprocess.Popen(['/bin/bash', str(DRIVE)], env=self.env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, start_new_session=True)
        def reap():
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
        self.addCleanup(reap)
        out, err = process.communicate(timeout=30)
        return process.returncode, out + err

    def copy(self, extra=(), remote=True):
        self.preflight(Path(intel.__file__), ['BACKUP_PAIRS', '--source', '--remote', '--records', 'runner='])
        runner = intel.NativeRunner(gate=lambda: {'ok': True}, policy=[str(self.tool)], poll=0.1)
        argv = ['memit_intel_copy', 'run', '--gen', 'fixture', '--records', str(self.base / 'records'), *extra]
        if remote:
            argv += ['--remote', shlex.join([str(self.tool), 'fixture'])]
        output = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), mock.patch.object(sys, 'argv', argv), \
                mock.patch.object(intel, 'REPO', self.repo), \
                mock.patch.object(intel, 'DEFAULT_REMOTE', [str(self.tool), 'default-host']), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = intel.main(runner=runner)
        return result, output.getvalue()

    def test_drive_both_sources(self):
        self.pairs('gdrive')
        self.env.update(SOURCES=str(self.sources[1]), DESTINATIONS=str(self.dests[1]),
                        RULES=str(self.excludes))
        status, output = self.drive()
        self.assertEqual(status, 0, output)
        calls = self.recorded()
        self.assertEqual([c[1:3] for c in calls], [[str(s) + '/', str(d) + '/'] for s, d in zip(self.sources, self.dests)])
        for call in calls:
            self.assertIn('--delete-after', call)
            self.assertIn('--dry-run=false', call)
            self.assertIn(str(self.excludes), call)
        self.assertEqual([(d / 'payload').read_text() for d in self.dests], ['0', '1'])
        logs = [c[c.index('--log-file') + 1] for c in calls]
        self.assertEqual(len(set(logs)), 2)
        self.assertTrue(all(Path(p).is_file() for p in logs))

    def test_drive_default_table_preserves_overrides(self):
        self.pairs('gdrive')
        folder = self.repo / 'code/ops/backup'
        for name in ('backup_gdrive.sh', 'backup_gdrive_status.py'):
            shutil.copy2(ROOT / 'code/ops/backup' / name, folder / name)
        shutil.copy2(self.table, folder / 'backup_pairs.tsv')
        del self.env['BACKUP_PAIRS']
        self.env.update(BACKUP_SRC=str(self.sources[1]), BACKUP_DEST=str(self.dests[1]))
        with mock.patch.dict(globals(), DRIVE=folder / 'backup_gdrive.sh'):
            status, output = self.drive()
        self.assertEqual(status, 0, output)
        self.assertEqual([c[1:3] for c in self.recorded()],
                         [[str(self.sources[1]) + '/', str(self.dests[1]) + '/']] * 2)

    def test_drive_final_row_without_newline(self):
        self.pairs('gdrive')
        self.table.write_text(self.table.read_text().rstrip('\n'))
        status, output = self.drive()
        self.assertEqual(status, 0, output)
        self.assertEqual(len(self.recorded()), 2)

    def test_drive_each_row_uses_its_excludes(self):
        self.pairs('gdrive')
        other = self.base / 'other-excludes'
        other.write_text('different\n')
        text = self.table.read_text()
        last = text.rfind('\texcludes\n')
        self.table.write_text(text[:last] + '\tother-excludes\n')
        status, output = self.drive()
        self.assertEqual(status, 0, output)
        self.assertEqual([c[c.index('--exclude-from') + 1] for c in self.recorded()],
                         [str(self.excludes), str(other)])

    def test_drive_malformed_known_row_refuses(self):
        self.table.write_text('reader\tsource\tdestination\texcludes\ngdrive\tonly-source\n')
        status, output = self.drive()
        self.assertNotEqual(status, 0)
        self.assertIn('invalid pair', output)
        self.assertEqual(self.recorded(), [])

    def test_drive_second_row_does_not_inherit_first_outcome(self):
        self.pairs('gdrive')
        wrapper = self.base / 'python-recorder'
        wrapper.write_text('#!' + sys.executable + '\nimport json,os,pathlib,sys\n'
                           'with (pathlib.Path(os.environ["FIXTURE_ROOT"])/"status-calls").open("a") as f:\n'
                           ' f.write(json.dumps(sys.argv[1:])+"\\n")\n'
                           'os.execv(sys.executable,[sys.executable,*sys.argv[1:]])\n')
        wrapper.chmod(0o700)
        self.env.update(BACKUP_PYTHON=str(wrapper), FIXTURE_DRIVE_WARNING='1')
        status, output = self.drive()
        self.assertEqual(status, 0, output)
        calls = [json.loads(line) for line in (self.base / 'status-calls').read_text().splitlines()]
        starts = [c for c in calls if 'record' in c and c[c.index('--phase') + 1] == 'start'
                  and c[c.index('--rclone-pid') + 1] != '0']
        self.assertEqual(len(starts), 2)
        self.assertEqual(starts[1][starts[1].index('--outcome-json') + 1], '')
        self.assertEqual(starts[1][starts[1].index('--rclone-exit-code') + 1], '0')
        final = json.loads((self.base / 'heartbeat').read_text())
        self.assertEqual(final['rclone_exit_code'], 0)

    def test_drive_missing_table_names_refusal(self):
        status, output = self.drive()
        self.assertNotEqual(status, 0)
        self.assertIn('pairs table missing: ' + str(self.table), output)
        self.assertEqual(self.recorded(), [])

    def test_drive_excludes_must_be_beside_table(self):
        self.pairs('gdrive')
        header, body = self.table.read_text().split('\n', 1)
        self.table.write_text(header + '\n' + body.replace('\texcludes\n', '\t../excludes\n'))
        status, output = self.drive()
        self.assertNotEqual(status, 0)
        self.assertIn('excludes must be next to table', output)
        self.assertEqual(self.recorded(), [])

    def test_drive_hold_second_before_any_sync(self):
        self.pairs('gdrive', hold=True)
        status, output = self.drive()
        self.assertNotEqual(status, 0)
        self.assertRegex(output, r'row 3[^\n]*Q5')
        self.assertEqual(self.recorded(), [])

    def test_intel_both_sources(self):
        self.pairs('intel')
        status, output = self.copy()
        self.assertEqual(status, 0, output)
        payloads = [c for c in self.recorded() if c[0] == 'payload']
        self.assertEqual([c[1] for c in payloads], [str(s) + '/' for s in self.sources])
        self.assertEqual([c[2].split('/incoming/')[0] for c in payloads], ['fixture:' + str(d) for d in self.dests])
        self.assertEqual([list(d.glob('incoming/*/data/payload'))[0].read_text() for d in self.dests], ['0', '1'])

    def test_intel_hold_second_before_any_copy(self):
        self.pairs('intel', hold=True)
        status, output = self.copy()
        self.assertNotEqual(status, 0)
        self.assertRegex(output, r'row 3[^\n]*Q6')
        self.assertEqual(self.recorded(), [])

    def test_intel_source_override_is_one_run(self):
        self.pairs('intel')
        status, output = self.copy(['--source', str(self.sources[1])])
        self.assertEqual(status, 0, output)
        self.assertEqual([c[1] for c in self.recorded() if c[0] == 'payload'], [str(self.sources[1]) + '/'])
        self.assertTrue((self.dests[0] / 'incoming/fixture/data/payload').exists())

    def test_intel_default_table_and_host(self):
        self.pairs('intel')
        target = self.repo / 'code/ops/backup/backup_pairs.tsv'
        shutil.copy2(self.table, target)
        shutil.copy2(self.excludes, target.parent / 'excludes')
        del self.env['BACKUP_PAIRS']
        status, output = self.copy(remote=False)
        self.assertEqual(status, 0, output)
        self.assertEqual(len([c for c in self.recorded() if c[0] == 'payload']), 2)

    def test_intel_failure_stops_later_rows(self):
        self.pairs('intel')
        self.env['FIXTURE_FAIL_COPY'] = '1'
        status, output = self.copy()
        self.assertEqual(status, 3, output)
        self.assertEqual(len([c for c in self.recorded() if c[0] == 'payload']), 1)

    def test_other_readers_do_not_dispatch_or_hold(self):
        self.pairs('ssd', hold=True)
        self.assertEqual(self.copy()[0], 0)
        self.assertEqual(self.drive()[0], 0)
        self.assertEqual(self.recorded(), [])

    def test_invalid_tables_refuse_before_dispatch(self):
        for reader in ('intel', 'gdrive'):
            for contents in ('', 'wrong\n', 'reader\tsource\tdestination\texcludes\nshort\n',
                             'reader\tsource\tdestination\texcludes\nunknown\ta\tb\tc\n'):
                with self.subTest(reader=reader, contents=contents):
                    self.table.write_text(contents)
                    status, output = self.copy() if reader == 'intel' else self.drive()
                    self.assertNotEqual(status, 0, output)
                    self.assertEqual(self.recorded(), [])

    def test_invalid_intel_destination_and_excludes(self):
        for destination, excludes in (('no-colon', 'excludes'), (':folder', 'excludes'),
                                      ('host:', 'excludes'), ('host:folder', '../escape')):
            with self.subTest(destination=destination, excludes=excludes):
                self.table.write_text('reader\tsource\tdestination\texcludes\n' +
                                      f'intel\t{self.sources[0]}\t{destination}\t{excludes}\n')
                self.assertNotEqual(self.copy()[0], 0)
                self.assertEqual(self.recorded(), [])

    def test_intel_table_symlink_refuses(self):
        self.pairs('intel')
        original = self.base / 'original'
        self.table.rename(original)
        self.table.symlink_to(original)
        self.assertNotEqual(self.copy()[0], 0)
        self.assertEqual(self.recorded(), [])

    def test_intel_table_excludes_apply(self):
        self.pairs('intel')
        self.excludes.write_text('payload\n')
        status, output = self.copy()
        self.assertEqual(status, 0, output)
        self.assertEqual([c for c in self.recorded() if c[0] == 'payload'], [])

    def test_intel_missing_table_is_named_refusal(self):
        status, output = self.copy()
        self.assertEqual(status, 3, output)
        self.assertIn(str(self.table), output)
        self.assertIn('ENOENT', output)
        self.assertEqual(self.recorded(), [])

    def test_intel_invalid_utf8_is_not_hidden(self):
        self.table.write_bytes(b'reader\tsource\tdestination\texcludes\nssd\t\xff\tdest\texcludes\n')
        with self.assertRaises(UnicodeDecodeError):
            self.copy()
        self.assertEqual(self.recorded(), [])

    def test_intel_direct_script_help_without_pythonpath(self):
        env = dict(self.env)
        env.pop('PYTHONPATH', None)
        result = subprocess.run([sys.executable, '-B', str(Path(intel.__file__)), '--help'],
                                cwd=self.base, env=env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--source', result.stdout)
        self.assertEqual(self.recorded(), [])

    def test_intel_default_excludes_still_apply_to_controller(self):
        (self.repo / 'code/ops/backup/backup_mirror.excludes').write_text('payload\n')
        self.preflight(Path(intel.__file__), ['BACKUP_PAIRS', '--source', '--records', 'runner='])
        runner = intel.NativeRunner(gate=lambda: {'ok': True}, policy=[str(self.tool)])
        with mock.patch.dict(os.environ, self.env, clear=True), mock.patch.object(intel, 'REPO', self.repo):
            controller = intel.Controller(self.sources[0], self.base / 'records', 'fixture',
                                          [str(self.tool), 'fixture'], runner)
            result = controller.manifest()
        self.assertEqual(result['entries'], [])

    def changed_source_receipt(self, stage):
        self.pairs('intel')
        self.env['FIXTURE_CHANGE'] = stage
        status, output = self.copy(['--source', str(self.sources[0])])
        self.assertEqual(status, 3, output)
        receipt = json.loads((self.base / 'records/fixture/receipt.json').read_text())
        self.assertEqual(receipt['status'], 'INCOMPLETE', output)
        control = json.loads((self.dests[0] / 'incoming/fixture/control.json').read_text())
        self.assertEqual(control['changed_paths'], ['payload'])

    def test_intel_control_after_payload_change(self):
        self.changed_source_receipt('payload')

    def test_intel_control_after_verify_error(self):
        self.changed_source_receipt('verify-error')

    def test_intel_control_after_verify_reply(self):
        self.changed_source_receipt('verify-reply')


NATIVE = r'''
import gzip, hashlib, json, os, pathlib, shlex, shutil, sys
root = pathlib.Path(os.environ['FIXTURE_ROOT']).resolve()
def path(value):
    p = pathlib.Path(value).resolve()
    if not p.is_relative_to(root):
        raise SystemExit('fixture refuses outside path: ' + value)
    return p
def record(value):
    with (root / 'calls.jsonl').open('a') as f:
        f.write(json.dumps(value) + '\n')
args = sys.argv[1:]
if args[0] == 'config':
    print('{}')
elif args[0] == 'version':
    print('rclone fixture')
elif args[0] == 'sync':
    source, dest = path(args[1]), path(args[2])
    path(args[args.index('--exclude-from') + 1])
    path(args[args.index('--backup-dir') + 1])
    log = path(args[args.index('--log-file') + 1])
    record(args)
    shutil.copytree(source, dest, dirs_exist_ok=True)
    if os.environ.get('FIXTURE_DRIVE_WARNING') and source.name == 'one':
        error = 'failed to open source object: lstat ' + str(source / 'lost.bin') + ': no such file or directory'
        records = [
            {'level':'error', 'msg':'Failed to copy: ' + error, 'object':'lost.bin', 'objectType':'*local.Object'},
            {'level':'error', 'msg':'not deleting files as there were IO errors'},
            {'level':'error', 'msg':'not deleting directories as there were IO errors'},
            {'level':'error', 'msg':'Attempt 1/1 failed with 1 errors and: ' + error},
            {'level':'notice', 'stats':{'bytes':1, 'errors':1, 'fatalError':False}},
            {'level':'notice', 'msg':'Failed to sync with 1 errors: ' + error}]
        log.write_text(''.join(json.dumps(r) + '\n' for r in records))
        raise SystemExit(1)
    log.write_text(json.dumps({'level': 'notice', 'msg': 'fixture', 'stats': {'bytes': 1, 'errors': 0, 'fatalError': False}}) + '\n')
elif args[0] == '/usr/bin/find':
    source = path(args[1])
    sys.stdout.buffer.write(b''.join(os.fsencode(p) + b'\0' for p in source.glob('payload')))
elif args[0] == '/usr/bin/stat':
    s = path(args[-1]).stat()
    print(s.st_size, s.st_mtime_ns // 10**9, s.st_ino)
elif args[0] == '/sbin/sha256sum':
    print(hashlib.sha256(path(args[-1]).read_bytes()).hexdigest(), args[-1])
elif args[0] == '/opt/homebrew/bin/rsync':
    sources = args[args.index('--') + 1:-1]
    dest = path(args[-1].split(':', 1)[1])
    if not dest.is_dir():
        raise SystemExit('fixture: remote destination was not prepared')
    for source in sources:
        src = path(source)
        if src.is_dir():
            record(['payload', source, args[-1]])
            if os.environ.get('FIXTURE_FAIL_COPY'):
                raise SystemExit(9)
            shutil.copy2(src / 'payload', dest / 'payload')
            if os.environ.get('FIXTURE_CHANGE') == 'payload':
                (src / 'payload').write_text('changed source')
        else:
            shutil.copy2(src, dest / src.name)
elif args[0] == str(root / 'native'):
    command = shlex.split(args[-1])
    if command[0] == 'mkdir':
        path(command[-1]).mkdir(parents=True, exist_ok=True)
    else:
        remote_root = path(command[command.index('--root') + 1])
        if 'inventory' in command:
            print(json.dumps({'digests': [], 'recovery_bytes': 0, 'free_bytes': 500000000000}))
        else:
            i = command.index('verify')
            gen, digest = command[i+1:i+3]
            manifest = remote_root / 'incoming' / gen / 'manifest.jsonl.gz'
            rows = [json.loads(line) for line in gzip.decompress(manifest.read_bytes()).splitlines()]
            marker = root / 'verification-started'
            mode = os.environ.get('FIXTURE_CHANGE')
            if mode in ('verify-error', 'verify-reply') and not marker.exists():
                marker.write_text('started')
                payload = next(json.loads(line) for line in (root / 'calls.jsonl').read_text().splitlines()
                               if json.loads(line)[0] == 'payload')
                (path(payload[1]) / 'payload').write_text('changed source')
                if mode == 'verify-error':
                    print(json.dumps({'error': 'object SHA-256 mismatch: payload'}))
                    raise SystemExit(3)
            control = json.loads((manifest.parent / 'control.json').read_text())
            status = 'INCOMPLETE' if control['changed_paths'] else 'COMPLETE'
            print(json.dumps({'gen': gen, 'manifest_sha256': digest, 'status': status, 'manifest_paths': len(rows), 'paths': len(rows)}))
else:
    raise SystemExit('fixture refuses unknown command: ' + repr(args))
'''
