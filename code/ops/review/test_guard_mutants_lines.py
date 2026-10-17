"""Tests for guard_mutants --base: only guards on lines that differ from REV are mutated.

Each lane is a temp git repo made by the test and removed by addCleanup; no real lane,
branch or PR is touched. The tool runs as a subprocess with cwd = the temp repo.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard_mutants.py")

MODULE = '''\
import os


def a(n):
    if n < 0:
        raise ValueError("a")
    return n


def b(n):
    if n > 9:
        raise ValueError("b")
    return n


def c(text):
    try:
        return int(text)
    except ValueError:
        return None


LIMIT = 3
'''
F = "pkg/guarded.py"
# Every mutant of MODULE, by id: what a run without --base generates.
ALL_IDS = {
    f"{F}:5:4:negate-if",
    f"{F}:6:8:raise-remove",
    f"{F}:11:4:negate-if",
    f"{F}:12:8:raise-remove",
    f"{F}:19:4:except-class",
    f"{F}:19:4:except-remove",
}
NEW = '''\
def d(n):
    if n == 4:
        raise KeyError(n)
    return n
'''
NEW_IDS = {"pkg/new.py:2:4:negate-if", "pkg/new.py:3:8:raise-remove"}


def git_env() -> dict:
    """The env without GIT_* (a hook's GIT_DIR or GIT_INDEX_FILE would aim git at another repo)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return env


class Lines(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="gm-lines-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.lane = os.path.join(self.tmp, "lane")
        self.tooltmp = os.path.join(self.tmp, "tooltmp")
        os.makedirs(os.path.join(self.lane, "pkg"))
        os.mkdir(self.tooltmp)
        self.n = 0
        self.git("init", "-q")
        self.write(F, MODULE)
        self.git("add", F)
        self.git("commit", "-q", "-m", "base")

    def git(self, *args: str, cwd: str | None = None) -> str:
        proc = subprocess.run(["git", *args], cwd=cwd or self.lane, env=git_env(), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def write(self, rel: str, text: str) -> None:
        with open(os.path.join(self.lane, rel), "w") as fh:
            fh.write(text)

    def edit(self, old: str, new: str, rel: str = F) -> None:
        with open(os.path.join(self.lane, rel)) as fh:
            text = fh.read()
        self.assertEqual(text.count(old), 1, old)
        self.write(rel, text.replace(old, new))

    def run_tool(self, *extra: str, files=(F,), env_extra=None) -> tuple[subprocess.CompletedProcess, str]:
        self.n += 1
        out = os.path.join(self.tmp, f"out{self.n}.json")
        argv = [a for f in files for a in ("--file", f)] + ["--test", "true", "--out", out, *extra]
        env = dict(git_env(), TMPDIR=self.tooltmp, **(env_extra or {}))
        env.pop("PYTHONPATH", None)
        proc = subprocess.run([sys.executable, "-B", TOOL, *argv], cwd=self.lane, env=env,
                              capture_output=True, text=True, timeout=240)
        self.assertEqual(os.listdir(self.tooltmp), [], "the tool left its scratch directory")
        return proc, out

    def ids(self, *extra: str, files=(F,), code: int = 1, env_extra=None) -> set[str]:
        proc, out = self.run_tool(*extra, files=files, env_extra=env_extra)
        self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)
        with open(out) as fh:
            rows = json.load(fh)
        for r in rows:  # the row shape is unchanged
            self.assertEqual(set(r), {"id", "location", "operator", "change", "result", "detail", "allowed"})
            self.assertEqual(r["result"], "survived")  # `true` kills nothing
            self.assertEqual(r["location"], ":".join(r["id"].split(":")[:2]))
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertIn(f"guard_mutants: {len(rows)} mutants, 0 killed, {len(rows)} survived, 0 error, 0 allowed; "
                      f"wrote {out}", proc.stdout)
        return {r["id"] for r in rows if r["operator"] != "revert-file"}

    def refused(self, *extra: str, files=(F,), env_extra=None) -> str:
        proc, out = self.run_tool(*extra, files=files, env_extra=env_extra)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertTrue(proc.stderr.startswith("guard_mutants: refused: "), proc.stderr)
        self.assertEqual(len(proc.stderr.strip().splitlines()), 1, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertFalse(os.path.lexists(out))
        return proc.stderr

    # (6) without --base the generated set is today's
    def test_without_base_every_guard_is_mutated(self):
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        self.assertEqual(self.ids(), ALL_IDS)

    # (1) an uncommitted edit to one guard line: only mutants anchored on that line
    def test_uncommitted_edit_mutates_only_that_line(self):
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        self.assertEqual(self.ids("--base", "HEAD"), {f"{F}:12:8:raise-remove"})

    def test_two_line_hunk_covers_both_lines(self):
        self.edit('    if n > 9:\n        raise ValueError("b")', '    if n > 8:\n        raise KeyError("b")')
        self.assertEqual(self.ids("--base", "HEAD"), {f"{F}:11:4:negate-if", f"{F}:12:8:raise-remove"})

    def test_except_line_edit_gives_both_except_mutants(self):
        self.edit("except ValueError:", "except (ValueError, TypeError):")
        self.assertEqual(self.ids("--base", "HEAD"), {f"{F}:19:4:except-class", f"{F}:19:4:except-remove"})

    def test_committed_edit_counts_against_an_older_rev(self):
        self.edit('raise ValueError("a")', 'raise ValueError("aa")')
        self.git("commit", "-q", "-am", "edit a")
        self.assertEqual(self.ids("--base", "HEAD~1"), {f"{F}:6:8:raise-remove"})
        self.assertEqual(self.ids("--base", "HEAD", code=0), set())

    # (2) a guard on an unchanged line is not generated, though it would survive
    def test_unchanged_guard_is_not_generated_though_it_survives(self):
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        whole = self.ids()
        self.assertIn(f"{F}:6:8:raise-remove", whole)  # it survives `true` when generated
        scoped = self.ids("--base", "HEAD")
        self.assertNotIn(f"{F}:6:8:raise-remove", scoped)
        self.assertEqual(whole - scoped, ALL_IDS - {f"{F}:12:8:raise-remove"})

    def test_pure_deletion_adds_no_line(self):
        # The hunk is "@@ -7 +6,0 @@": line 6 (a guard) is only its position, not a changed line.
        self.edit('raise ValueError("a")\n    return n\n', 'raise ValueError("a")\n')
        self.assertIn("@@ -7 +6,0 @@", self.git("diff", "-U0", "HEAD", "--", F))
        self.assertEqual(self.ids("--base", "HEAD", code=0), set())
        shifted = {i.replace(":11:4:", ":10:4:").replace(":12:8:", ":11:8:").replace(":19:4:", ":18:4:")
                   for i in ALL_IDS}
        self.assertEqual(self.ids(), shifted)

    # (3) a file untracked at REV is mutated as a whole, with the ids of a run without --base
    def test_file_absent_at_rev_is_mutated_whole(self):
        self.write("pkg/new.py", NEW)
        files = (F, "pkg/new.py")
        self.assertEqual(self.ids(files=("pkg/new.py",)), NEW_IDS)
        self.assertEqual(self.ids("--base", "HEAD", files=files), NEW_IDS)  # guarded.py is unchanged
        self.git("add", "pkg/new.py")  # staged, still not at REV
        self.assertEqual(self.ids("--base", "HEAD", files=files), NEW_IDS)

    # (4) an edit on a line with no guard: an empty list and exit 0
    def test_edit_without_guard_writes_empty_list_and_exits_0(self):
        self.edit("LIMIT = 3", "LIMIT = 4")
        proc, out = self.run_tool("--base", "HEAD")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        with open(out) as fh:
            self.assertEqual(json.load(fh), [{"id": f"{F}:23:0:revert-file", "location": f"{F}:23", "operator": "revert-file", "change": "file -> HEAD " + self.git("rev-parse", "HEAD")[:12], "result": "survived", "detail": "exit 0", "allowed": None}])
        self.assertIn(f"guard_mutants: 1 mutants, 0 killed, 1 survived, 0 error, 0 allowed; wrote {out}", proc.stdout)

    # (5) an unknown REV exits 2 and names the git command and its stderr
    def test_unknown_rev_refuses_naming_the_command(self):
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        err = self.refused("--base", "no-such-rev")
        self.assertIn("git rev-parse", err)
        self.assertIn("no-such-rev", err)
        self.assertIn("fatal:", err)

    def test_outside_a_repo_refuses(self):
        shutil.move(os.path.join(self.lane, ".git"), os.path.join(self.tmp, "moved.git"))
        err = self.refused("--base", "HEAD")
        self.assertIn("git rev-parse", err)

    def test_ambient_git_dir_is_not_used(self):
        """A hook's GIT_DIR naming another repo must not decide the scope: git is asked about the lane."""
        other = os.path.join(self.tmp, "other")
        os.mkdir(other)
        self.git("init", "-q", cwd=other)
        self.git("commit", "-q", "--allow-empty", "-m", "x", cwd=other)
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        got = self.ids("--base", "HEAD", env_extra={"GIT_DIR": os.path.join(other, ".git")})
        self.assertEqual(got, {f"{F}:12:8:raise-remove"})

    def test_skip_worktree_file_refuses(self):
        """git diff does not look at a skip-worktree file's edits: its scope cannot be known."""
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        self.git("update-index", "--skip-worktree", F)
        self.assertIn("git ls-files", self.refused("--base", "HEAD"))

    def test_assume_unchanged_file_refuses(self):
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        self.git("update-index", "--assume-unchanged", F)
        self.assertIn("git ls-files", self.refused("--base", "HEAD"))

    def test_file_at_rev_but_not_in_index_refuses(self):
        """git diff reports such a file deleted (no new-side line) although it is in the lane."""
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        self.git("rm", "-q", "--cached", F)
        self.assertIn("git ls-files", self.refused("--base", "HEAD"))

    def test_binary_diff_refuses(self):
        self.write(".gitattributes", "*.py -diff\n")
        self.git("add", ".gitattributes")
        self.git("commit", "-q", "-m", "attrs")
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        self.assertIn("git diff", self.refused("--base", "HEAD"))

    def test_glob_characters_in_a_file_name_are_literal(self):
        self.write("pkg/x*.py", NEW)
        self.write("pkg/xa.py", NEW)
        self.git("add", "pkg/x*.py", "pkg/xa.py")
        self.git("commit", "-q", "-m", "two")
        self.edit("raise KeyError(n)", "raise KeyError(n + 1)", rel="pkg/xa.py")
        self.assertEqual(self.ids("--base", "HEAD", files=("pkg/x*.py",), code=0), set())
        self.assertEqual(self.ids("--base", "HEAD", files=("pkg/xa.py",)), {"pkg/xa.py:3:8:raise-remove"})

    def test_lane_below_the_repo_top_names_its_files_from_the_lane(self):
        """--file is relative to the lane (cwd); git is asked about that same file, not a path at the repo top."""
        os.makedirs(os.path.join(self.lane, "sub", "pkg"))
        self.write("sub/pkg/only.py", NEW)  # no pkg/only.py at the repo top
        self.git("add", "sub/pkg/only.py")
        self.git("commit", "-q", "-m", "sub")
        self.edit("raise KeyError(n)", "raise KeyError(n + 1)", rel="sub/pkg/only.py")
        self.lane = os.path.join(self.lane, "sub")
        self.assertEqual(self.ids("--base", "HEAD", files=("pkg/only.py",)), {"pkg/only.py:3:8:raise-remove"})

    def test_git_that_cannot_run_refuses(self):
        empty = os.path.join(self.tmp, "nobin")
        os.mkdir(empty)
        err = self.refused("--base", "HEAD", env_extra={"PATH": empty})
        self.assertIn("git rev-parse", err)

    def test_unreadable_hunk_header_refuses(self):
        """A git whose diff prints a header the tool cannot read (a stand-in on PATH) is refused, not skipped.

        Each header has one digit group empty or wrong: a pattern that took an empty group would read it."""
        real = shutil.which("git", path=git_env()["PATH"])
        self.assertIsNotNone(real)
        fake = os.path.join(self.tmp, "fakebin")
        os.mkdir(fake)
        header = os.path.join(self.tmp, "header")
        with open(os.path.join(fake, "git"), "w") as fh:
            fh.write(f'#!/bin/sh\nif [ "$1" = diff ]; then cat "{header}"; printf "+a\\n"; exit 0; fi\n'
                     f'exec "{real}" "$@"\n')
        os.chmod(os.path.join(fake, "git"), 0o755)
        self.edit('raise ValueError("b")', 'raise ValueError("bee")')
        for bad in ("@@ -1 +x @@", "@@ - +12 @@", "@@ -1, +12 @@", "@@ -1 + @@", "@@ -1 +12, @@"):
            with self.subTest(header=bad):
                with open(header, "w") as fh:
                    fh.write(bad + "\n")
                err = self.refused("--base", "HEAD", env_extra={"PATH": fake + os.pathsep + git_env()["PATH"]})
                self.assertIn("hunk header it cannot read", err)
                self.assertIn(repr(bad.encode()), err)

if __name__ == "__main__":
    unittest.main()
