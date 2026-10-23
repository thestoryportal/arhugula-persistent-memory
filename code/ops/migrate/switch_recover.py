"""Recover an exclusive run folder through the journal, planner and executor.

The operator supplies <run>/journal and <run>/recovery.json. The latter contains
explicit effect arguments by kind: LAUNCHD, QUIESCE, RESYNC_P, BACKUP_COMPARE.
Commands are argv lists; no deployment command or path is implicit. QUIESCE's
clock and sleep are supplied here; programmatic callers can supply a fake clock.
Backup tables and displaced-file evidence belong to the run's caller. A torn
journal is preserved byte-for-byte as journal.torn-<sha256> before replacement.
"""
import argparse
from hashlib import sha256
import json
import math
import os
import sys
import time
from types import MappingProxyType
from uuid import uuid4

from ops.migrate import fdsafe, switch_exec, switch_effects, switch_inverse_core
# [LAW:one-source-of-truth] No recovery-local action, record or state types.
from ops.migrate.root_switch_core import BackupRun, FileState, Install, Launchd, Quiesce, Replace
from ops.migrate.switch_journal_core import (
    AgentIdentity, BackupCompare, Done, Intent, RecoveryState, ResyncP, encode, parse,
    recover as recover_state, _path,
)


def _agent(arguments):
    target = arguments['domain'] + '/' + arguments['service']
    result = switch_effects._run(arguments['command'], ('print', target))
    if result.returncode == 0 and result.stdout.strip():
        return AgentIdentity('loaded')
    if result.returncode == 113 and 'Could not find service' in result.stderr:
        return AgentIdentity('unloaded')
    raise fdsafe.Refusal(target, f'EIO: launchctl print: {result.returncode} {result.stderr}')


def _repair(run, parsed):
    identity, original = switch_exec._read(run + '/journal')
    try:
        current = parse(original.decode('ascii'))
    except UnicodeDecodeError as exc:
        raise fdsafe.Refusal(run + '/journal', 'EILSEQ: non-ASCII journal') from exc
    if current != parsed:
        raise fdsafe.Refusal(run + '/journal', 'ESTALE: journal changed before repair')
    archive = 'journal.torn-' + sha256(original).hexdigest()
    with fdsafe.hold_root(run) as parent:
        entry = switch_exec._entry(parent, archive)
        if entry is None:
            held = switch_exec._create(parent, archive, original, identity.mode)
            fdsafe.close(held.fd, run + '/' + archive)
        elif fdsafe.read_named(parent, archive) != original:
            raise fdsafe.Refusal(run + '/' + archive, 'ESTALE: torn-journal archive differs')
        data = ''.join(encode(record) for record in parsed.records).encode('ascii')
        held = switch_exec._create(parent, '.recovery-' + uuid4().hex, data, identity.mode)
        try:
            switch_exec._replace_existing(held, 'journal', identity)
            return _inode(fdsafe._fstat(held.fd, run + '/journal'))
        finally:
            fdsafe.close(held.fd, run + '/journal')


def _keys(state, run, actions, sequence):
    # [LAW:single-enforcer] Ask the inverse planner for ordinary inverses too;
    # the shell assigns the wire keys, without reimplementing inverse operands.
    candidates = []
    forwards = tuple(item for item in state.done if item.direction == 'forward')
    for item in reversed(forwards):
        if isinstance(item.action, (BackupRun, Quiesce)) or item.action.kind == 'CHECK':
            continue
        key = f'undo:{item.seq}'
        if key not in state.inverse_done:
            single = RecoveryState((item,), (), None, (), 0)
            candidates.extend((action, key) for action in switch_inverse_core.plan(single, run)
                              if not isinstance(action, Quiesce))
    obligations = {}
    for item in state.done + (() if state.pending is None else (state.pending,)):
        if item.direction == 'forward' and isinstance(item.action, BackupRun):
            obligations[str(item.seq)] = switch_inverse_core._pairs(item.action, forwards)
        elif isinstance(item.action, ResyncP):
            obligations[item.key[7:]] = item.action.pairs
    for seq, pairs in reversed(tuple(obligations.items())):
        candidates.extend(((ResyncP(pairs), 'resync:' + seq),
                           (BackupCompare(pairs), 'compare:' + seq)))
    keys = []
    for action in actions:
        if isinstance(action, Quiesce):
            keys.append(f'quiesce:{sequence + len(keys) + 1}')
        else:
            for index, (candidate, key) in enumerate(candidates):
                if candidate == action and key not in state.inverse_done:
                    keys.append(key)
                    candidates.pop(index)
                    break
            else:
                raise fdsafe.Refusal(action.kind, 'EINVAL: inverse has no journal key')
    return tuple(keys)


