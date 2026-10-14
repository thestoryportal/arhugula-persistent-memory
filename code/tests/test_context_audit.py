"""Frozen audit fixture interface for T006; product and host acceptance are separate.

Authority: sealed SPEC 494-537, WIRE-CONTRACTS 224-239 and plan S6.
All filesystem effects belong to miniature repositories, never the source root.
"""
import copy
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import test_icm21 as shared
from test_icm21 import BASE, FixtureCase, binding, digest, encoded, put, sealed, snapshot


SOURCE_ROOT = Path(os.environ['LLMDB_ROOT'])
SELECTED = {
    'AuditControls': (
        'test_guide_candidate', 'test_handoff_context', 'test_lane_ownership',
        'test_model_bulk_locators', 'test_partial_reduction',
        'test_registered_memory_loaders', 'test_report_writer_contract',
        'test_repository_copies', 'test_result_joins', 'test_view_twin_freshness'),
    'GraftControls': ('test_active_loader', 'test_historical_and_missing_coverage'),
}


def context_directive():
    text = sealed('brief').decode('utf-8')
    start = text.index('## Context management (BINDING,')
    end = text.find('\n## ', start + 1)
    return text[start:end if end != -1 else len(text)]


def report_fixture(root, status='PASS', instant='2026-10-13T23:59:59.000001Z'):
    """A wire example, not an observation of the host or a custody receipt."""
    return {
        'schema_version': 1, 'check_id': instant[11:].replace(':', '') + '-session',
        'observed_at': instant, 'root': str(root), 'source_commit': BASE,
        'dirty_source_digests': [], 'mode': 'session',
        'coverage': {'inspected': [str(root)], 'excluded': [],
                     'required_registry_ids': [], 'checked_registry_ids': []},
        'required_checks': ['C-AUDIT'],
        'check_results': [{'id': 'C-AUDIT', 'status': status, 'prd_ids': ['ICM-R10'],
                           'argv': [], 'exit_code': None, 'stdout_sha256': None,
                           'stderr_sha256': None, 'findings': [], 'reason': 'Fixture'}],
        'findings': [], 'previous_report': None, 'overall_status': status,
        'duration_ms': 0, 'reviewed_narrative_paths': [],
        'unreviewed_narrative_paths': [],
    }


def publish_fixture(root, report, directive):
    """MAESTRO's miniature writer contract; this is never a product publisher."""
    instant = datetime.fromisoformat(report['observed_at'].replace('Z', '+00:00'))
    if instant.utcoffset().total_seconds() != 0:
        raise ValueError('UTC required')
    check_id = instant.strftime('%H%M%S.%fZ-') + report['mode']
    if report['check_id'] != check_id:
        raise ValueError('check ID and captured UTC instant disagree')
    directory = root / 'audits/context' / instant.strftime('%Y-%m-%d') / check_id
    directory.mkdir(parents=True, exist_ok=False)
    with (directory / 'report.json').open('xb') as stream:
        stream.write(encoded(report))
    with (directory / 'REPORT.md').open('x', encoding='utf-8') as stream:
        stream.write('# Context audit\n\n' + report['overall_status'] + '\n\n' + directive)
    return directory


