"""Execute one ordered batch in a caller-owned, exclusive switch run folder.

The caller supplies stable inverse keys (Step 421's undo/resync/compare keys),
effect arguments and CHECK execution. Failed effects leave their intent pending.
Step 422 owns recovery observations, torn-suffix repair and receipt classification;
this executor refuses to append actions to an unresolved journal.
The seam receives (preimage|intent|mutation|done, Intent), for deterministic faults.
No real command, filesystem root, or deployment setting has a default here.
"""
from dataclasses import replace
import errno
from hashlib import sha256
import os
import stat

from ops.migrate import fdsafe, switch_effects
# [LAW:one-source-of-truth] Both directions use the planner and wire types.
from ops.migrate.root_switch_core import Absent, Check, FileState, Install, Launchd, Rename, Replace
from ops.migrate.switch_journal_core import (
    AgentIdentity, Done, FileIdentity, Inode, Intent, NoIdentity, RenameIdentity,
    encode, parse, recover, _post,
)


def _entry(parent, name):
    try:
        return fdsafe._scan(parent, name)
    except fdsafe.Refusal as exc:
        if exc.errno != errno.ENOENT:
            raise
        return None


def _file(parent, name):
    entry = _entry(parent, name)
    if entry is None:
        return Absent(), b''
    fdsafe._settled(parent)
    data = fdsafe.read_bytes(entry)
    fdsafe._settled(parent)
    return FileIdentity(sha256(data).hexdigest(), stat.S_IMODE(entry.st.st_mode)), data


def _read(path):
    with fdsafe.hold_root(os.path.dirname(path)) as parent:
        return _file(parent, os.path.basename(path))


def preimage_hash(path):
    """Observe absence explicitly; all other read failures remain refusals."""
    identity, _ = _read(path)
    return None if isinstance(identity, Absent) else identity.sha256


def read_journal(run):
    _, data = _read(os.path.join(run, 'journal'))
    try:
        return parse(data.decode('ascii'))
    except UnicodeDecodeError as exc:
        raise fdsafe.Refusal(run, 'EILSEQ: non-ASCII journal') from exc


def _sync(fd, path):
    with fdsafe.fs(path):
        os.fsync(fd)


def _append(run, record):
    data = encode(record).encode('ascii')
    with fdsafe.hold_root(run) as parent:
        path = os.path.join(run, 'journal')
        entry = _entry(parent, 'journal')
        flags = os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW | os.O_NONBLOCK
        if entry is None:
            flags |= os.O_CREAT | os.O_EXCL
        elif not stat.S_ISREG(entry.st.st_mode):
            raise fdsafe.Refusal(path, 'EINVAL: journal is not a regular file')
        fdsafe._settled(parent)
        with fdsafe.fs(path):
            fd = os.open('journal', flags, 0o600, dir_fd=parent.fd)
        try:
            opened = fdsafe._fstat(fd, path)
            if entry is not None and fdsafe._identity(opened) != fdsafe._identity(entry.st):
                raise fdsafe.Refusal(path, 'ESTALE: journal changed at open')
            held = fdsafe.Held(fd, parent, 'journal')
            fdsafe.write_held(held, data)
            fdsafe.settle(held, ())
            fdsafe._settled(parent)
            _sync(fd, path)
            _sync(parent.fd, run)
        finally:
            fdsafe.close(fd, path)


def append_receipt(run, record):
    """Durably close an observed pending intent; recovery owns the observation."""
    journal = read_journal(run)
    if journal.truncated or not journal.records or not isinstance(journal.records[-1], Intent):
        raise fdsafe.Refusal(run, 'EINVAL: no complete pending intent')
    pending = journal.records[-1]
    if not isinstance(record, Done) or record.seq != pending.seq:
        raise fdsafe.Refusal(run, 'EINVAL: receipt does not close pending intent')
    candidate = parse(''.join(encode(r) for r in journal.records) + encode(record))
    _check_journal(candidate)
    _append(run, record)


def _check_journal(journal):
    images = {r.action.pre.preimage: preimage_hash(r.action.pre.preimage)
              for r in journal.records if isinstance(r, Intent)
              and isinstance(r.action, (Replace, Install)) and isinstance(r.action.pre, FileState)}
    state = recover(journal, None, images)
    if state.status:
        raise fdsafe.Refusal('journal', 'EIO: ' + '; '.join(state.stopped))


def _directory(parent, name):
    entry = _entry(parent, name)
    if entry is None:
        held = fdsafe.mkdir(parent, name)
        try:
            _sync(parent.fd, parent.path)
        except BaseException:
            held.close()
            raise
        return held
    return fdsafe.hold_root(entry.path)


