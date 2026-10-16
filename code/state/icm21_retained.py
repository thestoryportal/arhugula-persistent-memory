"""check_retained: C-MOVE, C-KEEP and C-CONTAINER over admitted and observed leaf manifests.

SPEC.md:208 and :602-605, as amended by A/H-SLICE.md items 1, 9 and 10: MetadataSet is
dropped, and M/.git is never a subject. Pure: the caller reads the bound documents and
re-inventories the post state; this module compares only the values it is handed. Any
document it cannot check is refused with a finding, never treated as an empty PASS.
"""
import hashlib
import json

PRD_IDS = ['ICM-R4']
RETENTION_KEYS = frozenset({'schema_version', 'leaves', 'routes', 'repairs', 'executor',
                            'containers'})
CONTAINER_KEYS = frozenset({'id', 'source', 'moved_source_paths', 'added_source_paths',
                            'rewrite_ids'})
LEAF_KEYS = frozenset({'source', 'kind', 'bytes', 'sha256', 'link_text', 'device', 'inode',
                       'nlink'})
REPAIR_KEYS = frozenset({'schema_version', 'id', 'prd_ids', 'plan_id', 'plan_sha256', 'source',
                         'target', 'before_sha256', 'after_sha256', 'edits', 'reader_ids',
                         'reference_ids'})
ROUTE_HEADER = ['requirement_id', 'source', 'target', 'kind', 'observed_bytes', 'action',
                'lane', 'scientific_role']
COMPARED = ('kind', 'bytes', 'sha256', 'link_text')
GIT_SUBJECT = 'M/.git is never a subject (H-SLICE.md item 1)'


class Refusal(Exception):
    def __init__(self, status, reason, paths=()):
        super().__init__(reason)
        self.status, self.reason, self.paths = status, reason, list(paths)


def refuse(condition, reason, paths=(), status='UNVERIFIED'):
    if not condition:
        raise Refusal(status, reason, paths)


def is_path(value):
    return (type(value) is str and value.startswith('/') and len(value) > 1
            and not any(char in value for char in '\x00\r\n')
            and all(part not in ('', '.', '..') for part in value.split('/')[1:]))