def _inode(st):
    return st.st_dev, st.st_ino


def _bound(parent, journal_identity):
    # [LAW:single-enforcer] Every by-path step crosses this identity boundary.
    fdsafe._settled(parent)
    entry = fdsafe._scan(parent, 'journal')
    if _inode(entry.st) != journal_identity:
        raise fdsafe.Refusal(parent.path, 'ESTALE: journal identity changed')


def _parse(raw, run):
    try:
        return parse(raw.decode('ascii'))
    except UnicodeDecodeError as exc:
        raise fdsafe.Refusal(run, 'EILSEQ: non-ASCII journal') from exc


def recover(journal_path, *, effect_arguments, seam=lambda *args: None):
    """Return 1 after verified inverses, or print stopped items and return 3."""
    try:
        _path(journal_path, 'journal')
        run, name = os.path.split(journal_path)
        if name != 'journal':
            raise fdsafe.Refusal(journal_path, 'EINVAL: executor journal must be named journal')
        # [LAW:no-ambient-temporal-coupling] Retain the first folder through verification.
        with fdsafe.hold_root(run) as parent:
            journal_identity = _inode(fdsafe._scan(parent, name).st)
            raw = fdsafe.read_named(parent, name)
            _bound(parent, journal_identity)
            return _recover(parent, journal_identity, raw, effect_arguments, seam)
    except fdsafe.Refusal as exc:
        print(str(exc), file=sys.stderr)
        return 3


def _recover(parent, journal_identity, raw, effect_arguments, seam):
    run = parent.path
    parsed = _parse(raw, run)
    images = {}
    for item in parsed.records:
        if (isinstance(item, Intent) and isinstance(item.action, (Replace, Install))
                and isinstance(item.action.pre, FileState)):
            path = item.action.pre.preimage
            if not fdsafe.inside(run, path):
                raise fdsafe.Refusal(path, 'EINVAL: preimage outside run folder')
            _bound(parent, journal_identity)
            images[path] = switch_exec.preimage_hash(path)
            _bound(parent, journal_identity)
    pending = parsed.records[-1] if parsed.records and isinstance(parsed.records[-1], Intent) else None
    observation = None
    if pending is not None:
        _bound(parent, journal_identity)
        observation = (_agent(effect_arguments(pending.action))
                       if isinstance(pending.action, Launchd) else switch_exec.observe(pending.action))
        _bound(parent, journal_identity)
    state = recover_state(parsed, observation, images)
    if state.status:
        for stopped in state.stopped:
            print(stopped, file=sys.stderr)
        for item in state.done:
            if (isinstance(item.action, Launchd) and item.action.to_state == 'loaded'
                    and f'undo:{item.seq}' not in state.inverse_done):
                print(f'{item.key}: agent loaded; pause not held; no inverse applied',
                      file=sys.stderr)
        return 3
    if parsed.truncated or (raw and not raw.endswith(b'\n')):
        _bound(parent, journal_identity)
        journal_identity = _repair(run, parsed)
        _bound(parent, journal_identity)
    if pending is not None:
        # [LAW:single-enforcer] Recovery's classified state decides the receipt.
        outcome = ('applied' if pending in state.done else
                   'uncertain' if pending == state.pending else 'not-applied')
        _bound(parent, journal_identity)
        switch_exec.append_receipt(run, Done(pending.seq, observation, outcome))
        _bound(parent, journal_identity)
    actions = switch_inverse_core.plan(state, run)
    sequence = max((record.seq for record in parsed.records), default=0)
    keys = _keys(state, run, actions, sequence)
    _bound(parent, journal_identity)
    switch_exec.execute(actions, run, direction='inverse', keys=keys,
                        effect_arguments=effect_arguments, seam=seam)
    _bound(parent, journal_identity)
    final = _parse(fdsafe.read_named(parent, 'journal'), run)
    switch_exec._check_journal(final)
    # [LAW:verifiable-goals] A valid older prefix is not proof of this batch.
    intents = {r.seq: r for r in final.records if isinstance(r, Intent)}
    done = {r.seq for r in final.records if isinstance(r, Done) and r.outcome == 'applied'}
    for seq, key in enumerate(keys, sequence + 1):
        if (seq not in done or seq not in intents or intents[seq].direction != 'inverse'
                or intents[seq].key != key):
            raise fdsafe.Refusal(run, f'EIO: inverse {key} has no verified done record')
    _bound(parent, journal_identity)
    return 1


