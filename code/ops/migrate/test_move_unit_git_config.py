"""move_unit run accepts the main checkout's two Git keys by exact value (Step 367, ruling R1).

The main checkout's .git/config holds core.hookspath=code/ops/git/hooks and extensions.worktreeconfig=true.
Each is allowed only with exactly that value: any other value of either key, every key refused before, and a
.git/config.worktree still refuse, naming the file and the key, with nothing moved or staged.
"""
from __future__ import annotations

import os
import shlex
import subprocess
import unittest

from ops.migrate.test_move_unit_run import Base, Fixture, clean_env, git

ALLOWED = (("core.hooksPath", "code/ops/git/hooks"), ("extensions.worktreeConfig", "true"))


class MainCheckoutKeys(Base):
    def setUp(self):
        super().setUp()
        allow(self.fx)

    def refuses(self, fx, path, key):
        self.fx = fx
        # [LAW:behavior-not-structure] Invalid config must preserve index bytes without asking Git to read it.
        with open(f"{fx.m}/.git/index", "rb") as fh:
            before = fh.read()
        self.assert_refused(self.main(*fx.args()), path, key)
        self.assert_unmoved(staged=False)
        with open(f"{fx.m}/.git/index", "rb") as fh:
            self.assertEqual(fh.read(), before)
        self.assert_sources_in_place()
        self.assertEqual(fx.custody_files(), [])

    def test_both_keys_with_their_exact_values_pass_and_no_hook_runs(self):
        marker = self.fx.base + "/hook-marker"
        hook = self.fx.put("m/code/ops/git/hooks/post-index-change",
                           ("#!/bin/sh\nprintf 'called\\n' >> " + shlex.quote(marker) + "\n").encode())
        os.chmod(hook, 0o755)
        result = self.run_ok()
        self.assertIn("git-mv", [action["action"] for action in result["actions"]])
        self.assertFalse(os.path.lexists(self.u.source))
        self.assertEqual(sorted(os.listdir(self.fx.target(self.u))), sorted(self.u.files))
        for rel, data in self.u.files.items():
            with open(os.path.join(self.fx.target(self.u), rel), "rb") as fh:
                self.assertEqual(fh.read(), data)
        self.assertFalse(os.path.exists(marker), "a hook ran during move_unit run")
        # [LAW:verifiable-goals] positive control: Git itself resolves the configured hooks path to this hook.
        subprocess.run(["git", "-C", self.fx.m, "hook", "run", "post-index-change", "--", "0", "0"],
                       env=clean_env(), check=True, capture_output=True)
        with open(marker, "rb") as fh:
            self.assertEqual(fh.read(), b"called\n")

    def test_any_other_value_of_either_key_refuses(self):
        for key, value in (("core.hooksPath", "/elsewhere"), ("core.hooksPath", "code/ops/git/hooks/"),
                           ("core.hooksPath", "./code/ops/git/hooks"), ("core.hooksPath", "Code/ops/git/hooks"),
                           ("core.hooksPath", ""), ("extensions.worktreeConfig", "True"),
                           ("extensions.worktreeConfig", "yes"), ("extensions.worktreeConfig", "1"),
                           ("extensions.worktreeConfig", "false"), ("extensions.worktreeConfig", ""),
                           ("extensions.worktreeConfig", "true\n"), ("core.hooksPath", " code/ops/git/hooks")):
            with self.subTest(key=key, value=value):
                fx = Fixture(self.tmp)
                allow(fx)
                git(fx.m, "config", key, value)  # replaces the allowed value
                self.refuses(fx, f"{fx.m}/.git/config", key.lower())

    def test_a_second_record_of_an_allowed_key_with_another_value_refuses(self):
        for key, value in (("core.hooksPath", "/elsewhere"), ("extensions.worktreeConfig", "false")):
            with self.subTest(key=key):
                fx = Fixture(self.tmp)
                allow(fx)
                git(fx.m, "config", "--add", key, value)
                self.refuses(fx, f"{fx.m}/.git/config", key.lower())

    def test_a_valueless_or_multiline_value_refuses(self):
        for text, key in ((b"[core]\n\thooksPath\n", "core.hookspath"),
                          (b"[extensions]\n\tworktreeConfig\n", "extensions.worktreeconfig"),
                          (b'[core]\n\thooksPath = "code/ops/git/hooks\\n"\n', "core.hookspath")):
            with self.subTest(key=key):
                fx = Fixture(self.tmp)
                allow(fx)
                with open(f"{fx.m}/.git/config", "ab") as fh:
                    fh.write(text)
                self.refuses(fx, f"{fx.m}/.git/config", key)

    def test_every_key_refused_before_still_refuses_beside_the_allowed_keys(self):
        for key, value in (("include.path", "/elsewhere"), ("includeIf.gitdir:/x/.path", "/elsewhere"),
                           ("core.fsmonitor", "/bin/true"), ("core.sshCommand", "/bin/true"),
                           ("extensions.partialClone", "origin"), ("remote.origin.promisor", "true"),
                           ("remote.origin.partialclonefilter", "blob:none"), ("filter.x.clean", "cat")):
            with self.subTest(key=key):
                fx = Fixture(self.tmp)
                allow(fx)
                git(fx.m, "config", key, value)
                self.refuses(fx, f"{fx.m}/.git/config", key.lower())

    def test_config_worktree_still_refuses_with_worktree_config_on(self):
        path = self.fx.put(os.path.join(self.fx.m, ".git", "config.worktree"), b"[core]\n\tfsmonitor = x\n")
        self.assert_refused(self.main(*self.fx.args()), path, "second config")
        self.assert_unmoved()
        self.assert_sources_in_place()
        self.assertEqual(self.fx.custody_files(), [])


def allow(fx: Fixture) -> None:
    """Set the main checkout's two keys, with their exact values, in fx's config."""
    for key, value in ALLOWED:
        git(fx.m, "config", key, value)


if __name__ == "__main__":
    unittest.main()
