"""Tests for fault_kit. Every attack runs against a tiny target function defined here."""
import array
import errno
import fcntl
import inspect
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

import fault_kit as FK

# The required capabilities, copied from the Step 301 "out:"; never derived from fault_kit's own lists.
GETPATH = 'fcntl.F_GETPATH'
REQUIRED_TARGETS = ('open', 'scandir', 'read', 'write', 'fstat', 'close', GETPATH, 'mkdir', 'rename')
REQUIRED_ERRNOS = (errno.EIO, errno.ENOSPC, errno.EBADF, errno.ENOTDIR, errno.ELOOP)
REQUIRED_UNEXPECTED = (ValueError, KeyError, RuntimeError)
PARK_PREFIX = '.fault_kit-park-'

REAL = {name: getattr(os, name) for name in
        ('open', 'scandir', 'read', 'write', 'fstat', 'close', 'mkdir', 'rename')}
REAL[GETPATH] = fcntl.fcntl
HAS_GETPATH = hasattr(fcntl, 'F_GETPATH')


def current(name):
    return fcntl.fcntl if name == GETPATH else getattr(os, name)


def park_dirs(base):
    return sorted(name for name in os.listdir(base) if name.startswith(PARK_PREFIX))


def getpath(fd):
    """Target: the live path of an fd (macOS F_GETPATH)."""
    return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).rstrip(b'\0'))


def scan_names(path):
    """Target: the sorted entry names of a directory."""
    with os.scandir(path) as it:
        return sorted(entry.name for entry in it)


