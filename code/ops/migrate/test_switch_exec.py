"""T414: real filesystem transactions, with deterministic process-death seams."""
import dataclasses
import errno
import fcntl
import hashlib
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import fault_kit
from ops.migrate import fdsafe, switch_exec as executor
from ops.migrate.root_switch_core import Absent, Check, FileState, Install, Rename, Replace
from ops.migrate.switch_journal_core import Done, Intent, FileIdentity, NoIdentity, parse, recover
from ops.migrate.switch_inverse_core import plan
from ops.migrate import test_switch_effects as effects_test


def digest(data):
    return hashlib.sha256(data).hexdigest()


def recover_fixture(run, seam=lambda *args: None):
    """Step 422 test driver: only journal/run observations cross into the cores."""
    journal = executor.read_journal(run)
    images = {r.action.pre.preimage: executor.preimage_hash(r.action.pre.preimage)
              for r in journal.records if isinstance(r, Intent)
              and isinstance(r.action, (Replace, Install))
              and isinstance(r.action.pre, FileState)}
    pending = journal.records[-1] if journal.records and isinstance(journal.records[-1], Intent) else None
    observation = executor.observe(pending.action) if pending else None
    state = recover(journal, observation, images)
    if state.status:
        raise fdsafe.Refusal(run, 'EIO: ' + repr(state.stopped))
    if pending:
        outcome = 'applied' if pending in state.done else 'not-applied'
        executor.append_receipt(run, Done(pending.seq, observation, outcome))
    actions = plan(state, run)
    # Stable keys are the Step 421 wire contract; QUIESCE is a fresh barrier.
    forwards = [r for r in state.done if r.direction == 'forward'
                and not isinstance(r.action, Check) and 'undo:' + str(r.seq) not in state.inverse_done]
    keys = ['barrier:' + str(len(journal.records))] + ['undo:' + str(r.seq) for r in reversed(forwards)]
    executor.execute(actions, run, direction='inverse', keys=keys,
                     effect_arguments=lambda action: dict(command=(sys.executable, '-c', ''),
                         clock=lambda: 0, sleep=lambda _: None, timeout=0, interval=1), seam=seam)


class ExecTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.root)
        self.run = self.root / 'run'
        self.run.mkdir()
        self.target = self.root / 'targets'
        self.target.mkdir()
        self.file = self.target / 'launcher'
        self.file.write_bytes(b'old\x00bytes\n')
        self.file.chmod(0o755)

    def action(self, cls=Replace, path=None):
        path = path or self.file
        pre = FileState(path.read_bytes(), digest(path.read_bytes()), stat.S_IMODE(path.stat().st_mode),
                        str(self.run / 'unused-planner-name'))
        return cls(str(path), pre, b'new\x00bytes\n', pre.mode)

    def execute(self, actions, **kwargs):
        return executor.execute(actions, str(self.run), **kwargs)

    def journal(self):
        return executor.read_journal(str(self.run))

    def child(self, code, *args):
        proc = subprocess.Popen([sys.executable, '-B', '-c', code, *map(str, args)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        def cleanup():
            if proc.poll() is None:
                proc.kill()
            proc.communicate(timeout=10)
        self.addCleanup(cleanup)
        out, err = proc.communicate(timeout=10)
        return proc.returncode, out.decode(), err.decode()

    def test_replace_install_existing_roundtrip_bytes_and_executable_mode(self):
        for cls in (Replace, Install):
            action = self.action(cls)
            before_inode = self.file.stat().st_ino
            self.execute((action,))
            records = self.journal().records
            self.assertEqual(self.file.read_bytes(), action.post_bytes)
            self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o755)
            self.assertNotEqual(self.file.stat().st_ino, before_inode)
            intent, done = records[-2:]
            self.assertEqual(done, Done(intent.seq, FileIdentity(digest(action.post_bytes), 0o755)))
            self.assertEqual(intent.action.pre.preimage, str(self.run / 'pre' / str(intent.seq)))
            self.assertEqual(Path(intent.action.pre.preimage).read_bytes(), action.pre.data)
            recover_fixture(str(self.run))
            self.assertEqual(self.file.read_bytes(), action.pre.data)
            self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o755)
            # Each transaction has its own run; a rollback is terminal.
            self.run = self.root / 'second-run'
            self.run.mkdir(exist_ok=True)

    def test_absent_install_is_moved_to_undone(self):
        path = self.target / 'new'
        self.execute((Install(str(path), Absent(), b'installed', 0o751),))
        self.assertEqual(path.read_bytes(), b'installed')
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o751)
        recover_fixture(str(self.run))
        self.assertFalse(path.exists())
        self.assertEqual((self.run / 'undone' / '1').read_bytes(), b'installed')

    def test_newer_bytes_or_mode_stop_inverse_before_target(self):
        for change in ('bytes', 'mode'):
            with self.subTest(change=change):
                self.execute((self.action(),))
                if change == 'bytes':
                    self.file.write_bytes(b'newer work')
                else:
                    self.file.chmod(0o700)
                before = self.file.read_bytes(), self.file.stat().st_mode
                with self.assertRaises(fdsafe.Refusal) as caught:
                    recover_fixture(str(self.run))
                self.assertIn(str(self.file), str(caught.exception))
                self.assertEqual((self.file.read_bytes(), self.file.stat().st_mode), before)
                self.run = self.root / ('next-' + change)
                self.run.mkdir()

    def test_preimage_corruption_stops_recovery(self):
        self.execute((self.action(),))
        (self.run / 'pre' / '1').write_bytes(b'corrupt')
        with self.assertRaisesRegex(fdsafe.Refusal, 'pre/1'):
            recover_fixture(str(self.run))
        self.assertEqual(self.file.read_bytes(), b'new\x00bytes\n')

    def test_durable_order_and_atomic_target(self):
        action = self.action()
        events = []
        real_sync = os.fsync
        def sync(fd):
            events.append(('sync', fdsafe.live_path(fd, 'sync')))
            real_sync(fd)
        def seam(point, intent):
            events.append((point, intent.seq))
            if point in ('preimage', 'intent'):
                self.assertEqual(self.file.read_bytes(), action.pre.data)
            if point in ('mutation', 'done'):
                self.assertEqual(self.file.read_bytes(), action.post_bytes)
                self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o755)
        with patch('os.fsync', side_effect=sync):
            self.execute((action,), seam=seam)
        pre = events.index(('preimage', 1))
        intent = events.index(('intent', 1))
        mutation = events.index(('mutation', 1))
        done = events.index(('done', 1))
        for path in (self.run / 'pre' / '1', self.run / 'pre'):
            self.assertIn(('sync', str(path)), events[:pre])
        self.assertIn(('sync', str(self.run)), events[:pre])
        for path in (self.run / 'journal', self.run):
            self.assertIn(('sync', str(path)), events[pre:intent])
            self.assertIn(('sync', str(path)), events[mutation:done])
        self.assertIn(('sync', str(self.target)), events[intent:mutation])
        self.assertTrue(any(e[0] == 'sync' and str(self.target) + '/' in str(e[1])
                            for e in events[intent:mutation]))

    def test_fsync_failure_never_mutates_target(self):
        before = self.file.read_bytes()
        with patch('os.fsync', side_effect=OSError(errno.EIO, 'sync failed')):
            with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                self.execute((self.action(),))
        self.assertEqual(self.file.read_bytes(), before)

    def test_short_writes_complete_preimage_journal_and_target(self):
        with fault_kit.one_byte_writes():
            self.execute((self.action(),))
        self.assertEqual(self.file.read_bytes(), b'new\x00bytes\n')
        self.assertEqual((self.run / 'pre' / '1').read_bytes(), b'old\x00bytes\n')
        self.assertEqual(len(self.journal().records), 2)

    def test_pending_and_torn_journal_refuse_new_action(self):
        class Stop(Exception):
            pass
        def seam(point, intent):
            if point == 'intent':
                raise Stop()
        with self.assertRaises(Stop):
            self.execute((self.action(),), seam=seam)
        before = (self.run / 'journal').read_bytes()
        with self.assertRaises(fdsafe.Refusal):
            self.execute((self.action(),))
        self.assertEqual((self.run / 'journal').read_bytes(), before)
        with (self.run / 'journal').open('ab') as out:
            out.write(b'["done",')
        with self.assertRaises(fdsafe.Refusal):
            self.execute((self.action(),))
        self.assertEqual(self.file.read_bytes(), b'old\x00bytes\n')

    def test_precondition_mismatch_preserves_file(self):
        action = self.action()
        self.file.write_bytes(b'newer')
        with self.assertRaisesRegex(fdsafe.Refusal, 'launcher'):
            self.execute((action,))
        self.assertEqual(self.file.read_bytes(), b'newer')

    def test_rename_collision_preserves_both(self):
        other = self.target / 'other'
        other.write_bytes(b'other')
        with self.assertRaisesRegex(fdsafe.Refusal, 'EEXIST'):
            self.execute((Rename(str(self.file), str(other)),))
        self.assertEqual(other.read_bytes(), b'other')
        self.assertEqual(self.file.read_bytes(), b'old\x00bytes\n')

    def test_interrupted_inverse_before_mutation_can_retry(self):
        self.execute((self.action(),))
        class Stop(Exception):
            pass
        def seam(point, intent):
            if point == 'intent' and intent.key == 'undo:1':
                raise Stop()
        with self.assertRaises(Stop):
            recover_fixture(str(self.run), seam)
        recover_fixture(str(self.run))
        self.assertEqual(self.file.read_bytes(), b'old\x00bytes\n')
        self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o755)

    def test_observation_and_receipt_boundaries(self):
        from ops.migrate.root_switch_core import Launchd
        self.assertIsNone(executor.preimage_hash(str(self.root / 'absent')))
        with self.assertRaisesRegex(fdsafe.Refusal, 'LAUNCHD'):
            executor.observe(Launchd('loaded', 'unloaded'))
        with self.assertRaises(fdsafe.Refusal):
            executor.append_receipt(str(self.run), Done(1, NoIdentity()))
        class Stop(Exception):
            pass
        def stop(point, intent):
            if point == 'intent':
                raise Stop()
        with self.assertRaises(Stop):
            self.execute((Check('reader'),), seam=stop)
        before = (self.run / 'journal').read_bytes()
        with self.assertRaises(fdsafe.Refusal):
            executor.append_receipt(str(self.run), Done(2, NoIdentity()))
        self.assertEqual((self.run / 'journal').read_bytes(), before)

    def test_journal_bad_encoding_and_unexpected_read_errors(self):
        path = self.run / 'journal'
        path.write_bytes(b'\xff')
        with self.assertRaisesRegex(fdsafe.Refusal, 'EILSEQ'):
            self.journal()
        with patch('os.lstat', side_effect=OSError(errno.EIO, 'stat failed')):
            with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                self.journal()
        with patch('os.lstat', side_effect=RuntimeError('unexpected stat')):
            with self.assertRaisesRegex(RuntimeError, 'unexpected stat'):
                self.journal()
        with fault_kit.raise_unexpected('read', 1, RuntimeError):
            with self.assertRaisesRegex(RuntimeError, 'unexpected'):
                self.journal()

    def test_torn_closed_journal_and_corrupt_preimage_stop_append(self):
        self.execute((self.action(),))
        path = self.run / 'journal'
        good = path.read_bytes()
        path.write_bytes(good + b'["intent",')
        with self.assertRaises(fdsafe.Refusal):
            self.execute((Check('reader'),), check=lambda _: True)
        self.assertEqual(path.read_bytes(), good + b'["intent",')
        path.write_bytes(good)
        (self.run / 'pre' / '1').write_bytes(b'bad')
        with self.assertRaisesRegex(fdsafe.Refusal, 'pre/1'):
            self.execute((Check('reader'),), check=lambda _: True)
        self.assertEqual(path.read_bytes(), good)

    def test_inverse_keys_and_length_are_required(self):
        for arguments in (dict(direction='inverse'), dict(keys=())):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((Check('reader'),), check=lambda _: True, **arguments)
        self.assertFalse((self.run / 'journal').exists())

    def test_newer_work_between_intent_and_mutation_is_kept(self):
        def seam(point, intent):
            if point == 'intent':
                self.file.write_bytes(b'newer work')
        with self.assertRaisesRegex(fdsafe.Refusal, 'ESTALE'):
            self.execute((self.action(),), seam=seam)
        self.assertEqual(self.file.read_bytes(), b'newer work')
        self.assertEqual(len(self.journal().records), 1)

    def test_rename_rebound_source_after_intent_is_kept(self):
        parked = self.target / 'parked'
        dest = self.target / 'dest'
        def seam(point, intent):
            if point == 'intent':
                self.file.rename(parked)
                self.file.write_bytes(b'new inode')
        with self.assertRaisesRegex(fdsafe.Refusal, 'ESTALE'):
            self.execute((Rename(str(self.file), str(dest)),), seam=seam)
        self.assertEqual(self.file.read_bytes(), b'new inode')
        self.assertFalse(dest.exists())

    def test_journal_open_collisions_and_inode_rebind(self):
        real_open = os.open
        path = self.run / 'journal'
        created = False
        def collision(name, flags, *args, **kwargs):
            nonlocal created
            if name == 'journal' and flags & os.O_WRONLY and not created:
                created = True
                path.write_bytes(b'other writer')
            return real_open(name, flags, *args, **kwargs)
        with patch('os.open', side_effect=collision):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((Check('reader'),), check=lambda _: True)
        self.assertTrue(created)
        self.assertEqual(path.read_bytes(), b'other writer')
        path.write_bytes(b'')
        fired = False
        def rebind(name, flags, *args, **kwargs):
            nonlocal fired
            if name == 'journal' and flags & os.O_WRONLY and not fired:
                fired = True
                path.rename(self.run / 'parked-journal')
                path.write_bytes(b'new owner')
            return real_open(name, flags, *args, **kwargs)
        with patch('os.open', side_effect=rebind):
            with self.assertRaisesRegex(fdsafe.Refusal, 'ESTALE'):
                self.execute((Check('reader'),), check=lambda _: True)
        self.assertTrue(fired)
        self.assertEqual(path.read_bytes(), b'new owner')

    def test_journal_symlink_to_scanned_inode_refuses(self):
        path = self.run / 'journal'
        path.write_bytes(b'')
        real_open = os.open
        fired = False
        def rebind(name, flags, *args, **kwargs):
            nonlocal fired
            if name == 'journal' and flags & os.O_WRONLY and not fired:
                fired = True
                path.rename(self.run / 'parked-journal')
                path.symlink_to(self.run / 'parked-journal')
            return real_open(name, flags, *args, **kwargs)
        with patch('os.open', side_effect=rebind):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((Check('reader'),), check=lambda _: True)
        self.assertTrue(fired)
        self.assertEqual((self.run / 'parked-journal').read_bytes(), b'')

    def test_fifo_at_journal_write_open_refuses(self):
        path = self.run / 'journal'
        path.write_bytes(b'')
        with fault_kit.fifo_in_place(str(path), name='open', match=lambda name, flags, *a, **kw:
                                    name == 'journal' and flags & os.O_WRONLY, timeout=2):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((Check('reader'),), check=lambda _: True)

    def test_write_boundary_oserrors_are_named(self):
        action = self.action()
        for label, target, match in (
                ('pre', 'open', lambda name, flags, *a, **kw: name == '1' and flags & os.O_WRONLY),
                ('journal', 'open', lambda name, flags, *a, **kw: name == 'journal' and flags & os.O_WRONLY)):
            with self.subTest(label=label), fault_kit.inject_oserror(target, 1, errno.EIO, match=match):
                with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                    self.execute((action,))
            self.run = self.root / ('run-' + label)
            self.run.mkdir()
        with patch('os.fchmod', side_effect=OSError(errno.EIO, 'chmod')):
            with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                self.execute((action,))
        self.run = self.root / 'run-replace'
        self.run.mkdir()
        with patch('os.replace', side_effect=OSError(errno.EIO, 'replace')):
            with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                self.execute((action,))

    def test_interrupt_closes_created_descriptors(self):
        for target in ('directory', 'file'):
            with self.subTest(target=target):
                fds = set()
                real_open, real_close = os.open, os.close
                def opened(*args, **kwargs):
                    fd = real_open(*args, **kwargs)
                    fds.add(fd)
                    return fd
                def closed(fd):
                    real_close(fd)
                    fds.discard(fd)
                action = self.action()
                operation = 'os.fsync' if target == 'directory' else 'os.fchmod'
                with patch('os.open', side_effect=opened), patch('os.close', side_effect=closed), \
                        patch(operation, side_effect=KeyboardInterrupt):
                    with self.assertRaises(KeyboardInterrupt):
                        self.execute((action,))
                leaked = tuple(fds)
                for fd in leaked:
                    real_close(fd)
                self.assertEqual(leaked, ())
                self.run = self.root / ('after-' + target)
                self.run.mkdir()

    def test_check_failure_has_intent_without_done(self):
        with self.assertRaisesRegex(fdsafe.Refusal, 'reader'):
            self.execute((Check('reader'),), check=lambda name: False)
        self.assertEqual(len(self.journal().records), 1)
        self.assertEqual(self.journal().records[0].action, Check('reader'))

    def test_successful_check_records_no_identity(self):
        seen = []
        receipts = self.execute((Check('reader'),), check=lambda name: seen.append(name) or True)
        self.assertEqual(seen, ['reader'])
        self.assertEqual(receipts, (Done(1, NoIdentity()),))
        self.assertEqual(self.journal().records[-1], Done(1, NoIdentity()))

    def test_missing_check_runner_refuses(self):
        with self.assertRaisesRegex(fdsafe.Refusal, 'caller must supply'):
            self.execute((Check('reader'),))

    def test_restrictive_umask_does_not_change_target_mode(self):
        original = os.umask(0o077)
        self.addCleanup(os.umask, original)
        self.execute((self.action(),))
        self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o755)

    def test_normal_execution_closes_every_descriptor(self):
        opened_fds = set()
        real_open, real_close = os.open, os.close
        def opened(*args, **kwargs):
            fd = real_open(*args, **kwargs)
            opened_fds.add(fd)
            return fd
        def closed(fd):
            real_close(fd)
            opened_fds.discard(fd)
        with patch('os.open', side_effect=opened), patch('os.close', side_effect=closed):
            self.execute((self.action(),))
        leaked = tuple(opened_fds)
        for fd in leaked:
            real_close(fd)
        self.assertEqual(leaked, ())

    def test_move_syncs_both_parents_and_reports_observed_inode(self):
        other = self.root / 'destination'
        other.mkdir()
        target = other / 'launcher'
        calls = []
        real = os.fsync
        def sync(fd):
            calls.append(fdsafe.live_path(fd, 'fsync'))
            real(fd)
        with patch('os.fsync', side_effect=sync):
            self.execute((Rename(str(self.file), str(target)),))
        self.assertIn(str(self.target), calls)
        self.assertIn(str(other), calls)
        self.assertEqual(target.read_bytes(), b'old\x00bytes\n')
        self.assertEqual(self.journal().records[1].post.dst.st_ino, target.stat().st_ino)

    def test_moved_preimage_during_write_stops_before_target(self):
        action = self.action()
        path = self.run / 'pre' / '1'
        parked = self.root / 'displaced-preimage'
        real = os.write
        fired = False
        def write(fd, data):
            nonlocal fired
            result = real(fd, data)
            if fdsafe.live_path(fd, 'write') == str(path) and not fired:
                fired = True
                path.rename(parked)
            return result
        with patch('os.write', side_effect=write):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((action,))
        self.assertTrue(fired)
        self.assertEqual(self.file.read_bytes(), action.pre.data)

    def test_bad_readback_identity_is_not_recorded_as_done(self):
        action = self.action()
        # Fault at the filesystem read boundary, not a mocked executor result.
        real_read = os.read
        def read(fd, count):
            data = real_read(fd, count)
            if data == action.post_bytes:
                return b'bad\x00bytes\n'
            return data
        with patch('os.read', side_effect=read):
            with self.assertRaisesRegex(fdsafe.Refusal, 'post-identity'):
                self.execute((action,))
        self.assertEqual(len(self.journal().records), 1)

    def test_corrupt_preimage_between_actions_stops_before_next_target(self):
        second = self.target / 'second'
        second.write_bytes(b'second original')
        first_action, second_action = self.action(), self.action(path=second)
        def seam(point, intent):
            if point == 'done' and intent.seq == 1:
                (self.run / 'pre' / '1').write_bytes(b'corrupt')
        with self.assertRaisesRegex(fdsafe.Refusal, 'pre/1'):
            self.execute((first_action, second_action), seam=seam)
        self.assertEqual(second.read_bytes(), b'second original')

    def test_inverse_keeps_newer_work_at_replace_boundary(self):
        self.execute((self.action(),))
        real_replace = os.replace
        fired = False
        def newer_work(src, dst, *args, **kwargs):
            nonlocal fired
            if dst == self.file.name and not fired:
                fired = True
                self.file.write_bytes(b'newer work at replacement')
            return real_replace(src, dst, *args, **kwargs)
        with patch('os.replace', side_effect=newer_work):
            with self.assertRaises(fdsafe.Refusal) as caught:
                recover_fixture(str(self.run))
        self.assertIn(str(self.file), str(caught.exception))
        self.assertIn('newer work written during the replace; restored', str(caught.exception))
        self.assertTrue(fired, 'the positive-control write must run')
        self.assertEqual(self.file.read_bytes(), b'newer work at replacement')
        pending = self.journal().records[-1]
        self.assertIsInstance(pending, Intent)
        self.assertEqual(pending.key, 'undo:1')
        self.assertFalse(any(isinstance(r, Done) and r.seq == pending.seq for r in self.journal().records))

    def test_forward_keeps_newer_work_at_replace_boundary(self):
        action = self.action()
        real_replace = os.replace
        fired = False
        def newer_work(src, dst, *args, **kwargs):
            nonlocal fired
            if dst == self.file.name and not fired:
                fired = True
                self.file.write_bytes(b'newer work at replacement')
                self.file.chmod(0o700)
            return real_replace(src, dst, *args, **kwargs)
        with patch('os.replace', side_effect=newer_work):
            with self.assertRaises(fdsafe.Refusal) as caught:
                self.execute((action,))
        self.assertIn(str(self.file), str(caught.exception))
        self.assertIn('newer work written during the replace; restored', str(caught.exception))
        self.assertTrue(fired, 'the positive-control write must run')
        self.assertEqual(self.file.read_bytes(), b'newer work at replacement')
        self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o700)
        self.assertEqual(len(self.journal().records), 1)
        self.assertIsInstance(self.journal().records[0], Intent)

    def test_existing_install_keeps_newer_work_in_both_directions(self):
        for inverse in (False, True):
            with self.subTest(inverse=inverse):
                action = self.action(Install)
                if inverse:
                    self.execute((action,))
                real_replace = os.replace
                fired = False
                def newer_work(src, dst, *args, **kwargs):
                    nonlocal fired
                    if dst == self.file.name and not fired:
                        fired = True
                        self.file.chmod(0o600)
                    return real_replace(src, dst, *args, **kwargs)
                before = self.file.read_bytes()
                with patch('os.replace', side_effect=newer_work):
                    with self.assertRaisesRegex(fdsafe.Refusal, 'newer work.*restored') as caught:
                        if inverse:
                            recover_fixture(str(self.run))
                        else:
                            self.execute((action,))
                self.assertIn(str(self.file), str(caught.exception))
                self.assertTrue(fired)
                self.assertEqual(self.file.read_bytes(), before)
                self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o600)
                self.assertIsInstance(self.journal().records[-1], Intent)
                self.file.chmod(0o755)
                self.run = self.root / 'install-inverse'
                self.run.mkdir(exist_ok=True)

    def test_held_read_refuses_nonregular_and_changing_bytes(self):
        action = self.action()
        real_open = os.open
        active = False
        def seam(point, intent):
            nonlocal active
            active = point == 'intent'
        def opened(name, flags, *args, **kwargs):
            if active and name == self.file.name:
                self.file.rename(self.target / 'saved')
                self.file.mkdir()
            return real_open(name, flags, *args, **kwargs)
        with patch('os.open', side_effect=opened):
            with self.assertRaisesRegex(fdsafe.Refusal, 'regular file'):
                self.execute((action,), seam=seam)
        self.assertEqual((self.target / 'saved').read_bytes(), action.pre.data)

    def test_held_read_detects_write_during_read(self):
        action = self.action()
        active = False
        fired = False
        real_read = os.read
        def seam(point, intent):
            nonlocal active
            active = point == 'intent'
        def read(fd, count):
            nonlocal fired
            data = real_read(fd, count)
            if active and not fired and data == action.pre.data:
                fired = True
                self.file.write_bytes(b'changed during read')
            return data
        with patch('os.read', side_effect=read):
            with self.assertRaisesRegex(fdsafe.Refusal, 'changed while read'):
                self.execute((action,), seam=seam)
        self.assertTrue(fired)
        self.assertEqual(self.file.read_bytes(), b'changed during read')
        self.assertEqual(len(self.journal().records), 1)

    def test_journal_schema_refusal_is_not_encoding_failure(self):
        (self.run / 'journal').write_bytes(b'[]\n')
        with self.assertRaises(fdsafe.Refusal) as caught:
            self.journal()
        self.assertIn('EINVAL', str(caught.exception))
        self.assertNotIn('EILSEQ', str(caught.exception))

    def test_receipt_requires_matching_done_type(self):
        class Stop(Exception):
            pass
        def stop(point, intent):
            if point == 'intent':
                raise Stop()
        with self.assertRaises(Stop):
            self.execute((Check('reader'),), seam=stop)
        before = (self.run / 'journal').read_bytes()
        with self.assertRaisesRegex(fdsafe.Refusal, 'receipt does not close pending intent'):
            executor.append_receipt(str(self.run), self.journal().records[-1])
        self.assertEqual((self.run / 'journal').read_bytes(), before)

    def test_receipt_validates_post_before_append(self):
        class Stop(Exception):
            pass
        def stop(point, intent):
            if point == 'intent':
                raise Stop()
        with self.assertRaises(Stop):
            self.execute((self.action(),), seam=stop)
        before = (self.run / 'journal').read_bytes()
        with self.assertRaises(fdsafe.Refusal):
            executor.append_receipt(str(self.run), Done(1, NoIdentity()))
        self.assertEqual((self.run / 'journal').read_bytes(), before)

    def test_empty_batch_still_validates_closed_journal(self):
        self.execute((self.action(),))
        (self.run / 'pre' / '1').write_bytes(b'bad')
        with self.assertRaisesRegex(fdsafe.Refusal, 'pre/1'):
            self.execute(())

    def test_generator_actions_and_duplicate_keys(self):
        self.execute((Check(name) for name in ('one', 'two')), check=lambda _: True)
        self.assertEqual([r.action.check_id for r in self.journal().records if isinstance(r, Intent)], ['one', 'two'])
        with self.assertRaisesRegex(fdsafe.Refusal, 'duplicate operation'):
            self.execute((Check('three'), Check('four')), keys=('same', 'same'), check=lambda _: True)
        self.assertEqual(len(self.journal().records), 6)
        self.assertEqual(executor.observe(Check('reader')), NoIdentity())

    def test_observation_refuses_parent_moved_during_read(self):
        action = self.action()
        with fault_kit.rename_and_rebind('read', 1, str(self.target)):
            with self.assertRaises(fdsafe.Refusal):
                executor.observe(action)

    def test_observation_checks_parent_before_leaf_open(self):
        action = self.action()
        real_stat, real_open = os.lstat, os.open
        opened = []
        fired = False
        def scan(name, *args, **kwargs):
            nonlocal fired
            result = real_stat(name, *args, **kwargs)
            if name == self.file.name and not fired:
                fired = True
                self.target.rename(self.root / 'moved')
                self.target.mkdir()
            return result
        def opening(name, *args, **kwargs):
            opened.append(name)
            return real_open(name, *args, **kwargs)
        with patch('os.lstat', side_effect=scan), patch('os.open', side_effect=opening):
            with self.assertRaises(fdsafe.Refusal):
                executor.observe(action)
        self.assertTrue(fired)
        self.assertNotIn(self.file.name, opened)

    def test_rename_observation_refuses_rebound_parent(self):
        real_stat = os.lstat
        fired = False
        def scan(name, *args, **kwargs):
            nonlocal fired
            result = real_stat(name, *args, **kwargs)
            if name == self.file.name and not fired:
                fired = True
                self.target.rename(self.root / 'moved')
                self.target.mkdir()
            return result
        with patch('os.lstat', side_effect=scan):
            with self.assertRaises(fdsafe.Refusal):
                executor.observe(Rename(str(self.file), str(self.root / 'dest')))
        self.assertTrue(fired)

    def test_each_replace_syncs_parent_after_rename(self):
        for absent in (False, True):
            with self.subTest(absent=absent):
                events = []
                real_replace, real_sync = os.replace, os.fsync
                real_exclusive = fdsafe._rename_noreplace
                def moved(src, dst, *args, **kwargs):
                    result = real_replace(src, dst, *args, **kwargs)
                    events.append(('rename', dst))
                    return result
                def exclusive(src, dst, **kwargs):
                    result = real_exclusive(src, dst, **kwargs)
                    events.append(('rename', dst))
                    return result
                def synced(fd):
                    events.append(('sync', fdsafe.live_path(fd, 'sync')))
                    return real_sync(fd)
                target = self.target / 'new' if absent else self.file
                action = Install(str(target), Absent(), b'new', 0o755) if absent else self.action()
                with patch('os.replace', side_effect=moved), patch('os.fsync', side_effect=synced), \
                        patch.object(fdsafe, '_rename_noreplace', side_effect=exclusive):
                    self.execute((action,))
                index = events.index(('rename', target.name))
                self.assertIn(('sync', str(self.target)), events[index+1:])

    def test_newly_written_target_moved_away_refuses(self):
        for absent in (False, True):
            with self.subTest(absent=absent):
                target = self.target / 'new' if absent else self.file
                action = Install(str(target), Absent(), b'new', 0o755) if absent else self.action()
                real_replace, real_exclusive = os.replace, fdsafe._rename_noreplace
                fired = False
                def after(call, src, dst, **kwargs):
                    nonlocal fired
                    result = call(src, dst, **kwargs)
                    if dst == target.name and not fired:
                        fired = True
                        target.rename(self.target / ('parked-' + str(absent)))
                        target.write_bytes(action.post_bytes)
                        target.chmod(action.post_mode)
                    return result
                with patch('os.replace', side_effect=lambda s, d, **kw: after(real_replace, s, d, **kw)), \
                        patch.object(fdsafe, '_rename_noreplace', side_effect=lambda s, d, **kw: after(real_exclusive, s, d, **kw)):
                    with self.assertRaises(fdsafe.Refusal):
                        self.execute((action,))
                self.assertTrue(fired)
                self.assertIsInstance(self.journal().records[-1], Intent)
                self.run = self.root / 'run-absent'
                self.run.mkdir(exist_ok=True)

    def test_journal_moved_during_write_refuses(self):
        real_write = os.write
        fired = False
        def write(fd, data):
            nonlocal fired
            result = real_write(fd, data)
            if not fired and fdsafe.live_path(fd, 'write') == str(self.run / 'journal'):
                fired = True
                (self.run / 'journal').rename(self.run / 'moved-journal')
            return result
        with patch('os.write', side_effect=write):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((Check('reader'),), check=lambda _: True)
        self.assertTrue(fired)

    def test_settlement_move_stops_before_sync(self):
        for relative in ('pre/1', 'journal', 'target-temp', 'target-final', 'absent-final'):
            with self.subTest(relative=relative):
                base = self.root / relative.replace('/', '-')
                base.mkdir()
                run = base / 'run'
                run.mkdir()
                target_dir = base / 'target'
                target_dir.mkdir()
                target = target_dir / 'file'
                target.write_bytes(b'old')
                pre = FileState(b'old', digest(b'old'), 0o644, str(run / 'unused'))
                action = Replace(str(target), pre, b'new', 0o644)
                watched = run / relative
                if relative == 'target-temp':
                    watched = target_dir / '.switch-1'
                elif relative == 'target-final':
                    watched = target
                elif relative == 'absent-final':
                    watched = target_dir / 'new'
                    action = Install(str(watched), Absent(), b'new', 0o644)
                parent = watched.parent
                parked = base / 'moved'
                previous = None
                fired = False
                unsafe_sync = []
                real_fcntl, real_sync = fcntl.fcntl, os.fsync
                def query(fd, op, *args):
                    nonlocal previous, fired
                    result = real_fcntl(fd, op, *args)
                    if op == fcntl.F_GETPATH:
                        live = os.fsdecode(result.split(b'\0', 1)[0])
                        if previous == str(watched) and live == str(parent) and not fired:
                            fired = True
                            parent.rename(parked)
                            parent.mkdir()
                        previous = live
                    return result
                def sync(fd):
                    live = os.fsdecode(real_fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b'\0', 1)[0])
                    if fired and (live == str(parked) or live.startswith(str(parked) + '/')):
                        unsafe_sync.append(live)
                    return real_sync(fd)
                with patch('fcntl.fcntl', side_effect=query), patch('os.fsync', side_effect=sync):
                    with self.assertRaises(fdsafe.Refusal):
                        executor.execute((action,), str(run))
                self.assertTrue(fired)
                self.assertEqual(unsafe_sync, [])

    def test_target_parent_checks_before_create_open_and_rename(self):
        for boundary in ('create', 'open', 'rename'):
            with self.subTest(boundary=boundary):
                base = self.root / boundary
                base.mkdir()
                run = base / 'run'
                run.mkdir()
                target_dir = base / 'target'
                target_dir.mkdir()
                target = target_dir / 'file'
                target.write_bytes(b'old')
                pre = FileState(b'old', digest(b'old'), 0o644, str(run / 'unused'))
                action = Replace(str(target), pre, b'new', 0o644)
                active = False
                fired = False
                bad = []
                real_fcntl, real_sync, real_read, real_open, real_replace = fcntl.fcntl, os.fsync, os.read, os.open, os.replace
                parked = base / 'moved'
                def move():
                    nonlocal fired
                    fired = True
                    target_dir.rename(parked)
                    target_dir.mkdir()
                def seam(point, intent):
                    nonlocal active
                    active = point == 'intent'
                def query(fd, op, *args):
                    result = real_fcntl(fd, op, *args)
                    if boundary == 'create' and active and not fired and op == fcntl.F_GETPATH and os.fsdecode(result.split(b'\0', 1)[0]) == str(target_dir):
                        move()
                    return result
                def sync(fd):
                    result = real_sync(fd)
                    if boundary == 'open' and active and not fired and stat.S_ISDIR(os.fstat(fd).st_mode):
                        move()
                    return result
                def read(fd, count):
                    result = real_read(fd, count)
                    if boundary == 'rename' and active and not fired and result == b'':
                        move()
                    return result
                def opening(name, flags, *args, **kwargs):
                    if fired and ((boundary == 'create' and flags & os.O_CREAT) or (boundary == 'open' and name == 'file')):
                        bad.append('open')
                    return real_open(name, flags, *args, **kwargs)
                def replacing(*args, **kwargs):
                    if fired:
                        bad.append('replace')
                    return real_replace(*args, **kwargs)
                with patch('fcntl.fcntl', side_effect=query), patch('os.fsync', side_effect=sync), \
                        patch('os.read', side_effect=read), patch('os.open', side_effect=opening), patch('os.replace', side_effect=replacing):
                    with self.assertRaises(fdsafe.Refusal):
                        executor.execute((action,), str(run), seam=seam)
                self.assertTrue(fired)
                self.assertEqual(bad, [])

    def test_w17_restoration_closes_every_descriptor(self):
        action = self.action()
        fds = set()
        real_open, real_close, real_replace = os.open, os.close, os.replace
        fired = False
        def opened(*args, **kwargs):
            fd = real_open(*args, **kwargs)
            fds.add(fd)
            return fd
        def closed(fd):
            real_close(fd)
            fds.discard(fd)
        def replaced(src, dst, **kwargs):
            nonlocal fired
            if not fired:
                fired = True
                self.file.write_bytes(b'newer')
            return real_replace(src, dst, **kwargs)
        with patch('os.open', side_effect=opened), patch('os.close', side_effect=closed), patch('os.replace', side_effect=replaced):
            with self.assertRaisesRegex(fdsafe.Refusal, 'newer work.*restored'):
                self.execute((action,))
        leaked = tuple(fds)
        for fd in leaked:
            real_close(fd)
        self.assertEqual(leaked, ())

    def test_absent_install_collision_stops_at_identity_check(self):
        target = self.target / 'new'
        def seam(point, intent):
            if point == 'intent':
                target.write_bytes(b'new owner')
        with self.assertRaisesRegex(fdsafe.Refusal, 'ESTALE: target changed after intent'):
            self.execute((Install(str(target), Absent(), b'ours', 0o644),), seam=seam)
        self.assertEqual(target.read_bytes(), b'new owner')
        self.assertEqual(len(self.journal().records), 1)

    def test_absent_install_checks_parent_immediately_before_rename(self):
        target = self.target / 'new'
        real_stat = os.lstat
        active = False
        fired = False
        def seam(point, intent):
            nonlocal active
            active = point == 'intent'
        def scan(name, *args, **kwargs):
            nonlocal fired
            try:
                return real_stat(name, *args, **kwargs)
            except FileNotFoundError:
                if active and name == target.name and not fired:
                    fired = True
                    self.target.rename(self.root / 'moved-target')
                    self.target.mkdir()
                raise
        with patch('os.lstat', side_effect=scan):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((Install(str(target), Absent(), b'ours', 0o644),), seam=seam)
        self.assertTrue(fired)
        self.assertFalse((self.root / 'moved-target' / 'new').exists())
        self.assertEqual(len(self.journal().records), 1)

    def test_forward_does_not_create_undone(self):
        self.execute((self.action(),))
        self.assertFalse((self.run / 'undone').exists())

    def test_nonregular_journal_at_append_is_named(self):
        def seam(point, intent):
            if point == 'preimage':
                os.mkfifo(self.run / 'journal')
        with self.assertRaisesRegex(fdsafe.Refusal, 'journal is not a regular file'):
            self.execute((self.action(),), seam=seam)
        self.assertEqual(self.file.read_bytes(), b'old\x00bytes\n')

    def test_append_checks_parent_before_write_open(self):
        (self.run / 'journal').write_bytes(b'')
        real_stat, real_open = os.lstat, os.open
        scans = 0
        fired = False
        bad = []
        def scan(name, *args, **kwargs):
            nonlocal scans, fired
            result = real_stat(name, *args, **kwargs)
            if name == 'journal':
                scans += 1
                if scans == 2:
                    fired = True
                    self.run.rename(self.root / 'moved-run')
                    self.run.mkdir()
            return result
        def opened(name, flags, *args, **kwargs):
            if fired and name == 'journal' and flags & os.O_WRONLY:
                bad.append(name)
            return real_open(name, flags, *args, **kwargs)
        with patch('os.lstat', side_effect=scan), patch('os.open', side_effect=opened):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((Check('reader'),), check=lambda _: True)
        self.assertTrue(fired)
        self.assertEqual(bad, [])

    def test_w17_and_absent_install_oserrors_name_target(self):
        for boundary in ('seek', 'held-open', 'exclusive-rename'):
            with self.subTest(boundary=boundary):
                self.target = self.root / ('target-' + boundary)
                self.target.mkdir()
                self.file = self.target / 'launcher'
                self.file.write_bytes(b'old\x00bytes\n')
                self.file.chmod(0o755)
                target = self.target / 'new' if boundary == 'exclusive-rename' else self.file
                action = Install(str(target), Absent(), b'ours', 0o644) if boundary == 'exclusive-rename' else self.action()
                active = False
                fired = False
                real_open = os.open
                def seam(point, intent):
                    nonlocal active
                    active = point == 'intent'
                def failure(*args, **kwargs):
                    nonlocal fired
                    fired = True
                    raise OSError(errno.EIO, 'injected boundary failure')
                def opened(name, flags, *args, **kwargs):
                    if active and name == target.name:
                        return failure()
                    return real_open(name, flags, *args, **kwargs)
                operation = {'seek': 'os.lseek', 'held-open': 'os.open',
                             'exclusive-rename': 'ops.migrate.fdsafe._rename_noreplace'}[boundary]
                with patch(operation, side_effect=opened if boundary == 'held-open' else failure):
                    with self.assertRaises(fdsafe.Refusal) as caught:
                        self.execute((action,), seam=seam)
                self.assertTrue(fired)
                self.assertIn(str(target), str(caught.exception))
                self.assertEqual(caught.exception.errno, errno.EIO)
                self.assertEqual(len(self.journal().records), 1)
                self.assertEqual(self.file.read_bytes(), b'old\x00bytes\n')
                self.assertFalse((self.target / 'new').exists())
                self.run = self.root / ('after-' + boundary)
                self.run.mkdir()

    def test_fault_kit_io_errors_and_unexpected_errors(self):
        action = self.action()
        for target in ('open', 'read', 'write', 'fstat', 'close', fault_kit.GETPATH, 'mkdir'):
            with self.subTest(target=target), fault_kit.inject_oserror(target, 1, errno.EIO):
                with self.assertRaisesRegex(fdsafe.Refusal, 'EIO'):
                    self.execute((action,))
            self.run = self.root / ('run-' + target)
            self.run.mkdir()
        with fault_kit.raise_unexpected('read', 1, RuntimeError):
            with self.assertRaisesRegex(RuntimeError, 'unexpected'):
                self.execute((action,))

    def test_symlink_fifo_and_rebound_parent_refuse(self):
        action = self.action()
        other = self.root / 'other'
        other.write_bytes(b'untouched')
        with fault_kit.swap_for_symlink('open', 1, str(self.file), str(other),
                                      match=lambda path, *a, **kw: path == self.file.name):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((action,))
        self.assertEqual(other.read_bytes(), b'untouched')

    def test_fifo_refuses_without_blocking(self):
        action = self.action()
        with fault_kit.fifo_in_place(str(self.file)):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((action,))

    def test_rebound_parent_during_read_refuses(self):
        action = self.action()
        with fault_kit.rename_and_rebind('read', 1, str(self.target)):
            with self.assertRaises(fdsafe.Refusal):
                self.execute((action,))

    def test_process_deaths_and_fresh_recovery(self):
        for point, number, rename in (('preimage', 1, False), ('intent', 1, False),
                                      ('mutation', 1, False), ('mutation', 1, True),
                                      ('done', 3, False), ('rollback', 3, False)):
            with self.subTest(point=point, number=number, rename=rename):
                base = self.root / (point + str(rename))
                base.mkdir()
                run = base / 'run'
                run.mkdir()
                original = {}
                for i in range(6):
                    path = base / f'lane{i}' / '.git'
                    path.parent.mkdir()
                    path.write_bytes(b'gitdir: M\n')
                    path.chmod(0o755 if i == 0 else 0o640)
                    original[str(path)] = (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
                code = '''from pathlib import Path
import os, signal, stat, sys
from ops.migrate.test_switch_exec import digest, recover_fixture
from ops.migrate import switch_exec as e
from ops.migrate.root_switch_core import FileState, Replace, Rename
base, point, number, rename = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4] == 'True'
run = str(base / 'run')
def seam(at, intent):
    if at == point and intent.seq == number:
        os.kill(os.getpid(), signal.SIGKILL)
actions = []
for i in range(6):
    p = base / f'lane{i}' / '.git'
    pre = FileState(p.read_bytes(), digest(p.read_bytes()), stat.S_IMODE(p.stat().st_mode), str(base / 'unused'))
    actions.append(Replace(str(p), pre, b'gitdir: R\\n', pre.mode))
if rename:
    actions = [Rename(str(base / 'lane0'), str(base / 'moved'))]
e.execute(actions, run, seam=seam)
if point == 'rollback':
    def kill(at, intent):
        if at == 'mutation' and intent.direction == 'inverse' and intent.key == 'undo:6':
            os.kill(os.getpid(), signal.SIGKILL)
    recover_fixture(run, kill)
'''
                result = self.child(code, base, point, number, rename)
                self.assertEqual(result[0], -signal.SIGKILL, result)
                result = self.child('import sys; from ops.migrate.test_switch_exec import recover_fixture; recover_fixture(sys.argv[1])', run)
                self.assertEqual(result[0], 0, result)
                for path, expected in original.items():
                    self.assertEqual((Path(path).read_bytes(), stat.S_IMODE(Path(path).stat().st_mode)), expected)


class EffectJournalTest(unittest.TestCase):
    """Reuse Step 423's exact fakes; exercise the executor around real effects."""
    config = effects_test.EffectsTest.config
    command = effects_test.EffectsTest.command
    sleep = effects_test.EffectsTest.sleep
    child = ExecTest.child

    def setUp(self):
        effects_test.EffectsTest.setUp(self)
        self.run = self.root / 'run'
        self.run.mkdir()

    def test_executor_wraps_each_effect_in_durable_records(self):
        from ops.migrate.root_switch_core import BackupRun, Launchd, Quiesce
        from ops.migrate.switch_journal_core import BackupCompare, ResyncP
        actions = (Launchd('loaded', 'unloaded'), Quiesce(), BackupRun(self.pairs),
                   ResyncP(self.pairs), BackupCompare(self.pairs))
        def arguments(action):
            if isinstance(action, Launchd):
                return dict(command=self.command('launch'), domain='gui/501', service='fixture.agent', plist=str(self.plist))
            if isinstance(action, Quiesce):
                return dict(command=self.command('processes'), clock=lambda: 0, sleep=self.sleep, timeout=0, interval=1)
            if isinstance(action, BackupCompare):
                return dict(displaced=())
            seams = ('BACKUP_SRC', 'BACKUP_DEST', 'BACKUP_EXCLUDES', 'BACKUP_PAIRS', 'BACKUP_RSYNC', 'BACKUP_MOUNT', 'BACKUP_MOUNT_POINT')
            for name in seams:
                self.assertIn(name, self.fake.read_text())
            return dict(command=self.command('backup'), table=str(self.table), env={name: str(self.root) for name in seams}, timeout=2)
        for i, action in enumerate(actions):
            executor.execute((action,), str(self.run), direction='inverse' if i >= 3 else 'forward',
                             keys=(str(i),), effect_arguments=arguments)
        records = executor.read_journal(str(self.run)).records
        self.assertEqual(len(records), 10)
        self.assertEqual([r.action for r in records[::2]], list(actions))
        self.assertEqual((self.root / 'state').read_text(), 'unloaded')
        self.assertTrue(all(isinstance(r, Done) for r in records[1::2]))

    def test_failed_effect_leaves_pending_intent(self):
        from ops.migrate.root_switch_core import Launchd
        self.config(ignore=True)
        with self.assertRaisesRegex(fdsafe.Refusal, 'fixture.agent'):
            executor.execute((Launchd('loaded', 'unloaded'),), str(self.run), effect_arguments=lambda a:
                             dict(command=self.command('launch'), domain='gui/501', service='fixture.agent', plist=str(self.plist)))
        self.assertEqual(len(executor.read_journal(str(self.run)).records), 1)

    def test_kill_during_rollback_resync_recovers_in_new_process(self):
        from ops.migrate.root_switch_core import BackupRun
        from ops.migrate.switch_journal_core import ResyncP, BackupCompare
        pair = self.pairs[0]
        self.table.write_text('reader\tsource\tdestination\texcludes\n' +
                              f'ssd\t{pair.src}\t{pair.dst}\trules\n')
        target = Path(pair.src) / 'file'
        target.chmod(0o755)
        (Path(pair.dst) / 'file').chmod(0o755)
        before = target.read_bytes(), stat.S_IMODE(target.stat().st_mode)
        pre = FileState(before[0], digest(before[0]), before[1], str(self.run / 'unused'))
        executor.execute((Replace(str(target), pre, b'changed', before[1]),), str(self.run))
        class Stop(Exception):
            pass
        def stop(point, intent):
            if point == 'intent':
                raise Stop()
        with self.assertRaises(Stop):
            executor.execute((BackupRun((pair,)),), str(self.run), seam=stop)
        code = r'''import os, signal, sys
from pathlib import Path
from ops.migrate import switch_exec as e
from ops.migrate.root_switch_core import FileState, Replace, Install, Quiesce
from ops.migrate.switch_journal_core import Intent, Done, NoIdentity, ResyncP, BackupCompare, recover
from ops.migrate.switch_inverse_core import plan
run, kill = sys.argv[1], sys.argv[2] == 'kill'
root = Path(run).parent
journal = e.read_journal(run)
images = {i.action.pre.preimage: e.preimage_hash(i.action.pre.preimage)
          for i in journal.records if isinstance(i, Intent)
          and isinstance(i.action, (Replace, Install)) and isinstance(i.action.pre, FileState)}
pending = journal.records[-1] if isinstance(journal.records[-1], Intent) else None
state = recover(journal, NoIdentity() if pending else None, images)
assert state.status == 0, state
if pending:
    e.append_receipt(run, Done(pending.seq, NoIdentity(), 'uncertain'))
actions = plan(state, run)
keys = []
for action in actions:
    if isinstance(action, Quiesce):
        keys.append('barrier:' + str(len(journal.records)))
    elif isinstance(action, ResyncP):
        keys.append('resync:2')
    elif isinstance(action, BackupCompare):
        keys.append('compare:2')
    else:
        keys.append('undo:1')
def arguments(action):
    if isinstance(action, Quiesce):
        return dict(command=(sys.executable, str(root/'fake.py'), str(root), 'processes'),
                    clock=lambda: 0, sleep=lambda _: None, timeout=0, interval=1)
    if isinstance(action, BackupCompare):
        return dict(displaced=())
    seams = ('BACKUP_SRC', 'BACKUP_DEST', 'BACKUP_EXCLUDES', 'BACKUP_PAIRS',
             'BACKUP_RSYNC', 'BACKUP_MOUNT', 'BACKUP_MOUNT_POINT')
    text = (root/'fake.py').read_text()
    assert all(name in text for name in seams)
    return dict(command=(sys.executable, str(root/'fake.py'), str(root), 'backup'),
                table=str(root/'pairs.tsv'), env={name: str(root) for name in seams}, timeout=2)
def seam(point, intent):
    if kill and point == 'mutation' and isinstance(intent.action, ResyncP):
        os.kill(os.getpid(), signal.SIGKILL)
e.execute(actions, run, direction='inverse', keys=keys, effect_arguments=arguments, seam=seam)
'''
        result = self.child(code, self.run, 'kill')
        self.assertEqual(result[0], -signal.SIGKILL, result)
        records = executor.read_journal(str(self.run)).records
        self.assertIsInstance(records[-1], Intent)
        self.assertIsInstance(records[-1].action, ResyncP)
        self.assertEqual(records[-1].key, 'resync:2')
        result = self.child(code, self.run, 'recover')
        self.assertEqual(result[0], 0, result)
        self.assertEqual((target.read_bytes(), stat.S_IMODE(target.stat().st_mode)), before)
        records = executor.read_journal(str(self.run)).records
        self.assertIsInstance(records[-1], Done)
        self.assertIsInstance(records[-2].action, BackupCompare)
        resyncs = [r for r in records if isinstance(r, Intent) and isinstance(r.action, ResyncP)]
        self.assertEqual(len(resyncs), 2)
        self.assertEqual([r.key for r in resyncs], ['resync:2', 'resync:2'])
        self.assertEqual((Path(pair.dst) / 'file').read_bytes(), before[0])
        self.assertTrue((Path(pair.dst) / '.last_success').read_bytes())


if __name__ == '__main__':
    unittest.main()
