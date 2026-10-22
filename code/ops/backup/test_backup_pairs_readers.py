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
from ops.backup import test_backup_gdrive as drive_checks

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'code/tests'))
import fault_kit
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

    def test_drive_fifth_field_refuses(self):
        self.pairs('gdrive')
        header, body = self.table.read_text().split('\n', 1)
        self.table.write_text(header + '\n' + body.replace('\texcludes\n', '\texcludes\tEXTRA\n'))
        status, output = self.drive()
        self.assertNotEqual(status, 0, output)
        self.assertIn('row 2: invalid pair', output)
        self.assertEqual(self.recorded(), [])

    def late_intel_move(self, leaf):
        self.pairs('intel')
        folder = self.base / 'unit'
        folder.mkdir()
        table = folder / 'pairs.tsv'
        header, body = self.table.read_text().split('\n', 1)
        table.write_text(header + '\n' + (body.replace('excludes\n', '-\n')
                                         if leaf == 'pairs.tsv' else body))
        (folder / 'excludes').write_text('# fixture\n')
        self.env['BACKUP_PAIRS'] = str(table)
        read = intel.fdsafe.read_named
        fired = []
        reads = []
        def moved(parent, name):
            data = read(parent, name)
            reads.append(name)
            if name == leaf and reads.count(leaf) == (2 if leaf == 'excludes' else 1):
                with fault_kit.rename_and_rebind('open', 1, folder) as fault:
                    fd = os.open(self.excludes, os.O_RDONLY)
                    os.close(fd)
                fired.append(fault.fired)
            return data
        with mock.patch.object(intel.fdsafe, 'read_named', moved):
            status, output = self.copy()
        self.assertEqual(fired, [1])
        self.assertNotEqual(status, 0, output)
        self.assertIn('is held at', output)
        self.assertEqual(self.recorded(), [])

    def test_intel_table_after_read_move_refuses(self):
        self.late_intel_move('pairs.tsv')

    def test_intel_excludes_after_read_move_refuses(self):
        self.late_intel_move('excludes')

    def test_intel_default_excludes_after_read_move_refuses(self):
        read = intel.fdsafe.read_named
        fired = []
        def moved(parent, name):
            data = read(parent, name)
            with fault_kit.rename_and_rebind('open', 1, Path(parent.path)) as fault:
                fd = os.open(self.excludes, os.O_RDONLY)
                os.close(fd)
            fired.append(fault.fired)
            return data
        runner = mock.Mock()
        with mock.patch.object(intel, 'REPO', self.repo), \
                mock.patch.object(intel.fdsafe, 'read_named', moved):
            with self.assertRaisesRegex(intel.fdsafe.Refusal, 'is held at'):
                intel.Controller(self.sources[0], self.base / 'records', 'legacy',
                                 ['fake', 'host'], runner)
        self.assertEqual(fired, [1])
        runner.run.assert_not_called()

    def test_selftest_owns_wrapper_table(self):
        self.pairs('gdrive')
        (self.repo / 'results').mkdir()
        tool = self.base / 'selftest-native'
        tool.write_text('#!' + sys.executable + '\n' + SELFTEST_NATIVE)
        tool.chmod(0o700)
        wrapper_envs = []
        def process(args, *, env=None, timeout=None):
            if args[0] == '/bin/bash':
                overrides = {k: self.env[k] for k in ('BACKUP_PYTHON', 'BACKUP_MOUNT',
                             'RCLONE_CONFIG', 'HOME', 'FIXTURE_ROOT')}
                overrides.update(BACKUP_RCLONE=str(tool), BACKUP_MOUNT_POINT='/fixture')
                actual = dict(env, **overrides)
                self.preflight(Path(args[1]), [k for k in actual if k.startswith('BACKUP_')])
                wrapper_envs.append(dict(env))
                return subprocess.run(args, env=actual, capture_output=True, text=True, timeout=10)
            if args[1] == 'cat':
                raise RuntimeError('fixture stops after first wrapper sync')
            self.assertIn(args[1], ('lsd', 'purge'))
            return subprocess.CompletedProcess(args, 0, '', '')
        temporary = tempfile.TemporaryDirectory
        def confined_temp(*args, **kwargs):
            return temporary(*args, **dict(kwargs, dir=self.base))
        unit = self.base / 'unit'
        unit.mkdir()
        unit_table = unit / 'pairs.tsv'
        unit_table.write_bytes(self.table.read_bytes())
        (unit / 'excludes').write_bytes(self.excludes.read_bytes())
        self.env['BACKUP_PAIRS'] = str(unit_table)
        with mock.patch.object(drive_checks, 'ROOT', self.repo), \
                mock.patch.object(drive_checks, 'run_process', side_effect=process), \
                mock.patch.object(tempfile, 'TemporaryDirectory', side_effect=confined_temp), \
                mock.patch.dict(os.environ, self.env, clear=True), contextlib.redirect_stdout(io.StringIO()):
            status = drive_checks.drive_selftest()
        self.assertEqual(status, 1)  # deliberate stop, after the real wrapper
        calls = self.recorded()
        self.assertEqual(len(calls), 1, calls)
        self.assertTrue(calls[0][1].startswith(str(self.base) + '/backup_gdrive_drive_'), calls)
        self.assertEqual(calls[0][2], 'gdrive:memit-backup/_selftest/mirror/')
        self.assertEqual(len(wrapper_envs), 1)
        self.assertNotEqual(wrapper_envs[0]['BACKUP_PAIRS'], str(self.table))
        for key in ('BACKUP_SRC', 'BACKUP_DEST', 'BACKUP_EXCLUDES'):
            self.assertNotIn(key, wrapper_envs[0])
        self.assertTrue(all(str(p) not in str(calls) for p in self.sources + self.dests))

    def test_drive_dash_runs_both_without_exclude_file(self):
        self.pairs('gdrive')
        header, body = self.table.read_text().split('\n', 1)
        self.table.write_text(header + '\n' + body.replace('\texcludes\n', '\t-\n'))
        status, output = self.drive()
        self.assertEqual(status, 0, output)
        self.assertEqual([c[1:3] for c in self.recorded()],
                         [[str(s) + '/', str(d) + '/'] for s, d in zip(self.sources, self.dests)])
        self.assertTrue(all('--exclude-from' not in c for c in self.recorded()))

    def test_drive_missing_excludes_is_not_dash(self):
        self.pairs('gdrive')
        header, body = self.table.read_text().split('\n', 1)
        self.table.write_text(header + '\n' + body.replace('\texcludes\n', '\tmissing.rules\n'))
        status, output = self.drive()
        self.assertNotEqual(status, 0, output)
        self.assertIn('exclude list missing: ' + str(self.base / 'missing.rules'), output)
        self.assertEqual(self.recorded(), [])

    def test_drive_full_sync_argv(self):
        self.pairs('gdrive')
        status, output = self.drive()
        self.assertEqual(status, 0, output)
        heartbeat = json.loads((self.base / 'heartbeat').read_text())
        stamp = heartbeat['run_id']
        # [LAW:behavior-not-structure] Pin every native flag, including the schedule.
        self.assertEqual(self.recorded()[0], [
            'sync', str(self.sources[0]) + '/', str(self.dests[0]) + '/',
            '--backup-dir', str(self.base / '.deleted' / (stamp + '-' + self.dests[0].name)) + '/',
            '--exclude-from', str(self.excludes), '--links',
            '--log-file', str(self.base / 'runs' / (stamp + '-pair0.jsonl')),
            '--log-level', 'INFO', '--use-json-log',
            '--exclude', '**/.git/objects/**/tmp_obj_*', '--exclude', '**/.git/objects/tmp_obj_*',
            '--exclude', '/.git/objects/**/tmp_obj_*', '--exclude', '/.git/objects/tmp_obj_*',
            '--retries', '1', '--low-level-retries', '10', '--dry-run=false', '--interactive=false',
            '--ignore-errors=false', '--delete-excluded=false', '--delete-after',
            '--bwlimit', '08:00,512k 23:00,off', '--stats', '1m', '--stats-log-level', 'NOTICE'])

    def test_drive_hold_exact_line(self):
        self.pairs('gdrive', hold=True)
        status, output = self.drive()
        self.assertNotEqual(status, 0)
        self.assertEqual(output, f'backup_gdrive: row 3 ({self.sources[1]}): HOLD; Q5: operator must choose the Drive destination\n')
        self.assertEqual(self.recorded(), [])

    def test_intel_hold_exact_line(self):
        self.pairs('intel', hold=True)
        status, output = self.copy()
        self.assertNotEqual(status, 0)
        self.assertEqual(output, f"{str(self.table)!r}: row 3 ({self.sources[1]}): HOLD; Q6: operator must choose the Intel destination\n")
        self.assertEqual(self.recorded(), [])

    def test_intel_dash_runs_both(self):
        self.pairs('intel')
        header, body = self.table.read_text().split('\n', 1)
        self.table.write_text(header + '\n' + body.replace('\texcludes\n', '\t-\n'))
        with mock.patch.object(intel, 'Controller', wraps=intel.Controller) as controller:
            status, output = self.copy()
        self.assertEqual(status, 0, output)
        self.assertEqual([c.args[6] for c in controller.call_args_list], [(), ()])
        self.assertEqual([c[1] for c in self.recorded() if c[0] == 'payload'],
                         [str(s) + '/' for s in self.sources])

    def test_intel_missing_excludes_is_not_dash(self):
        self.pairs('intel')
        header, body = self.table.read_text().split('\n', 1)
        self.table.write_text(header + '\n' + body.replace('\texcludes\n', '\tmissing.rules\n'))
        status, output = self.copy()
        self.assertNotEqual(status, 0, output)
        self.assertIn(str(self.base / 'missing.rules'), output)
        self.assertEqual(self.recorded(), [])

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

    def test_drive_empty_fields_row_refusal(self):
        for index in (1, 2, 3):
            with self.subTest(field=index):
                row = ['gdrive', str(self.sources[0]), str(self.dests[0]), 'excludes']
                row[index] = ''
                self.table.write_text('reader\tsource\tdestination\texcludes\n' + '\t'.join(row) + '\n')
                status, output = self.drive()
                self.assertNotEqual(status, 0)
                self.assertIn('row 2: invalid pair', output)
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

    def test_intel_selected_hosts_and_folders(self):
        self.pairs('intel')
        self.table.write_text(self.table.read_text().replace('fixture:', 'first-host:', 1)
                              .replace('fixture:', 'second-host:', 1))
        status, output = self.copy(remote=False)
        self.assertEqual(status, 0, output)
        self.assertEqual([c[2].split('/incoming/')[0] for c in self.recorded() if c[0] == 'payload'],
                         [host + ':' + str(dest) for host, dest in
                          zip(('first-host', 'second-host'), self.dests)])

    def test_intel_empty_source_is_admission_refusal(self):
        self.assert_intel_bad_row('', 'host:folder', 'excludes', 'invalid pair')

    def test_intel_empty_host_is_admission_refusal(self):
        self.assert_intel_bad_row(str(self.sources[0]), ':folder', 'excludes', 'invalid destination')

    def test_intel_empty_folder_is_admission_refusal(self):
        self.assert_intel_bad_row(str(self.sources[0]), 'host:', 'excludes', 'invalid destination')

    def test_intel_excludes_slash_is_row_refusal(self):
        self.assert_intel_bad_row(str(self.sources[0]), 'host:folder', '../excludes', 'invalid destination')

    def assert_intel_bad_row(self, source, destination, excludes, message):
        self.pairs('intel')
        self.assertEqual(len(intel.read_pairs(self.table)), 2)  # nearest valid control
        self.table.write_text('reader\tsource\tdestination\texcludes\n' +
                              f'intel\t{source}\t{destination}\t{excludes}\n')
        with self.assertRaisesRegex(intel.fdsafe.Refusal, 'row 2: ' + message):
            intel.read_pairs(self.table)
        self.assertEqual(self.recorded(), [])

    def test_intel_source_override_cannot_bypass_hold(self):
        self.pairs('intel', hold=True)
        status, output = self.copy(['--source', str(self.sources[0])])
        self.assertEqual(status, 3, output)
        self.assertRegex(output, r'row 3[^\n]*Q6')
        self.assertEqual(self.recorded(), [])

    def test_intel_legacy_destination(self):
        with mock.patch.object(intel, 'REPO', self.repo):
            controller = intel.Controller(self.sources[0], self.base / 'records', 'legacy',
                                          ['fake', 'host'], mock.Mock())
            controller.runner.run.return_value = b'{}'
            controller.remote_script('inventory')
        command = controller.runner.run.call_args.args[0][-1]
        self.assertIn('"$HOME/"memit_copy', command)
        self.assertNotIn('incompatible_copy', command)

    def test_intel_ancestor_symlink_refuses_without_read(self):
        self.pairs('intel')
        self.assertEqual(len(intel.read_pairs(self.table)), 2)
        link = self.base / 'alias'
        nested = self.base / 'nested'
        nested.mkdir()
        shutil.copy2(self.table, nested / self.table.name)
        shutil.copy2(self.excludes, nested / 'excludes')
        link.symlink_to(self.base, target_is_directory=True)
        with mock.patch.object(intel.fdsafe, '_read', wraps=intel.fdsafe._read) as read:
            with self.assertRaises(intel.fdsafe.Refusal) as raised:
                intel.read_pairs(link / 'nested' / self.table.name)
        self.assertIn(str(link), str(raised.exception))
        self.assertEqual(len(str(raised.exception).splitlines()), 1)
        read.assert_not_called()

    def test_intel_excludes_symlink_refuses_without_outside_read(self):
        self.pairs('intel')
        self.assertEqual(len(intel.read_pairs(self.table)), 2)
        outside = self.base / 'outside'
        outside.write_text('payload\n')
        observed = []
        read = intel.fdsafe._read
        def observe(fd, path):
            data = read(fd, path)
            observed.append(data)
            return data
        with mock.patch.object(intel.fdsafe, '_read', side_effect=observe), \
                fault_kit.swap_for_symlink('read', 1, self.excludes, outside) as fault:
            with self.assertRaises(intel.fdsafe.Refusal) as raised:
                intel.read_pairs(self.table)
        self.assertEqual(fault.fired, 1)
        self.assertIn(str(self.excludes), str(raised.exception))
        self.assertEqual(len(str(raised.exception).splitlines()), 1)
        self.assertNotIn(b'payload\n', observed)

    def test_intel_parent_rebind_between_scan_and_read_refuses(self):
        folder = self.base / 'table-folder'
        folder.mkdir()
        self.pairs('intel')
        table = folder / 'pairs.tsv'
        shutil.copy2(self.table, table)
        shutil.copy2(self.excludes, folder / 'excludes')
        self.assertEqual(len(intel.read_pairs(table)), 2)
        header, body = table.read_text().split('\n', 1)
        table.write_text(header + '\n' + body.replace('\texcludes\n', '\t-\n'))
        scan = intel.fdsafe._scan
        attacks = []
        def rebind_after_scan(parent, name):
            entry = scan(parent, name)
            with fault_kit.rename_and_rebind('open', 1, folder) as fault:
                fd = os.open(self.table, os.O_RDONLY)
                os.close(fd)
            attacks.append(fault.fired)
            return entry
        with mock.patch.object(intel.fdsafe, '_scan', side_effect=rebind_after_scan):
            with self.assertRaises(intel.fdsafe.Refusal) as raised:
                intel.read_pairs(table)
        self.assertEqual(attacks, [1])
        self.assertIn(str(folder), str(raised.exception))

    def test_intel_excludes_bytes_are_not_reopened(self):
        self.pairs('intel')
        self.excludes.write_text('payload\n')
        pairs = intel.read_pairs(self.table)
        self.excludes.write_text('# no longer excludes payload\n')
        with mock.patch.object(intel, 'read_pairs', return_value=pairs):
            status, output = self.copy()
        self.assertEqual(status, 0, output)
        self.assertEqual([c for c in self.recorded() if c[0] == 'payload'], [])

    def test_intel_no_excludes_marker(self):
        self.pairs('intel')
        header, body = self.table.read_text().split('\n', 1)
        self.table.write_text(header + '\n' + body.replace('\texcludes\n', '\t-\n'))
        self.assertEqual([row[3] for row in intel.read_pairs(self.table)], [(), ()])

    def test_intel_patterns_preserve_filter_semantics(self):
        self.pairs('intel')
        self.excludes.write_text('# comment\n\n  \n payload \n/dir/\n')
        self.assertEqual([row[3] for row in intel.read_pairs(self.table)],
                         [('payload', '/dir/'), ('payload', '/dir/')])

    def test_intel_each_row_has_its_patterns(self):
        self.pairs('intel')
        other = self.base / 'other'
        other.write_text('payload\n')
        text = self.table.read_text()
        last = text.rfind('\texcludes\n')
        self.table.write_text(text[:last] + '\tother\n')
        status, output = self.copy()
        self.assertEqual(status, 0, output)
        self.assertEqual([c[1] for c in self.recorded() if c[0] == 'payload'], [str(self.sources[0]) + '/'])

    def test_intel_failure_stops_later_rows(self):
        self.pairs('intel')
        self.env['FIXTURE_FAIL_COPY'] = '1'
        status, output = self.copy()
        self.assertEqual(status, 3, output)
        self.assertEqual(len([c for c in self.recorded() if c[0] == 'payload']), 1)

    def test_other_readers_do_not_dispatch_or_hold(self):
        for reader in ('ssd', 'intel', 'gdrive'):
            with self.subTest(reader=reader):
                self.pairs(reader, hold=True)
                if reader != 'intel':
                    self.assertEqual(self.copy()[0], 0)
                if reader != 'gdrive':
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

    def test_intel_invalid_utf8_excludes_is_not_hidden(self):
        self.table.write_text('reader\tsource\tdestination\texcludes\n' +
                              f'intel\t{self.sources[0]}\tfixture:{self.dests[0]}\texcludes\n')
        self.excludes.write_bytes(b'*.tmp\n\xff\n')
        # [LAW:no-silent-failure] Bad excludes bytes must stop dispatch, not change patterns.
        with self.assertRaises(UnicodeDecodeError):
            self.copy()
        self.assertEqual(self.recorded(), [])

    def test_intel_invalid_utf8_default_excludes_is_not_hidden(self):
        (self.repo / 'code/ops/backup/backup_mirror.excludes').write_bytes(b'*.tmp\n\xff\n')
        runner = mock.Mock()
        # [LAW:no-silent-failure] Bad default excludes bytes must stop dispatch.
        with mock.patch.object(intel, 'REPO', self.repo):
            with self.assertRaises(UnicodeDecodeError):
                intel.Controller(self.sources[0], self.base / 'records', 'legacy',
                                 ['fake', 'host'], runner)
        runner.run.assert_not_called()
        self.assertEqual(self.recorded(), [])

    def test_intel_valid_utf8_replacement_character_excludes_runs(self):
        self.table.write_text('reader\tsource\tdestination\texcludes\n' +
                              f'intel\t{self.sources[0]}\tfixture:{self.dests[0]}\texcludes\n')
        self.excludes.write_bytes('*.tmp\n\ufffd\n'.encode('utf-8'))
        with mock.patch.object(intel, 'Controller', wraps=intel.Controller) as controller:
            status, output = self.copy()
        self.assertEqual(status, 0, output)
        self.assertEqual(controller.call_count, 1)
        self.assertEqual(controller.call_args.args[6], ('*.tmp', '\ufffd'))
        self.assertEqual([c[1] for c in self.recorded() if c[0] == 'payload'],
                         [str(self.sources[0]) + '/'])

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


