"""Pure inverse descriptions for Step 421.

The shell journals ordinary inverses as undo:<forward seq>, backup recovery as
resync:<BACKUP_RUN seq> and compare:<BACKUP_RUN seq>. QUIESCE is a fresh barrier
on every invocation, with a fresh shell-owned key. Completed keys are omitted.
The inverse file preimage is a description of a new copy the executor must save,
beside the original preimage as .inverse-<forward seq>; it never reuses that copy.
Only absent INSTALL destinations depend on the supplied run folder (W14).
Status 3 refuses a plan: the caller retains the pause and reports stopped items.
"""
from __future__ import annotations

from hashlib import sha256

from ops.migrate.fdsafe import Refusal
# [LAW:one-source-of-truth] Both directions use the journal's existing values.
from ops.migrate.root_switch_core import (
    Absent, BackupPair, BackupRun, Check, FileState, Install, Launchd,
    Quiesce, Rename, Replace,
)
from ops.migrate.switch_journal_core import (
    Action, RecoveryState, Intent, ResyncP, BackupCompare, _path, encode, parse,
)


def _require(condition, where, reason):
    if not condition:
        raise Refusal(where, 'EINVAL: ' + reason)


def _validate(state, run):
    _path(run, run)
    _require(type(state) is RecoveryState, 'state', 'expected RecoveryState')
    _require(type(state.done) is tuple and type(state.inverse_done) is tuple
             and type(state.stopped) is tuple, 'state', 'expected frozen sequences')
    _require(type(state.status) is int and state.status == 0 and not state.stopped,
             'state', 'recovery stopped: ' + repr(state.stopped))
    items = state.done + (() if state.pending is None else (state.pending,))
    seqs = set()
    for item in items:
        _require(type(item) is Intent, 'state', 'expected Intent')
        # [LAW:single-enforcer] The journal parser owns action/identity validity.
        _require(parse(encode(item)).records == (item,), item.key, 'invalid intent')
        _require(item.seq not in seqs, item.key, 'duplicate sequence')
        seqs.add(item.seq)
    _require(state.inverse_done == tuple(i.key for i in state.done if i.direction == 'inverse'),
             'state', 'inverse keys differ from completed intents')
    if state.pending is not None:
        _require(type(state.pending.action) in (BackupRun, ResyncP),
                 state.pending.key, 'unexpected pending action')


def _inverse(item):
    action = item.action
    if type(action) is Rename:
        return Rename(action.dst, action.src)
    if type(action) is Launchd:
        return Launchd(action.to_state, action.from_state)
    if type(action) in (Replace, Install):
        pre = FileState(action.post_bytes, sha256(action.post_bytes).hexdigest(),
                        action.post_mode, action.pre.preimage + f'.inverse-{item.seq}')
        if type(action) is Replace:
            return Replace(action.path, pre, action.pre.data, action.pre.mode)
        return Install(action.dst, pre, action.pre.data, action.pre.mode)
    raise Refusal(item.key, 'EINVAL: action has no ordinary inverse')


def _restore(path, forwards):
    for item in reversed(forwards):
        action = item.action
        if type(action) is Rename:
            if path == action.dst or path.startswith(action.dst + '/'):
                path = action.src + path[len(action.dst):]
    return path


def _pairs(action, forwards):
    restored = tuple(BackupPair(p.backend, _restore(p.src, forwards),
                               _restore(p.dst, forwards), _restore(p.excludes, forwards))
                     for p in action.pairs)
    parents = tuple(p for p in restored if all(
        (c.src == p.src and c.dst == p.dst)
        or (c.src.startswith(p.src + '/') and c.dst == p.dst + c.src[len(p.src):])
        for c in restored))
    _require(len(parents) == 1, 'BACKUP_RUN', 'no unique covering P pair')
    return parents


def plan(state: RecoveryState, run: str) -> tuple[Action, ...]:
    """Return the remaining inverse actions; never inspect a supplied path."""
    _validate(state, run)
    forwards = tuple(i for i in state.done if i.direction == 'forward')
    if state.pending is not None and type(state.pending.action) is BackupRun:
        forwards += (state.pending,)
    head, middle, backup, tail = [], [], [], []
    for index, item in reversed(tuple(enumerate(forwards))):
        action = item.action
        if type(action) is BackupRun:
            pairs = _pairs(action, forwards)
            if f'resync:{item.seq}' not in state.inverse_done:
                backup.append(ResyncP(pairs))
            if f'compare:{item.seq}' not in state.inverse_done:
                backup.append(BackupCompare(pairs))
        elif type(action) in (Check, Quiesce):
            continue
        elif f'undo:{item.seq}' not in state.inverse_done:
            if type(action) is Launchd:
                if index == 0:
                    tail.append(_inverse(item))
                else:
                    _require(action.from_state == 'unloaded' and action.to_state == 'loaded',
                             item.key, 'expected RESUME')
                    head.append(_inverse(item))
            elif type(action) is Install and type(action.pre) is Absent:
                middle.append(Rename(action.dst, run + f'/undone/{item.seq}'))
            else:
                middle.append(_inverse(item))
    if state.pending is not None and type(state.pending.action) is ResyncP:
        pending = state.pending
        _require(pending.direction == 'inverse', pending.key, 'RESYNC_P must be inverse')
        _require(pending.action in backup, pending.key, 'pending RESYNC_P differs from backup')
    return tuple(head) + (Quiesce(),) + tuple(middle) + tuple(backup) + tuple(tail)