def read_all(path):
    """Target: open, fstat, read and close one file."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        os.fstat(fd)
        return os.read(fd, 1 << 16)
    finally:
        os.close(fd)


def write_all(fd, data):
    """Target: write all of data, looping on short writes; returns the os.write call count."""
    view, calls = memoryview(data), 0
    while view:
        view = view[os.write(fd, view):]
        calls += 1
    return calls


def outcome(call):
    """Run one call and name its outcome: 'ok', an errno name, or an exception type name."""
    try:
        call()
    except OSError as error:
        return errno.errorcode[error.errno]
    except (ValueError, KeyError, RuntimeError) as error:
        return type(error).__name__
    return 'ok'


class Base(unittest.TestCase):
    def tmp(self):
        path = os.path.realpath(tempfile.mkdtemp(prefix='fault-kit-'))
        self.addCleanup(shutil.rmtree, path)
        return path

    def fd(self, path, flags):
        fd = os.open(path, flags)
        self.addCleanup(self.close_quietly, fd)
        return fd

    @staticmethod
    def close_quietly(fd):
        try:
            os.close(fd)
        except OSError:
            pass

    def assertRestored(self):
        for name, real in REAL.items():
            self.assertIs(current(name), real, name)

    def one_call(self, name, base):
        """Return a zero-argument function that makes one fresh call of the named target."""
        counter = iter(range(1000))
        leaf = os.path.join(base, 'leaf')
        with open(leaf, 'wb') as handle:
            handle.write(b'leaf bytes')
        if name == 'open':
            return lambda: os.close(os.open(leaf, os.O_RDONLY))
        if name == 'scandir':
            return lambda: scan_names(base)
        if name == 'read':
            fd = self.fd(leaf, os.O_RDONLY)
            return lambda: os.read(fd, 1)
        if name == 'write':
            fd = self.fd(os.path.join(base, 'sink'), os.O_WRONLY | os.O_CREAT)
            return lambda: os.write(fd, b'x')
        if name == 'fstat':
            fd = self.fd(leaf, os.O_RDONLY)
            return lambda: os.fstat(fd)
        if name == 'close':
            def close():
                fd = self.fd(leaf, os.O_RDONLY)
                self.last_close_fd = fd
                os.close(fd)
            return close
        if name == GETPATH:
            fd = self.fd(leaf, os.O_RDONLY)
            return lambda: getpath(fd)
        if name == 'mkdir':
            return lambda: os.mkdir(os.path.join(base, 'made-%d' % next(counter)))
        if name == 'rename':
            def rename():
                i = next(counter)
                src = os.path.join(base, 'src-%d' % i)
                open(src, 'wb').close()
                os.rename(src, os.path.join(base, 'dst-%d' % i))
            return rename
        raise AssertionError(name)


def targets():
    return [name for name in REQUIRED_TARGETS if name != GETPATH or HAS_GETPATH]


class InjectOSErrorTest(Base):
    def test_each_errno_fires_once_at_nth_call_of_each_target(self):
        for name in targets():
            for err in REQUIRED_ERRNOS:
                with self.subTest(name=name, err=errno.errorcode[err]):
                    call = self.one_call(name, self.tmp())
                    with FK.inject_oserror(name, 2, err) as fault:
                        seen = [outcome(call) for _ in range(3)]
                    self.assertEqual(seen, ['ok', errno.errorcode[err], 'ok'])
                    self.assertEqual((fault.calls, fault.fired), (3, 1))
                    self.assertRestored()

    def test_injected_close_still_closes_the_fd(self):
        call = self.one_call('close', self.tmp())
        with FK.inject_oserror('close', 1, errno.EIO):
            self.assertEqual(outcome(call), 'EIO')
        with self.assertRaises(OSError) as caught:
            os.fstat(self.last_close_fd)
        self.assertEqual(caught.exception.errno, errno.EBADF)

    def test_injected_open_creates_nothing(self):
        base = self.tmp()
        target = os.path.join(base, 'new')
        with FK.inject_oserror('open', 1, errno.ENOSPC):
            self.assertEqual(outcome(lambda: os.open(target, os.O_WRONLY | os.O_CREAT)), 'ENOSPC')
        self.assertFalse(os.path.lexists(target))

    @unittest.skipUnless(HAS_GETPATH, 'F_GETPATH is macOS only')
    def test_getpath_counts_only_getpath_commands(self):
        base = self.tmp()
        fd = self.fd(base, os.O_RDONLY)
        with FK.inject_oserror(GETPATH, 1, errno.EBADF) as fault:
            fcntl.fcntl(fd, fcntl.F_GETFD)
            fcntl.fcntl(fd, fcntl.F_GETFL)
            self.assertEqual(fault.calls, 0)
            self.assertEqual(outcome(lambda: getpath(fd)), 'EBADF')
        self.assertEqual(getpath(fd), base)

    def test_match_filters_which_calls_count(self):
        base = self.tmp()
        for leaf in ('a', 'b'):
            Path(base, leaf).write_bytes(b'x')
        with FK.inject_oserror('open', 1, errno.ELOOP,
                               match=lambda path, *a, **k: os.path.basename(path) == 'b') as fault:
            self.assertEqual(read_all(os.path.join(base, 'a')), b'x')
            self.assertEqual(outcome(lambda: read_all(os.path.join(base, 'b'))), 'ELOOP')
        self.assertEqual((fault.calls, fault.fired), (1, 1))


class RefusalTest(Base):
    def assertRefusedAtEntry(self, make):
        entered = []
        with self.assertRaises(FK.FaultKitError):
            with make():
                entered.append(True)
        self.assertEqual(entered, [])
        self.assertRestored()

    def test_unknown_target_is_refused(self):
        for name in ('unlink', 'lstat', 'fcntl', 'os.open'):
            with self.subTest(name=name):
                self.assertRefusedAtEntry(lambda: FK.inject_oserror(name, 1, errno.EIO))

    def test_errno_outside_the_list_is_refused(self):
        for err in (errno.ENOENT, errno.EACCES, 0):
            with self.subTest(err=err):
                self.assertRefusedAtEntry(lambda: FK.inject_oserror('read', 1, err))

    def test_exception_type_outside_the_list_is_refused(self):
        for exc in (TypeError, OSError, Exception, KeyboardInterrupt):
            with self.subTest(exc=exc):
                self.assertRefusedAtEntry(lambda: FK.raise_unexpected('read', 1, exc))

    def test_bad_call_number_is_refused(self):
        for n in (0, -1, True, 1.0, '1'):
            with self.subTest(n=n):
                self.assertRefusedAtEntry(lambda: FK.inject_oserror('read', n, errno.EIO))

    def test_bad_when_is_refused(self):
        base = self.tmp()
        for make in (lambda: FK.swap_for_symlink('scandir', 1, base, base, when='during'),
                     lambda: FK.rename_and_rebind('scandir', 1, base, when=None),
                     lambda: FK.fifo_in_place(base, name='open', when='later')):
            self.assertRefusedAtEntry(make)
        self.assertTrue(os.path.isdir(base))

    def test_bytes_path_is_refused(self):
        base = self.tmp()
        self.assertRefusedAtEntry(lambda: FK.swap_for_symlink('scandir', 1, os.fsencode(base), base))

    def test_attack_that_never_fires_fails_on_exit(self):
        call = self.one_call('read', self.tmp())
        with self.assertRaises(FK.FaultKitError):
            with FK.inject_oserror('read', 2, errno.EIO):
                call()
        self.assertRestored()

    def test_setup_failure_cannot_be_swallowed_by_the_tool(self):
        base = self.tmp()
        missing = os.path.join(base, 'missing')
        def tolerant_tool():
            try:
                scan_names(base)
            except BaseException:
                pass
        with self.assertRaises(FK.FaultKitError):
            with FK.swap_for_symlink('scandir', 1, missing, base):
                tolerant_tool()
        self.assertRestored()

    def test_existing_park_names_are_never_overwritten(self):
        base = self.tmp()
        victim = os.path.join(base, 'victim')
        Path(victim).write_bytes(b'victim')
        Path(victim + '.fault_kit-parked').write_bytes(b'already parked')
        os.mkdir(os.path.join(base, PARK_PREFIX + 'old'))
        Path(base, PARK_PREFIX + 'old', 'victim').write_bytes(b'old evidence')
        with FK.swap_for_symlink('open', 1, victim, base) as fault:
            self.assertEqual(outcome(lambda: read_all(victim)), 'ELOOP')
        self.assertEqual(Path(fault.parked).read_bytes(), b'victim')
        self.assertEqual(Path(victim + '.fault_kit-parked').read_bytes(), b'already parked')
        self.assertEqual(Path(base, PARK_PREFIX + 'old', 'victim').read_bytes(), b'old evidence')
        self.assertEqual(len(park_dirs(base)), 2)
        self.assertRestored()


    def test_failed_trigger_call_in_after_mode_fails_on_exit(self):
        base, outside = self.tmp(), self.tmp()
        made = os.path.join(base, 'no-parent', 'made')
        with self.assertRaises(FK.FaultKitError):
            with FK.swap_for_symlink('mkdir', 1, made, outside, when='after'):
                self.assertEqual(outcome(lambda: os.mkdir(made)), 'ENOENT')
        self.assertFalse(os.path.lexists(os.path.join(base, 'no-parent')))
        self.assertRestored()

def attacks(test):
    """One factory per attack, each armed to fire on the body's first scandir call."""
    base = test.tmp()
    Path(base, 'd').mkdir()
    return {
        'swap_for_symlink': lambda: FK.swap_for_symlink('scandir', 1, os.path.join(base, 'd'), base),
        'fifo_in_place': lambda: FK.fifo_in_place(os.path.join(base, 'd'), name='scandir', n=1),
        'inject_oserror': lambda: FK.inject_oserror('scandir', 1, errno.EIO),
        'one_byte_writes': FK.one_byte_writes,
        'rename_and_rebind': lambda: FK.rename_and_rebind('scandir', 1, os.path.join(base, 'd')),
        'raise_unexpected': lambda: FK.raise_unexpected('scandir', 1, KeyError),
    }