class AuditCase(FixtureCase):
    def checker(self):
        return self.module('code/state/icm21_check.py', 'audit')

    def seed(self, required):
        root = self.miniature()
        manifest = shared.ReaderControls.reference_manifest(self, root, [])
        ownership = put(root, 'ownership.tsv', 'phase\tlane\tpath\tscope\tprd_ids\n')
        # The held native custody contract is deliberately incomplete.
        retention = put(root, 'retention.json', encoded({'schema_version': 1}))
        references = put(root, 'reference-manifest.json', encoded(manifest))
        config = {'schema_version': 1, 'canonical_root': str(root),
                  'source_roots': [str(self.scratch / 'source')],
                  'preservation_root': str(self.scratch / 'preserved'),
                  'worktree_root': str(self.scratch / 'lanes'),
                  'tool_root': str(self.scratch / 'tools'),
                  'ownership_path': binding(ownership),
                  'registries': manifest['registries'], 'references': binding(references),
                  'retention': binding(retention), 'required_checks': list(required),
                  'nightly_utc': '02:00:00Z', 'migration_holds': []}
        for key in ('source_roots',):
            for path in config[key]:
                Path(path).mkdir()
        for key in ('preservation_root', 'worktree_root', 'tool_root'):
            Path(config[key]).mkdir()
        return root, config

    def registry(self, root, config, entries):
        value = {'schema_version': 1, 'dispatcher': ['checker'],
                 'reader_registry': [e for e in entries if e['role'] == 'reader'],
                 'loader_registry': [e for e in entries if e['role'] == 'loader']}
        path = put(root, 'registries.json', encoded(value))
        config['registries'] = binding(path)
        manifest = json.loads(Path(config['references']['path']).read_bytes())
        manifest['registries'] = binding(path)
        config['references'] = binding(put(root, 'reference-manifest.json', encoded(manifest)))
        return value

    def entry(self, root, path, check, role='reader', entry_id='fixture-reader'):
        full = Path(path) if Path(path).is_absolute() else root / path
        return {'id': entry_id, 'path': str(path), 'role': role, 'owner': 'fixture',
                'source_sha256': digest(full.read_bytes()) if full.is_file() else None,
                'adapter_argv': None, 'check_ids': [check], 'status': 'SPECIFIED',
                'hold_id': None}

    def observe(self, module, root, config, mode='session'):
        before = snapshot(root)
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            value = module.audit(root, mode, config)
        self.assertIsInstance(value, dict)
        self.assertEqual(snapshot(root), before, 'audit mutated its source')
        self.assertEqual(value['root'], str(root))
        self.assertEqual(value['mode'], mode)
        ids = [x['id'] for x in value['check_results']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(ids) <= set(config['required_checks']))
        self.assertEqual(value['required_checks'], config['required_checks'])
        schema = json.loads(sealed('WIRE-SCHEMAS.json'))
        module.validate_wire('AuditReport', value, schema, {})
        return value

    def check_status(self, value, check, status):
        rows = [x for x in value['check_results'] if x['id'] == check]
        self.assertEqual(len(rows), 1, value)
        self.assertEqual(rows[0]['status'], status, rows[0])
        return rows[0]

    def loader_fixture(self):
        root, config = self.seed(['C-GRAFT'])
        path = put(root, '.claude/settings.json', encoded({'hooks': {}}))
        entry = self.entry(root, '.claude/settings.json', 'C-GRAFT', 'loader', 'repo-claude')
        self.registry(root, config, [entry])
        return root, config, path, entry

    def candidate(self):
        path = self.require_file('audits/context/CONTEXT.md', 'audit subject guide candidate')
        return path.read_text(encoding='utf-8')


