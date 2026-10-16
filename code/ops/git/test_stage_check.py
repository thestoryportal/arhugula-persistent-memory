"""StageCheckRules: in-memory `-z` bytes, no Git (PLAN Step 101)."""
from __future__ import annotations

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
        failed = subprocess.CompletedProcess([], 128, stdout=b"", stderr=b"fatal: not a git repository")
        with mock.patch.object(S.subprocess, "run", return_value=failed), self.assertRaises(RuntimeError):
            S.run("/repo", ADMITTED)


if __name__ == "__main__":
    unittest.main()
