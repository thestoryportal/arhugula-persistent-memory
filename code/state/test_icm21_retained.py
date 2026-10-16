"""check_retained: C-MOVE, C-KEEP and C-CONTAINER over pre and post leaf manifests (Step 203).

Each case builds a real miniature repo in a temporary directory, inventories it into a
LeafManifest, performs the moves and the approved rewrite with os.rename and a write, and
inventories it again. Variants then edit those observed manifests. check_retained itself
never touches the filesystem (SPEC.md:208; H-SLICE.md items 1, 9 and 10).
"""
import base64
import builtins
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import icm21_check
from icm21_retained import check_retained

HEADER = 'requirement_id\tsource\ttarget\tkind\tobserved_bytes\taction\tlane\tscientific_role\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root, with_git=False):
    """LeafManifest of every file and symlink under root, never following a link."""
    leaves = []
    for directory, names, files in os.walk(root):
        if not with_git and Path(directory) == root:
            names[:] = [name for name in names if name != '.git']
        for name in sorted(files + [n for n in names if os.path.islink(os.path.join(directory, n))]):
            path = os.path.join(directory, name)
            status = os.lstat(path)
            if os.path.islink(path):
                text = os.readlink(path)
                raw, kind, link = text.encode(), 'symlink', text
            else:
                with open(path, 'rb') as handle:
                    raw = handle.read()
                kind, link = 'file', None
            leaves.append({'source': path, 'kind': kind, 'bytes': len(raw),
                           'sha256': digest(raw), 'link_text': link,
                           'device': status.st_dev, 'inode': status.st_ino,
                           'nlink': status.st_nlink})
    leaves.sort(key=lambda leaf: leaf['source'].encode())
    return {'schema_version': 1, 'leaves': leaves}


