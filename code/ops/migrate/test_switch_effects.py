"""Fixture-only behavioral contract for the switch effect shell."""
import dataclasses
import errno
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import fault_kit
from ops.migrate import fdsafe
from ops.migrate.root_switch_core import BackupPair, BackupRun, Launchd, Quiesce
from ops.migrate.switch_journal_core import AgentIdentity, BackupCompare, NoIdentity, ResyncP
from ops.migrate.switch_effects import execute


FAKE = r'''import json, os, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
def within(value):
    p = pathlib.Path(value).resolve()
    if not p.is_relative_to(root):
        raise SystemExit('outside fixture: ' + value)
    return p
mode, *args = sys.argv[2:]
config = json.loads((root / 'config').read_text())
with (root / 'calls').open('a') as out:
    out.write(json.dumps([mode, args]) + '\n')
if mode == 'launch':
    verb = args[0]
    if verb == 'bootstrap':
        within(args[2])
    if verb in ('bootstrap', 'bootout'):
        if not config.get('ignore'):
            (root / 'state').write_text('loaded' if verb == 'bootstrap' else 'unloaded')
        sys.exit(config.get('command_exit', 0))
    if verb != 'print':
        raise SystemExit('bad launch verb')
    state = (root / 'state').read_text()
    if state == 'loaded':
        print('fixture service = { state = running }')
        sys.exit(0)
    print('Could not find service', file=sys.stderr)
    sys.exit(config.get('print_exit', 113))
elif mode == 'processes':
    if args != ['-axo', 'pid=,command=']:
        raise SystemExit('bad process arguments')
    if 'live_pid' in config:
        os.kill(config['live_pid'], 0)
    print(config.get('processes', ''), end='')
    sys.exit(config.get('process_exit', 0))
elif mode == 'backup':
    # BACKUP_SRC BACKUP_DEST BACKUP_EXCLUDES BACKUP_PAIRS BACKUP_RSYNC
    # BACKUP_MOUNT BACKUP_MOUNT_POINT are mandatory fixture seams.
    for key in ('BACKUP_SRC', 'BACKUP_DEST', 'BACKUP_EXCLUDES', 'BACKUP_PAIRS',
                'BACKUP_RSYNC', 'BACKUP_MOUNT', 'BACKUP_MOUNT_POINT'):
        within(os.environ[key])
    rows = within(os.environ['BACKUP_PAIRS']).read_text().splitlines()[1:]
    for i, row in enumerate(rows):
        backend, src, dst, rules = row.split('\t')
        within(src); dest = within(dst)
        within(str(pathlib.Path(os.environ['BACKUP_PAIRS']).parent / rules))
        if i == config.get('fail_pair'):
            sys.exit(23)
        (dest / '.last_success').write_text('20261022T120000\n')
    sys.exit(0)
else:
    raise SystemExit('unknown fake mode')
'''


class EffectsTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(dir='/tmp')).resolve()
        self.addCleanup(shutil.rmtree, self.root)
        self.fake = self.root / 'fake.py'
        self.fake.write_text(FAKE)
        self.config()
        (self.root / 'state').write_text('loaded')
        self.plist = self.root / 'agent.plist'
        self.plist.write_text('fixture')
        self.now = 0.0
        self.sleeps = []
        self.rules = self.root / 'rules'
        self.rules.write_text('/.deleted/\n/.last_success\n/cache/\n')
        self.pairs = []
        for i in range(2):
            src, dst = self.root / f'src{i}', self.root / f'dst{i}'
            src.mkdir(); dst.mkdir()
            (src / 'file').write_bytes(b'current')
            (dst / 'file').write_bytes(b'current')
            self.pairs.append(BackupPair('ssd', str(src), str(dst), str(self.rules)))
        self.pairs = tuple(self.pairs)
        self.table = self.root / 'pairs.tsv'
        self.table.write_text('reader\tsource\tdestination\texcludes\n' + ''.join(
            f'ssd\t{p.src}\t{p.dst}\trules\n' for p in self.pairs))

    def config(self, **values):
        import json
        (self.root / 'config').write_text(json.dumps(values))

    def command(self, mode):
        return (sys.executable, str(self.fake), str(self.root), mode)

    def sleep(self, seconds):
        self.assertGreater(seconds, 0, 'wait must make progress')
        self.sleeps.append(seconds)
        self.now += seconds

    def launch(self, action):
        return execute(action, command=self.command('launch'), domain='gui/501',
                       service='fixture.agent', plist=str(self.plist))

    def quiesce(self):
        return execute(Quiesce(), command=self.command('processes'),
                       clock=lambda: self.now, sleep=self.sleep, timeout=2.5, interval=1)

    def backup(self, action):
        seams = ('BACKUP_SRC', 'BACKUP_DEST', 'BACKUP_EXCLUDES', 'BACKUP_PAIRS',
                 'BACKUP_RSYNC', 'BACKUP_MOUNT', 'BACKUP_MOUNT_POINT')
        text = self.fake.read_text()
        for seam in seams:
            self.assertIn(seam, text, 'W7 missing seam: ' + seam)
        env = {key: str(self.root) for key in seams}
        env.update(BACKUP_SRC=self.pairs[0].src, BACKUP_DEST=self.pairs[0].dst,
                   BACKUP_EXCLUDES=str(self.rules), BACKUP_PAIRS=str(self.table),
                   BACKUP_RSYNC=str(self.fake), BACKUP_MOUNT=str(self.fake))
        for value in env.values():
            self.assertTrue(Path(value).resolve().is_relative_to(self.root))
        return execute(action, command=self.command('backup'), table=str(self.table), env=env, timeout=2)

    def compare(self, displaced=()):
        return execute(BackupCompare(self.pairs), displaced=displaced)

    def test_launch_reads_actual_state_and_is_frozen(self):
        result = self.launch(Launchd('loaded', 'unloaded'))
        self.assertEqual(result.identity, AgentIdentity('unloaded'))
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stopped, ())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            result.exit_code = 1
        self.assertEqual(self.launch(Launchd('unloaded', 'loaded')).identity, AgentIdentity('loaded'))

    def test_ignored_launch_is_not_done(self):
        self.config(ignore=True)
        result = self.launch(Launchd('loaded', 'unloaded'))
        self.assertEqual(result.identity, AgentIdentity('loaded'))
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('fixture.agent', ' '.join(result.stopped))

    def test_failed_command_even_with_expected_readback_stops(self):
        self.config(command_exit=9)
        result = self.launch(Launchd('loaded', 'unloaded'))
        self.assertEqual(result.exit_code, 9)
        self.assertTrue(result.stopped)

    def test_unknown_print_error_refuses(self):
        self.config(print_exit=5)
        with self.assertRaises(fdsafe.Refusal):
            self.launch(Launchd('loaded', 'unloaded'))

    def test_quiesce_empty_succeeds_without_sleep(self):
        result = self.quiesce()
        self.assertEqual((result.identity, result.exit_code, result.stopped), (NoIdentity(), 0, ()))
        self.assertEqual(self.sleeps, [])

    def test_each_live_process_stops_at_fake_deadline(self):
        for name in ('MemitBackup.app/Contents/MacOS/applet', 'backup_mirror.sh', 'rsync'):
            with self.subTest(name=name):
                self.now = 0
                self.sleeps = []
                child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(5)',
                                          str(self.root / name)])
                def cleanup(proc=child):
                    if proc.poll() is None:
                        proc.kill()
                    proc.wait(timeout=5)
                self.addCleanup(cleanup)
                line = f'{child.pid} {self.root}/{name}'
                self.config(processes=line + '\n', live_pid=child.pid)
                result = self.quiesce()
                self.assertEqual(result.stopped, (line,))
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(result.identity, NoIdentity())
                self.assertEqual(self.sleeps, [1, 1, .5])
                cleanup()

    def test_probe_failure_and_malformed_output_refuse(self):
        for config in ({'process_exit': 7}, {'processes': 'not-a-pid rsync\n'}):
            self.config(**config)
            with self.assertRaises(fdsafe.Refusal) as caught:
                self.quiesce()
            self.assertIn(str(self.root), str(caught.exception))

    def test_both_backup_kinds_return_each_stamp(self):
        for cls in (BackupRun, ResyncP):
            result = self.backup(cls(self.pairs))
            self.assertEqual(result.identity, NoIdentity())
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stopped, ())
            self.assertEqual(result.last_success, tuple((p.dst, b'20261022T120000\n') for p in self.pairs))

    def test_failed_second_pair_has_no_new_success(self):
        self.config(fail_pair=1)
        result = self.backup(BackupRun(self.pairs))
        self.assertEqual(result.exit_code, 23)
        self.assertEqual(result.last_success, ((self.pairs[0].dst, b'20261022T120000\n'),
                                               (self.pairs[1].dst, None)))
        self.assertFalse((Path(self.pairs[1].dst) / '.last_success').exists())
        self.assertTrue(result.stopped)

    def test_wrong_table_refuses_before_command(self):
        self.table.write_text(self.table.read_text().replace('src1', 'src0'))
        with self.assertRaises(fdsafe.Refusal):
            self.backup(BackupRun(self.pairs))
        self.assertFalse((self.root / 'calls').exists())

    def test_equal_compare_and_excluded_content(self):
        cache = Path(self.pairs[0].dst) / 'cache'
        cache.mkdir(); (cache / 'different').write_bytes(b'ignored')
        result = self.compare()
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.identity, NoIdentity())

    def test_compare_changed_file_names_it(self):
        path = Path(self.pairs[0].dst) / 'file'
        path.write_bytes(b'changed')
        result = self.compare()
        self.assertEqual(result.exit_code, 1)
        self.assertIn(str(path), ' '.join(result.stopped))

    def test_compare_missing_displaced_file_and_equal_archive(self):
        import hashlib
        pair = self.pairs[0]
        displaced = ((pair.dst, 'old', hashlib.sha256(b'old bytes').hexdigest()),)
        result = self.compare(displaced)
        self.assertEqual(result.exit_code, 1)
        self.assertIn('old', ' '.join(result.stopped))
        archive = Path(pair.dst) / '.deleted' / '20261022T120000'
        archive.mkdir(parents=True)
        (archive / 'old').write_bytes(b'wrong')
        self.assertEqual(self.compare(displaced).exit_code, 1)
        (archive / 'old').write_bytes(b'old bytes')
        self.assertEqual(self.compare(displaced).exit_code, 0)

    def test_unknown_action_refuses(self):
        with self.assertRaises(fdsafe.Refusal):
            execute(object())

    def test_excludes_fifo_refuses(self):
        with fault_kit.fifo_in_place(str(self.rules)):
            with self.assertRaises(fdsafe.Refusal):
                self.compare()

    def test_read_oserror_is_named(self):
        with fault_kit.inject_oserror('read', 1, errno.EIO):
            with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                self.compare()

    def test_named_reader_detects_parent_rebind_during_read(self):
        parent = self.root / 'rule-folder'
        parent.mkdir()
        rules = parent / 'rules'
        rules.write_bytes(self.rules.read_bytes())
        self.pairs = (dataclasses.replace(self.pairs[0], excludes=str(rules)),)
        with fault_kit.rename_and_rebind('read', 1, str(parent)):
            with self.assertRaises(fdsafe.Refusal):
                self.compare()

    def test_rules_swapped_for_link_at_open_refuse(self):
        target = self.root / 'other-rules'
        target.write_bytes(self.rules.read_bytes())
        with fault_kit.swap_for_symlink('open', 1, str(self.rules), str(target),
                                        match=lambda path, *a, **kw: path == 'rules'):
            with self.assertRaises(fdsafe.Refusal):
                self.compare()

    def test_filesystem_boundary_errors_refuse(self):
        for target in ('open', 'scandir', 'fstat', 'close', fault_kit.GETPATH):
            with self.subTest(target=target), fault_kit.inject_oserror(target, 1, errno.EIO):
                with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                    self.compare()

    def test_unrelated_process_is_clean(self):
        self.config(processes=f'321 {self.root}/ordinary-worker\n')
        self.assertEqual(self.quiesce().exit_code, 0)

    def test_live_process_disappears_after_probe(self):
        self.config(processes=f'321 {self.root}/rsync\n')
        def sleep(seconds):
            self.sleep(seconds)
            self.config()
        result = execute(Quiesce(), command=self.command('processes'), clock=lambda: self.now,
                         sleep=sleep, timeout=5, interval=1)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.sleeps, [1])

    def test_invalid_wait_budgets_refuse(self):
        for timeout, interval in ((-1, 1), (float('inf'), 1), (1, 0), (1, float('nan'))):
            with self.assertRaises(fdsafe.Refusal):
                execute(Quiesce(), command=self.command('processes'), clock=lambda: 0,
                        sleep=self.sleep, timeout=timeout, interval=interval)

    def test_zero_deadline_probes_before_stopping(self):
        self.config(processes=f'321 {self.root}/rsync\n')
        result = execute(Quiesce(), command=self.command('processes'), clock=lambda: 0,
                         sleep=self.sleep, timeout=0, interval=1)
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(self.sleeps, [])

    def test_invalid_launch_state_refuses_before_call(self):
        with self.assertRaises(fdsafe.Refusal):
            self.launch(Launchd('loaded', 'unknown'))
        self.assertFalse((self.root / 'calls').exists())

    def test_malformed_and_unsupported_tables_refuse(self):
        valid = self.table.read_text()
        for text in ('', 'wrong\n', valid.replace('reader', 'wrong'), valid.replace('ssd', 'unknown'), valid + '\n',
                     valid.replace('rules', '/rules'), valid.replace('rules', '-'),
                     valid.replace('rules', str(self.rules)),
                     valid.replace('\trules', '\t'), valid.replace('ssd', 'intel')):
            self.table.write_text(text)
            with self.assertRaises(fdsafe.Refusal):
                self.backup(BackupRun(self.pairs))
        self.assertFalse((self.root / 'calls').exists())

    def test_non_ssd_rows_are_not_executed(self):
        self.table.write_text(self.table.read_text() + 'gdrive\tunused\tunused\t-\n')
        # The fake, like the wrapper, must ignore non-ssd rows.
        self.fake.write_text(FAKE.replace("backend, src, dst, rules = row.split('\\t')",
            "backend, src, dst, rules = row.split('\\t')\n        if backend != 'ssd': continue"))
        self.assertEqual(self.backup(BackupRun(self.pairs)).exit_code, 0)

    def test_success_without_stamp_stops(self):
        self.fake.write_text(FAKE.replace("(dest / '.last_success').write_text('20261022T120000\\n')", 'pass'))
        result = self.backup(BackupRun(self.pairs))
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.last_success, tuple((p.dst, None) for p in self.pairs))
        self.assertIn('.last_success', ' '.join(result.stopped))

    def test_stale_stamp_is_reported_on_failure(self):
        path = Path(self.pairs[1].dst) / '.last_success'
        path.write_bytes(b'old stamp')
        self.config(fail_pair=1)
        result = self.backup(BackupRun(self.pairs))
        self.assertEqual(result.exit_code, 23)
        self.assertEqual(result.last_success[1], (self.pairs[1].dst, b'old stamp'))

    def test_backup_read_error_does_not_become_absence(self):
        with fault_kit.inject_oserror('read', 3, errno.EIO,
                                     match=lambda fd, *a: stat.S_ISREG(os.fstat(fd).st_mode)):
            with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                self.backup(BackupRun(self.pairs))

    def test_unexpected_backup_read_error_propagates(self):
        with fault_kit.raise_unexpected('read', 3, ValueError,
                                       match=lambda fd, *a: stat.S_ISREG(os.fstat(fd).st_mode)):
            with self.assertRaisesRegex(ValueError, 'fault_kit: unexpected'):
                self.backup(BackupRun(self.pairs))

    def test_spawn_oserror_is_a_refusal(self):
        with self.assertRaisesRegex(fdsafe.Refusal, 'ENOENT') as caught:
            execute(Quiesce(), command=(str(self.root / 'missing-command'),), clock=lambda: 0,
                    sleep=self.sleep, timeout=0, interval=1)
        self.assertIn(str(self.root), str(caught.exception))

    def test_process_timeout_is_a_refusal_not_an_unknown_exception(self):
        # Fault injection at the subprocess boundary; the effect shell runs unchanged.
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('fixture', 2)):
            with self.assertRaisesRegex(fdsafe.Refusal, 'ETIMEDOUT') as caught:
                self.quiesce()
            self.assertIn(str(self.root), str(caught.exception))
        with patch('subprocess.run', side_effect=RuntimeError('unexpected spawn error')):
            with self.assertRaisesRegex(RuntimeError, 'unexpected spawn error'):
                self.quiesce()

    def test_excludes_invalid_utf8_and_filter_syntax_refuse(self):
        for data in (b'\xff', b'+ file\n', b'- file\n', b'!\n', b'**/file\n', b'a\\b\n'):
            self.rules.write_bytes(data)
            with self.assertRaises(fdsafe.Refusal):
                self.compare()

    def test_compare_exclude_boundaries(self):
        self.rules.write_text(self.rules.read_text() + '\n# comment\n; comment\n*.tmp\n')
        for name in ('x.tmp', 'cache/ignored'):
            path = Path(self.pairs[0].dst) / name
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(b'ignore')
        self.assertEqual(self.compare().exit_code, 0)
        path = Path(self.pairs[0].dst) / 'cache-neighbor'
        path.write_bytes(b'must compare')
        self.assertEqual(self.compare().exit_code, 1)

    def test_exclude_star_cannot_cross_directory_separator(self):
        self.rules.write_text(self.rules.read_text() + '/a*.tmp\n')
        path = Path(self.pairs[0].dst) / 'a-dir' / 'nested.tmp'
        path.parent.mkdir(); path.write_bytes(b'not excluded')
        self.assertEqual(self.compare().exit_code, 1)

    def test_anchored_exclude_does_not_hide_nested_file(self):
        self.rules.write_text(self.rules.read_text() + '/only\n')
        path = Path(self.pairs[0].dst) / 'nested' / 'only'
        path.parent.mkdir(); path.write_bytes(b'must compare')
        self.assertEqual(self.compare().exit_code, 1)

    def test_directory_exclude_does_not_hide_regular_file(self):
        (Path(self.pairs[0].dst) / 'cache').write_bytes(b'must compare')
        self.assertEqual(self.compare().exit_code, 1)

    def test_unanchored_directory_excludes_nested_contents(self):
        self.rules.write_text(self.rules.read_text() + 'temp/\n')
        path = Path(self.pairs[0].dst) / 'nested' / 'temp' / 'payload'
        path.parent.mkdir(parents=True); path.write_bytes(b'excluded')
        self.assertEqual(self.compare().exit_code, 0)

    def test_multicomponent_exclude(self):
        self.rules.write_text(self.rules.read_text() + '/foo/b?r\n')
        path = Path(self.pairs[0].dst) / 'foo' / 'bar'
        path.parent.mkdir(); path.write_bytes(b'excluded')
        self.assertEqual(self.compare().exit_code, 0)

    def test_excludes_apply_to_source_too(self):
        path = Path(self.pairs[0].src) / 'cache' / 'source-only'
        path.parent.mkdir(); path.write_bytes(b'excluded')
        self.assertEqual(self.compare().exit_code, 0)

    def test_comments_are_not_exclude_rules(self):
        self.rules.write_text(self.rules.read_text() + '# comment\n')
        (Path(self.pairs[0].dst) / '# comment').write_bytes(b'must compare')
        self.assertEqual(self.compare().exit_code, 1)

    def test_missing_file_and_mode_change_fail(self):
        path = Path(self.pairs[0].dst) / 'file'
        path.rename(path.with_name('other'))
        self.assertEqual(self.compare().exit_code, 1)
        path.with_name('other').rename(path)
        path.chmod(0o700)
        self.assertEqual(self.compare().exit_code, 1)

    def test_bad_displacement_evidence_refuses(self):
        for dest, relative in ((str(self.root), 'old'), (self.pairs[0].dst, '/old'),
                               (self.pairs[0].dst, '../old'), (self.pairs[0].dst, 'a//b')):
            with self.assertRaises(fdsafe.Refusal) as caught:
                self.compare(((dest, relative, '0' * 64),))
            self.assertIn(dest, str(caught.exception))

    def test_wrong_archive_location_does_not_prove_custody(self):
        import hashlib
        dest = Path(self.pairs[0].dst)
        path = dest / 'other-archive' / 'stamp' / 'old'
        path.parent.mkdir(parents=True); path.write_bytes(b'old')
        self.rules.write_text(self.rules.read_text() + '/other-archive/\n')
        result = self.compare(((str(dest), 'old', hashlib.sha256(b'old').hexdigest()),))
        self.assertEqual(result.exit_code, 1)
        self.assertIn('.deleted/<stamp>/old', ' '.join(result.stopped))


if __name__ == '__main__':
    unittest.main()