def is_sha(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def is_int(value):
    return type(value) is int and value >= 0


def keys(name, value, expected):
    refuse(type(value) is dict, name + ' is not an object')
    extra, missing = sorted(value.keys() - expected), sorted(expected - value.keys())
    refuse(not extra and not missing, name + ' keys differ from the wire contract: extra '
           + str(extra) + ', missing ' + str(missing))


def under(path, directory):
    return path.startswith(directory + '/')


def bound(binding, documents):
    keys('Binding', binding, {'path', 'sha256'})
    refuse(is_path(binding['path']) and is_sha(binding['sha256']), 'Binding is malformed')
    refuse(binding['path'] in documents, 'bound document was not supplied', [binding['path']])
    data = documents[binding['path']]
    refuse(type(data) is bytes, 'bound document is not bytes', [binding['path']])
    refuse(hashlib.sha256(data).hexdigest() == binding['sha256'],
           'binding digest differs from the supplied bytes', [binding['path']], 'FAIL')
    return data


def parse_json(data, name):
    try:
        return json.loads(data.decode('utf-8'),
                          parse_constant=lambda token: refuse(False, name + ' has ' + token))
    except (UnicodeDecodeError, ValueError) as error:
        raise Refusal('UNVERIFIED', name + ' is not valid JSON: ' + type(error).__name__)


def leaf_manifest(value, name):
    keys(name, value, {'schema_version', 'leaves'})
    refuse(type(value['schema_version']) is int and value['schema_version'] == 1,
           name + ' schema_version is not 1')
    refuse(type(value['leaves']) is list, name + ' leaves is not an array')
    leaves = {}
    for leaf in value['leaves']:
        keys('LeafRecord', leaf, LEAF_KEYS)
        refuse(is_path(leaf['source']), name + ' leaf source is not a normalized path')
        refuse(leaf['kind'] in ('file', 'symlink', 'socket') and is_sha(leaf['sha256'])
               and all(is_int(leaf[key]) for key in ('bytes', 'device', 'inode', 'nlink'))
               and (leaf['link_text'] is None or (type(leaf['link_text']) is str
                                                  and leaf['link_text'])),
               name + ' leaf is malformed', [leaf['source']])
        refuse(leaf['source'] not in leaves, name + ' duplicate leaf source', [leaf['source']])
        leaves[leaf['source']] = leaf
    return leaves


def route_table(data):
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        raise Refusal('UNVERIFIED', 'routes are not UTF-8')
    lines = text.split('\n')
    if lines[-1] == '':
        lines.pop()
    refuse(lines and lines[0].split('\t') == ROUTE_HEADER, 'routes do not carry the route header')
    routes, targets = {}, set()
    for line in lines[1:]:
        fields = line.split('\t')
        refuse(len(fields) == len(ROUTE_HEADER), 'route row does not have 8 fields')
        row = dict(zip(ROUTE_HEADER, fields))
        refuse(is_path(row['source']) and is_path(row['target']),
               'route row paths are not normalized paths')
        refuse(row['observed_bytes'].isdigit(), 'route row bytes are not a count', [row['source']])
        refuse(row['source'] not in routes, 'duplicate route source', [row['source']])
        refuse(row['target'] not in targets, 'duplicate route target', [row['target']])
        routes[row['source']] = row
        targets.add(row['target'])
    return routes


def repair_set(value):
    keys('RepairSet', value, {'schema_version', 'repairs'})
    refuse(type(value['schema_version']) is int and value['schema_version'] == 1
           and type(value['repairs']) is list, 'RepairSet is malformed')
    repairs = {}
    for repair in value['repairs']:
        keys('Repair', repair, REPAIR_KEYS)
        refuse(type(repair['id']) is str and repair['id'] and is_path(repair['source'])
               and is_path(repair['target']) and is_sha(repair['before_sha256'])
               and is_sha(repair['after_sha256']), 'Repair is malformed')
        refuse(repair['id'] not in repairs, 'duplicate Repair ID')
        repairs[repair['id']] = repair
    return repairs


def container_list(value):
    refuse(type(value) is list, 'containers is not an array')
    identities, sources = set(), set()
    for container in value:
        keys('ContainerExpectation', container, CONTAINER_KEYS)
        refuse(type(container['id']) is str and container['id']
               and container['id'] not in identities, 'duplicate or empty container ID')
        refuse(is_path(container['source']), 'container source is not a normalized path')
        refuse(container['source'] not in sources, 'duplicate container source',
               [container['source']])
        for key in ('moved_source_paths', 'added_source_paths'):
            refuse(type(container[key]) is list and all(map(is_path, container[key])),
                   'container ' + key + ' is malformed', [container['source']])
            refuse(len(set(container[key])) == len(container[key]),
                   'duplicate container ' + key, [container['source']])
        refuse(type(container['rewrite_ids']) is list
               and all(type(item) is str and item for item in container['rewrite_ids'])
               and len(set(container['rewrite_ids'])) == len(container['rewrite_ids']),
               'container rewrite_ids is malformed', [container['source']])
        identities.add(container['id'])
        sources.add(container['source'])
    return value


def differs(before, after):
    return [key for key in COMPARED if before[key] != after[key]]


def rewritten(repair, path, before, after):
    """The exact approved rewrite binds this leaf's before and after bytes."""
    return (repair['source'] == repair['target'] == path and before['kind'] == after['kind']
            == 'file' and before['link_text'] is None and after['link_text'] is None
            and repair['before_sha256'] == before['sha256']
            and repair['after_sha256'] == after['sha256'])


def check_retained(root, manifest, documents, observed):
    """Compare the admitted LeafManifest (manifest.leaves, bound in documents) with the observed
    post LeafManifest. root is M; documents maps each binding path to its complete bytes."""
    findings = {}

    def finding(status, reason, paths):
        paths = sorted(set(paths))
        identity = '\n'.join([status, reason] + paths)
        key = 'F-RETAINED-' + hashlib.sha256(identity.encode()).hexdigest()
        findings[key] = {'id': key, 'status': status, 'prd_ids': list(PRD_IDS), 'paths': paths,
                         'evidence': [], 'reason': reason, 'previous_finding': None,
                         'resolution_receipt': None}

    root = str(root)
    git = root + '/.git'

    def in_git(path):
        return path == git or under(path, git)

    try:
        refuse(is_path(root), 'root is not a normalized absolute path')
        keys('RetentionManifest', manifest, RETENTION_KEYS)
        refuse(type(manifest['schema_version']) is int and manifest['schema_version'] == 1,
               'RetentionManifest schema_version is not 1')
        containers = container_list(manifest['containers'])
        pre = leaf_manifest(parse_json(bound(manifest['leaves'], documents), 'LeafManifest'),
                            'admitted')
        routes = route_table(bound(manifest['routes'], documents))
        repairs = repair_set(parse_json(bound(manifest['repairs'], documents), 'RepairSet'))
        post = leaf_manifest(observed, 'observed')
    except Refusal as refusal:
        finding(refusal.status, refusal.reason, refusal.paths)
        return tuple(sorted(findings.values(), key=lambda item: item['id']))

    # Git is its own authority: an observed M/.git leaf is not compared (H-SLICE.md item 2).
    post = {path: leaf for path, leaf in post.items() if not in_git(path)}
    for path in [path for path in pre if in_git(path)]:
        finding('FAIL', 'admitted leaf: ' + GIT_SUBJECT, [path])
        del pre[path]
    for source, row in list(routes.items()):
        if in_git(source) or in_git(row['target']):
            finding('FAIL', 'route: ' + GIT_SUBJECT, [source, row['target']])
            del routes[source]
    for container in [item for item in containers if in_git(item['source'])]:
        finding('FAIL', 'container: ' + GIT_SUBJECT, [container['source']])
        containers.remove(container)
    if not pre:
        finding('UNVERIFIED', 'no admitted leaves to compare', [root])

    moves = {source: row['target'] for source, row in routes.items() if row['action'] == 'MOVE'}
    keeps = set()
    for source, row in routes.items():
        leaf = pre.get(source)
        if row['action'] not in ('KEEP', 'MOVE'):
            finding('UNVERIFIED', 'route action ' + row['action']
                    + ' is outside C-MOVE, C-KEEP and C-CONTAINER', [source])
        elif leaf is not None and (row['kind'] != leaf['kind']
                                   or int(row['observed_bytes']) != leaf['bytes']):
            finding('FAIL', 'route row disagrees with the admitted leaf', [source])
        elif row['action'] == 'KEEP':
            keeps.add(source)

    # C-MOVE (SPEC.md:605): target absent before, source absent after, bytes equal, once.
    for source, target in moves.items():
        if source not in pre:
            finding('UNVERIFIED', 'C-MOVE: source has no admitted leaf', [source])
            continue
        if target in pre:
            finding('FAIL', 'C-MOVE: target was occupied before the move', [target])
        if source in post:
            finding('FAIL', 'C-MOVE: source is still present after the move', [source])
        if target not in post:
            finding('FAIL', 'C-MOVE: target is absent after the move', [target])
        elif differs(pre[source], post[target]):
            finding('FAIL', 'C-MOVE: target differs from the admitted leaf in '
                    + ','.join(differs(pre[source], post[target])), [source, target])

    # C-KEEP (H-SLICE.md item 10): same path and digest unless an exact rewrite binds both.
    for source in sorted(keeps):
        if routes[source]['target'] != source:
            finding('FAIL', 'C-KEEP: route relocates a retained leaf', [source])
        elif source not in pre:
            finding('UNVERIFIED', 'C-KEEP: retained leaf has no admitted leaf', [source])
        elif source not in post:
            finding('FAIL', 'C-KEEP: retained leaf is absent', [source])
        elif differs(pre[source], post[source]):
            bound_repairs = [repair for repair in repairs.values()
                             if source in (repair['source'], repair['target'])]
            if not (len(bound_repairs) == 1
                    and rewritten(bound_repairs[0], source, pre[source], post[source])):
                finding('FAIL', 'C-KEEP: retained leaf changed without an exact approved '
                        'rewrite', [source])

    # C-CONTAINER (H-SLICE.md item 4 and :28): descendants derive from named moves and rewrites.
    for container in containers:
        folder = container['source']
        admitted = {path for path in pre if under(path, folder)}
        if not admitted:
            finding('UNVERIFIED', 'C-CONTAINER: container has no admitted descendant', [folder])
            continue
        outgoing = {source for source in moves if under(source, folder)}
        incoming = {source for source, target in moves.items()
                    if under(target, folder) and not under(source, folder)}
        named_out = set(container['moved_source_paths'])
        named_in = set(container['added_source_paths'])
        for path in sorted(outgoing - named_out):
            finding('FAIL', 'C-CONTAINER: unnamed outgoing move', [folder, path])
        for path in sorted(named_out - outgoing):
            finding('FAIL', 'C-CONTAINER: named outgoing path has no admitted move from the '
                    'container', [folder, path])
        for path in sorted(incoming - named_in):
            finding('FAIL', 'C-CONTAINER: unnamed incoming move', [folder, path])
        for path in sorted(named_in - incoming):
            finding('FAIL', 'C-CONTAINER: named incoming path has no admitted move into the '
                    'container', [folder, path])
        residual = admitted - outgoing
        rewrites = {}
        for identity in container['rewrite_ids']:
            repair = repairs.get(identity)
            if repair is None:
                finding('FAIL', 'C-CONTAINER: rewrite ID does not join RepairSet: ' + identity,
                        [folder])
            elif repair['source'] != repair['target'] or repair['source'] not in residual \
                    or repair['source'] in rewrites:
                finding('FAIL', 'C-CONTAINER: rewrite does not bind a residual leaf of the '
                        'container: ' + identity, [folder, repair['source']])
            else:
                rewrites[repair['source']] = repair
        expected = residual | {target for source, target in moves.items()
                               if under(target, folder)}
        present = {path for path in post if under(path, folder)}
        for path in sorted(expected - present):
            finding('FAIL', 'C-CONTAINER: expected descendant is absent', [folder, path])
        for path in sorted(present - expected):
            finding('FAIL', 'C-CONTAINER: unexplained descendant', [folder, path])
        for path in sorted(residual & present):
            if differs(pre[path], post[path]) and not (
                    path in rewrites and rewritten(rewrites[path], path, pre[path], post[path])):
                finding('FAIL', 'C-CONTAINER: residual leaf changed without a named approved '
                        'rewrite', [folder, path])

    folders = [container['source'] for container in containers]
    for path in sorted(pre):
        if path not in routes and not any(under(path, folder) for folder in folders):
            finding('UNVERIFIED', 'admitted leaf has no route and no container', [path])
    # Move sources and uncovered admitted leaves already carry their own finding.
    explained = keeps | set(moves) | set(moves.values()) | set(pre)
    for path in sorted(post):
        if path not in explained and not any(under(path, folder) for folder in folders):
            finding('FAIL', 'observed leaf is not explained by a route or a container', [path])
    return tuple(sorted(findings.values(), key=lambda item: item['id']))
