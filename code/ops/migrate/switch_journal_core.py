"""Pure T412 journal contract. All observations come from the shell.

Wire v1: one JSON array per LF-terminated line:
  ["intent", seq, direction, key, action, pre_identity]
  ["done", seq, post_identity]
  ["done", seq, observed_identity, "not-applied" or "uncertain"]
seq is a positive increasing intent number; done closes that intent.
The short receipt attests application; the long receipt durably closes a
recovery observation without claiming application. Its classification must
match the action's observation rule. Only applied keys cannot be retried.
direction is forward or inverse; key is a stable operation ID unique within
that direction. Inverse keys survive recovery retries.
Actions are [kind, operands...]: RENAME(src,dst), REPLACE(path,pre,hex,mode),
INSTALL(dst,pre,hex,mode), CHECK(id), LAUNCHD(from,to), QUIESCE(),
BACKUP_RUN(pairs), BACKUP_COMPARE(pairs), RESYNC_P(pairs). Each pair is
[backend,src,dst,excludes]. File pre is ["file",hex,sha256,mode,preimage] or
["absent"]. Identities are ["file",sha256,mode], ["absent"],
["rename",src_inode,dst_inode], ["agent",state], ["none"]. An inode is
[st_dev,st_ino] or null for observed absence. Missing observations are not absence.

A final non-LF line that is a proper prefix of valid JSON is retained as truncated;
any other malformed line refuses. Schema-invalid JSON always refuses. The shell resolves the torn suffix before appending. It closes
intents with applied, not-applied or uncertain receipts before appending other
actions. Unclosed intents may only be last; a missing classification refuses.
Recovery consumers exclude inverse_done keys; pending RESYNC_P restarts in full.
A classified uncertain backup remains pending throughout rollback. A later
uncertain RESYNC_P supersedes that obligation with its restart-from-M action;
there is still at most one pending obligation. Completed inverse keys are kept
so a completed RESYNC_P is not repeated just because BACKUP_RUN was uncertain.
When pre and post coincide, post wins (a no-op). NoIdentity is the only valid
observation for no-change and non-observable actions. preimages maps each
required preimage path to its observed sha256 or None for observed absence.
Missing observations refuse; missing/corrupt copies return status 3 as data.
Status 0 means a usable description, never successful rollback.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from json import JSONDecodeError, dumps, loads
from typing import Literal

from ops.migrate.fdsafe import Refusal
from ops.migrate import root_switch_core as a


@dataclass(frozen=True)
class FileIdentity:
    sha256: str
    mode: int


@dataclass(frozen=True)
class Inode:
    st_dev: int
    st_ino: int


@dataclass(frozen=True)
class RenameIdentity:
    src: Inode | None
    dst: Inode | None


@dataclass(frozen=True)
class AgentIdentity:
    state: Literal['loaded', 'unloaded']


@dataclass(frozen=True)
class NoIdentity:
    pass


Identity = FileIdentity | a.Absent | RenameIdentity | AgentIdentity | NoIdentity


@dataclass(frozen=True)
class BackupCompare:
    pairs: tuple[a.BackupPair, ...]
    kind: Literal['BACKUP_COMPARE'] = field(default='BACKUP_COMPARE', init=False)


@dataclass(frozen=True)
class ResyncP:
    pairs: tuple[a.BackupPair, ...]
    kind: Literal['RESYNC_P'] = field(default='RESYNC_P', init=False)


Action = a.Action | BackupCompare | ResyncP


# [LAW:types-are-the-program] Intent operands cannot be mistaken for a receipt.
@dataclass(frozen=True)
class Intent:
    seq: int
    direction: Literal['forward', 'inverse']
    key: str
    action: Action
    pre: Identity


@dataclass(frozen=True)
class Done:
    seq: int
    post: Identity
    outcome: Literal['applied', 'not-applied', 'uncertain'] = 'applied'


@dataclass(frozen=True)
class Journal:
    records: tuple[Intent | Done, ...]
    truncated: str


@dataclass(frozen=True)
class RecoveryState:
    done: tuple[Intent, ...]
    inverse_done: tuple[str, ...]
    pending: Intent | None
    stopped: tuple[str, ...]
    status: Literal[0, 3]


def _require(condition, where, reason):
    if not condition:
        raise Refusal(where, 'EINVAL: ' + reason)


def _array(value, size, where):
    _require(type(value) is list and len(value) == size, where, 'invalid array')


def _text(value, where):
    _require(type(value) is str and bool(value) and all(ord(c) >= 32 for c in value),
             where, 'invalid text')
    return value


def _path(value, where):
    _text(value, where)
    _require(value.startswith('/') and all(p not in ('', '.', '..')
             for p in value[1:].split('/')), where, 'invalid absolute path')
    return value


def _number(value, where):
    _require(type(value) is int and value >= 0, where, 'invalid integer')
    return value


def _mode(value, where):
    _number(value, where)
    _require(value <= 0o7777, where, 'invalid mode')
    return value


def _hex(value, where):
    _require(type(value) is str and len(value) % 2 == 0
             and all(c in '0123456789abcdef' for c in value), where, 'invalid hex')
    return bytes.fromhex(value)


def _hash(value, where):
    _require(type(value) is str and len(value) == 64
             and all(c in '0123456789abcdef' for c in value), where, 'invalid sha256')
    return value


def _agent(value, where):
    _require(type(value) is str and value in ('loaded', 'unloaded'), where, 'invalid agent state')
    return value


def _inode(value, where):
    if value is None:
        return None
    _array(value, 2, where)
    return Inode(_number(value[0], where), _number(value[1], where))


def _identity(value, where):
    _require(type(value) is list and bool(value), where, 'invalid identity')
    tag = value[0]
    if tag == 'file':
        _array(value, 3, where)
        return FileIdentity(_hash(value[1], where), _mode(value[2], where))
    if tag == 'absent':
        _array(value, 1, where)
        return a.Absent()
    if tag == 'rename':
        _array(value, 3, where)
        return RenameIdentity(_inode(value[1], where), _inode(value[2], where))
    if tag == 'agent':
        _array(value, 2, where)
        return AgentIdentity(_agent(value[1], where))
    _require(tag == 'none', where, 'unknown identity')
    _array(value, 1, where)
    return NoIdentity()


def _pre(value, where):
    if value == ['absent']:
        return a.Absent()
    _array(value, 5, where)
    _require(value[0] == 'file', where, 'invalid preimage')
    data = _hex(value[1], where)
    digest = _hash(value[2], where)
    _require(sha256(data).hexdigest() == digest, where, 'preimage bytes differ from sha256')
    return a.FileState(data, digest, _mode(value[3], where), _path(value[4], where))


def _pairs(value, where):
    _require(type(value) is list and bool(value), where, 'missing pairs')
    result = []
    for row in value:
        _array(row, 4, where)
        _require(row[0] == 'ssd', where, 'expected ssd pair')
        result.append(a.BackupPair('ssd', _path(row[1], where),
                                  _path(row[2], where), _path(row[3], where)))
    return tuple(result)


def _action(value, where):
    _require(type(value) is list and bool(value), where, 'invalid action')
    kind = value[0]
    if kind == 'RENAME':
        _array(value, 3, where)
        src, dst = _path(value[1], where), _path(value[2], where)
        _require(src != dst, where, 'same rename paths')
        return a.Rename(src, dst)
    if kind in ('REPLACE', 'INSTALL'):
        _array(value, 5, where)
        path, pre = _path(value[1], where), _pre(value[2], where)
        data, mode = _hex(value[3], where), _mode(value[4], where)
        if kind == 'REPLACE':
            _require(type(pre) is a.FileState, where, 'absent REPLACE preimage')
            return a.Replace(path, pre, data, mode)
        return a.Install(path, pre, data, mode)
    if kind == 'LAUNCHD':
        _array(value, 3, where)
        return a.Launchd(_agent(value[1], where), _agent(value[2], where))
    if kind == 'CHECK':
        _array(value, 2, where)
        return a.Check(_text(value[1], where))
    if kind == 'QUIESCE':
        _array(value, 1, where)
        return a.Quiesce()
    if kind in ('BACKUP_RUN', 'BACKUP_COMPARE', 'RESYNC_P'):
        _array(value, 2, where)
        pairs = _pairs(value[1], where)
        if kind == 'BACKUP_RUN':
            return a.BackupRun(pairs)
        if kind == 'BACKUP_COMPARE':
            return BackupCompare(pairs)
        return ResyncP(pairs)
    raise Refusal(where, 'EINVAL: unknown action')


def _file_identity(pre):
    if type(pre) is a.FileState:
        return FileIdentity(pre.sha256, pre.mode)
    return pre


def _post(item):
    action = item.action
    if type(action) in (a.Replace, a.Install):
        return FileIdentity(sha256(action.post_bytes).hexdigest(), action.post_mode)
    if type(action) is a.Rename:
        return RenameIdentity(None, item.pre.src)
    if type(action) is a.Launchd:
        return AgentIdentity(action.to_state)
    return NoIdentity()


def _record(value, where):
    _require(type(value) is list and bool(value), where, 'invalid record')
    if value[0] == 'done':
        _require(len(value) in (3, 4), where, 'invalid done array')
        seq = _number(value[1], where)
        _require(seq > 0, where, 'zero sequence')
        outcome = 'applied' if len(value) == 3 else value[3]
        _require(outcome in ('applied', 'not-applied', 'uncertain'), where, 'invalid outcome')
        return Done(seq, _identity(value[2], where), outcome)
    _require(value[0] == 'intent', where, 'unknown record')
    _array(value, 6, where)
    seq = _number(value[1], where)
    _require(seq > 0, where, 'zero sequence')
    _require(value[2] in ('forward', 'inverse'), where, 'invalid direction')
    key = _text(value[3], where)
    action, pre = _action(value[4], where), _identity(value[5], where)
    if type(action) in (a.Replace, a.Install):
        _require(pre == _file_identity(action.pre), where, 'pre-identity mismatch')
    elif type(action) is a.Rename:
        _require(type(pre) is RenameIdentity and pre.src is not None and pre.dst is None,
                 where, 'invalid rename pre-identity')
    elif type(action) is a.Launchd:
        _require(pre == AgentIdentity(action.from_state), where, 'agent pre-identity mismatch')
    else:
        _require(type(pre) is NoIdentity, where, 'unexpected pre-identity')
    if type(action) in (BackupCompare, ResyncP):
        _require(value[2] == 'inverse', where, 'inverse-only action')
    return Intent(seq, value[2], key, action, pre)


def _json_integer(text):
    # Avoid json's ambient interpreter digit limit; no filesystem or env lookup.
    negative = text.startswith('-')
    digits = text[1:] if negative else text
    result = 0
    for char in digits:
        result = result * 10 + ord(char) - 48
    return -result if negative else result


# [LAW:parse-dont-validate] JSON crosses once into frozen typed records.
def parse(text: str) -> Journal:
    _require(type(text) is str, 'journal', 'expected text')
    lines = text.split('\n')
    records = []
    truncated = ''
    for index, line in enumerate(lines):
        last = index == len(lines) - 1
        if last and line == '':
            break
        where = f'line {index + 1}'
        try:
            value = loads(line, parse_int=_json_integer)
        except JSONDecodeError as exc:
            # [LAW:parse-dont-validate] Only extendible JSON grammar states are torn writes.
            # Stack entries describe the remaining grammar; no error-message heuristics.
            digits = {ch: (ch, 'digits') for ch in '0123456789'}
            integer = {'0': ('0', 'fraction'),
                       **{ch: (ch, 'digits', 'fraction') for ch in '123456789'}}
            rules = {
                'value': {'"': ('"', 'string'), '[': ('[', 'array-first'),
                          '{': ('{', 'object-first'), 't': tuple('true'),
                          'f': tuple('false'), 'n': tuple('null'),
                          '-': ('-', 'integer'), **integer},
                'integer': integer,
                'digits': digits,
                'fraction': {'.': ('.', 'digit', 'exponent')},
                'digit': digits,
                'exponent': {ch: (ch, 'sign') for ch in 'eE'},
                'sign': {'+': ('+', 'digit'), '-': ('-', 'digit'), **digits},
                'array-first': {']': (']',)},
                'array-end': {']': (']',), ',': (',', 'value', 'array-end')},
                'object-first': {'}': ('}',)},
                'object-end': {'}': ('}',), ',': (',', 'key', ':', 'value', 'object-end')},
                'key': {'"': ('"', 'string')},
            }
            empty = {'digits': (), 'fraction': ('exponent',), 'exponent': (),
                     'array-first': ('value', 'array-end'),
                     'object-first': ('key', ':', 'value', 'object-end')}
            pending = ('value',)
            extendible = last
            for char in line:
                if not extendible:
                    break
                while True:
                    if not pending:
                        extendible = char in ' \t\r'
                        break
                    symbol = pending[0]
                    if symbol in ('value', 'array-first', 'array-end', 'object-first',
                                  'object-end', 'key', ':') and char in ' \t\r':
                        break
                    if symbol in rules:
                        if char in rules[symbol]:
                            pending = rules[symbol][char] + pending[1:]
                        elif symbol in empty:
                            pending = empty[symbol] + pending[1:]
                        else:
                            extendible = False
                            break
                        continue
                    if symbol == 'string':
                        if char == '"':
                            pending = pending[1:]
                        elif char == '\\':
                            pending = ('escape',) + pending
                        else:
                            extendible = ord(char) >= 32
                    elif symbol == 'escape':
                        extendible = char in '"\\/bfnrtu'
                        pending = (('hex',) * 4 if char == 'u' else ()) + pending[1:]
                    elif symbol == 'hex':
                        extendible = char in '0123456789abcdefABCDEF'
                        pending = pending[1:]
                    else:
                        extendible = char == symbol
                        pending = pending[1:]
                    break
            if extendible:
                truncated = line
                break
            raise Refusal(where, 'EINVAL: malformed JSON') from exc
        except RecursionError as exc:
            raise Refusal(where, 'EINVAL: JSON nesting exceeds parser capacity') from exc
        records.append(_record(value, where))
    return Journal(tuple(records), truncated)


def _wire_inode(value):
    return None if value is None else [value.st_dev, value.st_ino]


def _wire_identity(value):
    if type(value) is FileIdentity:
        return ['file', value.sha256, value.mode]
    if type(value) is a.Absent:
        return ['absent']
    if type(value) is RenameIdentity:
        return ['rename', _wire_inode(value.src), _wire_inode(value.dst)]
    if type(value) is AgentIdentity:
        return ['agent', value.state]
    _require(type(value) is NoIdentity, 'identity', 'unknown identity type')
    return ['none']


def _wire_pre(value):
    if type(value) is a.Absent:
        return ['absent']
    return ['file', value.data.hex(), value.sha256, value.mode, value.preimage]


def _wire_action(action):
    if type(action) is a.Rename:
        return [action.kind, action.src, action.dst]
    if type(action) is a.Replace:
        return [action.kind, action.path, _wire_pre(action.pre), action.post_bytes.hex(), action.post_mode]
    if type(action) is a.Install:
        return [action.kind, action.dst, _wire_pre(action.pre), action.post_bytes.hex(), action.post_mode]
    if type(action) is a.Launchd:
        return [action.kind, action.from_state, action.to_state]
    if type(action) is a.Check:
        return [action.kind, action.check_id]
    if type(action) is a.Quiesce:
        return [action.kind]
    _require(type(action) in (a.BackupRun, BackupCompare, ResyncP), 'action', 'unknown action type')
    return [action.kind, [[p.backend, p.src, p.dst, p.excludes] for p in action.pairs]]


def encode(record: Intent | Done) -> str:
    if type(record) is Intent:
        value = ['intent', record.seq, record.direction, record.key,
                 _wire_action(record.action), _wire_identity(record.pre)]
    else:
        _require(type(record) is Done, 'record', 'unknown record type')
        value = ['done', record.seq, _wire_identity(record.post)]
        if record.outcome != 'applied':
            value.append(record.outcome)
    return dumps(value, ensure_ascii=True, separators=(',', ':')) + '\n'


def _decision(item, observation):
    where = item.key
    _require(type(observation) in (FileIdentity, a.Absent, RenameIdentity,
                                  AgentIdentity, NoIdentity), where, 'unexpected observation')
    if type(observation) is RenameIdentity:
        _require(all(value is None or type(value) is Inode for value in (observation.src, observation.dst)),
                 where, 'invalid inode observation')
    observation = _identity(_wire_identity(observation), where)
    # [LAW:single-enforcer] Each kind has an explicit rule, never a default verdict.
    kind = item.action.kind
    if kind in ('REPLACE', 'INSTALL', 'RENAME', 'LAUNCHD'):
        if observation == _post(item):
            return 'done'
        if observation == item.pre:
            return 'not-done'
        raise Refusal(where, 'EINVAL: observation is neither pre nor post')
    if kind in ('CHECK', 'QUIESCE', 'BACKUP_COMPARE'):
        _require(type(observation) is NoIdentity, where, 'unexpected observation')
        return 'not-done'
    if kind in ('BACKUP_RUN', 'RESYNC_P'):
        _require(type(observation) is NoIdentity, where, 'unexpected observation')
        return 'pending'
    raise Refusal(where, 'EINVAL: unknown action kind')


def _restore_path(path, done):
    for item in reversed(done):
        action = item.action
        if item.direction == 'forward' and type(action) is a.Rename:
            if path == action.dst or path.startswith(action.dst + '/'):
                path = action.src + path[len(action.dst):]
    return path


def _supersede(prior, current, done):
    if prior is None:
        return
    _require(current.direction == 'inverse' and type(current.action) is ResyncP,
             current.key, 'multiple uncertain backup obligations')
    expected = prior.action.pairs
    if type(prior.action) is a.BackupRun:
        expected = tuple(a.BackupPair(p.backend, _restore_path(p.src, done),
                         _restore_path(p.dst, done), _restore_path(p.excludes, done)) for p in expected)
        _require(len(current.action.pairs) == 1 and current.action.pairs[0] in expected
                 and all(_covers(current.action.pairs[0], pair) for pair in expected),
                 current.key, 'RESYNC_P backup coverage differs')
    else:
        _require(current.key == prior.key, current.key, 'RESYNC_P retry key changed')
        _require(current.action.pairs == expected, current.key, 'RESYNC_P backup coverage differs')


def _covers(parent, child):
    if child.src == parent.src:
        return child.dst == parent.dst
    return child.src.startswith(parent.src + '/') and child.dst == parent.dst + child.src[len(parent.src):]


def recover(journal: Journal, observation: Identity | None,
            preimages: dict[str, str | None]) -> RecoveryState:
    _require(type(journal) is Journal, 'journal', 'expected parsed Journal')
    _require(type(preimages) is dict, 'preimages', 'expected observations')
    done, keys, stopped = [], set(), []
    bindings = {}
    pending = None
    uncertain = None
    last_seq = 0
    inverse = False
    for line, record in enumerate(journal.records, 1):
        where = f'line {line}'
        if type(record) is Intent:
            _require(pending is None, where, 'unclosed intent')
            _require(record.seq > last_seq, where, 'sequence is not increasing')
            _require((record.direction, record.key) not in keys, record.key, 'duplicate operation')
            identity = (record.direction, record.key)
            if identity in bindings:
                _require(bindings[identity] == (record.action, record.pre), record.key,
                         'operation operands changed')
            bindings[identity] = (record.action, record.pre)
            _require(not inverse or record.direction == 'inverse', where, 'forward after inverse')
            inverse = record.direction == 'inverse'
            last_seq = record.seq
            pending = record
            if type(record.action) in (a.Replace, a.Install):
                pre = record.action.pre
                if type(pre) is a.FileState:
                    _require(pre.preimage in preimages, record.key, 'missing preimage observation')
                    digest = preimages[pre.preimage]
                    if digest is not None:
                        _hash(digest, record.key)
                    if digest != pre.sha256:
                        stopped.append(f'{record.key}: {pre.preimage}: missing or changed preimage')
        else:
            _require(type(record) is Done and pending is not None, where, 'done without intent')
            _require(record.seq == pending.seq, where, 'done sequence mismatch')
            if record.outcome == 'applied':
                _require(record.post == _post(pending), pending.key, 'done post-identity mismatch')
                done.append(pending)
                keys.add((pending.direction, pending.key))
            else:
                verdict = _decision(pending, record.post)
                expected = 'not-done' if record.outcome == 'not-applied' else 'pending'
                _require(verdict == expected, pending.key, 'classification does not match observation')
                if verdict == 'pending':
                    _supersede(uncertain, pending, done)
                    uncertain = pending
            pending = None
    if pending is None:
        _require(observation is None, 'observation', 'no pending intent')
    else:
        verdict = _decision(pending, observation)
        if verdict == 'pending':
            _supersede(uncertain, pending, done)
        if verdict == 'done':
            done.append(pending)
        if verdict != 'pending':
            pending = None
    if uncertain is not None and any((r.direction, r.key) == (uncertain.direction, uncertain.key) for r in done):
        uncertain = None
    if pending is None:
        pending = uncertain
    return RecoveryState(tuple(done), tuple(r.key for r in done if r.direction == 'inverse'),
                         pending, tuple(stopped), 3 if stopped else 0)