def _argument(value, shape, where):
    """Parse JSON leaves and containers into immutable effect operands."""
    if shape is str:
        if type(value) is not str or '\0' in value:
            raise fdsafe.Refusal(where, 'EINVAL: expected string without NUL')
        return value
    if isinstance(shape, frozenset):
        if type(value) not in shape:
            raise fdsafe.Refusal(where, 'EINVAL: wrong numeric value type')
        try:
            finite = value is None or math.isfinite(value)
        except OverflowError as exc:
            raise fdsafe.Refusal(where, 'EINVAL: numeric conversion failed: ' + str(exc)) from exc
        if not finite:
            raise fdsafe.Refusal(where, 'EINVAL: expected finite number')
        return value
    if isinstance(shape, dict):
        if type(value) is not dict:
            raise fdsafe.Refusal(where, 'EINVAL: expected environment object')
        return MappingProxyType({_argument(k, str, where): _argument(v, str, where)
                                 for k, v in value.items()})
    if type(value) is not list:
        raise fdsafe.Refusal(where, 'EINVAL: expected array')
    if len(shape) == 1:
        return tuple(_argument(v, shape[0], where) for v in value)
    if len(value) != len(shape):
        raise fdsafe.Refusal(where, 'EINVAL: wrong array length')
    return tuple(_argument(v, s, where) for v, s in zip(value, shape))


def _configuration(config):
    # [LAW:parse-dont-validate] JSON becomes immutable kwargs once, before recovery;
    # later observations and effects receive only these parsed operands.
    if type(config) is not dict:
        raise fdsafe.Refusal('recovery.json', 'EINVAL: expected effect argument object')
    number = frozenset((int, float))
    schemas = {
        'LAUNCHD': dict(command=(str,), domain=str, service=str, plist=str),
        'QUIESCE': dict(command=(str,), timeout=number, interval=number),
        'RESYNC_P': dict(command=(str,), table=str, env={str: str},
                         timeout=frozenset((int, float, type(None)))),
        'BACKUP_COMPARE': dict(displaced=((str, str, str),)),
    }
    for kind in config.keys() - schemas.keys():
        raise fdsafe.Refusal(kind, 'EINVAL: unknown effect kind key')
    parsed = {}
    for kind, fields in schemas.items():
        if kind not in config:
            raise fdsafe.Refusal(kind, 'EINVAL: missing effect kind key')
        values = config[kind]
        if type(values) is not dict:
            raise fdsafe.Refusal(kind, 'EINVAL: expected effect argument object')
        for key in values.keys() - fields.keys():
            raise fdsafe.Refusal(kind + '.' + key, 'EINVAL: extra key')
        arguments = {}
        for key, shape in fields.items():
            if key not in values:
                raise fdsafe.Refusal(kind + '.' + key, 'EINVAL: missing key')
            arguments[key] = _argument(values[key], shape, kind + '.' + key)
        if 'command' in arguments and not arguments['command']:
            raise fdsafe.Refusal(kind + '.command', 'EINVAL: empty argv')
        parsed[kind] = arguments
    parsed['QUIESCE'].update(clock=time.monotonic, sleep=time.sleep)
    return MappingProxyType({kind: MappingProxyType(values) for kind, values in parsed.items()})


def main(argv=None):
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--journal', required=True)
        args = parser.parse_args(argv)
        run = os.path.dirname(args.journal)
        with fdsafe.hold_root(run) as parent:
            data = fdsafe.read_named(parent, 'recovery.json')
            fdsafe._settled(parent)
        try:
            config = json.loads(data)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise fdsafe.Refusal(run + '/recovery.json', 'EINVAL: invalid effect configuration') from exc
        arguments = _configuration(config)
        return recover(args.journal, effect_arguments=lambda action: arguments[action.kind])
    except fdsafe.Refusal as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except Exception as exc:
        # [LAW:no-silent-failure] Exit 1 belongs only to verified recovery.
        message = str(exc).replace('\r', r'\r').replace('\n', r'\n')
        print(f'switch_recover: unexpected {type(exc).__name__}: {message}', file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
