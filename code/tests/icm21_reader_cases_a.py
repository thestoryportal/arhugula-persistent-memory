"""ReaderControls helpers; composes the queue, resolver and LabViz-reader case leaves (mixin for test_icm21)."""
from icm21_case_labviz_reader import LabvizReaderCase
from icm21_case_queue import QueueCase
from icm21_case_resolver import ResolverCase
from icm21_fixtures import binding, encoded, put


class ReaderCasesA(QueueCase, ResolverCase, LabvizReaderCase):
    def reference_manifest(self, root, rows):
        references = put(root, 'references.jsonl', b''.join(encoded(row) + b'\n' for row in rows))
        registries = put(root, 'registries.json', encoded({'schema_version': 1,
            'dispatcher': ['checker'], 'reader_registry': [], 'loader_registry': []}))
        executor = put(root, 'executor.json', encoded({'schema_version': 1, 'operations': []}))
        repairs = put(root, 'repairs.json', encoded({'schema_version': 1, 'repairs': []}))
        coverage = put(root, 'coverage.json', encoded({'schema_version': 1, 'scope': 'miniature',
            'coverage': {'inspected': [str(root)], 'excluded': [],
                         'required_registry_ids': [], 'checked_registry_ids': []}, 'sources': []}))
        return {'schema_version': 1, 'references': binding(references), 'registries': binding(registries),
                'executor': binding(executor), 'repairs': binding(repairs), 'coverage': binding(coverage)}
