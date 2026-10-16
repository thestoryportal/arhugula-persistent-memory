"""Pure pre-run validation of one ICM v2.1 Move (SPEC.md:206, plan Step 202).

validate_move opens no file, writes none and decides no target: every fact it judges
is an argument, and the wire schema is read once at import. An empty tuple admits the
move. A fact the caller did not supply yields UNVERIFIED, never an empty PASS
(SPEC.md:230). Malformed input is refused with one FAIL, never repaired.
"""
import hashlib
from pathlib import PurePath, PurePosixPath

import icm21_check


SCHEMA = icm21_check.audit_schema()
# SPEC.md:83-84 and WIRE-CONTRACTS.md:133: these rows emit no move operation.
NO_ACTION = frozenset({'KEEP', 'RETAIN_CONTAINER', 'HOLD', 'FOLLOW_PARENT'})
PATTERN_CHARS = frozenset('*?[]<>')  # SPEC.md:87
LINK_HOPS = 40


def finding(move_id, status, paths, reason):
    identity = move_id + '\n' + reason
    return {'id': 'F-MOVE-' + hashlib.sha256(identity.encode()).hexdigest(),
            'status': status, 'prd_ids': ['ICM-R4'], 'paths': paths, 'evidence': [],
            'reason': reason, 'previous_finding': None, 'resolution_receipt': None}


def wire_path(value):
    text = str(value) if isinstance(value, PurePath) else value
    icm21_check.validate_schema(text, {'$ref': '#/$defs/path'}, SCHEMA['$defs'])
    return PurePosixPath(text)


def wire_record(name, value):
    """Validate against the sealed definition itself: icm21_check.WIRE_TYPES, which
    gates validate_wire, does not list Move or LeafRecord."""
    icm21_check.validate_schema(value, SCHEMA['$defs'][name], SCHEMA['$defs'])


def within(path, root):
    return path == root or root in path.parents


def link_stays_inside(link, text, unit, links):
    """Walk the link's text from inside the unit, following the unit's own links.
    True when every step stays inside the unit, False when one leaves it, None on a loop."""
    if link == unit or text.startswith('/'):
        return False  # an absolute text keeps naming the old location after the move
    parts = list(link.parent.relative_to(unit).parts) + text.split('/')
    done, hops = unit, 0
    while parts:
        part = parts.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            done = done.parent
        elif done / part in links:
            hops += 1
            if hops > LINK_HOPS:
                return None
            target = links[done / part]
            if target.startswith('/'):
                return False
            parts = target.split('/') + parts
            continue
        else:
            done = done / part
        if not within(done, unit):
            return False
    return True


def validate_move(move, admitted_roots, *, other_moves=None, existing_paths=None,
                  run_units=None, leaves=None):
    """Findings that block this move; () admits it.

    other_moves: the plan's other Moves. existing_paths: absolute paths observed present.
    run_units: absolute run-unit roots. leaves: the LeafRecords of this move's source.
    """
    move_id = move['id'] if type(move) is dict and type(move.get('id')) is str \
        and move['id'] else 'unidentified'
    try:
        wire_record('Move', move)
        source, target = PurePosixPath(move['source']), PurePosixPath(move['target'])
        roots = tuple(wire_path(root) for root in admitted_roots)
        if other_moves is not None:
            for other in other_moves:
                wire_record('Move', other)
        existing = None if existing_paths is None else \
            frozenset(wire_path(path) for path in existing_paths)
        runs = None if run_units is None else tuple(wire_path(path) for path in run_units)
        if leaves is not None:
            for record in leaves:
                wire_record('LeafRecord', record)
                icm21_check.require(within(PurePosixPath(record['source']), source),
                                    'leaf outside the unit: ' + record['source'])
                icm21_check.require((record['kind'] == 'symlink')
                                    == (record['link_text'] is not None),
                                    'link text disagrees with kind: ' + record['source'])
    except (ValueError, TypeError, KeyError) as error:
        return (finding(move_id, 'FAIL', [], 'Malformed input refused: ' + str(error)),)

    sides = [str(source), str(target)]
    found = []

    def fail(reason, status='FAIL'):
        found.append(finding(move_id, status, sides, reason))

    if move['action'] in NO_ACTION:
        fail(move['action'] + ' emits no executable action')
    for name, path in (('source', source), ('target', target)):
        if PATTERN_CHARS & set(str(path)):
            fail(name + ' is a wildcard or angle-bracket path: ' + str(path))
        if not any(root in path.parents for root in roots):
            fail(name + ' escapes every admitted root: ' + str(path))
    if within(target, source):
        fail('target lies inside its own source')

    if other_moves is None:
        fail('other_moves not supplied: overlap and collision unchecked', 'UNVERIFIED')
    else:
        for other in other_moves:
            if other['id'] == move['id']:
                fail('duplicate move ID in the plan: ' + other['id'])
            if within(target, PurePosixPath(other['source'])):
                fail("target lies inside another move's source: " + other['id'])
            other_target = PurePosixPath(other['target'])
            if within(target, other_target) or within(other_target, target):
                fail("target collides with another move's target: " + other['id'])

    if existing is None:
        fail('existing_paths not supplied: target existence unchecked', 'UNVERIFIED')
    elif target in existing:
        fail('target already exists: ' + str(target))

    if runs is None:
        fail('run_units not supplied: run splitting unchecked', 'UNVERIFIED')
    else:
        for run in runs:
            if run in source.parents or (move['action'] == 'SPLIT_FILES'
                                         and within(run, source)):
                fail('move splits run unit ' + str(run))

    if leaves is None:
        fail('leaves not supplied: link boundary unchecked', 'UNVERIFIED')
    else:
        records = [dict(record, source=PurePosixPath(record['source'])) for record in leaves]
        if move['kind'] != 'directory' and not any(r['source'] == source for r in records):
            fail('leaf manifest lacks the moved object', 'UNVERIFIED')
        links = {r['source']: r['link_text'] for r in records if r['kind'] == 'symlink'}
        for link, text in sorted(links.items()):
            inside = link_stays_inside(link, text, source, links)
            if inside is None:
                fail('ambiguous link (loop): ' + str(link))
            elif not inside:
                fail('link crosses the unit boundary: ' + str(link))
        names = {}
        for r in records:
            if r['kind'] == 'file':
                names.setdefault((r['device'], r['inode']), []).append(r)
        for group in names.values():
            if any(r['nlink'] > len(group) for r in group):
                fail('hard link crosses the unit boundary: ' + str(group[0]['source']))

    return tuple({item['id']: item for item in found}.values())
