"""Filesystem attacks for tests: each is a context manager that a test wraps around one call of the tool under test.

Every attack patches one os or fcntl function, restores it on exit (also when the body raises),
and fails the test on a normal exit unless it fired exactly once. A displaced path is parked by
rename into a new directory that the kit creates next to it (PARK_PREFIX + random); it is never
deleted or overwritten, and Fault.parked names it. Kit failures are FaultKitError, a BaseException,
so a tool's `except Exception` cannot swallow them.
"""
import contextlib
import errno
import fcntl
import math
import os
import secrets
import signal
import stat
import threading

GETPATH = 'fcntl.F_GETPATH'
TARGETS = ('open', 'scandir', 'read', 'write', 'fstat', 'close', GETPATH, 'mkdir', 'rename')
ERRNOS = (errno.EIO, errno.ENOSPC, errno.EBADF, errno.ENOTDIR, errno.ELOOP)
UNEXPECTED = (ValueError, KeyError, RuntimeError)
PARK_PREFIX = '.fault_kit-park-'
WHEN = ('before', 'after')

# The kit's own filesystem moves use the functions as they were at import, so an active patch never sees them.
_lstat, _rename, _symlink, _mkfifo, _mkdir = os.lstat, os.rename, os.symlink, os.mkfifo, os.mkdir


class FaultKitError(BaseException):
    """The attack could not run as asked, or did not fire exactly once."""


class AttackTimeout(FaultKitError):
    """The body of a FIFO attack ran past its timeout, for example in a blocking open."""


class Fault:
    """What one attack saw: matched calls of its target and how many times it fired."""

    def __init__(self):
        self.calls = 0
        self.fired = 0
        self.error = None
        self.parked = None


def _target(name):
    if name not in TARGETS:
        raise FaultKitError(f'fault_kit: unknown target {name!r}; known: {", ".join(TARGETS)}')
    if name == GETPATH:
        if not hasattr(fcntl, 'F_GETPATH'):
            raise FaultKitError('fault_kit: fcntl.F_GETPATH does not exist on this platform')
        return fcntl, 'fcntl', lambda args: len(args) > 1 and args[1] == fcntl.F_GETPATH
    return os, name, lambda args: True


def _check_n(n):
    if type(n) is not int or n < 1:
        raise FaultKitError(f'fault_kit: call number must be an int >= 1, got {n!r}')


def _check_when(when):
    if when not in WHEN:
        raise FaultKitError(f'fault_kit: when must be one of {WHEN}, got {when!r}')


def _path(path):
    path = os.fspath(path)
    if not isinstance(path, str):
        raise FaultKitError(f'fault_kit: path must be str, got {path!r}')
    return path


@contextlib.contextmanager
def _at_call(name, n, action, match):
    """Run action(fault, real, args, kwargs) in place of the Nth matched call of the named function."""
    _check_n(n)
    module, attr, is_kind = _target(name)
    real = getattr(module, attr)
    fault = Fault()

    def hooked(*args, **kwargs):
        if not is_kind(args) or (match is not None and not match(*args, **kwargs)):
            return real(*args, **kwargs)
        fault.calls += 1
        if fault.calls != n:
            return real(*args, **kwargs)
        fault.fired += 1
        return action(fault, real, args, kwargs)

    try:
        setattr(module, attr, hooked)
        yield fault
    finally:
        setattr(module, attr, real)
    if fault.error is not None:
        raise fault.error
    if fault.fired != 1:
        raise FaultKitError(f'fault_kit: {name} attack fired {fault.fired} times '
                            f'({fault.calls} matched calls, wanted call {n})')


def _setup(fault, move):
    """Run a filesystem move for an attack and record its parked path; any failure is recorded as a FaultKitError and re-raised on exit."""
    try:
        fault.parked = move()
    except FaultKitError as error:
        fault.error = error
        raise
    except OSError as error:
        fault.error = FaultKitError(f'fault_kit: attack setup failed: {error}')
        raise fault.error from error


def _park(path):
    """Rename path into a directory that this call creates exclusively (mkdir fails on any existing name)."""
    park = os.path.join(os.path.dirname(path), PARK_PREFIX + secrets.token_hex(8))
    _mkdir(park, 0o700)
    parked = os.path.join(park, os.path.basename(path))
    _rename(path, parked)
    return parked


def _moving(when, move):
    """An action that runs move() before or after the real call."""
    def action(fault, real, args, kwargs):
        if when == 'before':
            _setup(fault, move)
            return real(*args, **kwargs)
        try:
            result = real(*args, **kwargs)
        except BaseException:
            fault.error = FaultKitError('fault_kit: the trigger call failed before the attack ran')
            raise
        _setup(fault, move)
        return result
    return action