class AuditControls(AuditCase):
    def test_result_joins(self):
        module = self.module('code/state/icm21_check.py', 'validate_wire')
        schema = json.loads(sealed('WIRE-SCHEMAS.json'))
        value = report_fixture(self.scratch)
        module.validate_wire('AuditReport', value, schema, {})
        finding = {'id': 'F-AUDIT', 'status': 'FAIL', 'prd_ids': ['ICM-R10'],
                   'paths': [str(self.scratch)], 'evidence': [], 'reason': 'Fixture violation',
                   'previous_finding': None, 'resolution_receipt': None}
        failed = copy.deepcopy(value)
        failed.update(findings=[finding], overall_status='FAIL')
        failed['check_results'][0].update(status='FAIL', findings=['F-AUDIT'])
        module.validate_wire('AuditReport', failed, schema, {})
        for label, mutate in (
                ('duplicate-required', lambda v: v['required_checks'].append('C-AUDIT')),
                ('duplicate-result', lambda v: v['check_results'].append(copy.deepcopy(v['check_results'][0]))),
                ('unknown-result', lambda v: v['check_results'][0].update(id='C-ROOT')),
                ('dangling-finding', lambda v: v['check_results'][0].update(findings=['absent'])),
                ('unreferenced-finding', lambda v: v.update(findings=[finding])),
                ('empty-required', lambda v: v.update(required_checks=[])),
                ('false-pass', lambda v: v.update(check_results=[])),
                ('malformed-result', lambda v: v['check_results'][0].update(exit_code=True)),
                ('malformed-coverage', lambda v: v['coverage'].update(checked_registry_ids=['unknown'])),
                ('wrong-utc-pair', lambda v: v.update(check_id='000000.000000Z-nightly')),
                ('duplicate-finding', lambda v: v.update(findings=[finding, finding]))):
            changed = copy.deepcopy(value)
            mutate(changed)
            with self.subTest(mutant=label), self.assertRaises(ValueError):
                module.validate_wire('AuditReport', changed, schema, {})
        partial = copy.deepcopy(value)
        partial.update(check_results=[], overall_status='UNVERIFIED')
        module.validate_wire('AuditReport', partial, schema, {})
        partial = copy.deepcopy(value)
        partial['coverage']['required_registry_ids'] = ['external-loader']
        partial['overall_status'] = 'UNVERIFIED'
        module.validate_wire('AuditReport', partial, schema, {})

    def test_partial_reduction(self):
        module = self.checker()
        root, config = self.seed(['C-ROOT', 'C-WORKTREE'])
        # No commit or custody evidence exists in this miniature: never invent it.
        value = self.observe(module, root, config)
        self.assertEqual(value['overall_status'], 'UNVERIFIED')
        self.assertTrue(value['coverage']['inspected'])
        self.assertTrue(value['unreviewed_narrative_paths'] or
                        not value['reviewed_narrative_paths'])
        nightly = self.observe(module, root, config, 'nightly')
        self.assertEqual(nightly['overall_status'], 'UNVERIFIED')
        self.assertNotEqual(nightly['check_id'], value['check_id'])
        # A known violation wins over missing custody, source or nightly evidence.
        copy_root = root / 'ignored-copy'
        put(copy_root, 'CLAUDE.md', b'# Copy\n')
        put(copy_root, 'program/program_state.json', b'{}')
        put(copy_root, '_index/path-map.tsv', shared.HEADER)
        put(copy_root, '.git', 'gitdir: ' + str(root / '.git') + '\n')
        config['required_checks'].append('C-BOUNDARY')
        failed = self.observe(module, root, config)
        self.assertEqual(failed['overall_status'], 'FAIL')
        again = self.observe(module, root, config)
        self.assertEqual([f['id'] for f in failed['findings']],
                         [f['id'] for f in again['findings']])
        self.assertTrue(failed['findings'])

    def test_repository_copies(self):
        module = self.checker()
        root, config = self.seed(['C-BOUNDARY'])
        put(root, '.gitignore', 'ignored/\n')
        self.check_status(self.observe(module, root, config), 'C-BOUNDARY', 'PASS')
        foreign = root / 'foreign'
        foreign.mkdir()
        self.git(foreign, 'init', '-q')
        put(foreign, 'README.md', b'# Foreign project\n')
        self.check_status(self.observe(module, root, config), 'C-BOUNDARY', 'PASS')
        for name, markers in (
                ('ignored/current-copy', ('CLAUDE.md', 'program/program_state.json', '_index/path-map.tsv')),
                ('ignored/old-copy', ('CONTEXT.md', 'RUNBOOK.md', 'EXPERIMENTS.md'))):
            for marker in markers:
                put(root / name, marker, b'fixture authority marker\n')
            put(root / name, '.git', 'gitdir: ' + str(root / '.git') + '\n')
            result = self.observe(module, root, config)
            self.check_status(result, 'C-BOUNDARY', 'FAIL')
            self.assertTrue(any(str(root / name) in p for f in result['findings'] for p in f['paths']))
        # A named engine/fixture path cannot excuse this repository's common-dir.
        for name in ('code/vendor/engine', 'code/tests/fixtures/repo'):
            put(root / name, '.git', 'gitdir: ' + str(root / '.git') + '\n')
        self.check_status(self.observe(module, root, config), 'C-BOUNDARY', 'FAIL')
        # Existing authority absence is honest uncertainty, not an empty PASS.
        config['ownership_path']['sha256'] = '0' * 64
        self.assertNotEqual(self.observe(module, root, config)['overall_status'], 'PASS')

    def test_lane_ownership(self):
        self.checker()
        root, config = self.seed(['C-LANES'])
        header = 'phase\tlane\tpath\tscope\tprd_ids\n'
        def table(rows):
            return header + ''.join(f'{phase}\t{lane}\t{root / path}\texact-or-prefix\tICM-R11\n'
                                    for phase, lane, path in rows)
        def lanes(rows, exit_code):
            path = put(root, 'ownership.tsv', table(rows))
            result = self.cli(root, 'code/state/icm21_check.py', 'lanes', '--root', root,
                              '--ownership', path)
            return self.result(result, exit_code)
        good = [(2, 'A', 'code/a.py'), (2, 'B', 'code/b.py')]
        self.assertTrue(lanes(good, 0))
        for other in ('code/a.py', 'code', 'code/a.py/child'):
            with self.subTest(overlap=other):
                self.assertTrue(lanes([good[0], (2, 'B', other)], 1))
        self.assertTrue(lanes([good[0], (3, 'B', 'code/a.py')], 0))
        self.assertTrue(lanes([good[0], (2, 'B', 'code/ab.py')], 0))
        path = put(root, 'ownership.tsv', table(good))
        config['ownership_path'] = binding(path)
        for lane in ('A', 'B'):
            put(Path(config['worktree_root']) / lane, 'BRIEF.md',
                f'owner: {lane}\nbranch: fixture/{lane}\nbase: {BASE}\n'
                f'output: {root / ("code/a.py" if lane == "A" else "code/b.py")}\n'
                'custody: UNVERIFIED\nidle: false\n')
        module = self.checker()
        self.check_status(self.observe(module, root, config), 'C-LANES', 'PASS')
        put(Path(config['worktree_root']) / 'A', 'BRIEF.md', 'owner: A\n')
        self.assertNotEqual(self.observe(module, root, config)['overall_status'], 'PASS')

    def test_view_twin_freshness(self):
        module = self.checker()
        root, config = self.seed(['C-GENERATED', 'C-TWINS'])
        # Reuse the actual generators with miniature inputs, not mocked PASS rows.
        shared.StagedControls.seed_closure(self, root)
        before = snapshot(root)
        value = self.observe(module, root, config)
        self.check_status(value, 'C-GENERATED', 'PASS')
        self.check_status(value, 'C-TWINS', 'PASS')
        self.assertEqual(snapshot(root), before)
        for path, check in (('_index/projects.md', 'C-GENERATED'),
                            ('program/STATUS.md', 'C-GENERATED'),
                            ('map/AGENTS.md', 'C-TWINS')):
            original = (root / path).read_bytes()
            put(root, path, original + b'\nstale\n')
            observed = self.observe(module, root, config)
            self.check_status(observed, check, 'FAIL')
            self.assertEqual(observed['overall_status'], 'FAIL')
            put(root, path, original)
        self.check_status(self.observe(module, root, config), 'C-GENERATED', 'PASS')
        self.check_status(self.observe(module, root, config), 'C-TWINS', 'PASS')

    def test_model_bulk_locators(self):
        module = self.checker()
        root, config = self.seed(['C-MODEL'])
        payload = put(root, 'models/miniature.gguf', b'locator fixture; never a model\n')
        entries = [self.entry(root, 'models/miniature.gguf', 'C-MODEL', 'loader', 'model-readers')]
        self.registry(root, config, entries)
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'PASS')
        self.assertEqual(checked['status'], 'PASS', checked)
        parked = payload.with_suffix('.parked')
        payload.rename(parked)
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'FAIL')
        self.assertEqual(checked['status'], 'FAIL', checked)
        outside = put(self.scratch, 'outside.gguf', b'outside\n')
        payload.symlink_to(outside)
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'FAIL')
        self.assertEqual(checked['status'], 'FAIL', checked)
        missing = self.entry(root, str(self.scratch / 'unobserved/models'), 'C-MODEL',
                             'loader', 'model-readers')
        missing.update(status='UNVERIFIED', hold_id='H1-EXTERNAL-LOADERS')
        self.registry(root, config, [missing])
        checked = self.check_status(self.observe(module, root, config), 'C-MODEL', 'UNVERIFIED')
        self.assertEqual(checked['status'], 'UNVERIFIED', checked)

    def test_registered_memory_loaders(self):
        module = self.checker()
        root, config, path, entry = self.loader_fixture()
        self.check_status(self.observe(module, root, config), 'C-GRAFT', 'PASS')
        for mutate in (lambda x: x.append(copy.deepcopy(x[0])),
                       lambda x: x[0].update(check_ids=['UNKNOWN']),
                       lambda x: x[0].update(extra='forbidden')):
            changed = [copy.deepcopy(entry)]
            mutate(changed)
            self.registry(root, config, changed)
            self.assertNotEqual(self.observe(module, root, config)['overall_status'], 'PASS')
        missing = copy.deepcopy(entry)
        missing.update(id='global-claude', path=str(self.scratch / 'unseen/settings.json'),
                       source_sha256=None, status='UNVERIFIED', hold_id='H1-EXTERNAL-LOADERS')
        self.registry(root, config, [entry, missing])
        value = self.observe(module, root, config)
        self.check_status(value, 'C-GRAFT', 'UNVERIFIED')
        self.assertIn('global-claude', value['coverage']['required_registry_ids'])
        self.assertNotIn('global-claude', value['coverage']['checked_registry_ids'])
        self.assertEqual(path.read_bytes(), encoded({'hooks': {}}))

    def test_handoff_context(self):
        module = self.checker()
        root, config = self.seed(['C-HANDOFF'])
        directive = context_directive()
        text = ('# Handoff\n\nDone: fixture\nIn flight: none\n'
                f'Exact paths: {root / "record.md"}\nNext action: verify\n'
                'Open risks: host UNVERIFIED\n\n' + directive)
        path = put(root, 'HANDOFF.md', text)
        self.registry(root, config, [self.entry(root, 'HANDOFF.md', 'C-HANDOFF')])
        # Budget evidence belongs to the scoped lane handoff, not a global store.
        budget = {'context_left_percent': 60, 'starting_new_work': True,
                  'long_step_pending': False, 'compacted': False}
        put(root, 'context-budget.json', encoded(budget))
        checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'PASS')
        self.assertEqual(checked['status'], 'PASS', checked)
        for label, changed in (
                ('directive', text.replace('60%', '59%', 1)),
                ('done', text.replace('Done: fixture\n', '')),
                ('in-flight', text.replace('In flight: none\n', '')),
                ('paths', text.replace(f'Exact paths: {root / "record.md"}\n', '')),
                ('next', text.replace('Next action: verify\n', '')),
                ('risks', text.replace('Open risks: host UNVERIFIED\n', ''))):
            put(root, 'HANDOFF.md', changed)
            self.registry(root, config, [self.entry(root, 'HANDOFF.md', 'C-HANDOFF')])
            with self.subTest(mutant=label):
                checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'FAIL')
                self.assertEqual(checked['status'], 'FAIL', checked)
        put(root, 'HANDOFF.md', text)
        self.registry(root, config, [self.entry(root, 'HANDOFF.md', 'C-HANDOFF')])
        for remaining, long_step, compacted in ((59, False, False), (45, True, False),
                                               (40, False, False), (90, False, True)):
            budget.update(context_left_percent=remaining, long_step_pending=long_step,
                          compacted=compacted)
            put(root, 'context-budget.json', encoded(budget))
            checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'FAIL')
            self.assertEqual(checked['status'], 'FAIL', checked)
        put(root, 'context-budget.json', b'null')
        checked = self.check_status(self.observe(module, root, config), 'C-HANDOFF', 'UNVERIFIED')
        self.assertEqual(checked['status'], 'UNVERIFIED', checked)

    def test_report_writer_contract(self):
        self.candidate()
        directive = context_directive()
        complete = report_fixture(self.scratch)
        partial = report_fixture(self.scratch, 'UNVERIFIED', '2026-10-14T00:00:00.000002Z')
        first = publish_fixture(self.scratch, complete, directive)
        complete_binding = binding(first / 'report.json')
        second = publish_fixture(self.scratch, partial, directive)
        partial_binding = binding(second / 'report.json')
        self.assertEqual(first.parent.name, '2026-10-13')
        self.assertEqual(second.parent.name, '2026-10-14')
        self.assertNotEqual(first, second)
        for path, value in ((first, complete), (second, partial)):
            self.assertEqual((path / 'report.json').read_bytes(), encoded(value))
            self.assertIn(directive, (path / 'REPORT.md').read_text())
            self.assertEqual(path.name, value['check_id'])
        before = snapshot(self.scratch)
        with self.assertRaises(FileExistsError):
            publish_fixture(self.scratch, complete, directive)
        self.assertEqual(snapshot(self.scratch), before)
        wrong = copy.deepcopy(partial)
        wrong['check_id'] = '235959.000001Z-nightly'
        with self.assertRaises(ValueError):
            publish_fixture(self.scratch, wrong, directive)
        pointers = {'latest_complete': binding(first / 'report.json'),
                    'newer_partial': binding(second / 'report.json')}
        expected = {'latest_complete': complete_binding, 'newer_partial': partial_binding}
        for key, value in pointers.items():
            self.assertEqual(value, expected[key], key)
        self.assertEqual(json.loads(Path(pointers['latest_complete']['path']).read_bytes())['overall_status'], 'PASS')
        self.assertEqual(json.loads(Path(pointers['newer_partial']['path']).read_bytes())['overall_status'], 'UNVERIFIED')

    def test_guide_candidate(self):
        text = self.candidate()
        for word in ('scope', 'owner', 'method', 'complete', 'partial', 'UNVERIFIED'):
            self.assertIn(word.lower(), text.lower())
        self.assertIn(context_directive(), text)
        pointers = re.findall(r'\[[^\]]+\]\(([^)]+(?:report\.json|REPORT\.md))\)', text)
        for target in pointers:
            self.assertFalse(Path(target).is_absolute())
            path = SOURCE_ROOT / 'audits/context' / target
            self.assertTrue(path.is_file(), 'unbound report pointer: ' + target)
            if path.name == 'report.json':
                value = json.loads(path.read_bytes())
                self.assertEqual(value['check_id'], path.parent.name)
        if not pointers:
            self.assertIn('UNVERIFIED', text)


