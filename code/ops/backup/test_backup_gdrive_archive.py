"""T425: real local rclone preserves each row's displaced originals."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent


class ArchiveTest(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(dir='/tmp')).resolve()
        self.addCleanup(shutil.rmtree, self.base)
        installed = Path('/opt/homebrew/bin/rclone')
        self.rclone = str(installed) if installed.is_file() else shutil.which('rclone')
        self.assertTrue(self.rclone, 'real rclone is required; never skip')
        self.script = self.base / 'backup_gdrive.sh'
        shutil.copy2(HERE / 'backup_gdrive.sh', self.script)
        shutil.copy2(HERE / 'backup_gdrive_status.py', self.base / 'backup_gdrive_status.py')
        self.sources = [self.base / 'source one', self.base / 'source two']
        self.dests = [self.base / 'parent' / 'first-row', self.base / 'parent' / 'second row']
        for i, (source, dest) in enumerate(zip(self.sources, self.dests)):
            source.mkdir()
            dest.mkdir(parents=True)
            (source / 'a.bin').write_bytes(b'new payload' * (i + 2))
            (dest / 'a.bin').write_bytes(b'original ' + bytes([i]))
            (dest / 'gone.bin').write_bytes(b'deleted ' + bytes([i]))
        self.table = self.base / 'pairs.tsv'
        self.table.write_text('reader\tsource\tdestination\texcludes\n' + ''.join(
            f'gdrive\t{s}\t{d}/\texcludes\n' for s, d in zip(self.sources, self.dests)))
        self.excludes = self.base / 'excludes'
        self.excludes.write_text('# fixture\n')
        self.archive = self.dests[0].parent / '.deleted'
        self.legacy = self.archive / '20000101T000000Z-123' / 'a.bin'
        self.legacy.parent.mkdir(parents=True)
        self.legacy.write_bytes(b'old-layout history')
        self.legacy_stat = self.legacy.stat()
        self.tool = self.base / 'rclone'
        self.tool.write_text('#!' + sys.executable + '\n' + CONFINED_RCLONE)
        self.tool.chmod(0o700)
        self.mount = self.base / 'mount'
        self.mount.write_text('#!/bin/sh\nprintf "fixture on %s (local)\\n" "$BACKUP_MOUNT_POINT"\n')
        self.mount.chmod(0o700)
        config = self.base / 'rclone.conf'
        config.write_text('')
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(('BACKUP_', 'RCLONE_'))}
        self.env.update(BACKUP_PAIRS=str(self.table), BACKUP_SRC=str(self.sources[0]),
                        BACKUP_DEST=str(self.dests[0]), BACKUP_EXCLUDES=str(self.excludes),
                        BACKUP_RCLONE=str(self.tool), BACKUP_PYTHON=sys.executable,
                        BACKUP_MOUNT=str(self.mount), BACKUP_MOUNT_POINT=str(self.base),
                        BACKUP_LOG=str(self.base / 'backup.log'),
                        BACKUP_LOCK_DIR=str(self.base / 'lock'),
                        BACKUP_HEARTBEAT=str(self.base / 'heartbeat.json'),
                        RCLONE_CONFIG=str(config), HOME=str(self.base),
                        TMPDIR=str(self.base), FIXTURE_ROOT=str(self.base),
                        REAL_RCLONE=self.rclone, PYTHONDONTWRITEBYTECODE='1')

    def run_backup(self):
        text = self.script.read_text()
        for seam in (k for k in self.env if k.startswith('BACKUP_')):
            self.assertIn(seam, text, 'W7: reader missing fixture seam ' + seam)
        proc = subprocess.Popen(['/bin/bash', str(self.script)], env=self.env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
        def reap():
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate(timeout=10)
        self.addCleanup(reap)
        out, err = proc.communicate(timeout=10)
        self.assertEqual(proc.returncode, 0, out + err)
        self.assertFalse((self.base / 'lock').exists())
        return json.loads((self.base / 'heartbeat.json').read_text())['run_id']

    def test_rows_keep_replaced_deleted_and_old_layout_bytes(self):
        # [LAW:behavior-not-structure] Real syncs must retain bytes, not just name an archive.
        stamp = self.run_backup()
        expected = {self.legacy.parent.name}
        for i, (source, dest) in enumerate(zip(self.sources, self.dests)):
            folder = self.archive / (stamp + '-' + dest.name)
            expected.add(folder.name)
            self.assertTrue(folder.is_dir(), 'missing per-row archive: ' + folder.name)
            self.assertEqual((folder / 'a.bin').read_bytes(), b'original ' + bytes([i]))
            self.assertEqual((folder / 'gone.bin').read_bytes(), b'deleted ' + bytes([i]))
            self.assertEqual((dest / 'a.bin').read_bytes(), (source / 'a.bin').read_bytes())
            self.assertFalse((dest / 'gone.bin').exists())
        self.assertEqual({p.name for p in self.archive.iterdir()}, expected)
        self.assertEqual(self.legacy.read_bytes(), b'old-layout history')
        after = self.legacy.stat()
        self.assertEqual((after.st_ino, after.st_mtime_ns, after.st_mode),
                         (self.legacy_stat.st_ino, self.legacy_stat.st_mtime_ns,
                          self.legacy_stat.st_mode))
        calls = [json.loads(line) for line in (self.base / 'calls.jsonl').read_text().splitlines()]
        self.assertEqual([c[1:3] for c in calls],
                         [[str(s) + '/', str(d) + '/'] for s, d in zip(self.sources, self.dests)])


CONFINED_RCLONE = r'''
import json, os, pathlib, sys
root = pathlib.Path(os.environ['FIXTURE_ROOT']).resolve()
def local(value):
    path = pathlib.Path(value).resolve()
    if not path.is_relative_to(root):
        raise SystemExit('fixture refuses outside path: ' + value)
    return path
local(os.environ['RCLONE_CONFIG'])
args = sys.argv[1:]
if args == ['version'] or args == ['config', 'dump']:
    pass
elif args and args[0] == 'sync':
    local(args[1])
    local(args[2])
    for flag in ('--backup-dir', '--exclude-from', '--log-file'):
        local(args[args.index(flag) + 1])
    with (root / 'calls.jsonl').open('a') as stream:
        stream.write(json.dumps(args) + '\n')
else:
    raise SystemExit('fixture refuses command: ' + repr(args))
os.execv(os.environ['REAL_RCLONE'], [os.environ['REAL_RCLONE'], *args])
'''


class ConfinedRcloneTest(unittest.TestCase):
    def setUp(self):
        # [LAW:effects-at-boundaries] The exec target only records argv, even in mutants.
        self.base = Path(tempfile.mkdtemp(dir='/tmp')).resolve()
        self.addCleanup(shutil.rmtree, self.base)
        self.outside = Path(tempfile.mkdtemp(dir='/tmp')).resolve()
        self.addCleanup(shutil.rmtree, self.outside)
        self.tool = self.base / 'rclone'
        self.tool.write_text('#!' + sys.executable + '\n' + CONFINED_RCLONE)
        self.tool.chmod(0o700)
        sentinel = self.base / 'sentinel'
        sentinel.write_text('#!' + sys.executable + '\n'
                            'import json, pathlib, sys\n'
                            "pathlib.Path('sentinel.json').write_text(json.dumps(sys.argv[1:]))\n")
        sentinel.chmod(0o700)
        (self.base / 'rclone.conf').write_text('')
        (self.base / 'source').mkdir()
        (self.base / 'destination').mkdir()
        (self.base / 'archive').mkdir()
        (self.base / 'excludes').write_text('')
        (self.base / 'log').write_text('')
        self.env = dict(FIXTURE_ROOT=str(self.base),
                        RCLONE_CONFIG=str(self.base / 'rclone.conf'),
                        REAL_RCLONE=str(sentinel), HOME=str(self.base),
                        TMPDIR=str(self.base), PYTHONDONTWRITEBYTECODE='1')

    def sync_args(self):
        return ['sync', 'source', 'destination', '--backup-dir', 'archive',
                '--exclude-from', 'excludes', '--log-file', 'log']

    def run_fake(self, args):
        return subprocess.run([str(self.tool), *args], cwd=self.base, env=self.env,
                              capture_output=True, text=True, timeout=10)

    def assert_refused(self, args, message):
        # [LAW:behavior-not-structure] Refusal must precede both logging and exec.
        result = self.run_fake(args)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, message + '\n')
        self.assertFalse((self.base / 'sentinel.json').exists())
        self.assertFalse((self.base / 'calls.jsonl').exists())

    def test_refuses_outside_config(self):
        self.env['RCLONE_CONFIG'] = str(self.outside / 'rclone.conf')
        self.assert_refused(self.sync_args(),
                            f'fixture refuses outside path: {self.outside}/rclone.conf')

    def test_refuses_outside_source(self):
        args = self.sync_args()
        args[1] = str(self.outside / 'source')
        self.assert_refused(args, f'fixture refuses outside path: {self.outside}/source')

    def test_refuses_outside_destination(self):
        args = self.sync_args()
        args[2] = str(self.outside / 'destination')
        self.assert_refused(args, f'fixture refuses outside path: {self.outside}/destination')

    def test_refuses_outside_backup_dir(self):
        args = self.sync_args()
        args[4] = str(self.outside / 'archive')
        self.assert_refused(args, f'fixture refuses outside path: {self.outside}/archive')

    def test_refuses_outside_exclude_from(self):
        args = self.sync_args()
        args[6] = str(self.outside / 'excludes')
        self.assert_refused(args, f'fixture refuses outside path: {self.outside}/excludes')

    def test_refuses_outside_log_file(self):
        args = self.sync_args()
        args[8] = str(self.outside / 'log')
        self.assert_refused(args, f'fixture refuses outside path: {self.outside}/log')

    def test_refuses_lsjson(self):
        self.assert_refused(['lsjson', 'source'],
                            "fixture refuses command: ['lsjson', 'source']")

    def test_refuses_delete(self):
        self.assert_refused(['delete', 'source'],
                            "fixture refuses command: ['delete', 'source']")

    def test_refuses_symlink_destination(self):
        (self.base / 'escape').symlink_to(self.outside, target_is_directory=True)
        args = self.sync_args()
        args[2] = 'escape'
        self.assert_refused(args, 'fixture refuses outside path: escape')

    def test_accepts_sync(self):
        result = self.run_fake(self.sync_args())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        expected = ['sync', 'source', 'destination', '--backup-dir', 'archive',
                    '--exclude-from', 'excludes', '--log-file', 'log']
        self.assertEqual(json.loads((self.base / 'sentinel.json').read_text()), expected)
        self.assertTrue((self.base / 'calls.jsonl').is_file())
        self.assertEqual([json.loads(line) for line in
                          (self.base / 'calls.jsonl').read_text().splitlines()], [expected])

    def test_accepts_version(self):
        result = self.run_fake(['version'])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads((self.base / 'sentinel.json').read_text()), ['version'])
        self.assertFalse((self.base / 'calls.jsonl').exists())