def _create(parent, name, data, mode):
    # [LAW:effects-at-boundaries] These are authorized transaction writes, including
    # inside the moving root. fdsafe's read-only-output exclusion does not apply.
    path = fdsafe._child(parent, name)
    fdsafe._settled(parent)
    with fdsafe.fs(path):
        fd = os.open(name, fdsafe.CREATE_FLAGS | os.O_NONBLOCK, mode, dir_fd=parent.fd)
    held = fdsafe.Held(fd, parent, name)
    try:
        fdsafe.write_held(held, data)
        with fdsafe.fs(path):
            os.fchmod(fd, mode)
        fdsafe.settle(held, ())
        fdsafe._settled(parent)
        _sync(fd, path)
        _sync(parent.fd, parent.path)
        return held
    except BaseException:
        fdsafe.close(fd, path)
        raise


def observe(action):
    """Observe filesystem actions; launchd observations belong to Step 423/422."""
    if isinstance(action, (Replace, Install)):
        return _read(action.path if isinstance(action, Replace) else action.dst)[0]
    if isinstance(action, Rename):
        values = []
        for path in (action.src, action.dst):
            with fdsafe.hold_root(os.path.dirname(path)) as parent:
                entry = _entry(parent, os.path.basename(path))
                fdsafe._settled(parent)
                values.append(None if entry is None else Inode(entry.st.st_dev, entry.st.st_ino))
        return RenameIdentity(*values)
    if isinstance(action, Launchd):
        raise fdsafe.Refusal('LAUNCHD', 'EINVAL: supply the observed agent state through Step 422')
    return NoIdentity()


def _prepare(action, run, seq, direction):
    if isinstance(action, (Replace, Install)):
        path = action.path if isinstance(action, Replace) else action.dst
        observed, data = _read(path)
        expected = (FileIdentity(action.pre.sha256, action.pre.mode)
                    if isinstance(action.pre, FileState) else Absent())
        if observed != expected:
            raise fdsafe.Refusal(path, 'ESTALE: file differs from recorded pre-identity; kept')
        if isinstance(action.pre, FileState):
            # Inverses carry the forward post as pre, and the original bytes as post.
            # The recovery core checks the original preimage before planning them.
            with fdsafe.hold_root(run) as folder, _directory(folder, 'pre') as parent:
                name = str(seq)
                held = _create(parent, name, data, action.pre.mode)
                fdsafe.close(held.fd, os.path.join(parent.path, name))
            action = replace(action, pre=replace(action.pre, preimage=os.path.join(run, 'pre', name)))
        return action, observed
    if isinstance(action, Rename):
        observed = observe(action)
        if observed.src is None or observed.dst is not None:
            raise fdsafe.Refusal(action.src + ' -> ' + action.dst, 'EEXIST: expected source and absent destination')
        return action, observed
    if isinstance(action, Launchd):
        return action, AgentIdentity(action.from_state)
    return action, NoIdentity()


def _read_fd(fd, path):
    before = fdsafe._fstat(fd, path)
    if not stat.S_ISREG(before.st_mode):
        raise fdsafe.Refusal(path, 'EINVAL: target is not a regular file')
    with fdsafe.fs(path):
        os.lseek(fd, 0, os.SEEK_SET)
    parts = []
    while chunk := fdsafe._read(fd, path):
        parts.append(chunk)
    data = b''.join(parts)
    after = fdsafe._fstat(fd, path)
    if (fdsafe._identity(before) != fdsafe._identity(after)
            or before.st_mode != after.st_mode or len(data) != after.st_size):
        raise fdsafe.Refusal(path, 'ESTALE: target changed while read; kept')
    return FileIdentity(sha256(data).hexdigest(), stat.S_IMODE(after.st_mode)), data


def _land(held, name):
    parent = held.parent
    path = os.path.join(parent.path, name)
    fdsafe._settled(parent)
    with fdsafe.fs(path):
        os.replace(held.name, name, src_dir_fd=parent.fd, dst_dir_fd=parent.fd)
    fdsafe.settle(fdsafe.Held(held.fd, parent, name), ())
    fdsafe._settled(parent)
    _sync(parent.fd, parent.path)


def _replace_existing(held, name, expected):
    # [LAW:single-enforcer] Forward, inverse and existing INSTALL share W17.
    parent = held.parent
    path = os.path.join(parent.path, name)
    fdsafe._settled(parent)
    with fdsafe.fs(path):
        fd = os.open(name, fdsafe.LEAF_FLAGS, dir_fd=parent.fd)
    try:
        checked, _ = _read_fd(fd, path)
        if checked != expected:
            raise fdsafe.Refusal(path, 'ESTALE: target changed after intent; kept')
        _land(held, name)
        newer, data = _read_fd(fd, path)
        if newer != checked:
            restored = _create(parent, held.name, data, newer.mode)
            try:
                _land(restored, name)
            finally:
                fdsafe.close(restored.fd, path)
            raise fdsafe.Refusal(path, 'ESTALE: newer work written during the replace; restored')
    finally:
        fdsafe.close(fd, path)