class RestoreTest(Base):
    def test_every_attack_restores_when_the_body_raises(self):
        for label, factory in attacks(self).items():
            with self.subTest(attack=label):
                with self.assertRaises(ZeroDivisionError):
                    with factory():
                        self.assertIsNot(current('write' if label == 'one_byte_writes' else 'scandir'),
                                         REAL['write' if label == 'one_byte_writes' else 'scandir'])
                        1 / 0
                self.assertRestored()
                self.assertIs(signal.getsignal(signal.SIGALRM), signal.SIG_DFL)
                self.assertEqual(signal.getitimer(signal.ITIMER_REAL), (0.0, 0.0))

    def test_nested_attacks_restore_in_order(self):
        call = self.one_call('read', self.tmp())
        with FK.inject_oserror('read', 1, errno.EIO):
            with FK.raise_unexpected('read', 1, ValueError):
                self.assertEqual(outcome(call), 'ValueError')
            self.assertEqual(outcome(call), 'EIO')
        self.assertRestored()


class SymlinkSwapTest(Base):
    def test_directory_swapped_at_nth_scandir(self):
        base, outside = self.tmp(), self.tmp()
        d = os.path.join(base, 'd')
        os.mkdir(d)
        Path(d, 'inside').write_bytes(b'')
        Path(outside, 'outside').write_bytes(b'')
        with FK.swap_for_symlink('scandir', 2, d, outside) as fault:
            self.assertEqual(scan_names(d), ['inside'])
            self.assertEqual(scan_names(d), ['outside'])
            self.assertEqual(scan_names(d), ['outside'])
        self.assertEqual((fault.calls, fault.fired), (3, 1))
        self.assertEqual(os.readlink(d), outside)
        self.assertEqual(os.listdir(fault.parked), ['inside'])
        self.assertEqual(len(park_dirs(base)), 1)
        self.assertRestored()

    def test_file_swapped_before_open_is_refused_by_nofollow(self):
        base, outside = self.tmp(), self.tmp()
        leaf, secret = os.path.join(base, 'leaf'), os.path.join(outside, 'secret')
        Path(leaf).write_bytes(b'inside')
        Path(secret).write_bytes(b'outside')
        with FK.swap_for_symlink('open', 1, leaf, secret) as fault:
            self.assertEqual(outcome(lambda: read_all(leaf)), 'ELOOP')
        self.assertEqual(Path(fault.parked).read_bytes(), b'inside')
        self.assertTrue(os.path.islink(leaf))
        self.assertRestored()

    def test_swap_after_mkdir_replaces_the_new_directory(self):
        base, outside = self.tmp(), self.tmp()
        made = os.path.join(base, 'made')
        with FK.swap_for_symlink('mkdir', 1, made, outside, when='after') as fault:
            os.mkdir(made)
            self.assertEqual(os.readlink(made), outside)
        self.assertTrue(stat.S_ISDIR(os.lstat(fault.parked).st_mode))
        self.assertRestored()