class GraftControls(AuditCase):
    def test_active_loader(self):
        module = self.checker()
        root, config, path, entry = self.loader_fixture()
        for value in (
                {'hooks': {'SessionStart': [{'hooks': [{'type': 'command', 'command': 'graft load'}]}]}},
                {'mcpServers': {'graft': {'command': 'graft', 'args': ['serve']}}},
                {'search': {'exceptions': ['graft']}}):
            put(root, '.claude/settings.json', encoded(value))
            entry['source_sha256'] = digest(path.read_bytes())
            self.registry(root, config, [entry])
            result = self.observe(module, root, config)
            self.check_status(result, 'C-GRAFT', 'FAIL')
            self.assertTrue(result['findings'])

    def test_historical_and_missing_coverage(self):
        module = self.checker()
        root, config, path, entry = self.loader_fixture()
        history = put(root, 'history.md', b'Historical graft load receipt; do not execute.\n')
        exclusion = put(root, '.gitignore', b'graft/\n')
        self.check_status(self.observe(module, root, config), 'C-GRAFT', 'PASS')
        missing = copy.deepcopy(entry)
        missing.update(id='global-codex', path=str(self.scratch / 'external/hooks.json'),
                       source_sha256=None, status='UNVERIFIED', hold_id='H1-EXTERNAL-LOADERS')
        self.registry(root, config, [entry, missing])
        self.check_status(self.observe(module, root, config), 'C-GRAFT', 'UNVERIFIED')
        self.assertIn(b'graft load', history.read_bytes())
        self.assertEqual(exclusion.read_bytes(), b'graft/\n')
        self.assertEqual(path.read_bytes(), encoded({'hooks': {}}))


