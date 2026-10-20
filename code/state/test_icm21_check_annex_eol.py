"""T366: real moves inputs obey the shared, strict annex line-ending rule.

MovesCase owns fixture cleanup and the macOS filesystem boundary; Linux discovery
skips these integration cases without calling F_GETPATH.
"""
import unittest
from unittest import mock

from ops.migrate import fdsafe, move_plan_core
from test_icm21_moves_cli import IDS, MovesCase


TABLES = ('req-a.tsv', 'req-b.tsv', 'phase.tsv')


def crlf(data):
    return data.replace(b'\n', b'\r\n')


class AnnexLineEnds(MovesCase):
    def lf_bytes(self):
        self.fx.publish()
        return {name: self.fx.path(name).read_bytes() for name in TABLES}

    def run_with(self, stage, tables):
        for name, data in tables.items():
            self.fx.path(name).write_bytes(data)
        return self.run_stage(stage, publish=False)

    def assertSameAsLf(self, stage):
        lf = self.lf_bytes()
        expected = self.run_with(stage, lf)
        for changed in [(name,) for name in TABLES] + [TABLES]:
            with self.subTest(stage=stage, crlf=changed):
                tables = dict(lf, **{name: crlf(lf[name]) for name in changed})
                self.assertEqual(self.run_with(stage, tables), expected)
        return expected

    def test_crlf_tables_pass_as_lf_tables(self):
        for stage in ('pre', 'post'):
            code, result = self.assertSameAsLf(stage)
            self.assertEqual((code, result['findings']), (0, []), result)

    def test_crlf_tables_give_the_lf_findings(self):
        self.fx.operations = IDS[:3]
        self.fx.observed_leaves[0]['sha256'] = '9' * 64
        code, result = self.assertSameAsLf('post')
        self.assertEqual(code, 2, result)
        self.assertEqual(sorted({item['status'] for item in result['findings']}),
                         ['FAIL', 'UNVERIFIED'], result)

    def test_every_table_uses_the_shared_line_rule(self):
        lf = self.lf_bytes()
        # [LAW:single-enforcer] R4 requires delegation, not an equivalent local copy.
        for tables in (lf, {name: crlf(data) for name, data in lf.items()}):
            for stage in ('pre', 'post'):
                with self.subTest(stage=stage, crlf=tables != lf):
                    with mock.patch.object(move_plan_core, 'tsv_lines',
                                           wraps=move_plan_core.tsv_lines) as rule:
                        code, result = self.run_with(stage, tables)
                    self.assertEqual((code, result['findings']), (0, []), result)
                    self.assertEqual(rule.call_args_list, [
                        mock.call(tables[name].decode('utf-8'), str(self.fx.path(name)))
                        for name in TABLES])

    def test_shared_line_rule_refusal_is_returned_unchanged(self):
        lf = self.lf_bytes()
        refusal = fdsafe.Refusal('shared line rule', 'T366 sentinel refusal')
        for stage in ('pre', 'post'):
            with self.subTest(stage=stage):
                with mock.patch.object(move_plan_core, 'tsv_lines', side_effect=refusal):
                    code, result = self.run_with(stage, lf)
                self.assertEqual((code, result),
                                 (2, {'status': 'UNVERIFIED', 'reason': str(refusal)}))

    def assertLineRefusal(self, stage, lf, name, data):
        path = str(self.fx.path(name))
        # [LAW:behavior-not-structure] Compare real refusals, never replace the parser.
        with self.assertRaises(fdsafe.Refusal) as caught:
            move_plan_core.tsv_lines(data.decode('utf-8'), path)
        expected = str(caught.exception)
        self.assertIn(path, expected)
        code, result = self.run_with(stage, dict(lf, **{name: data}))
        self.assertEqual((code, result),
                         (2, {'status': 'UNVERIFIED', 'reason': expected}))

    def test_field_cr_and_mixed_line_ends_refuse_as_tsv_lines(self):
        lf = self.lf_bytes()
        for name in TABLES:
            first, rest = lf[name].split(b'\n', 1)
            cases = {
                'CR in LF field': first + b'\n' + rest.replace(b'\t', b'\r\t', 1),
                'CR in CRLF field': crlf(first + b'\n'
                                        + rest.replace(b'\t', b'\r\t', 1)),
                'CR before CRLF end': crlf(lf[name])[:-2] + b'\r\r\n',
                'CRLF header, LF rows': first + b'\r\n' + rest,
                'LF header, CRLF rows': first + b'\n' + crlf(rest),
            }
            for case, data in cases.items():
                for stage in ('pre', 'post'):
                    with self.subTest(table=name, case=case, stage=stage):
                        self.assertLineRefusal(stage, lf, name, data)

    def test_empty_and_unterminated_tables_refuse_as_tsv_lines(self):
        lf = self.lf_bytes()
        for name in TABLES:
            for data in (b'', lf[name][:-1], crlf(lf[name])[:-2], crlf(lf[name])[:-1]):
                for stage in ('pre', 'post'):
                    with self.subTest(table=name, data=data, stage=stage):
                        self.assertLineRefusal(stage, lf, name, data)

    def test_header_and_row_refusals_survive_crlf_normalization(self):
        lf = self.lf_bytes()
        for name, kind in (('req-a.tsv', 'requirements'), ('phase.tsv', 'phase-files')):
            header = lf[name].split(b'\n', 1)[0]
            for data, reason in (
                    (b'wrong\theader\n', 'does not start with the ' + kind + ' header'),
                    (header + b'\nshort\trow\n',
                     'has a row without %d fields' % len(header.split(b'\t')))):
                for ending in (data, crlf(data)):
                    with self.subTest(table=name, data=ending):
                        code, result = self.run_with('post', dict(lf, **{name: ending}))
                        self.assertEqual((code, result), (2, {
                            'status': 'UNVERIFIED',
                            'reason': str(fdsafe.Refusal(str(self.fx.path(name)), reason))}))


if __name__ == '__main__':
    unittest.main()
