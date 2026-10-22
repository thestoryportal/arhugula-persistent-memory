"""Fixture-only contract for the Step 407 registry and scan classifier."""
import ast
import copy
import inspect
import unittest
from dataclasses import FrozenInstanceError
from unittest import mock

from ops.migrate import fdsafe
from ops.migrate import root_readers_core as core


class Registry(unittest.TestCase):
    def test_all_kinds_and_fields(self):
        rows = core.parse_registry(
            '# registry\n\nREPLACE\tconfig\t/M\t/R\t2\n'
            'REPLACE\t/outside\told\tnew\tmeasured\n'
            'RENAME\t/a\t/b\nINSTALL\tcode/script\t/bin/script\n'
            'CHECK\treader-class\tcheck-id\nSTOP\tworker\n'
            'RECORD\t/history\tretained evidence\nRECORD\trel/history\n')
        self.assertEqual(rows, (
            core.Replace('config', '/M', '/R', 2),
            core.Replace('/outside', 'old', 'new', 'measured'),
            core.Rename('/a', '/b'), core.Install('code/script', '/bin/script'),
            core.Check('reader-class', 'check-id'), core.Stop('worker'),
            core.Record('/history', 'retained evidence'), core.Record('rel/history')))
        self.assertEqual([r.kind for r in rows],
                         ['REPLACE', 'REPLACE', 'RENAME', 'INSTALL', 'CHECK', 'STOP', 'RECORD', 'RECORD'])

    def test_tsv_quoted_edits_preserve_tabs_newlines_and_quotes(self):
        rows = core.parse_registry('REPLACE\tp\t"a\tb"\t"c\n""d"""\t0\n')
        self.assertEqual(rows, (core.Replace('p', 'a\tb', 'c\n"d"', 0),))

    def test_malformed_rows_name_physical_line(self):
        bads = ['UNKNOWN\tx', 'STOP', 'STOP\tx\ty', 'RECORD\t',
                'CHECK\tx\t', 'RENAME\t/a\t', 'INSTALL\t/a\t/b',
                'INSTALL\ta\tb', 'REPLACE\tp\t\tn\t1',
                'REPLACE\tp\to\t\t1', 'REPLACE\tp\to\tn',
                'REPLACE\tp\to\tn\t-1', 'REPLACE\tp\to\tn\t1.0',
                'REPLACE\tp\to\tn\tTrue', 'REPLACE\tp\to\tn\t١',
                'REPLACE\tp\to\tn\t+1', 'REPLACE\tp\to\tn\t',
                'STOP\t"unterminated', 'STOP\ta\x00b']
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(fdsafe.Refusal) as ctx:
                core.parse_registry('# header\n\n' + bad)
            self.assertIn('line 3', str(ctx.exception))
            self.assertIn('EINVAL', str(ctx.exception))
            self.assertEqual(len(str(ctx.exception).splitlines()), 1)

    def test_path_fields_refuse_escapes_and_noncanonical_spellings(self):
        for bad in ('../x', 'a/../x', './x', 'a//x', 'a/', '/a/./b', '~/.x'):
            for row in (f'REPLACE\t{bad}\to\tn\t1', f'RENAME\t{bad}\t/b',
                        f'RENAME\t/a\t{bad}', f'INSTALL\t{bad}\t/b',
                        f'INSTALL\ta\t{bad}', f'RECORD\t{bad}'):
                with self.subTest(row=row), self.assertRaises(fdsafe.Refusal):
                    core.parse_registry(row)

    def test_registry_types(self):
        for bad in (None, [], {}, b'STOP\tx', 4, True):
            with self.subTest(bad=bad), self.assertRaises(fdsafe.Refusal):
                core.parse_registry(bad)

    def test_count_conversion_is_bounded_and_names_line(self):
        for digits in (19, 5000):
            for path in ('p', ''):
                with self.subTest(digits=digits, path=path):
                    with self.assertRaisesRegex(fdsafe.Refusal, 'registry line 3'):
                        core.parse_registry('# header\n\nREPLACE\t' + path +
                                            '\to\tn\t' + '1' * digits)
        self.assertEqual(core.parse_registry('REPLACE\tp\to\tn\t' + '9' * 18),
                         (core.Replace('p', 'o', 'n', 999999999999999999),))

    def test_non_string_text_refuses(self):
        with self.assertRaisesRegex(fdsafe.Refusal, 'STOP.process_class'):
            core.Stop(17)

    def test_record_control_characters_refuse_with_line(self):
        for char in ('\n', '\r', '\t'):
            with self.subTest(char=char):
                with self.assertRaisesRegex(fdsafe.Refusal, 'registry line 2'):
                    core.parse_registry('# header\nRECORD\t"history' + char + 'x"')

    def test_multiple_edits_same_path(self):
        self.assertEqual(len(core.parse_registry('REPLACE\tp\ta\tb\t1\nREPLACE\tp\tc\td\t2')), 2)

    def test_direct_rows_reject_bad_fields_and_are_frozen(self):
        for value in (None, '', 'a\0b'):
            factories = ((core.Replace, (value, 'o', 'n', 1)),
                         (core.Replace, ('p', value, 'n', 1)),
                         (core.Replace, ('p', 'o', value, 1)),
                         (core.Rename, (value, '/b')), (core.Rename, ('/a', value)),
                         (core.Install, (value, '/b')), (core.Install, ('a', value)),
                         (core.Check, (value, 'id')), (core.Check, ('class', value)),
                         (core.Stop, (value,)), (core.Record, (value,)))
            for factory, args in factories:
                with self.subTest(factory=factory, args=args), self.assertRaises(fdsafe.Refusal):
                    factory(*args)
        for value in (-1, True, 1.5, '1', None):
            with self.subTest(value=value), self.assertRaises(fdsafe.Refusal):
                core.Replace('p', 'o', 'n', value)
        for value in (None, 1, 'bad\0reason'):
            with self.subTest(value=value), self.assertRaises(fdsafe.Refusal):
                core.Record('p', value)
        with self.assertRaises(fdsafe.Refusal):
            core.parse_registry('RECORD\tp\tbad\0reason')
        for row in core.parse_registry('REPLACE\tp\to\tn\t1\nRENAME\ta\tb\n'
                                       'INSTALL\ta\t/b\nCHECK\tp\tc\nSTOP\tp\nRECORD\tp'):
            with self.assertRaises(FrozenInstanceError):
                row.kind = 'RECORD'

    def test_multiline_edits_keep_next_physical_line(self):
        with self.assertRaises(fdsafe.Refusal) as ctx:
            core.parse_registry('REPLACE\tp\t"a\nb"\tc\t1\nCHECK\t\tid')
        self.assertIn('line 3', str(ctx.exception))

    def test_unexpected_dependency_errors_propagate(self):
        class BrokenText(str):
            def startswith(self, *args):
                raise RuntimeError('dependency failure')

        class Reader:
            line_num = 1

            def __iter__(self):
                return iter([['RENAME', BrokenText('a'), 'b']])

        # Fault the CSV dependency, never the parser or row constructors.
        with mock.patch('csv.reader', return_value=Reader()):
            with self.assertRaisesRegex(RuntimeError, 'dependency failure'):
                core.parse_registry('input')

    def test_constructor_value_error_propagates_unchanged(self):
        error = ValueError('dependency failure')

        class BrokenText(str):
            def startswith(self, *args):
                raise error

        class Reader:
            line_num = 1

            def __iter__(self):
                return iter([['RENAME', BrokenText('a'), 'b']])

        with mock.patch('csv.reader', return_value=Reader()):
            with self.assertRaises(ValueError) as ctx:
                core.parse_registry('input')
        # [LAW:behavior-not-structure] Refusal is also a ValueError; preserve identity.
        self.assertIs(ctx.exception, error)


