"""Queue compatibility and current index output cases (ReaderControls)."""
import copy
import json
from pathlib import Path
import unittest

from icm21_fixtures import INDEX_PATHS, SOURCE_ROOT, digest, encoded, put


class QueueCase:
    def test_queue_compatibility_and_candidates(self):
        self.require_file('code/state/icm21_check.py', 'D1 strict queue candidate validation')
        root = self.miniature()
        original = (SOURCE_ROOT / 'program/program_state.json').read_bytes()
        state = json.loads(original)
        items = state['work_queue']['items']
        self.assertTrue(items)
        self.assertTrue(all('artifact' not in item for item in items))
        put(root, 'program/program_state.json', original)
        view = self.generate(root)['projects.md'].decode()
        self.assertIn('legacy-unspecified', view)
        self.assertEqual((root / 'program/program_state.json').read_bytes(), original)
        for artifact, label in ((None, 'no-materialized-record'), *(
                ({'kind': kind, 'path': 'records/' + kind}, kind)
                for kind in ('project', 'plan', 'audit', 'research', 'experiment'))):
            with self.subTest(artifact=artifact):
                candidate = copy.deepcopy(state)
                candidate['work_queue']['items'][0]['artifact'] = artifact
                if artifact is not None:
                    (root / artifact['path']).mkdir(parents=True, exist_ok=True)
                data = encoded(candidate)
                put(root, 'program/program_state.json', data)
                self.assertIn(label, self.generate(root)['projects.md'].decode())
                self.assertEqual((root / 'program/program_state.json').read_bytes(), data)
        for artifact in ({}, {'kind': 'unknown', 'path': 'records/project'},
                         {'kind': 'project', 'path': '../escape'},
                         {'kind': 'project', 'path': str(self.scratch)},
                         {'kind': 'project', 'path': 'missing'},
                         {'kind': 'project', 'path': 'records/project', 'extra': 1}):
            candidate = copy.deepcopy(state)
            candidate['work_queue']['items'][0]['artifact'] = artifact
            put(root, 'program/program_state.json', encoded(candidate))
            with self.subTest(invalid=artifact), self.assertRaises(ValueError):
                self.generate(root)
        # The references checker applies strict creation/repair admission separately.
        put(root, 'program/program_state.json', original)
        self.assertEqual(json.loads(original)['updated'], state['updated'])
        self.assertEqual(json.loads(original)['next_actions'][6], state['next_actions'][6])
        self.assertEqual(json.loads(original)['work_queue']['items'][2]['notes'][1],
                         state['work_queue']['items'][2]['notes'][1])

    def test_current_index_outputs(self):
        self.require_file('code/state/icm21_check.py', 'installed D1 current index outputs')
        expected = self.generate(SOURCE_ROOT)
        for relative in INDEX_PATHS:
            self.assertEqual(digest((SOURCE_ROOT / relative).read_bytes()),
                             digest(expected[Path(relative).name]), relative)
        self.assertIn('legacy-unspecified', (SOURCE_ROOT / '_index/projects.md').read_text())