class AuditFixtureControls(unittest.TestCase):
    def test_complete_collection(self):
        loader = unittest.TestLoader()
        for name, methods in SELECTED.items():
            cls = globals()[name]
            self.assertTrue(issubclass(cls, unittest.TestCase))
            self.assertEqual(set(loader.getTestCaseNames(cls)), set(methods))
            self.assertEqual(loader.loadTestsFromTestCase(cls).countTestCases(), len(methods))

    def test_sealed_interface_definition(self):
        definition = json.loads(sealed('foundation-specs'))['T006']
        self.assertEqual(definition['subject'], 'code/tests/test_context_audit.py')
        self.assertEqual(definition['contract'], type(self).__name__)
        for name, methods in definition['required'].items():
            self.assertTrue(set(methods) <= set(SELECTED[name]))
        self.assertEqual(context_directive(), json.loads(
            (shared.PACKAGE / 'context.json').read_bytes())['verbatim'][0]['text'])

    def test_saved_behavioral_baselines(self):
        with tempfile.TemporaryDirectory(prefix='icm21-audit-base-', dir='/private/tmp') as temporary:
            baseline = Path(temporary)
            # Extract exact base bytes before executing controls; absent subjects stay absent.
            for relative in ('code/state/build_index.py', 'code/state/render_state.py',
                             'code/agents/twins.py'):
                result = subprocess.run(['git', 'show', BASE + ':' + relative],
                                        cwd=SOURCE_ROOT, capture_output=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                self.assertTrue(result.stdout)
                self.assertEqual(result.stdout, sealed('base/' + relative))
                put(baseline, relative, result.stdout)
            for relative in ('code/state/icm21_check.py', 'audits/context/CONTEXT.md'):
                result = subprocess.run(['git', 'show', BASE + ':' + relative],
                                        cwd=SOURCE_ROOT, capture_output=True, timeout=30)
                self.assertEqual(result.returncode, 128, result.stderr.decode())
                self.assertEqual(result.stdout, b'')
                self.assertIn(relative, result.stderr.decode())
            with patch.dict(globals(), {'SOURCE_ROOT': baseline}), patch.object(shared, 'SOURCE_ROOT', baseline):
                for name, methods in SELECTED.items():
                    for method in methods:
                        stream = io.StringIO()
                        with patch.dict(sys.modules), patch.dict(os.environ, {'LLMDB_ROOT': str(baseline)}):
                            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
                                unittest.TestSuite([globals()[name](method)]))
                        output = stream.getvalue()
                        observation = {'control': name + '.' + method, 'base': BASE,
                                       'tests': result.testsRun, 'failures': len(result.failures),
                                       'errors': len(result.errors), 'output': output}
                        print('BEHAVIORAL_BASELINE ' + json.dumps(observation, sort_keys=True))
                        self.assertEqual(result.testsRun, 1, output)
                        self.assertEqual(len(result.failures), 1, output)
                        self.assertEqual(result.errors, [], output)
                        self.assertEqual(result.skipped, [], output)
                        self.assertEqual(result.expectedFailures, [], output)
                        self.assertEqual(result.unexpectedSuccesses, [], output)
                        self.assertIn('AssertionError', output)
                        self.assertIn('absent behavior:', output)


if __name__ == '__main__':
    unittest.main()
