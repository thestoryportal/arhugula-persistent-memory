"""StageCheckRules: in-memory `-z` bytes, no Git (PLAN Step 101)."""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import unittest
from unittest import mock

import stage_check as S

ADMITTED = "R100\ta/moved.md\tb/moved.md\nD\tgone.md\nM\ta/reader.md\nA\trec/new.json\n"
STAGED = b"R100\0a/moved.md\0b/moved.md\0D\0gone.md\0M\0a/reader.md\0A\0rec/new.json\0"


def check(admitted_text: str, raw: bytes):
    return S.compare(S.parse_admitted(admitted_text), S.parse_staged(raw))


class StageCheckRules(unittest.TestCase):
    def test_exact_list_passes(self):
        self.assertEqual(check(ADMITTED, STAGED), ([], []))
        staged = S.parse_staged(STAGED)
        self.assertIn(("R100", "a/moved.md", "b/moved.md"), staged)
        self.assertIn(("D", "gone.md"), staged)
        # -z keeps tabs and quotes in paths exact.
        self.assertEqual(check('M\twe"ird name.md\n', b'M\0we"ird name.md\0'), ([], []))

    def test_missing_row_fails(self):
        missing, extra = check(ADMITTED, b"R100\0a/moved.md\0b/moved.md\0M\0a/reader.md\0A\0rec/new.json\0")
        self.assertEqual(missing, [("D", "gone.md")])
        self.assertEqual(extra, [])
        self.assertEqual(S.format_row(missing[0]), "D\tgone.md")

    def test_extra_row_fails(self):
        missing, extra = check(ADMITTED, STAGED + b"A\0stray.txt\0")
        self.assertEqual(missing, [])
        self.assertEqual(extra, [("A", "stray.txt")])

    def test_partial_rename_fails(self):
        raw = STAGED.replace(b"R100\0", b"R087\0")
        missing, extra = check(ADMITTED, raw)
        self.assertEqual(missing, [("R100", "a/moved.md", "b/moved.md")])
        self.assertEqual(extra, [("R087", "a/moved.md", "b/moved.md")])
        # An admitted list can never accept a rename below R100.
        with self.assertRaises(ValueError):
            S.parse_admitted("R087\ta/moved.md\tb/moved.md\n")

    def test_unadmitted_modify_fails(self):
        missing, extra = check(ADMITTED, STAGED + b"M\0code/other.py\0")
        self.assertEqual(missing, [])
        self.assertEqual(extra, [("M", "code/other.py")])

    def test_malformed_admitted_rejected(self):
        bad = {
            "unknown status": "T\tx.md\n",
            "bare R": "R\ta\tb\n",
            "rename below R100": "R099\ta\tb\n",
            "copy": "C100\ta\tb\n",
            "too few fields": "R100\ta\n",
            "too many fields": "D\ta\tb\n",
            "empty path": "M\t\n",
            "duplicate row": "D\tx.md\nD\tx.md\n",
            "path in two rows": "D\tx.md\nM\tx.md\n",
            "rename source reused": "R100\tx.md\ty.md\nD\tx.md\n",
            "rename onto itself": "R100\tx.md\tx.md\n",
            "spaces not tabs": "D x.md\n",
        }
        for name, text in bad.items():
            with self.subTest(name), self.assertRaises(ValueError):
                S.parse_admitted(text)
        for name, raw in {"truncated record": b"R100\0a\0", "no terminator": b"M\0x.md",
                          "unknown status": b"Z\0x.md\0"}.items():
            with self.subTest(name), self.assertRaises(ValueError):
                S.parse_staged(raw)

    def test_git_env_stripped(self):
        env = {"GIT_DIR": "/elsewhere/.git", "GIT_WORK_TREE": "/elsewhere",
               "GIT_INDEX_FILE": "/elsewhere/index", "PATH": os.environ.get("PATH", "")}
        done = subprocess.CompletedProcess([], 0, stdout=STAGED, stderr=b"")
        with mock.patch.dict(os.environ, env), \
                mock.patch.object(S.subprocess, "run", return_value=done) as run:
            result = S.run("/repo", ADMITTED)
        self.assertEqual(result, {"ok": True, "missing": [], "extra": []})
        self.assertEqual(run.call_count, 1)
        args, kwargs = run.call_args
        argv = args[0] if args else kwargs["args"]
        self.assertEqual(list(argv), ["git", "-C", "/repo", "diff", "--cached", "--name-status", "-M", "-z"])
        self.assertIsNotNone(kwargs.get("env"))
        self.assertEqual([k for k in kwargs["env"] if k.startswith("GIT_")], [])
        self.assertEqual(kwargs["env"]["PATH"], env["PATH"])

    def test_run_reports_named_rows_and_fails_closed(self):
        done = subprocess.CompletedProcess([], 0, stdout=STAGED.replace(b"R100\0", b"R087\0"), stderr=b"")
        with mock.patch.object(S.subprocess, "run", return_value=done):
            result = S.run("/repo", ADMITTED)
        self.assertEqual(result, {"ok": False, "missing": ["R100\ta/moved.md\tb/moved.md"],
                                  "extra": ["R087\ta/moved.md\tb/moved.md"]})
        # Each side alone is enough to fail.
        only_extra = subprocess.CompletedProcess([], 0, stdout=STAGED + b"A\0stray.txt\0", stderr=b"")
        with mock.patch.object(S.subprocess, "run", return_value=only_extra):
            self.assertEqual(S.run("/repo", ADMITTED), {"ok": False, "missing": [], "extra": ["A\tstray.txt"]})
        only_missing = subprocess.CompletedProcess([], 0, stdout=b"", stderr=b"")
        with mock.patch.object(S.subprocess, "run", return_value=only_missing):
            self.assertEqual(S.run("/repo", "D\tgone.md\n"), {"ok": False, "missing": ["D\tgone.md"], "extra": []})
        failed = subprocess.CompletedProcess([], 128, stdout=b"", stderr=b"fatal: not a git repository")
        with mock.patch.object(S.subprocess, "run", return_value=failed), self.assertRaises(RuntimeError):
            S.run("/repo", ADMITTED)
        # An invalid admitted row raises even when the staged index is empty.
        with mock.patch.object(S.subprocess, "run", return_value=only_missing), self.assertRaises(ValueError):
            S.run("/repo", "T\tx.md\n")

    def main_with(self, admitted_text: str, proc: subprocess.CompletedProcess, argv=None):
        argv = ["--repo", "/repo", "--admitted", "/admitted.tsv"] if argv is None else argv
        out, err = io.StringIO(), io.StringIO()
        with mock.patch("builtins.open", mock.mock_open(read_data=admitted_text)), \
                mock.patch.object(S.subprocess, "run", return_value=proc), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = S.main(argv)
        return code, out.getvalue()

    def test_main_exit_and_json(self):
        match = subprocess.CompletedProcess([], 0, stdout=STAGED, stderr=b"")
        code, out = self.main_with(ADMITTED, match)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"ok": True, "missing": [], "extra": []})

        mismatch = subprocess.CompletedProcess([], 0, stdout=STAGED.replace(b"R100\0", b"R087\0"), stderr=b"")
        code, out = self.main_with(ADMITTED, mismatch)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out), {"ok": False, "missing": ["R100\ta/moved.md\tb/moved.md"],
                                           "extra": ["R087\ta/moved.md\tb/moved.md"]})

        code, out = self.main_with("T\tx.md\n", match)
        self.assertEqual((code, out), (2, ""))
        failed = subprocess.CompletedProcess([], 128, stdout=b"", stderr=b"fatal: not a git repository")
        code, out = self.main_with(ADMITTED, failed)
        self.assertEqual((code, out), (2, ""))

        for name, argv in {"no --repo": ["--admitted", "/admitted.tsv"], "no --admitted": ["--repo", "/repo"]}.items():
            with self.subTest(name), self.assertRaises(SystemExit):
                self.main_with(ADMITTED, match, argv)

    def test_staged_parser_refusals(self):
        bad = {
            "unterminated trailing record": b"D\0x\0M",
            "non-numeric rename score": b"Rab\0a\0b\0",
            "non-numeric copy score": b"Cxx\0a\0b\0",
            "empty path": b"M\0\0",
            "empty rename destination": b"R100\0a\0\0",
            "invalid UTF-8": b"M\0\xff\0",
        }
        for name, raw in bad.items():
            with self.subTest(name), self.assertRaises(ValueError):
                S.parse_staged(raw)


if __name__ == "__main__":
    unittest.main()