class Classification(unittest.TestCase):
    def setUp(self):
        self.rows = core.parse_registry('REPLACE\tconfig\t/M\t/R\t2\nRECORD\t/history')

    def run_scan(self, stage='pre', **overrides):
        kw = dict(rows=self.rows, stage=stage, hits={'config': 2, '/history/x': 1},
                  counts={('config', '/M'): 2, ('config', '/R'): 0},
                  old_root_exists=True, measured_counts={})
        kw.update(overrides)
        return core.classify(**kw)

    def test_pre_live_record_and_unregistered(self):
        result = self.run_scan(hits={'config': 2, '/history': 1, '/history/x': 1,
                                    '/history-live/x': 1, 'unknown': 1})
        self.assertEqual(result.classifications,
                         (('config', 'LIVE'), ('/history', 'RECORD'), ('/history/x', 'RECORD'),
                          ('/history-live/x', 'unregistered'), ('unknown', 'unregistered')))
        self.assertEqual(result.findings, ('/history-live/x: unregistered', 'unknown: unregistered'))
        self.assertEqual(result.exit_status, 1)

    def test_clean_pre_and_zero_hits(self):
        result = self.run_scan(hits={'config': 2, 'unknown': 0})
        self.assertEqual(result.findings, ())
        self.assertEqual(result.classifications, (('config', 'LIVE'),))
        self.assertEqual(result.exit_status, 0)

    def test_pre_exact_count_too_low_high_and_zero(self):
        for count in (0, 1, 3):
            with self.subTest(count=count):
                result = self.run_scan(counts={('config', '/M'): count})
                self.assertEqual(result.exit_status, 1)
                self.assertEqual(result.findings, (f'config: old count {count}, expected 2',))

    def test_missing_observation_refuses_not_zero(self):
        for stage in ('pre', 'post'):
            with self.subTest(stage=stage), self.assertRaises(fdsafe.Refusal):
                self.run_scan(stage, counts={})
        with self.assertRaises(fdsafe.Refusal):
            self.run_scan('post', counts={('config', '/M'): 0})

    def test_post_all_requirements(self):
        result = self.run_scan('post', hits={'/history/x': 1},
                               counts={('config', '/M'): 0, ('config', '/R'): 2}, old_root_exists=False)
        self.assertEqual((result.exit_status, result.findings), (0, ()))
        result = self.run_scan('post', hits={'config': 1, 'other': 2})
        self.assertEqual(result.exit_status, 1)
        self.assertEqual(result.findings, ('config: old count 2, expected 0',
                         'config: new count 0, expected 2', 'old root still exists',
                         'config: unregistered', 'other: unregistered'))

    def test_record_does_not_waive_replace_counts(self):
        rows = core.parse_registry('REPLACE\t/history/a\to\tn\t1\nRECORD\t/history')
        result = self.run_scan(rows=rows, counts={('/history/a', 'o'): 0}, hits={'/history/a': 1})
        self.assertEqual(result.exit_status, 1)
        self.assertEqual(result.classifications, (('/history/a', 'RECORD'),))

    def test_other_row_kinds_never_allow_hits(self):
        rows = core.parse_registry('CHECK\tp\tc\nSTOP\tp\nRENAME\tp\tq\nINSTALL\ts\t/d')
        result = self.run_scan(rows=rows, counts={}, hits={'p': 1, 'q': 1, 's': 1, '/d': 1})
        self.assertEqual(len(result.findings), 4)
        self.assertEqual(result.exit_status, 1)

    def test_root_record_and_relative_component_boundary(self):
        rows = core.parse_registry('RECORD\t/\nRECORD\thistory')
        result = self.run_scan(rows=rows, counts={}, hits={'/x': 1, 'history/x': 1, 'history-live/x': 1})
        self.assertEqual(result.classifications, (('/x', 'RECORD'), ('history/x', 'RECORD'),
                                                 ('history-live/x', 'unregistered')))

    def test_measured_pre_exports_positive_count_post_requires_it(self):
        rows = core.parse_registry('REPLACE\tp\to\tn\tmeasured')
        result = self.run_scan(rows=rows, counts={('p', 'o'): 3}, hits={'p': 3})
        self.assertEqual(result.measured_counts, ((0, 3),))
        self.assertEqual(result.exit_status, 0)
        result = self.run_scan(rows=rows, counts={('p', 'o'): 0}, hits={})
        self.assertEqual(result.exit_status, 1)
        with self.assertRaises(fdsafe.Refusal):
            self.run_scan('post', rows=rows, counts={('p', 'o'): 0, ('p', 'n'): 3}, hits={})
        for count in (2, 3, 4):
            result = self.run_scan('post', rows=rows, counts={('p', 'o'): 0, ('p', 'n'): count},
                                   hits={}, old_root_exists=False, measured_counts={0: 3})
            self.assertEqual(result.exit_status, int(count != 3))

    def test_zero_exact_count_and_multiple_edits(self):
        rows = core.parse_registry('REPLACE\tp\ta\tb\t0\nREPLACE\tp\tc\td\t1')
        result = self.run_scan(rows=rows, counts={('p', 'a'): 0, ('p', 'c'): 1}, hits={'p': 1})
        self.assertEqual(result.exit_status, 0)

    def test_no_input_mutation(self):
        kw = dict(hits={'config': 2}, counts={('config', '/M'): 2}, measured_counts={})
        before = copy.deepcopy(kw)
        self.run_scan(**kw)
        self.assertEqual(kw, before)

    def test_bad_scan_facts_refuse(self):
        cases = [('stage', 'other'), ('stage', []), ('old_root_exists', 1),
                 ('hits', None), ('counts', []), ('measured_counts', []),
                 ('rows', 'RECORD'), ('rows', [None]),
                 ('counts', {'p': 1}), ('counts', {('p', ''): 1}),
                 ('hits', {'../p': 1}), ('measured_counts', {True: 1}),
                 ('measured_counts', {0: 0}), ('measured_counts', {-1: 1})]
        for bad in (-1, True, 1.5, '1', None):
            cases.extend([('hits', {'p': bad}), ('counts', {('p', 'o'): bad}),
                          ('measured_counts', {0: bad})])
        for field, value in cases:
            with self.subTest(field=field, value=value), self.assertRaises(fdsafe.Refusal):
                self.run_scan(**{field: value})

    def test_rows_mapping_refuses(self):
        with self.assertRaisesRegex(fdsafe.Refusal, 'rows'):
            self.run_scan(rows={}, hits={}, counts={})

    def test_count_key_non_tuple_refuses(self):
        with self.assertRaisesRegex(fdsafe.Refusal, 'counts'):
            self.run_scan(rows=(), hits={}, counts={'po': 1})

    def test_count_key_wrong_arity_refuses(self):
        for key in ((), ('p',), ('p', 'o', 'ignored')):
            with self.subTest(key=key), self.assertRaisesRegex(fdsafe.Refusal, 'counts'):
                self.run_scan(rows=(), hits={}, counts={key: 1})

    def test_invalid_facts_are_not_hidden_by_missing_counts(self):
        for key in (('../p', 'o'), ('p', ''), ('p', None)):
            counts = {('config', '/M'): 2, key: 1}
            with self.subTest(key=key), self.assertRaises(fdsafe.Refusal):
                self.run_scan(counts=counts)
        for value in (-1, True, 1.5, '1', None):
            with self.subTest(value=value), self.assertRaises(fdsafe.Refusal):
                self.run_scan(counts={('config', '/M'): value})

    def test_measured_snapshot_rejects_bad_index_and_zero(self):
        rows = core.parse_registry('REPLACE\tp\to\tn\tmeasured\nRECORD\thistory')
        for snapshot in ({False: 2}, {True: 2}, {-1: 2}, {0: 0}, {1: 2}, {2: 2}):
            with self.subTest(snapshot=snapshot), self.assertRaises(fdsafe.Refusal):
                self.run_scan(rows=rows, counts={('p', 'o'): 2}, hits={}, measured_counts=snapshot)
        with self.assertRaises(fdsafe.Refusal):
            self.run_scan(measured_counts={0: 2})


    def test_empty_registry_never_allows_hits(self):
        # [LAW:behavior-not-structure] Folder names confer no registry authority.
        paths = ('/history/x', '/history', 'history/x', 'code/x', 'program/x',
                 'knowledge/x', 'experiments/x', 'data/x', '_archive/x',
                 '_system/x', '_index/x', '.claude/x', '.venv/x', '/Users/x/y',
                 'bare', 'evidence/x', 'plans/x', 'audits/x', '_templates/x',
                 'projects/x', 'map/x', '.codex/x', '.github/x')
        for stage in ('pre', 'post'):
            for path in paths:
                with self.subTest(stage=stage, path=path):
                    result = self.run_scan(stage, rows=(), counts={},
                                           hits={path: 1}, old_root_exists=False)
                    self.assertEqual(result.classifications, ((path, 'unregistered'),))
                    self.assertEqual(result.findings, (f'{path}: unregistered',))
                    self.assertEqual(result.exit_status, 1)

    def test_mixed_registry_allows_only_covered_hits(self):
        # [LAW:behavior-not-structure] Assert the complete partition at each stage.
        rows = core.parse_registry('RECORD\t/history\nREPLACE\tconfig\t/M\t/R\t2')
        uncovered = ('/history-old/x', '/history-old', 'history/x', 'code/x',
                     'program/x', 'knowledge/x', 'experiments/x', 'data/x',
                     '_archive/x', '_system/x', '_index/x', '.claude/x', '.venv/x',
                     '/Users/x/y', 'bare', 'config-old', 'config/x', 'evidence/x',
                     'plans/x', 'audits/x', '_templates/x', 'projects/x', 'map/x',
                     '.codex/x', '.github/x')
        hits = {'/history': 1, '/history/x': 1, 'config': 2,
                **dict.fromkeys(uncovered, 1)}
        for stage, old_count, new_count, replace_kind in (
                ('pre', 2, 0, 'LIVE'), ('post', 0, 2, 'unregistered')):
            with self.subTest(stage=stage):
                result = self.run_scan(
                    stage, rows=rows, hits=hits, old_root_exists=False,
                    counts={('config', '/M'): old_count, ('config', '/R'): new_count})
                expected = (('/history', 'RECORD'), ('/history/x', 'RECORD'),
                            ('config', replace_kind)) + tuple(
                                (path, 'unregistered') for path in uncovered)
                self.assertEqual(result.classifications, expected)
                self.assertEqual(result.findings, tuple(
                    f'{path}: unregistered' for path, kind in expected
                    if kind == 'unregistered'))
                self.assertEqual(result.exit_status, 1)


