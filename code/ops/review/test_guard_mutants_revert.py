"""Tests for guard_mutants' revert-file mutant: with --base REV, a changed file is put back to its bytes at REV.

Each lane is a temp git repo made by the test and removed by addCleanup; no real lane,
branch or PR is touched. The tool runs as a subprocess with cwd = the temp repo.
Rows are selected by operator == "revert-file"; the fixture modules have no guard, so other
operator modules add no row to a run that must exit 0.
"""
from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard_mutants.py")
PY = os.path.abspath(sys.executable)

BASE = "A = 0\nB = 0\nVALUE = 1\nC = 0\nD = 0\n"
EDITED = "A = 0\nB = 0\nVALUE = 2\nC = 0\nD = 9\n"  # two hunks, lines 3 and 5: the anchor is line 3
CHECKS = f'{PY} -B -c "import m; assert m.VALUE == 2"'  # fails when m.py is put back to BASE
GUARDED = "def f(n):\n    if n:\n        raise ValueError(n)\n    return n\n"
SHORT = 12  # hex digits of the resolved commit in the change text


def git_env() -> dict:
    """The env without GIT_* (a hook's GIT_DIR or GIT_INDEX_FILE would aim git at another repo)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return env


class RevertFile(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="gm-revert-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.lane = os.path.join(self.tmp, "lane")
        self.tooltmp = os.path.join(self.tmp, "tooltmp")
        os.mkdir(self.lane)
        os.mkdir(self.tooltmp)
        self.n = 0
        self.git("init", "-q")
        self.write("m.py", BASE)
        self.git("add", "m.py")
        self.git("commit", "-q", "-m", "base")
        self.base_sha = self.git("rev-parse", "HEAD").strip()

    def git(self, *args: str) -> str:
        proc = subprocess.run(["git", *args], cwd=self.lane, env=git_env(), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def write(self, rel: str, text: str) -> None:
        with open(os.path.join(self.lane, rel), "w") as fh:
            fh.write(text)

    def run_tool(self, *extra: str, files=("m.py",), test=CHECKS, env_extra=None, cwd=None):
        self.n += 1
        out = os.path.join(self.tmp, f"out{self.n}.json")
        argv = [a for f in files for a in ("--file", f)] + ["--test", test, "--out", out, *extra]
        env = dict(git_env(), TMPDIR=self.tooltmp, **(env_extra or {}))
        env.pop("PYTHONPATH", None)
        proc = subprocess.run([PY, "-B", TOOL, *argv], cwd=cwd or self.lane, env=env,
                              capture_output=True, text=True, timeout=240)
        self.assertEqual(os.listdir(self.tooltmp), [], "the tool left its scratch directory")
        return proc, out

    def rows(self, *extra: str, code: int, **kw) -> tuple[list[dict], str]:
        """All rows of a run that exits code, and its stdout."""
        proc, out = self.run_tool(*extra, **kw)
        self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)
        with open(out) as fh:
            return json.load(fh), proc.stdout

    def reverts(self, *extra: str, code: int, **kw) -> list[dict]:
        return [r for r in self.rows(*extra, code=code, **kw)[0] if r["operator"] == "revert-file"]

    def row(self, rel: str, line: int, result: str, rev: str = "HEAD", sha: str | None = None,
            allowed: str | None = None) -> dict:
        return {"id": f"{rel}:{line}:0:revert-file", "location": f"{rel}:{line}", "operator": "revert-file",
                "change": f"file -> {rev} {(sha or self.base_sha)[:SHORT]}", "result": result,
                "detail": "exit 0" if result == "survived" else "exit 1", "allowed": allowed}

    # (1) (2) a change that the test checks: the file put back to REV fails the test
    def test_checked_change_gives_a_killed_revert_file(self):
        self.write("m.py", EDITED)
        self.assertEqual(self.reverts("--base", "HEAD", code=0), [self.row("m.py", 3, "killed")])

    def test_source_is_the_bytes_at_rev(self):
        """The test fails (kills) exactly when m.py in the copy holds BASE's bytes."""
        self.write("m.py", EDITED)
        copy = os.path.join(self.tmp, "base-bytes")
        with open(copy, "w") as fh:
            fh.write(BASE)
        test = f"! cmp -s m.py {shlex.quote(copy)}"
        self.assertEqual(self.reverts("--base", "HEAD", code=0, test=test), [self.row("m.py", 3, "killed")])

    # a change that the test does not exercise: a survivor, reported like any other
    def test_unexercised_change_survives_and_is_reported(self):
        self.write("m.py", EDITED)
        rows, stdout = self.rows("--base", "HEAD", code=1, test="true")
        reverts = [r for r in rows if r["operator"] == "revert-file"]
        self.assertEqual(reverts, [self.row("m.py", 3, "survived")])
        self.assertIn(f"survived m.py:3:0:revert-file: file -> HEAD {self.base_sha[:SHORT]} [exit 0]\n", stdout)

    def test_rev_text_as_given_and_the_resolved_commit(self):
        self.write("m.py", EDITED)
        self.git("commit", "-q", "-am", "edit")
        self.assertEqual(self.reverts("--base", "HEAD~1", code=0),
                         [self.row("m.py", 3, "killed", rev="HEAD~1", sha=self.base_sha)])
        self.assertEqual(self.reverts("--base", "HEAD", code=0), [])  # no changed line against HEAD

    def test_anchor_is_the_first_changed_line(self):
        self.write("m.py", "A = 0\nB = 0\nVALUE = 2\nC = 0\nD = 0\nE = 0\n")  # changed lines 3 and 6
        self.assertEqual(self.reverts("--base", "HEAD", code=0), [self.row("m.py", 3, "killed")])
        self.write("m.py", "A = 7\nB = 0\nVALUE = 2\nC = 0\nD = 0\n")  # lines 1 and 3
        self.assertEqual(self.reverts("--base", "HEAD", code=0), [self.row("m.py", 1, "killed")])

    # (3) a file new since REV gives no revert-file id (it is in scope as a whole)
    def test_file_absent_at_rev_gives_no_revert_file(self):
        self.write("m.py", EDITED)
        self.write("new.py", "X = 1\n")
        files = ("m.py", "new.py")
        self.assertEqual(self.reverts("--base", "HEAD", code=0, files=files), [self.row("m.py", 3, "killed")])
        self.git("add", "new.py")  # staged, still not at REV
        self.assertEqual(self.reverts("--base", "HEAD", code=0, files=files), [self.row("m.py", 3, "killed")])
        self.assertEqual(self.reverts("--base", "HEAD", code=0, files=("new.py",), test="true"), [])

    def test_pure_deletion_gives_no_revert_file(self):
        self.write("m.py", BASE.replace("D = 0\n", ""))
        self.assertIn("@@ -5 +4,0 @@", self.git("diff", "-U0", "HEAD", "--", "m.py"))
        self.assertEqual(self.reverts("--base", "HEAD", code=0, test="true"), [])

    def test_lane_below_the_repo_top_reads_its_own_file(self):
        sub = os.path.join(self.lane, "sub")
        os.mkdir(sub)
        sub_base = BASE + "# sub\n"  # differs from the top-level m.py at REV
        self.write("sub/m.py", sub_base)
        self.git("add", "sub/m.py")
        self.git("commit", "-q", "-m", "sub")
        sha = self.git("rev-parse", "HEAD").strip()
        self.write("sub/m.py", EDITED)
        copy = os.path.join(self.tmp, "sub-base-bytes")
        with open(copy, "w") as fh:
            fh.write(sub_base)
        self.assertEqual(self.reverts("--base", "HEAD", code=0, cwd=sub, test=f"! cmp -s m.py {shlex.quote(copy)}"),
                         [self.row("m.py", 3, "killed", sha=sha)])

    # (4) a run without --base has no revert-file id
    def test_without_base_no_revert_file(self):
        self.write("m.py", EDITED)
        self.assertEqual(self.rows(code=0, test="true")[0], [])

    # (6) an allow entry for the id passes; the allow file knows the id only when it is made
    def test_allow_entry_for_the_id_passes(self):
        self.write("m.py", EDITED)
        allow = os.path.join(self.tmp, "allow.json")
        with open(allow, "w") as fh:
            json.dump([{"id": "m.py:3:0:revert-file", "reason": "VALUE is not checked here"}], fh)
        rows, stdout = self.rows("--base", "HEAD", "--allow", allow, code=0, test="true")
        self.assertEqual([r for r in rows if r["operator"] == "revert-file"],
                         [self.row("m.py", 3, "survived", allowed="VALUE is not checked here")])
        self.assertIn(" 1 allowed; wrote ", stdout)
        proc, out = self.run_tool("--allow", allow, test="true")  # no --base: no such mutant
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("lists m.py:3:0:revert-file, which is no mutant of these files", proc.stderr)
        self.assertFalse(os.path.lexists(out))

    def test_revert_file_follows_its_files_operator_mutants(self):
        self.write("g.py", GUARDED)
        self.git("add", "g.py")
        self.git("commit", "-q", "-m", "g")
        sha = self.git("rev-parse", "HEAD").strip()
        self.write("g.py", GUARDED.replace("if n:", "if n > 1:").replace("ValueError", "KeyError"))
        self.write("m.py", "A = 0\nB = 0\nVALUE = 3\nC = 0\nD = 0\n")
        rows, _ = self.rows("--base", "HEAD", code=1, files=("g.py", "m.py"), test="true")
        rels = [r["location"].split(":")[0] for r in rows]
        self.assertEqual(rels, sorted(rels, key=("g.py", "m.py").index))  # each file's rows together
        for rel, line in (("g.py", 2), ("m.py", 3)):
            mine = [r for r in rows if r["location"].split(":")[0] == rel]
            self.assertGreater(len(mine), 1 if rel == "g.py" else 0)
            self.assertEqual(mine[-1], self.row(rel, line, "survived", sha=sha))
            self.assertEqual([r for r in mine if r["operator"] == "revert-file"], [mine[-1]])

    # (5) a git failure while reading REV bytes refuses (exit 2), naming the command
    def stand_in_git(self, body: str) -> dict:
        real = shutil.which("git", path=git_env()["PATH"])
        self.assertIsNotNone(real)
        fake = os.path.join(self.tmp, "fakebin")
        os.mkdir(fake)
        with open(os.path.join(fake, "git"), "w") as fh:
            fh.write(f"#!/bin/sh\n{body}\nexec {shlex.quote(real)} \"$@\"\n")
        os.chmod(os.path.join(fake, "git"), 0o755)
        return {"PATH": fake + os.pathsep + git_env()["PATH"]}

    def test_cat_file_failure_refuses_naming_the_command(self):
        self.write("m.py", EDITED)
        env = self.stand_in_git('if [ "$1" = cat-file ] && [ "$2" = blob ]; then echo "fatal: no blob" >&2; exit 7; fi')
        proc, out = self.run_tool("--base", "HEAD", env_extra=env)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertEqual(proc.stderr, f"guard_mutants: refused: `git cat-file blob {self.base_sha}:./m.py` failed "
                                      "(exit 7): fatal: no blob\n")
        self.assertFalse(os.path.lexists(out))

    def test_rev_bytes_read_once_per_file_before_any_test_run(self):
        self.write("m.py", EDITED)
        self.write("n.py", BASE)
        self.git("add", "n.py")
        self.git("commit", "-q", "-m", "n")
        self.write("n.py", EDITED)
        log = os.path.join(self.tmp, "calls.log")
        env = self.stand_in_git(f'echo "git $*" >> {shlex.quote(log)}')
        test = f'echo test >> {shlex.quote(log)}; {PY} -B -c "import m, n; assert m.VALUE == n.VALUE == 2"'
        self.assertEqual(len(self.reverts("--base", "HEAD", code=0, files=("m.py", "n.py"), test=test,
                                          env_extra=env)), 2)
        with open(log) as fh:
            calls = fh.read().splitlines()
        blobs = [c for c in calls if c.startswith("git cat-file blob ")]
        sha = self.git("rev-parse", "HEAD").strip()
        self.assertEqual(blobs, [f"git cat-file blob {sha}:./m.py", f"git cat-file blob {sha}:./n.py"])
        first_test = calls.index("test")
        self.assertTrue(all(c == "test" for c in calls[first_test:]), calls)  # no git call after a copy ran


if __name__ == "__main__":
    unittest.main()
