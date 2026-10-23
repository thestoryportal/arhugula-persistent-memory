"""Pure version-1 codec for backup-pre.json; no filesystem observations."""
import errno
import json
import re
from dataclasses import dataclass
from typing import Literal, NamedTuple

from ops.migrate import fdsafe


class Leaf(NamedTuple):
    path: str
    kind: Literal['file', 'symlink']
    value: str


class Destination(NamedTuple):
    root: str
    leaves: tuple[Leaf, ...]


@dataclass(frozen=True)
class PreState:
    destinations: tuple[Destination, ...]

    # [LAW:single-enforcer] Both construction paths cross this semantic boundary.
    def __post_init__(self):
        _check(self.destinations)


def _refuse(reason: str):
    raise fdsafe.Refusal('backup-pre.json', 'EINVAL: ' + reason, errno.EINVAL)


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _refuse('duplicate JSON key')
        result[key] = value
    return result


def _check(destinations: tuple[Destination, ...]):
    if type(destinations) is not tuple:
        _refuse('expected destinations tuple')
    seen = set()
    for destination in destinations:
        if type(destination) is not Destination:
            _refuse('expected Destination')
        root = destination.root
        if type(root) is not str or not root.startswith('/'):
            _refuse('expected absolute root')
        if type(destination.leaves) is not tuple:
            _refuse('expected leaves tuple')
        for leaf in destination.leaves:
            if type(leaf) is not Leaf:
                _refuse('expected Leaf')
            path, kind, content = leaf
            if type(path) is not str or any(p in ('', '.', '..') for p in path.split('/')):
                _refuse('expected relative leaf path without empty, dot or dotdot components')
            if path == '.last_success':
                _refuse('root stamp is not evidence')
            if type(kind) is not str or kind not in ('file', 'symlink'):
                _refuse('unknown leaf kind')
            if type(content) is not str:
                _refuse('expected leaf text')
            if kind == 'file' and re.fullmatch('[0-9a-f]{64}', content) is None:
                _refuse('expected lowercase sha256')
            if (root, path) in seen:
                _refuse('duplicate root and path')
            seen.add((root, path))


def parse(data: bytes) -> PreState:
    if type(data) is not bytes:
        _refuse('expected bytes')
    try:
        value = json.loads(data, object_pairs_hook=_object)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise fdsafe.Refusal('backup-pre.json', 'EINVAL: invalid JSON', errno.EINVAL) from exc
    if type(value) is not dict or value.keys() != {'version', 'destinations'}:
        _refuse('expected exact pre-state object')
    if type(value['version']) is not int or value['version'] != 1:
        _refuse('unknown version')
    if type(value['destinations']) is not list:
        _refuse('expected destinations array')
    destinations = []
    for destination in value['destinations']:
        if type(destination) is not dict or destination.keys() != {'root', 'leaves'}:
            _refuse('expected exact destination object')
        root = destination['root']
        if type(destination['leaves']) is not list:
            _refuse('expected leaves array')
        leaves = []
        for leaf in destination['leaves']:
            if type(leaf) is not list or len(leaf) != 3:
                _refuse('expected leaf triple')
            leaves.append(Leaf(*leaf))
        destinations.append(Destination(root, tuple(leaves)))
    return PreState(tuple(destinations))


def encode(pre: PreState) -> bytes:
    # [LAW:single-enforcer] Serialization consumes the proof; it never rechecks it.
    return json.dumps({'version': 1, 'destinations': [
        {'root': d.root, 'leaves': d.leaves} for d in pre.destinations
    ]}, separators=(',', ':')).encode('utf-8')