class DriveMode(unittest.TestCase):
    """Exercise the real --drive entry point with every external call intercepted."""

    def admission(self, prepare):
        with tempfile.TemporaryDirectory(dir='/private/tmp') as name:
            root = Path(name)
            (root / 'results').mkdir()
            unit = root / 'unit'
            unit.mkdir()
            table = unit / 'pairs.tsv'
            table.write_text('reader\tsource\tdestination\texcludes\n'
                             'gdrive\t/source\tfixture:dest\trules\n')
            (unit / 'rules').write_bytes(b'payload\n')
            calls = []
            def process(args, **kwargs):
                calls.append(args)
                raise RuntimeError('fixture reached dispatch')
            with prepare(table), mock.patch.object(drive_checks, 'ROOT', root), \
                    mock.patch.object(drive_checks, 'run_process', side_effect=process), \
                    mock.patch.dict(os.environ, BACKUP_PAIRS=str(table)), \
                    contextlib.redirect_stdout(io.StringIO()):
                status = drive_checks.drive_selftest()
            summary = json.loads(next((root / 'results').glob('*/summary.json')).read_text())
            self.assertNotEqual(status, 0, summary)
            self.assertEqual(summary['status'], 'FAILED')
            self.assertEqual(calls, [], summary)
            return summary

    def bad_table(self, change, message):
        def prepare(table):
            table.write_text(change(table.read_text()))
            return contextlib.nullcontext()
        self.assertIn(message, self.admission(prepare)['error'])

    def test_drive_mode_parent_symlink_refuses(self):
        def prepare(table):
            actual = table.parent.parent / 'actual'
            table.parent.rename(actual)
            table.parent.symlink_to(actual, target_is_directory=True)
            return contextlib.nullcontext()
        self.assertIn('unit', self.admission(prepare)['error'])

    def test_drive_mode_other_readers_do_not_dispatch_or_hold(self):
        def prepare(table):
            table.write_text(table.read_text().replace('gdrive', 'ssd', 1)
                             .replace('gdrive', 'intel', 1).replace('fixture:second', 'HOLD'))
            return contextlib.nullcontext()
        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertEqual(status, 0, summary)
        self.assertEqual(dry, [])

    def test_selftest_excludes_after_read_move_refuses(self):
        fired = []
        @contextlib.contextmanager
        def prepare(table):
            read = drive_checks.fdsafe.read_named
            def moved(parent, name):
                data = read(parent, name)
                if name == 'backup_mirror.excludes':
                    with fault_kit.rename_and_rebind('open', 1, Path(parent.path)) as fault:
                        fd = os.open(table, os.O_RDONLY)
                        os.close(fd)
                    fired.append(fault.fired)
                return data
            with mock.patch.object(drive_checks.fdsafe, 'read_named', moved):
                yield
        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertEqual(fired, [1])
        self.assertNotEqual(status, 0, summary)
        self.assertIn('is held at', summary['error'])
        self.assertEqual(dry, [])

    def test_drive_mode_wrong_header_refuses(self):
        self.bad_table(lambda text: text.replace('reader', 'wrong', 1), 'header')

    def test_drive_mode_empty_table_refuses(self):
        self.bad_table(lambda text: '', 'header')

    def test_drive_mode_fifth_field_refuses(self):
        self.bad_table(lambda text: text.replace('rules\n', 'rules\textra\n'), 'invalid pair')

    def test_drive_mode_empty_field_refuses(self):
        self.bad_table(lambda text: text.replace('/source', ''), 'invalid pair')

    def test_drive_mode_unknown_reader_refuses(self):
        self.bad_table(lambda text: text.replace('gdrive', 'unknown'), 'unknown reader')

    def test_drive_mode_absolute_excludes_refuses(self):
        self.bad_table(lambda text: text.replace('rules\n', '/outside.rules\n'), 'excludes must be next to table')

    def test_drive_mode_quoted_row_refuses(self):
        self.bad_table(lambda text: text.replace('gdrive', '"gdrive"'), 'unknown reader')

    def test_drive_mode_invalid_utf8_refuses(self):
        def prepare(table):
            table.write_bytes(table.read_bytes().replace(b'/source', b'/bad\xff'))
            return contextlib.nullcontext()
        self.assertIn('utf-8', self.admission(prepare)['error'])

    def test_drive_mode_excludes_symlink_refuses(self):
        fired = []
        @contextlib.contextmanager
        def prepare(table):
            outside = table.parent.parent / 'outside'
            outside.write_bytes(b'outside\n')
            with fault_kit.swap_for_symlink('open', 1, table.parent / 'rules', outside) as fault:
                fd = os.open(table, os.O_RDONLY)
                os.close(fd)
                yield
            fired.append(fault.fired)
        self.assertIn('rules', self.admission(prepare)['error'])
        self.assertEqual(fired, [1])

    def late_drive_move(self, leaf):
        fired = []
        @contextlib.contextmanager
        def prepare(table):
            if leaf == 'pairs.tsv':
                table.write_text(table.read_text().replace('rules\n', '-\n'))
            read = drive_checks.fdsafe.read_named
            def moved(parent, name):
                data = read(parent, name)
                if name == leaf and not fired:
                    with fault_kit.rename_and_rebind('open', 1, table.parent) as fault:
                        fd = os.open(table.parent.parent, os.O_RDONLY)
                        os.close(fd)
                    fired.append(fault.fired)
                return data
            with mock.patch.object(drive_checks.fdsafe, 'read_named', moved):
                yield
        self.assertIn('is held at', self.admission(prepare)['error'])
        self.assertEqual(fired, [1])

    def test_drive_mode_table_after_read_move_refuses(self):
        self.late_drive_move('pairs.tsv')

    def test_drive_mode_excludes_after_read_move_refuses(self):
        self.late_drive_move('rules')

    def test_output_setup_failure_closes_results(self):
        with tempfile.TemporaryDirectory(dir='/private/tmp') as name:
            root = Path(name)
            (root / 'results').mkdir()
            held = []
            open_file = os.open
            def remember(path, *args, **kwargs):
                fd = open_file(path, *args, **kwargs)
                held.append(fd)
                return fd
            with mock.patch.object(drive_checks, 'ROOT', root), \
                    mock.patch.object(os, 'open', remember), \
                    fault_kit.raise_unexpected('mkdir', 1, RuntimeError) as fault:
                with self.assertRaises(RuntimeError):
                    drive_checks.drive_selftest()
            self.assertEqual(fault.fired, 1)
            self.assertEqual(len(held), 1)
            with self.assertRaises(OSError):
                os.fstat(held[0])

    def test_output_holds_close_after_run(self):
        held = []
        @contextlib.contextmanager
        def prepare(table):
            open_file = os.open
            def remember(*args, **kwargs):
                fd = open_file(*args, **kwargs)
                held.append(fd)
                return fd
            with mock.patch.object(os, 'open', remember):
                yield
            for fd in held:
                with self.assertRaises(OSError):
                    os.fstat(fd)
        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertEqual(status, 0, summary)
        self.assertGreaterEqual(len(held), 3)

    def test_output_results_symlink_refuses(self):
        with tempfile.TemporaryDirectory(dir='/private/tmp') as name:
            root = Path(name)
            results, other = root / 'results', root / 'other'
            results.mkdir()
            other.mkdir()
            with fault_kit.swap_for_symlink('open', 1, results, other,
                    match=lambda path, *a, **k: path == str(results)) as fault, \
                    mock.patch.object(drive_checks, 'ROOT', root), \
                    mock.patch.object(drive_checks, 'run_process') as process:
                with self.assertRaises(drive_checks.fdsafe.Refusal):
                    drive_checks.drive_selftest()
            self.assertEqual(fault.fired, 1)
            process.assert_not_called()
            self.assertEqual(list(other.iterdir()), [])

    def test_output_directory_rebind_refuses(self):
        with tempfile.TemporaryDirectory(dir='/private/tmp') as name:
            root = Path(name)
            (root / 'results').mkdir()
            mkdir = os.mkdir
            faults = []
            with contextlib.ExitStack() as stack:
                def create_dir(path, *args, **kwargs):
                    value = mkdir(path, *args, **kwargs)
                    if Path(path).name.startswith('backup_gdrive_drive_'):
                        out = root / 'results' / Path(path).name
                        faults.append(stack.enter_context(fault_kit.rename_and_rebind(
                            'open', 1, out, match=lambda path, *a, **k: Path(path).name == out.name)))
                    return value
                stack.enter_context(mock.patch.object(os, 'mkdir', create_dir))
                stack.enter_context(mock.patch.object(drive_checks, 'ROOT', root))
                process = stack.enter_context(mock.patch.object(drive_checks, 'run_process'))
                with self.assertRaisesRegex(drive_checks.fdsafe.Refusal, 'changed between create and open'):
                    drive_checks.drive_selftest()
            self.assertEqual([fault.fired for fault in faults], [1])
            process.assert_not_called()

    def output_create_case(self, leaf, kind):
        # [LAW:behavior-not-structure] Observe refusal, input custody and dispatch.
        observed = {}
        calls = []
        @contextlib.contextmanager
        def prepare(table):
            before = table.read_bytes()
            mkdir = os.mkdir
            with contextlib.ExitStack() as stack:
                def create_dir(path, *args, **kwargs):
                    value = mkdir(path, *args, **kwargs)
                    if Path(path).name.startswith('backup_gdrive_drive_') and (
                            Path(path).parent.name == 'results' or kwargs.get('dir_fd') is not None):
                        out = table.parent.parent / 'results' / Path(path).name
                        target = out / leaf
                        fake = drive_checks.run_process
                        def record(argv, **options):
                            calls.append(argv)
                            return fake(argv, **options)
                        stack.enter_context(mock.patch.object(drive_checks, 'run_process', record))
                        if kind == 'parent':
                            observed['fault'] = stack.enter_context(fault_kit.swap_for_symlink(
                                'open', 1, out, table.parent,
                                match=lambda name, *a, **k: name == leaf))
                        elif kind == 'link':
                            target.write_bytes(b'keep existing output')
                            observed['fault'] = stack.enter_context(fault_kit.swap_for_symlink(
                                'open', 1, target, table,
                                match=lambda name, *a, **k: name == leaf))
                        elif kind == 'file':
                            target.write_bytes(b'keep existing output')
                        observed['target'] = target
                    return value
                stack.enter_context(mock.patch.object(os, 'mkdir', create_dir))
                yield
                self.assertEqual(table.read_bytes(), before)
                self.assertEqual(list(table.parent.glob('excludes_*.txt')), [])
                self.assertEqual(list(table.parent.glob('dry_run_changes*.txt')), [])
                if kind == 'file':
                    self.assertEqual(observed['target'].read_bytes(), b'keep existing output')
                if kind == 'control':
                    out = observed['target'].parent
                    self.assertEqual([(out / f'excludes_{i}.txt').read_bytes() for i in range(2)],
                                     [(table.parent / name).read_bytes() for name in ('one.rules', 'two.rules')])
        status, summary, dry, table = self.run_drive_table(prepare)
        if kind == 'control':
            self.assertEqual(status, 0, summary)
            self.assertEqual(summary['status'], 'PASS')
            self.assertEqual(len(dry), 2)
        else:
            self.assertEqual(status, 1, summary)
            self.assertEqual(summary['status'], 'FAILED')
            self.assertIn('is held at' if kind == 'parent' else 'File exists', summary['error'])
            if leaf == 'excludes_0.txt':
                self.assertEqual(calls, [], summary)
            if kind in ('parent', 'link'):
                self.assertEqual(observed['fault'].fired, 1)

    def test_output_excludes_parent_swap_refuses(self):
        self.output_create_case('excludes_0.txt', 'parent')

    def test_output_excludes_leaf_link_refuses(self):
        self.output_create_case('excludes_0.txt', 'link')

    def test_output_excludes_existing_file_refuses(self):
        self.output_create_case('excludes_0.txt', 'file')

    def test_output_changes_parent_swap_refuses(self):
        self.output_create_case('dry_run_changes.txt', 'parent')

    def test_output_changes_leaf_link_refuses(self):
        self.output_create_case('dry_run_changes.txt', 'link')

    def test_output_changes_existing_file_refuses(self):
        self.output_create_case('dry_run_changes.txt', 'file')

    def test_output_control_copies_exact_bytes(self):
        self.output_create_case('excludes_0.txt', 'control')

    def aggregate_drive_case(self, payloads, listings):
        # [LAW:effects-at-boundaries] Supply rclone evidence through its fake command seam.
        observed = {}
        selftest = drive_checks.drive_selftest

        @contextlib.contextmanager
        def prepare(table):
            sources = [str(table.parent.parent / name) + '/' for name in ('one', 'two')]

            def run():
                process = drive_checks.run_process

                def evidence(args, **options):
                    if args[1] == 'sync':
                        self.assertIn('--dry-run', args)
                        number = sources.index(args[2])
                        target = Path(args[args.index('--combined') + 1])
                        self.assertEqual(target.parent.parent, table.parent.parent / 'results')
                        target.write_bytes(payloads[number])
                        return subprocess.CompletedProcess(args, 0, '', '')
                    if args[1] == 'lsjson' and args[2] in sources:
                        return subprocess.CompletedProcess(args, 0,
                            json.dumps(listings[sources.index(args[2])]), '')
                    return process(args, **options)

                # [LAW:no-ambient-temporal-coupling] A fixed upload interval pins the projection.
                with mock.patch.object(drive_checks, 'run_process', side_effect=evidence), \
                        mock.patch.object(drive_checks.time, 'monotonic', side_effect=[100.0, 104.0]):
                    status = selftest()
                out = next((table.parent.parent / 'results').iterdir())
                observed['combined'] = (out / 'dry_run_changes.txt').read_bytes()
                observed['commands'] = json.loads((out / 'commands.json').read_text())
                return status

            with mock.patch.object(drive_checks, 'drive_selftest', side_effect=run):
                yield

        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertEqual(status, 0, summary)
        self.assertEqual(summary['status'], 'PASS')
        calls = [entry['args'] for entry in observed['commands'] if entry['args'][1] == 'sync']
        out = Path(summary['evidence_dir'])
        self.assertEqual([call[call.index('--combined') + 1] for call in calls],
                         [str(out / 'dry_run_changes_0.txt'), str(out / 'dry_run_changes_1.txt')])
        self.assertEqual([call[2:4] for call in calls],
                         [[str(Path(table).parent.parent / 'one') + '/', 'fixture:first/'],
                          [str(Path(table).parent.parent / 'two') + '/', 'fixture:second/']])
        self.assertEqual(summary['measured_bytes_per_s'], 50_000_000)
        self.assertEqual(summary['estimate_scope'],
                         'Payload-rate projection; small-file/API overhead and source churn not measured')
        return summary, observed['combined']

    def test_drive_aggregate_duplicate_names_exact(self):
        # [LAW:behavior-not-structure] Distinct row sizes must survive identical basenames.
        summary, combined = self.aggregate_drive_case(
            (b'+ a.txt\n', b'+ a.txt\n'),
            ([{'Path': 'a.txt', 'Size': 5}], [{'Path': 'a.txt', 'Size': 9}]))
        self.assertEqual(combined, b'+ 0/a.txt\n+ 1/a.txt\n')
        self.assertEqual(summary['dry_run_transfer_files'], 2)
        self.assertEqual(summary['dry_run_transfer_bytes'], 14)
        self.assertEqual(summary['payload_rate_estimate_s'], 0.00000028)

    def test_drive_aggregate_mixed_markers_exact(self):
        summary, combined = self.aggregate_drive_case(
            (b'+ a.txt\n- gone.txt\n* edit.txt\n', b'* a.txt\n= same.txt\n'),
            ([{'Path': 'a.txt', 'Size': 5}, {'Path': 'gone.txt', 'Size': 101},
              {'Path': 'edit.txt', 'Size': 11}],
             [{'Path': 'a.txt', 'Size': 19}, {'Path': 'same.txt', 'Size': 103}]))
        self.assertEqual(combined,
                         b'+ 0/a.txt\n- 0/gone.txt\n* 0/edit.txt\n* 1/a.txt\n= 1/same.txt\n')
        self.assertEqual(summary['dry_run_transfer_files'], 3)
        self.assertEqual(summary['dry_run_transfer_bytes'], 35)
        self.assertEqual(summary['payload_rate_estimate_s'], 0.0000007)

    def test_drive_nested_rows_complete_argv(self):
        # [LAW:behavior-not-structure] Pin the whole command contract for both row shapes.
        observed = {}
        selftest = drive_checks.drive_selftest

        @contextlib.contextmanager
        def prepare(table):
            root = table.parent.parent
            table.write_text('reader\tsource\tdestination\texcludes\n' +
                             f'gdrive\t{root}/one\tfixture:a/first\tone.rules\n' +
                             f'gdrive\t{root}/two/\tfixture:b/c/second/\t-\n')
            (table.parent / 'one.rules').write_bytes(b'*.cache\nprivate/**\n')

            def run():
                process = drive_checks.run_process

                def evidence(args, **options):
                    if args[1] == 'sync':
                        target = Path(args[args.index('--combined') + 1])
                        self.assertEqual(target.parent.parent, root / 'results')
                        target.write_text('+ payload\n')
                        return subprocess.CompletedProcess(args, 0, '', '')
                    return process(args, **options)

                # [LAW:no-ambient-temporal-coupling] Rate checks use a fixed interval.
                with mock.patch.object(drive_checks, 'run_process', side_effect=evidence), \
                        mock.patch.object(drive_checks.time, 'monotonic', side_effect=[100.0, 104.0]):
                    status = selftest()
                out = next((root / 'results').iterdir())
                observed['commands'] = json.loads((out / 'commands.json').read_text())
                observed['rules'] = (out / 'excludes_0.txt').read_bytes()
                return status

            with mock.patch.object(drive_checks, 'drive_selftest', side_effect=run):
                yield

        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertEqual(status, 0, summary)
        self.assertEqual(summary['status'], 'PASS')
        self.assertEqual(observed['rules'], b'*.cache\nprivate/**\n')
        root = Path(table).parent.parent
        out = Path(summary['evidence_dir'])
        calls = [entry['args'] for entry in observed['commands']
                 if entry['args'][1] == 'sync' or
                 (entry['args'][1] == 'lsjson' and entry['args'][2].startswith(str(root) + '/'))]
        self.assertEqual(calls, [
            ['/opt/homebrew/bin/rclone', 'sync', str(root / 'one') + '/', 'fixture:a/first/',
             '--dry-run', '--links', '--exclude-from', str(out / 'excludes_0.txt'),
             '--exclude', '**/.git/objects/**/tmp_obj_*', '--exclude', '**/.git/objects/tmp_obj_*',
             '--exclude', '/.git/objects/**/tmp_obj_*', '--exclude', '/.git/objects/tmp_obj_*',
             '--backup-dir', 'fixture:a/.deleted/DRY-RUN/',
             '--combined', str(out / 'dry_run_changes_0.txt'),
             '--contimeout', '10s', '--timeout', '60s', '--retries', '1', '--low-level-retries', '1'],
            ['/opt/homebrew/bin/rclone', 'lsjson', str(root / 'one') + '/',
             '--recursive', '--files-only', '--links', '--exclude-from', str(out / 'excludes_0.txt'),
             '--exclude', '**/.git/objects/**/tmp_obj_*', '--exclude', '**/.git/objects/tmp_obj_*',
             '--exclude', '/.git/objects/**/tmp_obj_*', '--exclude', '/.git/objects/tmp_obj_*',
             '--contimeout', '10s', '--timeout', '60s', '--retries', '1', '--low-level-retries', '1'],
            ['/opt/homebrew/bin/rclone', 'sync', str(root / 'two') + '/', 'fixture:b/c/second/',
             '--dry-run', '--links',
             '--exclude', '**/.git/objects/**/tmp_obj_*', '--exclude', '**/.git/objects/tmp_obj_*',
             '--exclude', '/.git/objects/**/tmp_obj_*', '--exclude', '/.git/objects/tmp_obj_*',
             '--backup-dir', 'fixture:b/c/.deleted/DRY-RUN/',
             '--combined', str(out / 'dry_run_changes_1.txt'),
             '--contimeout', '10s', '--timeout', '60s', '--retries', '1', '--low-level-retries', '1'],
            ['/opt/homebrew/bin/rclone', 'lsjson', str(root / 'two') + '/',
             '--recursive', '--files-only', '--links',
             '--exclude', '**/.git/objects/**/tmp_obj_*', '--exclude', '**/.git/objects/tmp_obj_*',
             '--exclude', '/.git/objects/**/tmp_obj_*', '--exclude', '/.git/objects/tmp_obj_*',
             '--contimeout', '10s', '--timeout', '60s', '--retries', '1', '--low-level-retries', '1'],
        ])

    def check_drive_mode(self, hold):
        with tempfile.TemporaryDirectory(dir='/private/tmp') as name:
            root = Path(name)
            (root / 'results').mkdir()
            defaults = root / 'code/ops/backup'
            defaults.mkdir(parents=True)
            (defaults / 'backup_mirror.excludes').write_text('.cache/\n')
            unit = root / 'unit'
            unit.mkdir()
            table = unit / 'pairs.tsv'
            table.write_text('reader\tsource\tdestination\texcludes\n' +
                             f'gdrive\t{root}/one\tfixture:first\tone.rules\n' +
                             f'gdrive\t{root}/two\t' + ('HOLD' if hold else 'fixture:second') + '\ttwo.rules\n')
            (unit / 'one.rules').write_bytes(b'first rules\n')
            (unit / 'two.rules').write_bytes(b'second rules\n')
            calls, dry = [], []
            syncs = 0

            def process(args, *, env=None, timeout=None):
                nonlocal syncs
                calls.append(args)
                output, error, status = '', '', 0
                if args[0] == '/bin/bash':
                    source = Path(Path(env['BACKUP_PAIRS']).read_text().splitlines()[1].split('\t')[1])
                    self.assertTrue(str(source).startswith('/private/tmp/'))
                    if Path(env['BACKUP_LOCK_DIR']).exists():
                        status, error = 1, 'lock'
                    elif env['BACKUP_MOUNT_POINT'] != '/':
                        status, error = 1, 'mounted'
                    elif not list(source.iterdir()):
                        status, error = 1, 'empty'
                    else:
                        syncs += 1
                elif args[1] == 'cat':
                    output = ('deleted version' if args[2].endswith('gone.txt') else
                              'original' if '/.deleted/' in args[2] or syncs == 1 else 'modified contents')
                elif args[1] == 'lsjson':
                    target = args[2]
                    if target.endswith('/mirror'):
                        output = json.dumps([{'Path': p} for p in
                                             (['keep.txt', 'gone.txt'] if syncs == 1 else ['keep.txt'])])
                    elif target.endswith('/.deleted'):
                        output = json.dumps([{'Path': 'stamp/' + p} for p in ('keep.txt', 'gone.txt')])
                    elif target.endswith('/_selftest'):
                        output = json.dumps([{'Path': 'upload_rate.bin', 'Size': 200_000_000}])
                    else:
                        output = json.dumps([{'Path': 'payload', 'Size': 7}])
                elif args[1] == 'sync':
                    self.assertIn('--dry-run', args)
                    dry.append(args)
                    Path(args[args.index('--combined') + 1]).write_text('+ payload\n')
                else:
                    self.assertIn(args[1], ('lsd', 'copyto', 'purge'))
                return subprocess.CompletedProcess(args, status, output, error)

            class Sink:
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def write(self, block):
                    return len(block)

            original_open = Path.open
            def open_file(path, *args, **kwargs):
                return Sink() if path.name == 'upload_rate.bin' else original_open(path, *args, **kwargs)

            with mock.patch.object(drive_checks, 'ROOT', root), \
                    mock.patch.object(drive_checks, 'run_process', side_effect=process), \
                    mock.patch.dict(os.environ, BACKUP_PAIRS=str(table)), \
                    mock.patch.object(Path, 'open', open_file), \
                    mock.patch.object(os, 'urandom', side_effect=bytes), \
                    contextlib.redirect_stdout(io.StringIO()):
                status = drive_checks.drive_selftest()
            summary = json.loads(next((root / 'results').glob('*/summary.json')).read_text())
            self.assertTrue(calls, 'positive control: the real selftest reached its command boundary')
            if hold:
                self.assertEqual(status, 1, summary)
                self.assertIn('HOLD; Q5', summary['error'])
                self.assertEqual(dry, [])
            else:
                self.assertEqual(status, 0, summary)
                self.assertEqual([call[2:4] for call in dry],
                                 [[str(root / 'one') + '/', 'fixture:first/'],
                                  [str(root / 'two') + '/', 'fixture:second/']])
                self.assertTrue(all('--exclude-from' in call for call in dry))
                copies = [Path(call[call.index('--exclude-from') + 1]) for call in dry]
                self.assertEqual([p.read_bytes() for p in copies],
                                 [(unit / 'one.rules').read_bytes(), (unit / 'two.rules').read_bytes()])
                self.assertTrue(all(p.parent == Path(summary['evidence_dir']) for p in copies))

    def run_drive_table(self, prepare):
        with tempfile.TemporaryDirectory(dir='/private/tmp') as name:
            root = Path(name)
            (root / 'results').mkdir()
            defaults = root / 'code/ops/backup'
            defaults.mkdir(parents=True)
            (defaults / 'backup_mirror.excludes').write_text('.cache/\n')
            unit = root / 'unit'
            unit.mkdir()
            table = unit / 'pairs.tsv'
            table.write_text('reader\tsource\tdestination\texcludes\n' +
                             f'gdrive\t{root}/one\tfixture:first\tone.rules\n' +
                             f'gdrive\t{root}/two\t' + 'fixture:second' + '\ttwo.rules\n')
            (unit / 'one.rules').write_text('# fixture\n')
            (unit / 'two.rules').write_text('# fixture\n')
            attack = prepare(table)
            calls, dry = [], []
            syncs = 0

            def process(args, *, env=None, timeout=None):
                nonlocal syncs
                calls.append(args)
                output, error, status = '', '', 0
                if args[0] == '/bin/bash':
                    source = Path(Path(env['BACKUP_PAIRS']).read_text().splitlines()[1].split('\t')[1])
                    self.assertTrue(str(source).startswith('/private/tmp/'))
                    if Path(env['BACKUP_LOCK_DIR']).exists():
                        status, error = 1, 'lock'
                    elif env['BACKUP_MOUNT_POINT'] != '/':
                        status, error = 1, 'mounted'
                    elif not list(source.iterdir()):
                        status, error = 1, 'empty'
                    else:
                        syncs += 1
                elif args[1] == 'cat':
                    output = ('deleted version' if args[2].endswith('gone.txt') else
                              'original' if '/.deleted/' in args[2] or syncs == 1 else 'modified contents')
                elif args[1] == 'lsjson':
                    target = args[2]
                    if target.endswith('/mirror'):
                        output = json.dumps([{'Path': p} for p in
                                             (['keep.txt', 'gone.txt'] if syncs == 1 else ['keep.txt'])])
                    elif target.endswith('/.deleted'):
                        output = json.dumps([{'Path': 'stamp/' + p} for p in ('keep.txt', 'gone.txt')])
                    elif target.endswith('/_selftest'):
                        output = json.dumps([{'Path': 'upload_rate.bin', 'Size': 200_000_000}])
                    else:
                        output = json.dumps([{'Path': 'payload', 'Size': 7}])
                elif args[1] == 'sync':
                    self.assertIn('--dry-run', args)
                    if '--exclude-from' in args and not Path(args[args.index('--exclude-from') + 1]).is_file():
                        return subprocess.CompletedProcess(args, 1, '', 'exclude list missing')
                    dry.append(args)
                    Path(args[args.index('--combined') + 1]).write_text('+ payload\n')
                else:
                    self.assertIn(args[1], ('lsd', 'copyto', 'purge'))
                return subprocess.CompletedProcess(args, status, output, error)

            class Sink:
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def write(self, block):
                    return len(block)

            with attack:
                original_open = Path.open
                def open_file(path, *args, **kwargs):
                    return Sink() if path.name == 'upload_rate.bin' else original_open(path, *args, **kwargs)

                with mock.patch.object(drive_checks, 'ROOT', root), \
                        mock.patch.object(drive_checks, 'run_process', side_effect=process), \
                        mock.patch.dict(os.environ, BACKUP_PAIRS=str(table)), \
                        mock.patch.object(Path, 'open', open_file), \
                        mock.patch.object(os, 'urandom', side_effect=bytes), \
                        contextlib.redirect_stdout(io.StringIO()):
                    status = drive_checks.drive_selftest()
            summary = json.loads(next((root / 'results').glob('*/summary.json')).read_text())
            return status, summary, dry, str(table)

    def test_drive_mode_dash_runs_both_without_exclude_file(self):
        def prepare(table):
            table.write_text(table.read_text().replace('one.rules', '-').replace('two.rules', '-'))
            return contextlib.nullcontext()
        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertEqual(status, 0, summary)
        root = Path(table).parent.parent
        self.assertEqual([c[2:4] for c in dry],
                         [[str(root / 'one') + '/', 'fixture:first/'],
                          [str(root / 'two') + '/', 'fixture:second/']])
        self.assertTrue(all('--exclude-from' not in c for c in dry))

    def test_drive_mode_missing_excludes_is_not_dash(self):
        def prepare(table):
            table.write_text(table.read_text().replace('one.rules', 'missing.rules'))
            return contextlib.nullcontext()
        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertNotEqual(status, 0, summary)
        self.assertIn('exclude list missing', summary['error'])
        self.assertEqual(dry, [])

    def test_drive_mode_hold_exact_line(self):
        def prepare(table):
            table.write_text(table.read_text().replace('fixture:second', 'HOLD'))
            return contextlib.nullcontext()
        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertNotEqual(status, 0)
        self.assertEqual(summary['error'], 'gdrive row 1: HOLD; Q5: operator must choose the Drive destination')
        self.assertEqual(dry, [])

    def test_drive_mode_table_swap_refuses(self):
        fired = []
        @contextlib.contextmanager
        def prepare(table):
            target = table.parent / 'substitute.tsv'
            target.write_text(table.read_text().replace(str(table.parent / 'one'), str(table.parent / 'two')))
            original_open = Path.open
            original_read = intel.fdsafe.read_named
            def swap():
                with fault_kit.swap_for_symlink('open', 1, table, target) as fault:
                    fd = os.open(target, os.O_RDONLY)
                    os.close(fd)
                fired.append(fault.fired)
            def opened(path, *args, **kwargs):
                if path == table and not fired:
                    swap()
                return original_open(path, *args, **kwargs)
            def read(parent, name):
                if Path(parent.path) / name == table and not fired:
                    swap()
                return original_read(parent, name)
            with mock.patch.object(Path, 'open', opened), mock.patch.object(intel.fdsafe, 'read_named', read):
                yield
        status, summary, dry, table = self.run_drive_table(prepare)
        self.assertEqual(fired, [1])
        self.assertNotEqual(status, 0, summary)
        self.assertIn(table, summary['error'])
        self.assertEqual(dry, [])

    def test_drive_mode_selected_rows(self):
        self.check_drive_mode(False)

    def test_drive_mode_hold_before_any_row(self):
        self.check_drive_mode(True)


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
    if '--exclude-from' in args:
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


SELFTEST_NATIVE = r'''
import json, os, pathlib, sys
root = pathlib.Path(os.environ['FIXTURE_ROOT']).resolve()
args = sys.argv[1:]
def local(value):
    path = pathlib.Path(value).resolve()
    if not path.is_relative_to(root):
        raise SystemExit('fixture refuses outside path: ' + value)
    return path
if args[0] == 'config':
    print('{}')
elif args[0] == 'version':
    print('confined fixture')
elif args[0] == 'sync':
    local(args[1])
    for value in (args[2], args[args.index('--backup-dir') + 1]):
        if not value.startswith('gdrive:memit-backup/_selftest/'):
            local(value)
    local(args[args.index('--exclude-from') + 1])
    log = local(args[args.index('--log-file') + 1])
    with (root / 'calls.jsonl').open('a') as f:
        f.write(json.dumps(args) + '\n')
    log.write_text(json.dumps({'level': 'notice', 'stats': {'bytes': 1, 'errors': 0, 'fatalError': False}}) + '\n')
else:
    raise SystemExit('fixture refuses unknown command: ' + repr(args))
'''