def _mutate_file(intent, run):
    action = intent.action
    path = action.path if isinstance(action, Replace) else action.dst
    with fdsafe.hold_root(os.path.dirname(path)) as parent:
        name = os.path.basename(path)
        held = _create(parent, f'.switch-{intent.seq}', action.post_bytes, action.post_mode)
        try:
            if isinstance(intent.pre, Absent):
                if _file(parent, name)[0] != intent.pre:
                    raise fdsafe.Refusal(path, 'ESTALE: target changed after intent; kept')
                fdsafe._settled(parent)
                with fdsafe.fs(path):
                    fdsafe._rename_noreplace(held.name, name, src_dir_fd=parent.fd, dst_dir_fd=parent.fd)
                fdsafe.settle(fdsafe.Held(held.fd, parent, name), ())
                fdsafe._settled(parent)
                _sync(parent.fd, parent.path)
            else:
                _replace_existing(held, name, intent.pre)
        finally:
            fdsafe.close(held.fd, path)
    return observe(action)


def _mutate(intent, run, effect_arguments, check):
    action = intent.action
    if isinstance(action, (Replace, Install)):
        return _mutate_file(intent, run)
    if isinstance(action, Rename):
        if observe(action) != intent.pre:
            raise fdsafe.Refusal(action.src, 'ESTALE: rename changed after intent')
        with fdsafe.hold_root(os.path.dirname(action.src)) as src, fdsafe.hold_root(os.path.dirname(action.dst)) as dst:
            fdsafe.rename(src, os.path.basename(action.src), dst, os.path.basename(action.dst), (src, dst))
            _sync(src.fd, src.path)
            _sync(dst.fd, dst.path)
        return observe(action)
    if isinstance(action, Check):
        if check(action.check_id) is not True:
            raise fdsafe.Refusal(action.check_id, 'EIO: check failed or unavailable')
        return NoIdentity()
    result = switch_effects.execute(action, **effect_arguments(action))
    if result.exit_code != 0:
        raise fdsafe.Refusal(action.kind, 'EIO: ' + '; '.join(result.stopped))
    return result.identity


def _missing(action):
    raise fdsafe.Refusal(str(action), 'EINVAL: caller must supply effect arguments or CHECK runner')


def execute(actions, run, *, direction='forward', keys=None, effect_arguments=_missing,
            check=_missing, seam=lambda *args: None):
    """Append a batch; return its observed Done receipts. No exception is suppressed."""
    journal = read_journal(run)
    if journal.truncated or (journal.records and isinstance(journal.records[-1], Intent)):
        raise fdsafe.Refusal(run, 'EINVAL: recover pending or truncated journal before append')
    _check_journal(journal)
    seq = max((r.seq for r in journal.records), default=0)
    actions = tuple(actions)
    if keys is None:
        if direction != 'forward':
            raise fdsafe.Refusal(run, 'EINVAL: inverse requires stable keys')
        keys = tuple('forward:' + str(seq + i + 1) for i in range(len(actions)))
    if len(keys) != len(actions):
        raise fdsafe.Refusal(run, 'EINVAL: action/key count differs')
    receipts = []
    for action, key in zip(actions, keys):
        seq += 1
        if isinstance(action, Rename) and action.dst.startswith(run + '/undone/'):
            with fdsafe.hold_root(run) as parent, _directory(parent, 'undone'):
                pass
        action, pre = _prepare(action, run, seq, direction)
        # [LAW:one-source-of-truth] A retry keeps its first recorded operands.
        # The new seq copy is still saved above; the original stays authoritative.
        for previous in journal.records:
            if (isinstance(previous, Intent) and previous.direction == direction and previous.key == key
                    and isinstance(action, (Replace, Install)) and isinstance(action.pre, FileState)):
                action = replace(action, pre=replace(action.pre, preimage=previous.action.pre.preimage))
        intent = Intent(seq, direction, key, action, pre)
        # [LAW:single-enforcer] The wire parser owns schema and recovery owns ordering.
        candidate = parse(''.join(encode(r) for r in journal.records) + encode(intent)
                          + encode(Done(seq, _post(intent))))
        _check_journal(candidate)
        if isinstance(action, (Replace, Install)) and isinstance(action.pre, FileState):
            seam('preimage', intent)
        _append(run, intent)
        seam('intent', intent)
        post = _mutate(intent, run, effect_arguments, check)
        seam('mutation', intent)
        done = Done(seq, post)
        completed = parse(''.join(encode(r) for r in journal.records) + encode(intent) + encode(done))
        _check_journal(completed)
        _append(run, done)
        seam('done', intent)
        journal = completed
        receipts.append(done)
    return tuple(receipts)
