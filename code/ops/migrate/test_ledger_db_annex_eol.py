"""T348: annex and plan readers share one LF-or-CRLF boundary."""
import os
import unittest

from ops.migrate import fdsafe, move_plan_core as core
from test_ledger_db import Fixture, REPORTS, readb
from test_move_plan_core_historical import Historical  # noqa: F401


class AnnexEndings(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture(self)

    def test_crlf_matches_lf_reports(self):
        fx = self.fx
        original = readb(fx.req)
        code, _, err = fx.run()
        self.assertEqual((code, err), (0, ""))
        expected = {name: readb(os.path.join(fx.out, name)) for name in REPORTS}
        fx.write(fx.req, original.replace(b"\n", b"\r\n"))
        other = os.path.join(fx.outp, "crlf")
        code, _, err = fx.run(fx.argv(out=other))
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(sorted(os.listdir(other)), sorted(REPORTS))
        self.assertEqual({name: readb(os.path.join(other, name)) for name in REPORTS}, expected)

    def refused(self, data, location, reason):
        fx = self.fx
        fx.write(fx.req, data)
        code, out, err = fx.run()
        self.assertEqual((code, out), (2, ""), err)
        self.assertEqual(err, f"ledger_db: refused: {location!r}: {reason}\n")
        self.assertFalse(os.path.lexists(fx.out))

    def test_mixed_first_line(self):
        fx = self.fx
        self.refused(readb(fx.req).replace(b"\n", b"\r\n", 1), fx.req + ":2",
                     "mixes LF and CRLF line endings")

    def test_mixed_later_line(self):
        fx = self.fx
        data = readb(fx.req)
        self.refused(data[:-1] + b"\r\n", fx.req + ":3", "mixes LF and CRLF line endings")

    def test_no_final_newline(self):
        fx = self.fx
        self.refused(readb(fx.req)[:-1], fx.req, "is empty or does not end with a newline")

    def test_crlf_preserves_last_action_field_cr_for_refusal(self):
        fx = self.fx
        rows = [line.split(b"\t") for line in readb(fx.req)[:-1].split(b"\n")]
        action = rows[0].index(b"action")
        for row in rows:
            row.append(row.pop(action))
        rows[1][-1] += b"\r"
        data = b"\r\n".join(b"\t".join(row) for row in rows) + b"\r\n"
        self.refused(data, fx.req + ":2", "holds a CR that is not part of a line end")

    def test_unread_columns_refuse_embedded_cr(self):
        fx = self.fx
        original = readb(fx.req)
        for ending in (b"\n", b"\r\n"):
            for column in ("target", "observed_bytes", "class", "lane", "check_id", "admission", "prd_ids"):
                with self.subTest(ending=ending, column=column):
                    rows = [line.split(b"\t") for line in original[:-1].split(b"\n")]
                    index = rows[0].index(column.encode())
                    rows[1][index] += b"\rx"
                    data = ending.join(b"\t".join(row) for row in rows) + ending
                    self.refused(data, fx.req + ":2", "holds a CR that is not part of a line end")


class TsvLines(unittest.TestCase):
    def test_lf(self):
        self.assertEqual(core.tsv_lines("a\tb\nc\td\n", "annex"), ["a\tb", "c\td"])

    def test_crlf(self):
        self.assertEqual(core.tsv_lines("a\tb\r\nc\td\r\n", "annex"), ["a\tb", "c\td"])

    def test_crlf_removes_exactly_one_line_end_cr(self):
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.tsv_lines("\ra\rb\r\r\n c\t\r\n", "annex")
        self.assertEqual(caught.exception.path, "annex:1")
        self.assertEqual(str(caught.exception), "'annex:1': holds a CR that is not part of a line end")

    def test_field_cr_is_left_for_the_field_parser(self):
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.tsv_lines("a\rb\n", "annex")
        self.assertEqual(caught.exception.path, "annex:1")
        self.assertEqual(str(caught.exception), "'annex:1': holds a CR that is not part of a line end")

    def test_embedded_cr_refusals(self):
        cases = (("\ra\r\n", "annex:1"), ("a\rb\r\n", "annex:1"),
                 ("a\r\r\n", "annex:1"), ("\ra\n", "annex:1"), ("a\rb\n", "annex:1"),
                 ("a\r\nb\rc\r\n", "annex:2"), ("a\nb\rc\n", "annex:2"))
        for text, path in cases:
            with self.subTest(text=text):
                with self.assertRaises(fdsafe.Refusal) as caught:
                    core.tsv_lines(text, "annex")
                self.assertEqual(caught.exception.path, path)
                self.assertEqual(str(caught.exception), f"{path!r}: holds a CR that is not part of a line end")

    def test_empty_line(self):
        self.assertEqual(core.tsv_lines("\n", "annex"), [""])

    def test_refusals(self):
        cases = (("", "annex", "is empty or does not end with a newline"),
                 ("a", "annex", "is empty or does not end with a newline"),
                 ("a\r\nb\n", "annex:2", "mixes LF and CRLF line endings"),
                 ("a\nb\nc\r\n", "annex:3", "mixes LF and CRLF line endings"),
                 ("a\r\nb\r\nc\n", "annex:3", "mixes LF and CRLF line endings"))
        for text, path, reason in cases:
            with self.subTest(text=text), self.assertRaises(fdsafe.Refusal) as caught:
                core.tsv_lines(text, "annex")
            self.assertEqual(caught.exception.path, path)
            self.assertEqual(str(caught.exception), f"{path!r}: {reason}")


if __name__ == "__main__":
    unittest.main()
