"""ReaderControls candidate registry-adapter case."""
import json
import unittest

from icm21_fixtures import sealed


class CandidateRegistryCase:
    def test_candidate_registry_adapter(self):
        self.require_file('code/state/icm21_check.py', 'candidate registry adapter integration')
        candidate = self.require_file('plans/icm21/specs/REGISTRIES.json', 'candidate registry')
        registry = json.loads(candidate.read_bytes())
        original = json.loads(sealed('REGISTRIES.json'))
        for collection in ('reader_registry', 'loader_registry'):
            old = {row['id']: row for row in original[collection]}
            new = {row['id']: row for row in registry[collection]}
            self.assertEqual(set(new), set(old))
            self.assertEqual(len(new), len(registry[collection]))
            for key in old:
                self.assertEqual(new[key]['check_ids'], old[key]['check_ids'])
        entry = next(row for row in registry['reader_registry'] if row['id'] == 'labviz-context')
        self.assertEqual(entry['adapter_argv'], ['.venv/bin/python', '-B', '-m', 'unittest',
                                                 'test_icm21.ReaderControls'])
        self.assertNotIn('code.tests', ' '.join(entry['adapter_argv']))
        self.assertEqual(registry['dispatcher'], original['dispatcher'])