def swap_for_symlink(name, n, path, target, *, when='before', match=None):
    """At the Nth matched call of `name`, park `path` and put a symlink to `target` in its place."""
    _check_when(when)
    path, target = _path(path), _path(target)

    def move():
        parked = _park(path)
        _symlink(target, path)
        return parked
    return _at_call(name, n, _moving(when, move), match)


class _Clock:
    """The FIFO timer's state. The alarm raises only while the body runs; outside it, the alarm is
    recorded and raised once setup or restore is complete, so it can never cut a restore short."""

    def __init__(self, timeout):
        self.timeout = timeout
        self.live = False
        self.expired = False

    def error(self):
        return AttackTimeout(f'fault_kit: FIFO attack body ran past {self.timeout} s')

    def alarm(self, signum, frame):
        self.expired = True
        if self.live:
            raise self.error()

    @contextlib.contextmanager
    def body(self):
        try:
            self.live = True
            if self.expired:
                raise self.error()
            yield
        finally:
            self.live = False


@contextlib.contextmanager
def _deadline(timeout):
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0 < timeout < math.inf:
        raise FaultKitError(f'fault_kit: timeout must be a finite number > 0, got {timeout!r}')
    if signal.getitimer(signal.ITIMER_REAL) != (0.0, 0.0):
        raise FaultKitError('fault_kit: a real-time timer is already running')
    if threading.current_thread() is not threading.main_thread():
        raise FaultKitError('fault_kit: FIFO attack needs the main thread')
    clock = _Clock(timeout)
    previous = signal.getsignal(signal.SIGALRM)
    try:
        signal.signal(signal.SIGALRM, clock.alarm)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        yield clock
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
    if clock.expired:
        raise clock.error()


@contextlib.contextmanager
def fifo_in_place(path, *, name=None, n=1, when='before', match=None, timeout=5.0):
    """Park `path` and put a FIFO in its place, at entry or at the Nth matched call of `name`; the body runs under `timeout` seconds."""
    _check_when(when)
    path = _path(path)

    def move():
        parked = _park(path)
        _mkfifo(path)
        return parked
    with _deadline(timeout) as clock:
        if name is None:
            fault = Fault()
            _setup(fault, move)
            fault.fired = 1
            with clock.body():
                yield fault
        else:
            with _at_call(name, n, _moving(when, move), match) as fault, clock.body():
                yield fault


def inject_oserror(name, n, err, *, match=None):
    """Raise OSError(err) at the Nth matched call of `name`; close runs the real close first so no fd leaks."""
    if err not in ERRNOS:
        raise FaultKitError(f'fault_kit: errno {err!r} is not one of {ERRNOS}')

    def action(fault, real, args, kwargs):
        if name == 'close':
            real(*args, **kwargs)
        raise OSError(err, os.strerror(err))
    return _at_call(name, n, action, match)


@contextlib.contextmanager
def one_byte_writes():
    """Make os.write write at most one byte per call; fails on exit if nothing was written."""
    real = os.write
    fault = Fault()

    def hooked(fd, data):
        fault.calls += 1
        return real(fd, memoryview(data).cast('B')[:1])
    try:
        os.write = hooked
        yield fault
    finally:
        os.write = real
    if fault.calls == 0:
        raise FaultKitError('fault_kit: one_byte_writes saw no os.write call')
    fault.fired = 1


def rename_and_rebind(name, n, path, *, when='before', match=None):
    """At the Nth matched call of `name`, park the directory `path` and make a new empty directory at its old path, so a held fd names the parked one."""
    _check_when(when)
    path = _path(path)

    def move():
        if not stat.S_ISDIR(_lstat(path).st_mode):
            raise FaultKitError(f'fault_kit: {path} is not a real directory')
        parked = _park(path)
        _mkdir(path)
        return parked
    return _at_call(name, n, _moving(when, move), match)


def raise_unexpected(name, n, exc_type, *, match=None):
    """Raise exc_type (ValueError, KeyError or RuntimeError) at the Nth matched call of `name`."""
    if exc_type not in UNEXPECTED:
        raise FaultKitError(f'fault_kit: {exc_type!r} is not one of {UNEXPECTED}')

    def action(fault, real, args, kwargs):
        raise exc_type(f'fault_kit: unexpected {exc_type.__name__} from {name}')
    return _at_call(name, n, action, match)