class Purity(unittest.TestCase):
    def assert_pure(self, source):
        tree = ast.parse(source)
        allowed_imports = {
            '__future__': {'annotations'}, 'collections.abc': {'Mapping'},
            'dataclasses': {'dataclass', 'field'}, 'typing': {'Literal'},
            'ops.migrate': {'fdsafe'},
        }
        module_attributes = {'csv': {'reader', 'Error'}, 'io': {'StringIO'},
                             'fdsafe': {'Refusal'}}
        calls = {'_refuse', '_text', '_path', '_count', '_mapping', 'isinstance',
                 'type', 'any', 'len', 'int', 'str', 'tuple', 'bool', 'enumerate',
                 'dataclass', 'field', 'constructor', 'ScanResult'}
        methods = {'startswith', 'removeprefix', 'split', 'rstrip', 'items', 'append'}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name, {'csv', 'io'})
                    self.assertIsNone(alias.asname)
            elif isinstance(node, ast.ImportFrom):
                self.assertEqual(node.level, 0)
                self.assertIn(node.module, allowed_imports)
                for alias in node.names:
                    self.assertIn(alias.name, allowed_imports[node.module])
                    self.assertIsNone(alias.asname)
            elif isinstance(node, ast.Attribute):
                root = node.value
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name) and root.id in module_attributes:
                    self.assertIsInstance(node.value, ast.Name)
                    self.assertIn(node.attr, module_attributes[root.id])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertIn(node.func.id, calls)
                else:
                    self.assertIsInstance(node.func, ast.Attribute)
                    if (isinstance(node.func.value, ast.Name) and
                            node.func.value.id in module_attributes):
                        self.assertIn(node.func.attr, module_attributes[node.func.value.id])
                    else:
                        self.assertIn(node.func.attr, methods)

    def test_imports_and_calls_allowlist(self):
        # [LAW:effects-at-boundaries] Imported modules must not expose an I/O escape.
        self.assert_pure(inspect.getsource(core))

    def test_purity_rejects_imported_effects_and_unlisted_calls(self):
        source = inspect.getsource(core)
        for statement in ('fdsafe.os.access(__file__, 0)', 'fdsafe.os.listdir(".")',
                          'effect = fdsafe.os', 'print("effect")',
                          'getattr(fdsafe, "os")', 'import os'):
            with self.subTest(statement=statement), self.assertRaises(AssertionError):
                self.assert_pure(source + '\n' + statement + '\n')


if __name__ == '__main__':
    unittest.main()
