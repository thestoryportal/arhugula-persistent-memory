"""AuditControls report-writer and guide cases; a mixin composed by test_context_audit."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import re

from test_icm21 import BASE, SOURCE_ROOT, binding, encoded, sealed, snapshot


def context_directive():
    text = sealed('brief.md').decode('utf-8')
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


class ReportGuideCases:
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