class FifoTest(Base):
    def test_fifo_replaces_file_at_entry_and_blocking_open_times_out(self):
        base = self.tmp()
        leaf = os.path.join(base, 'leaf')
        Path(leaf).write_bytes(b'inside')
        started = time.monotonic()
        with self.assertRaises(FK.AttackTimeout):
            with FK.fifo_in_place(leaf, timeout=0.3) as fault:
                self.assertEqual(fault.fired, 1)
                self.assertTrue(stat.S_ISFIFO(os.lstat(leaf).st_mode))
                read_all(leaf)
        self.assertLess(time.monotonic() - started, 5)
        self.assertEqual(Path(fault.parked).read_bytes(), b'inside')
        self.assertIs(signal.getsignal(signal.SIGALRM), signal.SIG_DFL)
        self.assertEqual(signal.getitimer(signal.ITIMER_REAL), (0.0, 0.0))
        self.assertRestored()

    def test_fifo_replaces_directory_at_nth_open(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        os.mkdir(d)
        def open_dir():
            fd = os.open(d, os.O_RDONLY | os.O_NONBLOCK)
            try:
                return stat.S_IFMT(os.fstat(fd).st_mode)
            finally:
                os.close(fd)
        with FK.fifo_in_place(d, name='open', n=2, timeout=2) as fault:
            self.assertEqual(open_dir(), stat.S_IFDIR)
            self.assertEqual(open_dir(), stat.S_IFIFO)
        self.assertEqual((fault.calls, fault.fired), (2, 1))
        self.assertTrue(stat.S_ISDIR(os.lstat(fault.parked).st_mode))
        self.assertEqual(signal.getitimer(signal.ITIMER_REAL), (0.0, 0.0))
        self.assertRestored()

    def test_fifo_timeout_cannot_be_swallowed_by_the_tool(self):
        base = self.tmp()
        leaf = os.path.join(base, 'leaf')
        Path(leaf).write_bytes(b'')
        def tolerant_tool():
            try:
                read_all(leaf)
            except Exception:
                return 'swallowed'
        with self.assertRaises(FK.AttackTimeout):
            with FK.fifo_in_place(leaf, timeout=0.3):
                tolerant_tool()

    def test_fifo_refused_while_another_timer_runs(self):
        base = self.tmp()
        previous = signal.signal(signal.SIGALRM, lambda signum, frame: None)
        self.addCleanup(signal.signal, signal.SIGALRM, previous)
        signal.setitimer(signal.ITIMER_REAL, 100)
        self.addCleanup(signal.setitimer, signal.ITIMER_REAL, 0)
        entered = []
        with self.assertRaises(FK.FaultKitError):
            with FK.fifo_in_place(base, timeout=1):
                entered.append(True)
        self.assertEqual(entered, [])
        self.assertTrue(os.path.isdir(base))
        self.assertGreater(signal.getitimer(signal.ITIMER_REAL)[0], 50)

    def test_fifo_refused_outside_the_main_thread(self):
        base = self.tmp()
        caught = []
        def worker():
            try:
                with FK.fifo_in_place(base, timeout=1):
                    caught.append('entered')
            except BaseException as error:
                caught.append(type(error))
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(10)
        self.assertEqual(caught, [FK.FaultKitError])
        self.assertTrue(os.path.isdir(base))

    def test_fifo_timeout_must_be_positive(self):
        base = self.tmp()
        for timeout in (0, -1, None, True):
            entered = []
            with self.subTest(timeout=timeout), self.assertRaises(FK.FaultKitError):
                with FK.fifo_in_place(base, timeout=timeout):
                    entered.append(True)
            self.assertEqual(entered, [])
        self.assertTrue(os.path.isdir(base))


class OneByteWritesTest(Base):
    def test_each_write_accepts_one_byte(self):
        base = self.tmp()
        out = os.path.join(base, 'out')
        fd = self.fd(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        with FK.one_byte_writes() as fault:
            self.assertEqual(os.write(fd, b'ab'), 1)
            self.assertEqual(write_all(fd, b'cdef'), 4)
        self.assertEqual(fault.calls, 5)
        self.assertEqual(Path(out).read_bytes(), b'acdef')
        self.assertRestored()
        self.assertEqual(os.write(fd, b'gh'), 2)

    def test_no_write_at_all_fails_on_exit(self):
        with self.assertRaises(FK.FaultKitError):
            with FK.one_byte_writes():
                pass
        self.assertRestored()


class RenameRebindTest(Base):
    def test_held_fd_follows_the_parked_directory(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        os.mkdir(d)
        fd = self.fd(d, os.O_RDONLY | os.O_DIRECTORY)
        with FK.rename_and_rebind('open', 1, d, match=lambda *a, dir_fd=None, **k: dir_fd == fd) as fault:
            out = os.open('leaf', os.O_WRONLY | os.O_CREAT | os.O_EXCL, dir_fd=fd)
            os.close(out)
        self.assertEqual(os.listdir(fault.parked), ['leaf'])
        self.assertEqual(os.listdir(d), [])
        self.assertFalse(os.path.islink(d))
        self.assertNotEqual(os.stat(d).st_ino, os.fstat(fd).st_ino)
        self.assertEqual(os.stat(fault.parked).st_ino, os.fstat(fd).st_ino)
        if HAS_GETPATH:
            self.assertEqual(getpath(fd), fault.parked)
        self.assertRestored()

    def test_a_file_is_refused(self):
        base = self.tmp()
        leaf = os.path.join(base, 'leaf')
        Path(leaf).write_bytes(b'keep')
        with self.assertRaises(FK.FaultKitError):
            with FK.rename_and_rebind('scandir', 1, leaf):
                try:
                    scan_names(base)
                except BaseException:
                    pass
        self.assertEqual(Path(leaf).read_bytes(), b'keep')
        self.assertEqual(os.listdir(base), ['leaf'])


class RaiseUnexpectedTest(Base):
    def test_each_type_fires_once_at_nth_call(self):
        for exc in REQUIRED_UNEXPECTED:
            with self.subTest(exc=exc.__name__):
                call = self.one_call('mkdir', self.tmp())
                with FK.raise_unexpected('mkdir', 2, exc) as fault:
                    seen = [outcome(call) for _ in range(3)]
                self.assertEqual(seen, ['ok', exc.__name__, 'ok'])
                self.assertEqual(fault.fired, 1)
                self.assertRestored()


class RequiredCapabilityTest(Base):
    def test_each_required_target_errno_and_type_is_accepted(self):
        for name in targets():
            with self.subTest(target=name):
                call = self.one_call(name, self.tmp())
                with FK.raise_unexpected(name, 1, RuntimeError) as fault:
                    self.assertEqual(outcome(call), 'RuntimeError')
                self.assertEqual(fault.fired, 1)
        for err in REQUIRED_ERRNOS:
            with self.subTest(err=errno.errorcode[err]):
                call = self.one_call('rename', self.tmp())
                with FK.inject_oserror('rename', 1, err):
                    self.assertEqual(outcome(call), errno.errorcode[err])
        for exc in REQUIRED_UNEXPECTED:
            with self.subTest(exc=exc.__name__):
                call = self.one_call('rename', self.tmp())
                with FK.raise_unexpected('rename', 1, exc):
                    self.assertEqual(outcome(call), exc.__name__)
        self.assertRestored()

    def test_getpath_target_is_refused_when_the_platform_lacks_it(self):
        if HAS_GETPATH:
            value = fcntl.F_GETPATH
            del fcntl.F_GETPATH
            self.addCleanup(setattr, fcntl, 'F_GETPATH', value)
        base = self.tmp()
        for make in (lambda: FK.inject_oserror(GETPATH, 1, errno.EIO),
                     lambda: FK.raise_unexpected(GETPATH, 1, ValueError),
                     lambda: FK.swap_for_symlink(GETPATH, 1, base, base),
                     lambda: FK.rename_and_rebind(GETPATH, 1, base),
                     lambda: FK.fifo_in_place(base, name=GETPATH, timeout=1)):
            entered = []
            with self.assertRaises(FK.FaultKitError):
                with make():
                    entered.append(True)
            self.assertEqual(entered, [])
            self.assertRestored()
        self.assertTrue(os.path.isdir(base))
        self.assertEqual(park_dirs(os.path.dirname(base)), [])


class ParkTest(Base):
    def test_parked_path_is_in_a_new_directory_the_kit_made(self):
        base = self.tmp()
        leaf = os.path.join(base, 'leaf')
        Path(leaf).write_bytes(b'evidence')
        before = os.listdir(base)
        with FK.swap_for_symlink('open', 1, leaf, base) as fault:
            self.assertEqual(outcome(lambda: read_all(leaf)), 'ELOOP')
        made = park_dirs(base)
        self.assertEqual(len(made), 1)
        self.assertNotIn(made[0], before)
        self.assertEqual(fault.parked, os.path.join(base, made[0], 'leaf'))
        self.assertEqual(os.listdir(os.path.join(base, made[0])), ['leaf'])
        self.assertEqual(Path(fault.parked).read_bytes(), b'evidence')
        self.assertFalse(os.path.lexists(leaf + '.fault_kit-parked'))

    def test_kit_moves_are_not_counted_as_target_calls(self):
        base, outside = self.tmp(), self.tmp()
        made = os.path.join(base, 'made')
        with FK.swap_for_symlink('mkdir', 1, made, outside, when='after') as fault:
            os.mkdir(made)
        self.assertEqual((fault.calls, fault.fired), (1, 1))
        d = os.path.join(base, 'd')
        os.mkdir(d)
        with FK.rename_and_rebind('mkdir', 1, d) as fault:
            os.mkdir(os.path.join(base, 'other'))
        self.assertEqual((fault.calls, fault.fired), (1, 1))
        self.assertTrue(os.path.isdir(fault.parked))

    def test_park_name_collision_refuses_and_keeps_both_files(self):
        base = self.tmp()
        victim = os.path.join(base, 'victim')
        Path(victim).write_bytes(b'victim')
        os.mkdir(os.path.join(base, PARK_PREFIX + 'forced'))
        evidence = Path(base, PARK_PREFIX + 'forced', 'victim')
        evidence.write_bytes(b'pre-existing evidence')
        with mock.patch.object(FK.secrets, 'token_hex', return_value='forced'):
            with self.assertRaises(FK.FaultKitError):
                with FK.swap_for_symlink('open', 1, victim, base):
                    read_all(victim)
        self.assertEqual(evidence.read_bytes(), b'pre-existing evidence')
        self.assertFalse(os.path.islink(victim))
        self.assertEqual(Path(victim).read_bytes(), b'victim')
        self.assertRestored()


def sleep_in(func_name, ready, seconds=0.3):
    """A trace function that sleeps once at the first line run in fault_kit's func_name while ready() is true."""
    slept = []
    def trace(frame, event, arg):
        if (not slept and event == 'line' and frame.f_code.co_name == func_name
                and frame.f_globals.get('__name__') == 'fault_kit' and ready()):
            slept.append(True)
            time.sleep(seconds)
        return trace
    return trace, slept


class FifoCleanupTest(Base):
    def setUp(self):
        self.addCleanup(signal.setitimer, signal.ITIMER_REAL, 0)
        self.addCleanup(signal.signal, signal.SIGALRM, signal.getsignal(signal.SIGALRM))
        self.addCleanup(setattr, os, 'open', REAL['open'])

    def run_traced(self, func_name, ready, body):
        """Run a 0.05 s FIFO attack on the first open of a leaf, sleeping inside func_name once ready() holds."""
        leaf = os.path.join(self.tmp(), 'leaf')
        Path(leaf).write_bytes(b'keep')
        trace, slept = sleep_in(func_name, ready)
        caught = None
        sys.settrace(trace)
        try:
            with FK.fifo_in_place(leaf, name='open', timeout=0.05):
                body(leaf)
        except BaseException as error:
            caught = type(error)
        finally:
            sys.settrace(None)
            restored = (os.open is REAL['open'], signal.getsignal(signal.SIGALRM) is signal.SIG_DFL,
                        signal.getitimer(signal.ITIMER_REAL) == (0.0, 0.0))
        self.assertEqual(slept, [True])
        self.assertIs(caught, FK.AttackTimeout)
        self.assertEqual(restored, (True, True, True))

    @staticmethod
    def open_once(leaf):
        os.close(os.open(leaf, os.O_RDONLY | os.O_NONBLOCK))

    def test_alarm_after_patch_install_restores_the_function(self):
        self.run_traced('_at_call', lambda: os.open is not REAL['open'], lambda leaf: None)

    def test_alarm_after_timer_arm_restores_the_handler(self):
        self.run_traced('_deadline', lambda: signal.getitimer(signal.ITIMER_REAL)[0] > 0, lambda leaf: None)

    def test_alarm_while_restoring_the_function_still_restores_it(self):
        done = []
        def body(leaf):
            self.open_once(leaf)
            done.append(True)
        self.run_traced('_at_call', lambda: bool(done), body)

    def test_alarm_while_restoring_the_handler_still_restores_it(self):
        done = []
        def body(leaf):
            self.open_once(leaf)
            done.append(True)
        self.run_traced('_deadline', lambda: bool(done) and signal.getitimer(signal.ITIMER_REAL)[0] > 0, body)

    def test_success_restores_the_callers_own_handler(self):
        def handler(signum, frame):
            raise AssertionError('caller alarm ran')
        signal.signal(signal.SIGALRM, handler)
        leaf = os.path.join(self.tmp(), 'leaf')
        Path(leaf).write_bytes(b'keep')
        with FK.fifo_in_place(leaf, timeout=1):
            self.open_once(leaf)
        self.assertIs(signal.getsignal(signal.SIGALRM), handler)

    def test_alarm_between_timer_cancel_and_handler_restore_skips_the_caller(self):
        called, fired = [], []
        signal.signal(signal.SIGALRM, lambda signum, frame: called.append(True))
        code = FK._deadline.__wrapped__.__code__
        lines, first = inspect.getsourcelines(FK._deadline.__wrapped__)
        cancel = first + next(i for i, line in enumerate(lines)
                              if 'signal.setitimer(signal.ITIMER_REAL, 0)' in line)
        def trace(frame, event, arg):
            if not fired and frame.f_code is code and event == 'line' and frame.f_lineno == cancel:
                fired.append(True)
                os.kill(os.getpid(), signal.SIGALRM)
            return trace
        leaf = os.path.join(self.tmp(), 'leaf')
        Path(leaf).write_bytes(b'keep')
        caught = None
        sys.settrace(trace)
        try:
            with FK.fifo_in_place(leaf, timeout=5):
                self.open_once(leaf)
        except FK.AttackTimeout as error:
            caught = type(error)
        finally:
            sys.settrace(None)
        self.assertEqual(fired, [True])
        self.assertEqual(called, [])
        self.assertIs(caught, FK.AttackTimeout)
        self.assertEqual(signal.getitimer(signal.ITIMER_REAL), (0.0, 0.0))

    def test_timer_arm_failure_restores_the_handler(self):
        base = self.tmp()
        with self.assertRaises(OverflowError):
            with FK.fifo_in_place(base, timeout=1e300):
                self.fail('entered')
        self.assertIs(signal.getsignal(signal.SIGALRM), signal.SIG_DFL)
        self.assertEqual(signal.getitimer(signal.ITIMER_REAL), (0.0, 0.0))
        self.assertTrue(os.path.isdir(base))

    def test_timeout_that_is_not_finite_is_refused_before_install(self):
        base = self.tmp()
        for timeout in (float('inf'), float('-inf'), float('nan')):
            entered = []
            with self.subTest(timeout=timeout), self.assertRaises(FK.FaultKitError):
                with FK.fifo_in_place(base, timeout=timeout):
                    entered.append(True)
            self.assertEqual(entered, [])
            self.assertIs(signal.getsignal(signal.SIGALRM), signal.SIG_DFL)
        self.assertTrue(os.path.isdir(base))
        self.assertEqual(park_dirs(os.path.dirname(base)), [])


class Interrupted(BaseException):
    """Stands for an asynchronous exception such as KeyboardInterrupt."""


class InterruptAfterPatchTest(Base):
    """An asynchronous exception right after a patch is installed must still restore it."""

    def interrupt_after_patch(self, func_name, attr, attack):
        real = getattr(os, attr)
        self.addCleanup(setattr, os, attr, real)
        self.addCleanup(signal.signal, signal.SIGALRM, signal.getsignal(signal.SIGALRM))
        self.addCleanup(signal.setitimer, signal.ITIMER_REAL, 0)
        def interrupt(signum, frame):
            raise Interrupted()
        signal.signal(signal.SIGALRM, interrupt)
        trace, slept = sleep_in(func_name, lambda: getattr(os, attr) is not real)
        signal.setitimer(signal.ITIMER_REAL, 0.05)
        sys.settrace(trace)
        try:
            with self.assertRaises(Interrupted):
                with attack():
                    self.fail('body entered')
        finally:
            sys.settrace(None)
            restored = getattr(os, attr) is real
        self.assertEqual(slept, [True])
        self.assertTrue(restored)

    def test_named_call_patch(self):
        self.interrupt_after_patch('_at_call', 'read', lambda: FK.inject_oserror('read', 1, errno.EIO))

    def test_one_byte_writes_patch(self):
        self.interrupt_after_patch('one_byte_writes', 'write', FK.one_byte_writes)


class TypedBufferTest(Base):
    def test_typed_buffer_writes_one_byte(self):
        out = os.path.join(self.tmp(), 'out')
        fd = self.fd(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        data = array.array('i', [0x01020304, 0x05060708])
        with FK.one_byte_writes():
            self.assertEqual(os.write(fd, memoryview(data)), 1)
            self.assertEqual(os.write(fd, data), 1)
        self.assertEqual(Path(out).read_bytes(), data.tobytes()[:1] * 2)


class ForwardingTest(Base):
    def test_rebind_after_mode_parks_the_directory_the_call_made(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        with FK.rename_and_rebind('mkdir', 1, d, when='after') as fault:
            os.mkdir(d)
        self.assertEqual((fault.calls, fault.fired), (1, 1))
        self.assertTrue(stat.S_ISDIR(os.lstat(d).st_mode))
        self.assertTrue(stat.S_ISDIR(os.lstat(fault.parked).st_mode))

    def test_swap_after_mode_parks_the_directory_the_call_made(self):
        base, outside = self.tmp(), self.tmp()
        d = os.path.join(base, 'd')
        with FK.swap_for_symlink('mkdir', 1, d, outside, when='after') as fault:
            os.mkdir(d)
        self.assertEqual(os.readlink(d), outside)
        self.assertTrue(stat.S_ISDIR(os.lstat(fault.parked).st_mode))

    def test_fifo_after_mode_parks_the_directory_the_call_made(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        with FK.fifo_in_place(d, name='mkdir', when='after', timeout=2) as fault:
            os.mkdir(d)
            self.assertTrue(stat.S_ISFIFO(os.lstat(d).st_mode))
        self.assertEqual((fault.calls, fault.fired), (1, 1))
        self.assertTrue(stat.S_ISDIR(os.lstat(fault.parked).st_mode))

    def test_rebind_fires_at_the_nth_call(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        os.mkdir(d)
        ino = os.stat(d).st_ino
        with FK.rename_and_rebind('scandir', 2, d) as fault:
            scan_names(d)
            self.assertEqual(os.stat(d).st_ino, ino)
            scan_names(d)
            self.assertNotEqual(os.stat(d).st_ino, ino)
        self.assertEqual((fault.calls, fault.fired), (2, 1))
        self.assertEqual(os.stat(fault.parked).st_ino, ino)

    def test_rebind_counts_only_matching_calls(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        os.mkdir(d)
        ino = os.stat(d).st_ino
        with FK.rename_and_rebind('scandir', 1, d, match=lambda path, *a, **k: path == d) as fault:
            scan_names(base)
            self.assertEqual(os.stat(d).st_ino, ino)
            scan_names(d)
            self.assertNotEqual(os.stat(d).st_ino, ino)
        self.assertEqual((fault.calls, fault.fired), (1, 1))

    def test_swap_counts_only_matching_calls(self):
        base, outside = self.tmp(), self.tmp()
        d = os.path.join(base, 'd')
        os.mkdir(d)
        Path(outside, 'outside').write_bytes(b'')
        with FK.swap_for_symlink('scandir', 1, d, outside, match=lambda path, *a, **k: path == d) as fault:
            scan_names(base)
            self.assertFalse(os.path.islink(d))
            self.assertEqual(scan_names(d), ['outside'])
        self.assertEqual((fault.calls, fault.fired), (1, 1))

    def test_fifo_counts_only_matching_calls(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        os.mkdir(d)
        with FK.fifo_in_place(d, name='open', match=lambda path, *a, **k: path == d, timeout=2) as fault:
            os.close(os.open(base, os.O_RDONLY))
            self.assertTrue(stat.S_ISDIR(os.lstat(d).st_mode))
            os.close(os.open(d, os.O_RDONLY | os.O_NONBLOCK))
            self.assertTrue(stat.S_ISFIFO(os.lstat(d).st_mode))
        self.assertEqual((fault.calls, fault.fired), (1, 1))

    def test_raise_unexpected_counts_only_matching_calls(self):
        base = self.tmp()
        d = os.path.join(base, 'd')
        with FK.raise_unexpected('mkdir', 1, ValueError, match=lambda path, *a, **k: path == d) as fault:
            os.mkdir(os.path.join(base, 'unrelated'))
            self.assertEqual(outcome(lambda: os.mkdir(d)), 'ValueError')
        self.assertEqual((fault.calls, fault.fired), (1, 1))
        self.assertFalse(os.path.lexists(d))


class ParallelTempDirTest(unittest.TestCase):
    def test_two_concurrent_runs_in_separate_temp_dirs(self):
        here = os.path.dirname(os.path.abspath(__file__))
        procs = []
        for _ in range(2):
            tmp = os.path.realpath(tempfile.mkdtemp(prefix='fault-kit-par-'))
            self.addCleanup(shutil.rmtree, tmp)
            env = dict(os.environ, TMPDIR=tmp, PYTHONPATH=here)
            proc = subprocess.Popen(
                [sys.executable, '-B', '-m', 'unittest', 'test_fault_kit.SymlinkSwapTest',
                 'test_fault_kit.FifoTest', 'test_fault_kit.RenameRebindTest'],
                cwd=here, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.addCleanup(proc.kill)
            self.addCleanup(proc.stdout.close)
            procs.append(proc)
        for proc in procs:
            out, _ = proc.communicate(timeout=60)
            self.assertEqual(proc.returncode, 0, out.decode())


if __name__ == '__main__':
    unittest.main()