class Retained(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='icm21-retained-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(os.path.realpath(temporary.name)) / 'M'
        self.write('CLAUDE.md', b'routing\n')
        self.write('projects/a.md', b'outgoing child\n')
        self.write('projects/guide.md', b'see projects/a.md\n')
        self.write('projects/notes.md', b'unchanged residual\n')
        self.write('projects/sub/inner.md', b'moves inside the container\n')
        self.write('projects/tool/.git/HEAD', b'ref: refs/heads/main\n')
        os.symlink('notes.md', self.root / 'projects/link')
        self.write('experiments/old.md', b'experiment record\n')
        self.write('plans/incoming.md', b'incoming leaf\n')
        self.write('.git/HEAD', b'ref: refs/heads/master\n')
        self.write('.git/index', b'index before\n')
        self.pre = inventory(self.root)
        self.routes = [('MV-011', 'CLAUDE.md', 'CLAUDE.md', 'KEEP'),
                       ('MV-122', 'projects/a.md', 'experiments/x/a.md', 'MOVE'),
                       ('MV-137', 'projects/sub/inner.md', 'projects/sub2/inner.md', 'MOVE'),
                       ('MV-160', 'plans/incoming.md', 'projects/incoming.md', 'MOVE')]
        os.makedirs(self.root / 'experiments/x')
        os.rename(self.root / 'projects/a.md', self.root / 'experiments/x/a.md')
        os.makedirs(self.root / 'projects/sub2')
        os.rename(self.root / 'projects/sub/inner.md', self.root / 'projects/sub2/inner.md')
        os.rename(self.root / 'plans/incoming.md', self.root / 'projects/incoming.md')
        self.write('projects/guide.md', b'see experiments/x/a.md\n')
        self.write('.git/index', b'index after git mv\n')
        self.write('.git/objects/ab/cdef', b'blob written by git add\n')
        self.post = inventory(self.root, with_git=True)
        self.repairs = [self.repair('RP-GUIDE', 'projects/guide.md', b'see projects/a.md\n',
                                    b'see experiments/x/a.md\n')]
        self.containers = [
            {'id': 'MV-041', 'source': self.path('projects'),
             'moved_source_paths': [self.path('projects/a.md'), self.path('projects/sub/inner.md')],
             'added_source_paths': [self.path('plans/incoming.md')],
             'rewrite_ids': ['RP-GUIDE']},
            {'id': 'MV-030', 'source': self.path('experiments'), 'moved_source_paths': [],
             'added_source_paths': [self.path('projects/a.md')], 'rewrite_ids': []}]
        # The G5 approval that authorizes every fixture Repair (WIRE-CONTRACTS.md:115, :163).
        self.approval = {'approval_id': 'approval-1', 'plan_id': 'G5-PLAN',
                         'plan_sha256': digest(b'plan'), 'gate': 'G5', 'approved_by': 'operator',
                         'approved_at': '2026-10-16T00:00:00+00:00',
                         'expires_at': '2026-10-17T00:00:00+00:00', 'decision': 'approved'}
        self.operation = {'operation_id': 'OP-1', 'prd_ids': ['ICM-R6'],
                          'plan': {'path': '/fixture/plan.json', 'sha256': digest(b'plan')},
                          'approval': {'path': '/fixture/approval.json', 'sha256': ''},
                          'journal': {'path': '/fixture/journal.jsonl', 'sha256': digest(b'')},
                          'verification': None, 'readers': None, 'acceptance': None,
                          'rollback': None}
        self.extra_documents = {}

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def path(self, relative):
        return str(self.root / relative)

    def repair(self, identity, relative, before, after):
        return {'schema_version': 1, 'id': identity, 'prd_ids': ['ICM-R6'], 'plan_id': 'G5-PLAN',
                'plan_sha256': digest(b'plan'), 'source': self.path(relative),
                'target': self.path(relative), 'before_sha256': digest(before),
                'after_sha256': digest(after),
                'edits': [{'start': 0, 'end': len(before),
                           'before_base64': base64.b64encode(before).decode(),
                           'after_base64': base64.b64encode(after).decode()}],
                'reader_ids': ['R-1'], 'reference_ids': ['REF-1']}

    def route_bytes(self):
        lines = [HEADER]
        for requirement, source, target, action in self.routes:
            leaf = self.leaf(self.pre, source)
            lines.append('\t'.join((requirement, self.path(source), self.path(target),
                                    leaf['kind'] if leaf else 'file',
                                    str(leaf['bytes'] if leaf else 0),
                                    action, 'integration', 'record')) + '\n')
        return ''.join(lines).encode()

    def leaf(self, manifest, relative):
        for leaf in manifest['leaves']:
            if leaf['source'] == self.path(relative):
                return leaf
        return None

    def arguments(self):
        documents = {'/fixture/leaves.json': json.dumps(self.pre, sort_keys=True).encode(),
                     '/fixture/routes.tsv': self.route_bytes(),
                     '/fixture/repairs.json': json.dumps(
                         {'schema_version': 1, 'repairs': self.repairs}, sort_keys=True).encode(),
                     '/fixture/approval.json': json.dumps(self.approval, sort_keys=True).encode()}
        operation = copy.deepcopy(self.operation)
        operation['approval']['sha256'] = digest(documents['/fixture/approval.json'])
        documents['/fixture/executor.json'] = json.dumps(
            {'schema_version': 1, 'operations': [operation]}, sort_keys=True).encode()
        documents.update(self.extra_documents)
        manifest = {'schema_version': 1, 'containers': copy.deepcopy(self.containers)}
        for key, path in (('leaves', '/fixture/leaves.json'), ('routes', '/fixture/routes.tsv'),
                          ('repairs', '/fixture/repairs.json'),
                          ('executor', '/fixture/executor.json')):
            manifest[key] = {'path': path, 'sha256': digest(documents[path])}
        return manifest, documents

    def check(self, manifest=None, documents=None):
        default_manifest, default_documents = self.arguments()
        findings = check_retained(self.root, manifest or default_manifest,
                                  documents or default_documents, copy.deepcopy(self.post))
        schema = icm21_check.audit_schema()
        for finding in findings:
            icm21_check.validate_wire('Finding', finding, schema, {})
        self.assertEqual(len({finding['id'] for finding in findings}), len(findings))
        return findings

    def assertFinding(self, findings, status, reason, relative=None):
        matches = [finding for finding in findings if reason in finding['reason']
                   and finding['status'] == status
                   and (relative is None or self.path(relative) in finding['paths'])]
        self.assertTrue(matches, (status, reason, relative, findings))

    def edit_post(self, relative, **fields):
        self.leaf(self.post, relative).update(fields)

    def drop_post(self, relative):
        self.post['leaves'].remove(self.leaf(self.post, relative))

    def add_post(self, relative, data=b'new\n'):
        self.post['leaves'].append({'source': self.path(relative), 'kind': 'file',
                                    'bytes': len(data), 'sha256': digest(data),
                                    'link_text': None, 'device': 1, 'inode': 99, 'nlink': 1})

    # --- the whole fixture --------------------------------------------------------------

    def test_exact_moves_rewrite_and_git_staging_pass(self):
        self.assertEqual(self.check(), ())

    def test_retained_container(self):
        """SPEC.md:723. RED control: the old aggregate digest of the container changes."""
        def aggregate(manifest):
            rows = [leaf for leaf in manifest['leaves']
                    if leaf['source'].startswith(self.path('projects') + '/')]
            return digest(json.dumps([[r['source'], r['sha256']] for r in rows]).encode())
        self.assertNotEqual(aggregate(self.pre), aggregate(self.post))
        self.assertEqual(self.check(), ())
        self.edit_post('projects/notes.md', sha256=digest(b'unrelated edit\n'))
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/notes.md')

    # --- C-MOVE ---------------------------------------------------------------------------

    def test_move_target_bytes_differ(self):
        self.edit_post('experiments/x/a.md', sha256=digest(b'corrupt\n'))
        self.assertFinding(self.check(), 'FAIL', 'C-MOVE: target differs from the admitted leaf',
                           'experiments/x/a.md')

    def test_move_target_link_text_differs(self):
        self.routes.append(('MV-161', 'projects/link', 'experiments/link', 'MOVE'))
        self.containers[0]['moved_source_paths'].append(self.path('projects/link'))
        self.containers[1]['added_source_paths'].append(self.path('projects/link'))
        moved = self.leaf(self.post, 'projects/link')
        moved['source'] = self.path('experiments/link')
        self.assertEqual(self.check(), ())
        moved['link_text'] = 'elsewhere.md'
        self.assertFinding(self.check(), 'FAIL', 'C-MOVE: target differs', 'experiments/link')

    def test_move_source_still_present(self):
        self.add_post('plans/incoming.md', b'incoming leaf\n')
        self.assertFinding(self.check(), 'FAIL', 'C-MOVE: source is still present',
                           'plans/incoming.md')

    def test_move_target_absent(self):
        self.drop_post('experiments/x/a.md')
        self.assertFinding(self.check(), 'FAIL', 'C-MOVE: target is absent',
                           'experiments/x/a.md')

    def test_move_target_occupied_before(self):
        self.routes.append(('MV-162', 'CLAUDE.md', 'experiments/old.md', 'MOVE'))
        self.routes.remove(('MV-011', 'CLAUDE.md', 'CLAUDE.md', 'KEEP'))
        self.assertFinding(self.check(), 'FAIL', 'C-MOVE: target was occupied before the move',
                           'experiments/old.md')

    def test_move_custody_completes_once(self):
        self.routes.append(('MV-163', 'CLAUDE.md', 'experiments/x/a.md', 'MOVE'))
        self.routes.remove(('MV-011', 'CLAUDE.md', 'CLAUDE.md', 'KEEP'))
        self.assertFinding(self.check(), 'UNVERIFIED', 'duplicate route target',
                           'experiments/x/a.md')

    def test_move_source_not_admitted(self):
        self.routes.append(('MV-164', 'plans/ghost.md', 'experiments/ghost.md', 'MOVE'))
        self.assertFinding(self.check(), 'UNVERIFIED', 'C-MOVE: source has no admitted leaf',
                           'plans/ghost.md')

    def test_route_row_disagrees_with_admitted_leaf(self):
        manifest, documents = self.arguments()
        rows = documents['/fixture/routes.tsv'].decode().split('\n')
        fields = rows[2].split('\t')
        fields[4] = str(int(fields[4]) + 1)
        rows[2] = '\t'.join(fields)
        documents['/fixture/routes.tsv'] = '\n'.join(rows).encode()
        manifest['routes']['sha256'] = digest(documents['/fixture/routes.tsv'])
        self.assertFinding(self.check(manifest, documents), 'FAIL',
                           'route row disagrees with the admitted leaf', 'projects/a.md')

    # --- C-KEEP ---------------------------------------------------------------------------

    def test_keep_change_without_rewrite_fails(self):
        self.edit_post('CLAUDE.md', sha256=digest(b'edited\n'), bytes=7)
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_keep_change_with_exact_rewrite_passes(self):
        self.edit_post('CLAUDE.md', sha256=digest(b'edited\n'), bytes=7)
        self.repairs.append(self.repair('RP-ROUTING', 'CLAUDE.md', b'routing\n', b'edited\n'))
        self.assertEqual(self.check(), ())
        self.repairs[-1]['after_sha256'] = digest(b'other\n')
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_keep_rewrite_must_be_unique(self):
        self.edit_post('CLAUDE.md', sha256=digest(b'edited\n'), bytes=7)
        self.repairs.append(self.repair('RP-ROUTING', 'CLAUDE.md', b'routing\n', b'edited\n'))
        self.repairs.append(self.repair('RP-ROUTING-2', 'CLAUDE.md', b'routing\n', b'edited\n'))
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_keep_route_cannot_relocate(self):
        self.routes[0] = ('MV-011', 'CLAUDE.md', 'docs/CLAUDE.md', 'KEEP')
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: route relocates', 'CLAUDE.md')

    def test_keep_leaf_absent(self):
        self.drop_post('CLAUDE.md')
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf is absent', 'CLAUDE.md')

    def test_keep_leaf_not_admitted(self):
        self.routes.append(('MV-165', 'README.md', 'README.md', 'KEEP'))
        self.assertFinding(self.check(), 'UNVERIFIED', 'C-KEEP: retained leaf has no admitted',
                           'README.md')

    # --- C-CONTAINER ----------------------------------------------------------------------

    def test_unnamed_outgoing_move_fails(self):
        self.containers[0]['moved_source_paths'].remove(self.path('projects/a.md'))
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: unnamed outgoing move',
                           'projects/a.md')

    def test_unnamed_internal_move_fails(self):
        self.containers[0]['moved_source_paths'].remove(self.path('projects/sub/inner.md'))
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: unnamed outgoing move',
                           'projects/sub/inner.md')

    def test_named_outgoing_without_move_fails(self):
        self.containers[0]['moved_source_paths'].append(self.path('projects/notes.md'))
        self.assertFinding(self.check(), 'FAIL', 'named outgoing path has no admitted move',
                           'projects/notes.md')

    def test_unnamed_incoming_move_fails(self):
        self.containers[0]['added_source_paths'] = []
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: unnamed incoming move',
                           'plans/incoming.md')

    def test_named_incoming_without_move_fails(self):
        self.containers[1]['added_source_paths'].append(self.path('plans/incoming.md'))
        self.assertFinding(self.check(), 'FAIL', 'named incoming path has no admitted move',
                           'plans/incoming.md')

    def test_unnamed_rewrite_fails(self):
        self.containers[0]['rewrite_ids'] = []
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/guide.md')

    def test_rewrite_with_wrong_digest_fails(self):
        self.repairs[0]['before_sha256'] = digest(b'other before\n')
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/guide.md')

    def test_unresolved_rewrite_id_fails(self):
        self.containers[0]['rewrite_ids'].append('RP-MISSING')
        self.assertFinding(self.check(), 'FAIL', 'rewrite ID does not join RepairSet')

    def test_out_of_container_rewrite_fails(self):
        self.containers[1]['rewrite_ids'] = ['RP-GUIDE']
        self.assertFinding(self.check(), 'FAIL', 'rewrite does not bind a residual leaf',
                           'projects/guide.md')

    def test_unexplained_descendant_fails(self):
        self.add_post('projects/new.md')
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: unexplained descendant',
                           'projects/new.md')

    def test_missing_descendant_fails(self):
        self.drop_post('projects/notes.md')
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: expected descendant is absent',
                           'projects/notes.md')

    def test_container_without_admitted_leaf_is_unverified(self):
        self.containers.append({'id': 'MV-099', 'source': self.path('empty'),
                                'moved_source_paths': [], 'added_source_paths': [],
                                'rewrite_ids': []})
        self.assertFinding(self.check(), 'UNVERIFIED', 'container has no admitted descendant',
                           'empty')

    def test_duplicate_container_source_is_refused(self):
        self.containers.append(dict(copy.deepcopy(self.containers[1]), id='MV-031'))
        self.assertFinding(self.check(), 'UNVERIFIED', 'duplicate container source')

    def test_nested_git_inside_container_stays_a_subject(self):
        self.edit_post('projects/tool/.git/HEAD', sha256=digest(b'detached\n'))
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/tool/.git/HEAD')

    # --- coverage and refusal -------------------------------------------------------------

    def test_leaf_without_route_or_container_is_unverified(self):
        self.routes.remove(('MV-011', 'CLAUDE.md', 'CLAUDE.md', 'KEEP'))
        self.assertFinding(self.check(), 'UNVERIFIED', 'admitted leaf has no route and no container',
                           'CLAUDE.md')

    def test_unexplained_observed_leaf_fails(self):
        self.add_post('stray.md')
        self.assertFinding(self.check(), 'FAIL', 'observed leaf is not explained', 'stray.md')

    def test_no_admitted_leaves_is_never_an_empty_pass(self):
        self.pre['leaves'] = []
        self.routes, self.containers, self.post['leaves'] = [], [], []
        self.assertFinding(self.check(), 'UNVERIFIED', 'no admitted leaves')

    def test_other_route_actions_are_refused(self):
        self.routes.append(('MV-019', 'experiments/old.md', 'models/old.md', 'HOLD'))
        self.assertFinding(self.check(), 'UNVERIFIED', 'route action HOLD is outside',
                           'experiments/old.md')

    def test_changed_binding_digest_fails(self):
        manifest, documents = self.arguments()
        documents['/fixture/repairs.json'] += b' '
        self.assertFinding(self.check(manifest, documents), 'FAIL', 'binding digest differs')

    def test_missing_bound_document_is_unverified(self):
        manifest, documents = self.arguments()
        del documents['/fixture/leaves.json']
        self.assertFinding(self.check(manifest, documents), 'UNVERIFIED',
                           'bound document was not supplied')

    def test_malformed_route_header_is_unverified(self):
        manifest, documents = self.arguments()
        documents['/fixture/routes.tsv'] = documents['/fixture/routes.tsv'].replace(
            b'scientific_role', b'role', 1)
        manifest['routes']['sha256'] = digest(documents['/fixture/routes.tsv'])
        self.assertFinding(self.check(manifest, documents), 'UNVERIFIED', 'route header')

    def test_leaf_path_with_newline_is_unverified(self):
        self.add_post('bad\nname.md')
        self.assertFinding(self.check(), 'UNVERIFIED', 'leaf source is not a normalized path')

    def test_unknown_leaf_field_is_unverified(self):
        self.post['leaves'][0]['mtime_ns'] = 1
        self.assertFinding(self.check(), 'UNVERIFIED', 'LeafRecord keys differ')

    def test_malformed_inputs_are_refused(self):
        def leaves(mutate):
            def change(manifest, documents, observed):
                value = json.loads(documents['/fixture/leaves.json'])
                mutate(value)
                documents['/fixture/leaves.json'] = json.dumps(value).encode()
            return change

        def repairs(mutate):
            def change(manifest, documents, observed):
                value = json.loads(documents['/fixture/repairs.json'])
                mutate(value)
                documents['/fixture/repairs.json'] = json.dumps(value).encode()
            return change

        def routes(old, new):
            def change(manifest, documents, observed):
                documents['/fixture/routes.tsv'] = documents['/fixture/routes.tsv'].replace(
                    old, new, 1)
            return change

        def containers(mutate):
            return lambda manifest, documents, observed: mutate(manifest['containers'])

        cases = [
            ('root', lambda m, d, o: None, 'root is not a normalized absolute path'),
            ('version', lambda m, d, o: m.update(schema_version=2),
             'RetentionManifest schema_version is not 1'),
            ('containers type', lambda m, d, o: m.update(containers={}),
             'containers is not an array'),
            ('container id', containers(lambda c: c[1].update(id='MV-041')),
             'duplicate or empty container ID'),
            ('container source', containers(lambda c: c[1].update(source='experiments')),
             'container source is not a normalized path'),
            ('moved paths', containers(lambda c: c[0]['moved_source_paths'].append('a.md')),
             'container moved_source_paths is malformed'),
            ('moved duplicate', containers(lambda c: c[0]['added_source_paths'].append(
                c[0]['added_source_paths'][0])), 'duplicate container added_source_paths'),
            ('rewrite ids', containers(lambda c: c[0]['rewrite_ids'].append('RP-GUIDE')),
             'container rewrite_ids is malformed'),
            ('binding keys', lambda m, d, o: m['leaves'].update(size=1),
             'Binding keys differ'),
            ('binding value', lambda m, d, o: m['leaves'].update(sha256='0'),
             'Binding is malformed'),
            ('document type', lambda m, d, o: d.update({'/fixture/leaves.json': 'text'}),
             'bound document is not bytes'),
            ('json', lambda m, d, o: d.update({'/fixture/leaves.json': b'{'}),
             'LeafManifest is not valid JSON'),
            ('json constant', lambda m, d, o: d.update({'/fixture/repairs.json': b'NaN'}),
             'RepairSet has NaN'),
            ('leaf version', leaves(lambda v: v.update(schema_version=True)),
             'admitted schema_version is not 1'),
            ('leaf array', lambda m, d, o: o.update(leaves={}), 'observed leaves is not an array'),
            ('leaf kind', leaves(lambda v: v['leaves'][0].update(kind='directory')),
             'admitted leaf is malformed'),
            ('leaf link', leaves(lambda v: v['leaves'][0].update(link_text='')),
             'admitted leaf is malformed'),
            ('leaf duplicate', leaves(lambda v: v['leaves'].append(v['leaves'][0])),
             'admitted duplicate leaf source'),
            ('routes utf-8', lambda m, d, o: d.update({'/fixture/routes.tsv': b'\xff'}),
             'routes are not UTF-8'),
            ('route fields', routes(b'\tintegration\t', b'\t'), 'route row does not have 8 fields'),
            ('route path', routes(b'\t' + str(self.root).encode() + b'/CLAUDE.md\t', b'\tCLAUDE.md\t'),
             'route row paths are not normalized paths'),
            ('route bytes', routes(b'\t8\tKEEP', b'\t-8\tKEEP'), 'route row bytes are not a count'),
            ('route source', lambda m, d, o: d.update({'/fixture/routes.tsv': d[
                '/fixture/routes.tsv'] + d['/fixture/routes.tsv'].split(b'\n')[1] + b'\n'}),
             'duplicate route source'),
            ('repair set', repairs(lambda v: v.update(repairs={})), 'RepairSet is malformed'),
            ('repair keys', repairs(lambda v: v['repairs'][0].pop('edits')), 'Repair keys differ'),
            ('repair value', repairs(lambda v: v['repairs'][0].update(source='guide.md')),
             'Repair is malformed'),
            ('repair duplicate', repairs(lambda v: v['repairs'].append(v['repairs'][0])),
             'duplicate Repair ID'),
        ]
        for name, mutate, reason in cases:
            with self.subTest(name):
                manifest, documents = self.arguments()
                observed = copy.deepcopy(self.post)
                mutate(manifest, documents, observed)
                for key in ('leaves', 'routes', 'repairs'):
                    if type(documents.get(manifest[key]['path'])) is bytes \
                            and len(manifest[key]['sha256']) == 64:
                        manifest[key]['sha256'] = digest(documents[manifest[key]['path']])
                root = 'M' if name == 'root' else self.root
                findings = check_retained(root, manifest, documents, observed)
                self.assertEqual([(f['status'], reason in f['reason']) for f in findings],
                                 [('UNVERIFIED', True)], findings)

    # --- out: MetadataSet is dropped (A/H-SLICE.md:66-83) ---------------------------------

    def test_retention_metadata_binding_is_refused(self):
        manifest, documents = self.arguments()
        manifest['metadata'] = {'path': '/fixture/metadata.json', 'sha256': digest(b'{}')}
        documents['/fixture/metadata.json'] = b'{}'
        self.assertFinding(self.check(manifest, documents), 'UNVERIFIED',
                           "RetentionManifest keys differ from the wire contract: extra ['metadata']")

    def test_container_metadata_operations_are_refused(self):
        self.containers[0]['metadata_operation_ids'] = []
        self.assertFinding(self.check(), 'UNVERIFIED',
                           "ContainerExpectation keys differ from the wire contract: "
                           "extra ['metadata_operation_ids']")

    # --- out: M/.git is never a subject (A/H-SLICE.md:12) ---------------------------------

    def test_git_metadata_changes_are_not_subjects(self):
        self.write('.git/refs/heads/T203', b'0' * 40 + b'\n')
        self.post = inventory(self.root, with_git=True)
        self.assertTrue(any('/.git/objects/' in leaf['source'] for leaf in self.post['leaves']))
        self.assertEqual(self.check(), ())

    def test_git_container_is_refused(self):
        self.containers.append({'id': 'MV-004', 'source': self.path('.git'),
                                'moved_source_paths': [], 'added_source_paths': [],
                                'rewrite_ids': []})
        self.assertFinding(self.check(), 'FAIL', 'M/.git is never a subject', '.git')

    def test_git_admitted_leaf_is_refused(self):
        self.pre = inventory(self.root, with_git=True)
        self.assertFinding(self.check(), 'FAIL', 'M/.git is never a subject', '.git/HEAD')

    def test_git_route_is_refused(self):
        self.routes.append(('MV-166', 'CLAUDE.md', '.git/CLAUDE.md', 'MOVE'))
        self.routes.remove(('MV-011', 'CLAUDE.md', 'CLAUDE.md', 'KEEP'))
        self.assertFinding(self.check(), 'FAIL', 'M/.git is never a subject', '.git/CLAUDE.md')

    # --- out: pure function ---------------------------------------------------------------

    def test_pure_function_touches_no_filesystem(self):
        manifest, documents = self.arguments()
        clean_post = copy.deepcopy(self.post)
        self.add_post('stray.md')
        stray_post = copy.deepcopy(self.post)
        expected_clean = check_retained(self.root, manifest, documents, copy.deepcopy(clean_post))
        expected_stray = check_retained(self.root, manifest, documents, copy.deepcopy(stray_post))
        self.assertEqual(expected_clean, ())
        self.assertTrue(expected_stray)

        def refuse(*args, **kwargs):
            raise AssertionError('filesystem access during check_retained')
        names = ('stat', 'lstat', 'open', 'listdir', 'scandir', 'readlink', 'walk', 'access')
        patches = [mock.patch.object(builtins, 'open', refuse), mock.patch.object(io, 'open', refuse)]
        patches += [mock.patch.object(os, name, refuse) for name in names]
        for patch in patches:
            patch.start()
        try:
            clean = check_retained(self.root, manifest, documents, clean_post)
            stray = check_retained(self.root, manifest, documents, stray_post)
        finally:
            for patch in patches:
                patch.stop()
        self.assertEqual(clean, expected_clean)
        self.assertEqual(stray, expected_stray)

    # --- fixer round 1: helpers -----------------------------------------------------------

    def rebind(self, manifest, documents, key, data):
        documents[manifest[key]['path']] = data
        manifest[key]['sha256'] = digest(data)

    def edit_json(self, key, mutate):
        def change(manifest, documents, observed):
            value = json.loads(documents[manifest[key]['path']])
            mutate(value)
            self.rebind(manifest, documents, key, json.dumps(value).encode())
        return change

    def refused(self, change, reason, status='UNVERIFIED'):
        """Exactly one refusal finding, with this status and reason."""
        manifest, documents = self.arguments()
        observed = copy.deepcopy(self.post)
        replaced = change(manifest, documents, observed)
        observed = observed if replaced is None else replaced
        findings = check_retained(self.root, manifest, documents, observed)
        self.assertEqual([(f['status'], reason in f['reason']) for f in findings],
                         [(status, True)], findings)

    # --- ruling 1: executor authority -----------------------------------------------------

    def test_executor_binding_is_checked(self):
        cases = [('null', lambda m, d, o: m.update(executor=None), 'Binding is not an object',
                  'UNVERIFIED'),
                 ('missing bytes', lambda m, d, o: d.pop('/fixture/executor.json'),
                  'bound document was not supplied', 'UNVERIFIED'),
                 ('digest mismatch', lambda m, d, o: d.update(
                     {'/fixture/executor.json': b'tampered'}), 'binding digest differs', 'FAIL')]
        for name, change, reason, status in cases:
            with self.subTest(name):
                self.refused(change, reason, status)

    def test_executor_evidence_is_validated(self):
        cases = [('json', lambda m, d, o: self.rebind(m, d, 'executor', b'{'),
                  'ExecutorEvidence is not valid JSON'),
                 ('operations', self.edit_json('executor', lambda v: v.update(operations={})),
                  'ExecutorEvidence fails the wire schema'),
                 ('journal', self.edit_json('executor', lambda v: v['operations'][0].pop('journal')),
                  'ExecutorEvidence fails the wire schema')]
        for name, change, reason in cases:
            with self.subTest(name):
                self.refused(change, reason)

    def test_approval_bytes_are_checked(self):
        self.refused(lambda m, d, o: d.pop('/fixture/approval.json'),
                     'bound document was not supplied')
        self.refused(lambda m, d, o: d.update({'/fixture/approval.json': b'{}'}),
                     'binding digest differs', 'FAIL')

    def test_approval_keys_are_checked(self):
        self.approval['expiry'] = 'never'
        self.refused(lambda m, d, o: None, 'approval keys differ')

    def test_approval_values_are_checked(self):
        self.approval['plan_sha256'] = 'bad'
        self.refused(lambda m, d, o: None, 'approval is malformed')

    def test_approval_plan_id_is_checked(self):
        self.approval['plan_id'] = ''
        self.refused(lambda m, d, o: None, 'approval is malformed')

    def test_approval_must_bind_its_operation_plan(self):
        self.operation['plan']['sha256'] = digest(b'another plan')
        self.refused(lambda m, d, o: None, 'approval does not bind its operation plan', 'FAIL')

    def test_container_rewrite_needs_its_g5_plan_id(self):
        self.repairs[0]['plan_id'] = 'G5-OTHER'
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/guide.md')

    def test_container_rewrite_needs_its_g5_plan_digest(self):
        self.repairs[0]['plan_sha256'] = digest(b'another plan')
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/guide.md')

    def test_container_rewrite_needs_a_g5_gate(self):
        self.approval['gate'] = 'G4'
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/guide.md')

    def test_container_rewrite_needs_an_approved_decision(self):
        self.approval['decision'] = 'rejected'
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: residual leaf changed',
                           'projects/guide.md')

    def test_keep_rewrite_needs_its_g5_approval(self):
        self.edit_post('CLAUDE.md', sha256=digest(b'edited\n'), bytes=7)
        self.repairs.append(self.repair('RP-ROUTING', 'CLAUDE.md', b'routing\n', b'edited\n'))
        self.repairs[-1]['plan_id'] = 'UNAPPROVED'
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    # --- ruling 2: purity -----------------------------------------------------------------

    def test_inputs_are_never_mutated(self):
        self.containers.append({'id': 'MV-004', 'source': self.path('.git'),
                                'moved_source_paths': [], 'added_source_paths': [],
                                'rewrite_ids': []})
        self.add_post('stray.md')
        manifest, documents = self.arguments()
        observed = copy.deepcopy(self.post)
        before = copy.deepcopy((manifest, documents, observed))
        first = check_retained(self.root, manifest, documents, observed)
        second = check_retained(self.root, manifest, documents, observed)
        self.assertEqual((manifest, documents, observed), before)
        self.assertEqual(first, second)
        self.assertFinding(first, 'FAIL', 'M/.git is never a subject', '.git')
        self.assertFinding(first, 'FAIL', 'observed leaf is not explained', 'stray.md')

    # --- ruling 3: Repair wire schema -----------------------------------------------------

    def test_repair_wire_schema_is_enforced(self):
        cases = [('schema_version', 999), ('prd_ids', []), ('plan_id', None),
                 ('plan_sha256', 'bad'), ('edits', 'not-an-array'), ('reader_ids', False),
                 ('reference_ids', 17), ('reader_ids', [])]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                self.refused(self.edit_json('repairs', lambda v: v['repairs'][0].update(
                    {field: value})), 'Repair fails the wire schema')

    # --- ruling 4: unaffected and stale repairs -------------------------------------------

    def test_repair_of_no_leaf_fails(self):
        self.repairs.append(self.repair('RP-DANGLING', 'nonexistent.md', b'a', b'b'))
        self.assertFinding(self.check(), 'FAIL',
                           'Repair target is not a KEEP leaf or a named container rewrite',
                           'nonexistent.md')

    def test_unnamed_repair_of_a_container_leaf_fails(self):
        self.repairs.append(self.repair('RP-NOTES', 'projects/notes.md', b'unchanged residual\n',
                                        b'unchanged residual\n'))
        self.assertFinding(self.check(), 'FAIL',
                           'Repair target is not a KEEP leaf or a named container rewrite',
                           'projects/notes.md')

    def test_named_repair_of_unchanged_leaf_is_checked(self):
        self.repairs.append(self.repair('RP-NOTES', 'projects/notes.md', b'unchanged residual\n',
                                        b'unchanged residual\n'))
        self.containers[0]['rewrite_ids'].append('RP-NOTES')
        self.assertEqual(self.check(), ())
        self.repairs[-1]['before_sha256'] = self.repairs[-1]['after_sha256'] = digest(b'stale\n')
        self.assertFinding(self.check(), 'FAIL', 'C-CONTAINER: named rewrite does not bind',
                           'projects/notes.md')

    def test_keep_repair_of_unchanged_leaf_is_checked(self):
        self.repairs.append(self.repair('RP-ROUTING', 'CLAUDE.md', b'stale\n', b'stale\n'))
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: Repair of an unchanged retained leaf',
                           'CLAUDE.md')

    # --- ruling 5: route counts -----------------------------------------------------------

    def test_route_count_is_ascii_digits(self):
        for text in ('²', '٨'):
            with self.subTest(text=text):
                self.refused(lambda m, d, o: self.rebind(m, d, 'routes', d['/fixture/routes.tsv']
                                                         .replace(b'\t8\tKEEP', b'\t' + text.encode()
                                                                  + b'\tKEEP', 1)),
                             'route row bytes are not a count')

    def test_route_count_longer_than_18_digits_is_refused(self):
        """int() never sees a count past Python's int-string limit (fix round 2)."""
        for text in ('1' * 19, '9' * 5000, '0' * 4999 + '8'):
            with self.subTest(digits=len(text)):
                self.refused(lambda m, d, o: self.rebind(m, d, 'routes', d['/fixture/routes.tsv']
                                                         .replace(b'\t8\tKEEP', b'\t' + text.encode()
                                                                  + b'\tKEEP', 1)),
                             'route row bytes are not a count')

    def test_empty_route_count_is_refused(self):
        """An empty count gives UNVERIFIED and raises nothing (ruling 7)."""
        self.refused(lambda m, d, o: self.rebind(m, d, 'routes', d['/fixture/routes.tsv']
                                                 .replace(b'\t8\tKEEP', b'\t\tKEEP', 1)),
                     'route row bytes are not a count')

    # --- ruling 6: coverage ---------------------------------------------------------------

    def test_move_target_kind_differs(self):
        self.edit_post('experiments/x/a.md', kind='socket')
        self.assertFinding(self.check(), 'FAIL', 'C-MOVE: target differs from the admitted leaf '
                           'in kind', 'experiments/x/a.md')

    def test_move_target_byte_count_differs(self):
        self.edit_post('experiments/x/a.md', bytes=999)
        self.assertFinding(self.check(), 'FAIL', 'C-MOVE: target differs from the admitted leaf '
                           'in bytes', 'experiments/x/a.md')

    def keep_rewrite(self):
        self.edit_post('CLAUDE.md', sha256=digest(b'edited\n'), bytes=7)
        self.repairs.append(self.repair('RP-ROUTING', 'CLAUDE.md', b'routing\n', b'edited\n'))
        return self.repairs[-1]

    def test_keep_rewrite_target_must_be_the_leaf(self):
        self.keep_rewrite()['target'] = self.path('projects/notes.md')
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_keep_rewrite_source_must_be_the_leaf(self):
        self.keep_rewrite()['source'] = self.path('projects/notes.md')
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_keep_rewrite_binds_file_kinds(self):
        self.keep_rewrite()
        self.edit_post('CLAUDE.md', kind='socket')
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_keep_rewrite_binds_before_link_text(self):
        self.keep_rewrite()
        self.leaf(self.pre, 'CLAUDE.md')['link_text'] = 'elsewhere.md'
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_keep_rewrite_binds_after_link_text(self):
        self.keep_rewrite()
        self.edit_post('CLAUDE.md', link_text='elsewhere.md')
        self.assertFinding(self.check(), 'FAIL', 'C-KEEP: retained leaf changed', 'CLAUDE.md')

    def test_container_rewrites_cannot_overlap(self):
        self.repairs.append(self.repair('RP-GUIDE-2', 'projects/guide.md', b'see projects/a.md\n',
                                        b'see experiments/x/a.md\n'))
        self.containers[0]['rewrite_ids'].append('RP-GUIDE-2')
        self.assertFinding(self.check(), 'FAIL', 'rewrite does not bind a residual leaf of the '
                           'container: RP-GUIDE-2', 'projects/guide.md')

    def test_container_rewrite_cannot_relocate(self):
        self.repairs.append(self.repair('RP-MOVE', 'projects/guide.md', b'see projects/a.md\n',
                                        b'see experiments/x/a.md\n'))
        self.repairs[-1]['target'] = self.path('projects/notes.md')
        self.containers[0]['rewrite_ids'] = ['RP-MOVE']
        self.assertFinding(self.check(), 'FAIL', 'rewrite does not bind a residual leaf of the '
                           'container: RP-MOVE', 'projects/guide.md')

    def test_route_kind_disagrees_with_admitted_leaf(self):
        manifest, documents = self.arguments()
        self.rebind(manifest, documents, 'routes', documents['/fixture/routes.tsv'].replace(
            b'\tfile\t8\tKEEP', b'\tsymlink\t8\tKEEP', 1))
        self.assertFinding(self.check(manifest, documents), 'FAIL',
                           'route row disagrees with the admitted leaf', 'CLAUDE.md')

    def test_malformed_values_are_refused(self):
        def leaf(**fields):
            def change(manifest, documents, observed):
                observed['leaves'].append(dict(copy.deepcopy(self.leaf(self.post, 'CLAUDE.md')),
                                               **fields))
            return change

        def repair(**fields):
            return self.edit_json('repairs', lambda v: v['repairs'][0].update(fields))

        root = str(self.root)
        cases = [
            ('observed object', lambda m, d, o: [], 'observed is not an object'),
            ('dot component', leaf(source=root + '/projects/./x.md'),
             'observed leaf source is not a normalized path'),
            ('empty component', leaf(source=root + '/projects//x.md'),
             'observed leaf source is not a normalized path'),
            ('digest alphabet', leaf(source=root + '/x.md', sha256='A' * 64),
             'observed leaf is malformed'),
            ('boolean integer', leaf(source=root + '/x.md', bytes=True),
             'observed leaf is malformed'),
            ('negative integer', leaf(source=root + '/x.md', inode=-1),
             'observed leaf is malformed'),
            ('leaf manifest keys', self.edit_json('leaves', lambda v: v.update(extra=1)),
             'admitted keys differ'),
            ('repair set keys', self.edit_json('repairs', lambda v: v.update(extra=1)),
             'RepairSet keys differ'),
            ('repair set version', self.edit_json('repairs', lambda v: v.update(schema_version=2)),
             'RepairSet is malformed'),
            ('repair before digest', repair(before_sha256='bad'), 'Repair is malformed'),
            ('repair after digest', repair(after_sha256='B' * 64), 'Repair is malformed'),
        ]
        for name, change, reason in cases:
            with self.subTest(name):
                self.refused(change, reason)

if __name__ == '__main__':
    unittest.main()
