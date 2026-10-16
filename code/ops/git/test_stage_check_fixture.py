"""StageFixture: a temp-repo miniature stages real moves and runs stage_check on it (PLAN Step 102).

Every repository lives in a tempfile.TemporaryDirectory. Every Git call gets stage_check.git_env(),
so no inherited GIT_* variable can point it at the real repository or index. Nothing is committed
after staging.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import stage_check as S

MOVED = b"moved body\nunchanged by the move\n"
READER = b"reader line one\nreader line two\nreader line three\n"
REWRITTEN = b"reader line one\nreader line two, rewritten\nreader line three\n"
SEED_COMMIT = ["-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
               "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit"]


def sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class StageFixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = os.path.join(tmp.name, "repo")
        self.outside = os.path.join(tmp.name, "outside")
        os.makedirs(self.outside)
        # A HOME inside the temp dir keeps the user's global Git config out of the miniature.
        env = mock.patch.dict(os.environ, {"HOME": tmp.name, "XDG_CONFIG_HOME": tmp.name})
        env.start()
        self.addCleanup(env.stop)
        self.git("init", "-q", self.repo, cwd=tmp.name)
        self.write("a/moved.md", MOVED)
        self.write("a/reader.md", READER)
        self.git("add", "--", "a/moved.md", "a/reader.md")
        self.git(*SEED_COMMIT, "-q", "-m", "seed")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.count = self.git("rev-list", "--count", "HEAD").strip()
        self.assertEqual(self.count, "1")
        self.assertEqual(S.run(self.repo, ""), {"ok": True, "missing": [], "extra": []})

    def git(self, *args: str, cwd: str | None = None) -> str:
        env = S.git_env()
        self.assertEqual([k for k in env if k.startswith("GIT_")], [])
        argv = ["git", *args] if cwd else ["git", "-C", self.repo, *args]
        proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, check=False)
        self.assertEqual(proc.returncode, 0, f"{argv}: {proc.stderr.decode(errors='replace')}")
        return proc.stdout.decode("utf-8")

    def write(self, rel: str, data: bytes) -> None:
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

    def leaves(self) -> dict:
        found = {}
        for root, dirs, files in os.walk(self.repo):
            if root == self.repo:
                dirs.remove(".git")
            for name in files:
                path = os.path.join(root, name)
                found[os.path.relpath(path, self.repo).replace(os.sep, "/")] = sha256(path)
        return found

    def loose_objects(self) -> int:
        objects = os.path.join(self.repo, ".git", "objects")
        return sum(len(os.listdir(os.path.join(objects, d))) for d in os.listdir(objects)
                   if len(d) == 2 and all(c in "0123456789abcdef" for c in d))

    def stage_move_and_rewrite(self) -> None:
        os.makedirs(os.path.join(self.repo, "b"))  # git mv does not create the destination directory.
        self.git("mv", "a/moved.md", "b/moved.md")
        self.write("a/reader.md", REWRITTEN)
        self.git("add", "--", "a/reader.md")

    def assert_no_commit(self) -> None:
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.head)
        self.assertEqual(self.git("rev-list", "--count", "HEAD").strip(), self.count)

    def test_move_and_rewrite_pass_without_commit(self):
        before = self.leaves()
        self.assertEqual(before, {"a/moved.md": hashlib.sha256(MOVED).hexdigest(),
                                  "a/reader.md": hashlib.sha256(READER).hexdigest()})
        objects_before = self.loose_objects()
        self.stage_move_and_rewrite()

        result = S.run(self.repo, "R100\ta/moved.md\tb/moved.md\nM\ta/reader.md\n")
        self.assertEqual(result, {"ok": True, "missing": [], "extra": []})
        self.assert_no_commit()
        # Staging the rewrite stores a new blob: Git's own objects grow without any commit.
        self.assertGreater(self.loose_objects(), objects_before)
        # Leaf conservation outside .git: every leaf sits at its admitted path with its expected bytes.
        self.assertEqual(self.leaves(), {"b/moved.md": before["a/moved.md"],
                                         "a/reader.md": hashlib.sha256(REWRITTEN).hexdigest()})

    def test_unadmitted_stage_fails(self):
        self.stage_move_and_rewrite()
        result = S.run(self.repo, "R100\ta/moved.md\tb/moved.md\n")
        self.assertEqual(result, {"ok": False, "missing": [], "extra": ["M\ta/reader.md"]})
        self.assert_no_commit()

    def test_removal_stages_as_d(self):
        digest = self.leaves()["a/moved.md"]
        shutil.move(os.path.join(self.repo, "a/moved.md"), os.path.join(self.outside, "moved.md"))
        self.git("rm", "-q", "--cached", "--", "a/moved.md")

        result = S.run(self.repo, "D\ta/moved.md\n")
        self.assertEqual(result, {"ok": True, "missing": [], "extra": []})
        self.assert_no_commit()
        self.assertEqual(self.leaves(), {"a/reader.md": hashlib.sha256(READER).hexdigest()})
        self.assertEqual(sha256(os.path.join(self.outside, "moved.md")), digest)


if __name__ == "__main__":
    unittest.main()
