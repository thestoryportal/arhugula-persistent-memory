"""admitted_list: the exact stage_check rows for one unit plan (PLAN Step 208, A/H-SLICE.md:40-42).

Every repository lives in a tempfile.TemporaryDirectory. Every Git call gets stage_check.git_env(),
so no inherited GIT_* variable can point it at the real repository or index. Nothing is committed
after the seed commit.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import admitted_list as AL
from ops.git import stage_check as S

SEED_COMMIT = ["-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
               "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit"]


class Fixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = tmp.name
        self.repo = os.path.join(tmp.name, "repo")
        self.outside = os.path.join(tmp.name, "outside")
        os.makedirs(self.outside)
        # A HOME inside the temp dir keeps the user's global Git config out of the miniature.
        env = mock.patch.dict(os.environ, {"HOME": tmp.name, "XDG_CONFIG_HOME": tmp.name})
        env.start()
        self.addCleanup(env.stop)
        self.git("init", "-q", self.repo, cwd=tmp.name)
        self.seed({"a/dir/one.md": b"one\n", "a/dir/sub/two.md": b"two\n", "a/gone.md": b"gone\n",
                   "a/regen.md": b"regen v1\n", "a/keep.md": b"keep\n"})

    def seed(self, files: dict) -> None:
        for rel, data in files.items():
            self.write(rel, data)
        self.git("add", "--", *files)
        self.git(*SEED_COMMIT, "-q", "-m", "seed")

    def git(self, *args: str, cwd: str | None = None) -> str:
        argv = ["git", *args] if cwd else ["git", "-C", self.repo, *args]
        proc = subprocess.run(argv, cwd=cwd, env=S.git_env(), capture_output=True, check=False)
        self.assertEqual(proc.returncode, 0, f"{argv}: {proc.stderr.decode(errors='replace')}")
        return proc.stdout.decode("utf-8")

    def write(self, rel: str, data: bytes, root: str | None = None) -> str:
        path = os.path.join(root or self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        return path

    def run_cli(self, plan: dict, out: str | None = None) -> tuple:
        plan_path = os.path.join(self.tmp, "plan.json")
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump(plan, f)
        out = out or os.path.join(self.tmp, "admitted.tsv")
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            code = AL.main(["--repo", self.repo, "--plan", plan_path, "--out", out])
        os.remove(plan_path)
        text = None
        if os.path.lexists(out):
            with open(out, encoding="utf-8") as f:
                text = f.read()
        return code, text, err.getvalue()

    def assert_refused(self, plan: dict, code: int, needle: str) -> None:
        out = os.path.join(self.tmp, "admitted.tsv")
        got, text, err = self.run_cli(plan, out)
        self.assertEqual(got, code, err)
        self.assertIn(needle, err)
        self.assertIsNone(text, "a refused plan must write no admitted list")


class AdmittedRows(Fixture):
    def test_exact_rows_and_stage_check_passes_after_item5_staging(self):
        record = self.write("rec.json", b'{"record": 1}\n', root=self.outside)
        self.write("units/u1/retention.json", b'{"unit": "u1"}\n')
        self.write("junk/untracked.txt", b"junk\n")
        index_before = self.git("ls-files", "-s")
        status_before = self.git("status", "--porcelain", "--untracked-files=all")
        out = os.path.join(self.repo, "units/u1/admitted.tsv")
        plan = {"move": [{"src": "a/dir", "dst": "b/dir"}],
                "remove": ["a/gone.md"],
                "add": [{"dst": "records/rec.json", "src": record},
                        {"dst": "units/u1/retention.json"},
                        {"dst": "units/u1/admitted.tsv"}],
                "modify": ["a/regen.md"]}

        code, text, err = self.run_cli(plan, out)

        self.assertEqual(code, 0, err)
        self.assertEqual(text, "".join([
            "A\trecords/rec.json\n",
            "A\tunits/u1/admitted.tsv\n",
            "A\tunits/u1/retention.json\n",
            "D\ta/gone.md\n",
            "M\ta/regen.md\n",
            "R100\ta/dir/one.md\tb/dir/one.md\n",
            "R100\ta/dir/sub/two.md\tb/dir/sub/two.md\n",
        ]))
        self.assertEqual(len(S.parse_admitted(text)), 7)
        # The tool staged nothing and added nothing: index and untracked set are unchanged.
        self.assertEqual(self.git("ls-files", "-s"), index_before)
        self.assertEqual(sorted(self.git("status", "--porcelain", "--untracked-files=all").splitlines()),
                         sorted(status_before.splitlines() + ["?? units/u1/admitted.tsv"]))

        # H-SLICE item 5 staging, then the check: the written list is exactly what Git stages.
        os.makedirs(os.path.join(self.repo, "b"))
        self.git("mv", "a/dir", "b/dir")
        shutil.move(os.path.join(self.repo, "a/gone.md"), os.path.join(self.outside, "gone.md"))
        self.git("rm", "-q", "--cached", "--", "a/gone.md")
        os.makedirs(os.path.join(self.repo, "records"))
        shutil.move(record, os.path.join(self.repo, "records/rec.json"))
        self.write("a/regen.md", b"regen v2\n")
        self.git("add", "--", "records/rec.json", "units/u1/retention.json",
                 "units/u1/admitted.tsv", "a/regen.md")
        self.assertEqual(S.run(self.repo, text), {"ok": True, "missing": [], "extra": []})

    def test_untracked_move_emits_no_row_and_equal_bytes_on_one_side_pass(self):
        self.seed({"x/d1.md": b"same\n", "x/d2.md": b"same\n"})
        self.write("loose/u.md", b"untracked\n")
        self.write("new/a1.json", b"twin\n")
        self.write("new/a2.json", b"twin\n")
        plan = {"move": [{"src": "loose", "dst": "moved/loose"}],
                "remove": ["x/d1.md", "x/d2.md"],
                "add": [{"dst": "new/a1.json"}, {"dst": "new/a2.json"}]}
        code, text, err = self.run_cli(plan)
        self.assertEqual(code, 0, err)
        self.assertEqual(text, "A\tnew/a1.json\nA\tnew/a2.json\nD\tx/d1.md\nD\tx/d2.md\n")

    def test_symlink_record_is_hashed_as_its_link_text(self):
        self.write("target.md", b"gone\n", root=self.outside)
        os.symlink(os.path.join(self.outside, "target.md"), os.path.join(self.repo, "link.md"))
        # Followed, the link would equal a/gone.md and be refused; unfollowed it is its own link text.
        code, text, err = self.run_cli({"remove": ["a/gone.md"], "add": [{"dst": "link.md"}]})
        self.assertEqual(code, 0, err)
        self.assertEqual(text, "A\tlink.md\nD\ta/gone.md\n")


class PairingRefusals(Fixture):
    def test_git_pairs_equal_d_and_a_so_the_plan_is_refused(self):
        self.write("rec.json", b"gone\n")  # equal bytes to tracked a/gone.md
        plan = {"remove": ["a/gone.md"], "add": [{"dst": "rec.json"}]}
        self.assert_refused(plan, 1, "a/gone.md")
        # Positive control: Git really pairs them (A/H-SLICE.md:42 probe), so the D/A list would fail.
        shutil.move(os.path.join(self.repo, "a/gone.md"), os.path.join(self.outside, "gone.md"))
        self.git("rm", "-q", "--cached", "--", "a/gone.md")
        self.git("add", "--", "rec.json")
        self.assertEqual(S.run(self.repo, "D\ta/gone.md\nA\trec.json\n")["extra"],
                         ["R100\ta/gone.md\trec.json"])

    def test_identical_moves_are_refused(self):
        self.seed({"z/z1.md": b"twin\n", "z/z2.md": b"twin\n"})
        plan = {"move": [{"src": "z/z1.md", "dst": "y/y1.md"}, {"src": "z/z2.md", "dst": "y/x2.md"}]}
        self.assert_refused(plan, 1, "z/z1.md")

    def test_add_equal_to_moved_file_is_refused(self):
        self.write("rec.json", b"one\n")  # equal bytes to a/dir/one.md, which moves
        plan = {"move": [{"src": "a/dir", "dst": "b/dir"}], "add": [{"dst": "rec.json"}]}
        self.assert_refused(plan, 1, "rec.json")

    def test_remove_equal_to_moved_file_is_refused(self):
        self.seed({"c/copy.md": b"one\n"})  # equal bytes to a/dir/one.md, which moves
        plan = {"move": [{"src": "a/dir", "dst": "b/dir"}], "remove": ["c/copy.md"]}
        self.assert_refused(plan, 1, "c/copy.md")


class InputRefusals(Fixture):
    def test_never_overwrites_the_output(self):
        out = self.write("admitted.tsv", b"old\n", root=self.outside)
        code, text, err = self.run_cli({"remove": ["a/gone.md"]}, out)
        self.assertEqual(code, 2, err)
        self.assertEqual(text, "old\n")

    def test_output_symlink_is_not_followed(self):
        target = self.write("victim.tsv", b"victim\n", root=self.outside)
        out = os.path.join(self.tmp, "admitted.tsv")
        os.symlink(target, out)
        code, _, err = self.run_cli({"remove": ["a/gone.md"]}, out)
        self.assertEqual(code, 2, err)
        with open(target, "rb") as f:
            self.assertEqual(f.read(), b"victim\n")

    def test_staged_index_is_refused(self):
        self.write("a/keep.md", b"keep v2\n")
        self.git("add", "--", "a/keep.md")
        self.assert_refused({"remove": ["a/gone.md"]}, 2, "index")

    def test_repo_must_be_the_toplevel(self):
        self.repo = os.path.join(self.repo, "a")
        self.assert_refused({"remove": ["gone.md"]}, 2, "top level")

    def test_root_escape_and_git_paths_are_refused(self):
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": "../escape.md"}]}, 2, "../escape.md")
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": "/abs.md"}]}, 2, "/abs.md")
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": "b/./g.md"}]}, 2, "b/./g.md")
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": ".git/g.md"}]}, 2, ".git/g.md")
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": "b//g.md"}]}, 2, "b//g.md")
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": 5}]}, 2, "not a non-empty string")

    def test_tab_or_newline_path_is_refused(self):
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": "b/g\tx.md"}]}, 2, "tab or newline")
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": "b/g\nx.md"}]}, 2, "tab or newline")
        # A tracked name with a tab reaches the rows through a directory move, not through the plan.
        self.seed({"t/a\tb.md": b"tabbed\n"})
        self.assert_refused({"move": [{"src": "t", "dst": "u"}]}, 2, "tab or newline")

    def test_add_that_is_not_a_regular_file_or_symlink_is_refused(self):
        os.mkfifo(os.path.join(self.repo, "pipe"))
        self.assert_refused({"add": [{"dst": "pipe"}]}, 2, "not a regular file")

    def test_add_through_a_symlinked_parent_is_refused(self):
        self.write("rec.json", b"outside\n", root=self.outside)
        os.symlink(self.outside, os.path.join(self.repo, "escape"))
        self.assert_refused({"add": [{"dst": "escape/rec.json"}]}, 2, "symlink")

    def test_target_collision_is_refused(self):
        self.assert_refused({"move": [{"src": "a/gone.md", "dst": "a/keep.md"}]}, 2, "a/keep.md")
        self.write("a/keep.md", b"edited, unstaged\n")
        self.assert_refused({"add": [{"dst": "a/keep.md"}]}, 2, "a/keep.md")

    def test_path_in_two_rows_is_refused(self):
        plan = {"move": [{"src": "a/dir", "dst": "b/dir"}, {"src": "a/dir/one.md", "dst": "c/one.md"}]}
        self.assert_refused(plan, 2, "a/dir/one.md")
        self.assert_refused({"remove": ["a/regen.md"], "modify": ["a/regen.md"]}, 2, "a/regen.md")

    def test_modify_must_be_tracked(self):
        self.write("new.md", b"new\n")
        self.assert_refused({"modify": ["new.md"]}, 2, "new.md")

    def test_missing_add_source_is_refused(self):
        self.assert_refused({"add": [{"dst": "units/u1/executor.json"}]}, 2, "units/u1/executor.json")

    def test_malformed_or_empty_plan_is_refused(self):
        self.assert_refused({"mv": [{"src": "a/gone.md", "dst": "b/gone.md"}]}, 2, "mv")
        self.assert_refused({}, 2, "no rows")
        self.assert_refused({"move": [{"src": "untracked/only", "dst": "b/only"}]}, 2, "no rows")
        self.assert_refused({"remove": "a/gone.md"}, 2, "list")
        self.assert_refused({"move": [{"src": "a/gone.md"}]}, 2, "src and dst")
        self.assert_refused({"add": [{"dst": "rec.json", "from": "x"}]}, 2, "optional src")
        self.assert_refused({"add": [{"dst": "rec.json", "src": 5}]}, 2, "not a string")


class Destinations(Fixture):
    """Every repository destination is checked before anything is written (ruling 1)."""

    def setUp(self):
        super().setUp()
        os.symlink(self.outside, os.path.join(self.repo, "escape"))

    def assert_outside_untouched(self, plan: dict, out: str | None = None) -> str:
        code, text, err = self.run_cli(plan, out)
        self.assertEqual(code, 2, err)
        self.assertIsNone(text, "a refused plan must write no admitted list")
        self.assertEqual(os.listdir(self.outside), [], "nothing may be written outside the repository")
        return err

    def test_self_output_destination_through_a_symlink_is_refused(self):
        out = os.path.join(self.repo, "escape", "admitted.tsv")
        err = self.assert_outside_untouched({"add": [{"dst": "escape/admitted.tsv"}]}, out)
        self.assertIn("symlink", err)

    def test_explicit_source_destination_through_a_symlink_is_refused(self):
        source = self.write("src/record.json", b"record\n", root=self.tmp)
        err = self.assert_outside_untouched({"add": [{"dst": "escape/record.json", "src": source}]})
        self.assertIn("escape/record.json", err)
        self.assertIn("symlink", err)

    def test_explicit_source_destination_that_is_a_symlink_is_refused(self):
        source = self.write("src/record.json", b"record\n", root=self.tmp)
        err = self.assert_outside_untouched({"add": [{"dst": "escape", "src": source}]})
        self.assertIn("symlink", err)

    def test_move_destination_through_a_symlink_is_refused(self):
        err = self.assert_outside_untouched({"move": [{"src": "a/dir", "dst": "escape/dir"}]})
        self.assertIn("symlink", err)
        self.assert_outside_untouched({"move": [{"src": "a/gone.md", "dst": "escape"}]})
        # The move dst is a real directory, but a target below it passes through a symlink.
        os.makedirs(os.path.join(self.repo, "b/dir"))
        os.symlink(self.outside, os.path.join(self.repo, "b/dir/sub"))
        err = self.assert_outside_untouched({"move": [{"src": "a/dir", "dst": "b/dir"}]})
        self.assertIn("b/dir/sub/two.md", err)
        # An untracked move emits no row, but its destination is still checked.
        self.write("loose/u.md", b"untracked\n")
        self.assert_outside_untouched({"move": [{"src": "loose", "dst": "escape/loose"}],
                                       "remove": ["a/gone.md"]})

    def test_destination_under_a_file_is_refused(self):
        self.assert_refused({"move": [{"src": "a/keep.md", "dst": "a/gone.md/keep.md"}]}, 2, "not a directory")


class ControlCharacters(Fixture):
    """Every plan path must survive the file handoff to stage_check (ruling 2)."""

    def test_control_characters_are_refused_and_name_the_field(self):
        for ch in ("\r", "\0", "\x01", "\x1f", "\x7f"):
            with self.subTest(ch=ch):
                self.assert_refused({"move": [{"src": "a/gone.md", "dst": f"b/x{ch}y.md"}]}, 2, "move[0].dst")
                self.assert_refused({"move": [{"src": f"a/x{ch}y", "dst": "b/y"}]}, 2, "move[0].src")
                self.assert_refused({"remove": ["a/gone.md", f"a/x{ch}y.md"]}, 2, "remove[1]")
                self.assert_refused({"modify": [f"a/x{ch}y.md"]}, 2, "modify[0]")
                self.assert_refused({"add": [{"dst": f"r{ch}.json"}]}, 2, "add[0].dst")
                self.assert_refused({"add": [{"dst": "r.json", "src": f"/tmp/x{ch}y"}]}, 2, "add[0].src")

    def test_tracked_name_with_carriage_return_is_refused(self):
        self.seed({"t/a\rb.md": b"carriage\n"})
        self.assert_refused({"move": [{"src": "t", "dst": "u"}]}, 2, "move[0]")
        self.assert_refused({"remove": ["t"]}, 2, "remove[0]")

    def test_written_file_passes_the_stage_check_cli(self):
        self.seed({"a/dir/with space.md": b"spaced\n"})
        out = os.path.join(self.repo, "units/u1/admitted.tsv")
        os.makedirs(os.path.dirname(out))
        plan = {"move": [{"src": "a/dir", "dst": "b/dir"}], "remove": ["a/gone.md"],
                "add": [{"dst": "units/u1/admitted.tsv"}], "modify": ["a/regen.md"]}
        code, text, err = self.run_cli(plan, out)
        self.assertEqual(code, 0, err)
        os.makedirs(os.path.join(self.repo, "b"))
        self.git("mv", "a/dir", "b/dir")
        shutil.move(os.path.join(self.repo, "a/gone.md"), os.path.join(self.outside, "gone.md"))
        self.git("rm", "-q", "--cached", "--", "a/gone.md")
        self.write("a/regen.md", b"regen v2\n")
        self.git("add", "--", "units/u1/admitted.tsv", "a/regen.md")
        stage_check = os.path.join(os.path.dirname(os.path.abspath(S.__file__)), "stage_check.py")
        proc = subprocess.run([sys.executable, "-B", stage_check, "--repo", self.repo, "--admitted", out],
                              env=S.git_env(), capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), {"ok": True, "missing": [], "extra": []})


class Coverage(Fixture):
    """Behavioral witnesses for the guards Astra round 1 found unprotected (ruling 3)."""

    def test_inherited_git_variables_do_not_redirect_reads(self):
        absent = os.path.join(self.tmp, "absent-index")
        with mock.patch.dict(os.environ, {"GIT_INDEX_FILE": absent, "GIT_DIR": os.path.join(self.tmp, "no.git")}):
            code, text, err = self.run_cli({"remove": ["a/gone.md"]})
        self.assertEqual(code, 0, err)
        self.assertEqual(text, "D\ta/gone.md\n")

    def test_failing_git_command_is_refused(self):
        # An unborn HEAD makes `git ls-tree HEAD` fail; its empty output must not read as "nothing tracked".
        self.repo = os.path.join(self.tmp, "unborn")
        self.git("init", "-q", self.repo, cwd=self.tmp)
        self.write("rec.json", b"record\n")
        self.assert_refused({"add": [{"dst": "rec.json"}]}, 2, "ls-tree")

    def test_non_object_plan_and_entries_are_refused(self):
        self.assert_refused(["move"], 2, "plan keys")
        self.assert_refused({"move": [["src", "dst"]]}, 2, "src and dst")
        self.assert_refused({"add": [["dst"]]}, 2, "optional src")

    def seed_filtered_pair(self):
        self.seed({".gitattributes": b"*.txt text eol=lf\n", "gone.txt": b"paired\n"})

    def test_regular_file_is_hashed_through_git_filters(self):
        self.seed_filtered_pair()
        self.write("rec.txt", b"paired\r\n")  # Git stores it as paired\n, equal to gone.txt
        self.assert_refused({"remove": ["gone.txt"], "add": [{"dst": "rec.txt"}]}, 1, "gone.txt")

    def test_symlink_link_text_is_hashed_without_filters(self):
        self.seed_filtered_pair()
        os.symlink("paired\r\n", os.path.join(self.repo, "rec.txt"))  # Git stores the link text unfiltered
        code, text, err = self.run_cli({"remove": ["gone.txt"], "add": [{"dst": "rec.txt"}]})
        self.assertEqual(code, 0, err)
        self.assertEqual(text, "A\trec.txt\nD\tgone.txt\n")

    def test_self_output_needs_the_same_directory(self):
        self.write("new/admitted.tsv", b"gone\n")  # not the output: hashed from disk, equal to a/gone.md
        self.assert_refused({"remove": ["a/gone.md"], "add": [{"dst": "new/admitted.tsv"}]}, 1, "a/gone.md")

    def test_self_output_needs_the_same_name(self):
        self.write("new/record.json", b"gone\n")  # not the output: hashed from disk, equal to a/gone.md
        out = os.path.join(self.repo, "new/admitted.tsv")
        code, text, err = self.run_cli({"remove": ["a/gone.md"], "add": [{"dst": "new/record.json"}]}, out)
        self.assertEqual(code, 1, err)
        self.assertIn("a/gone.md", err)
        self.assertIsNone(text)

    def test_no_git_object_is_written(self):
        self.write("rec.json", b"unique untracked object\n")
        objects = os.path.join(self.repo, ".git", "objects")

        def listing():
            return sorted(os.path.join(d, f) for d, _, files in os.walk(objects) for f in files)

        before = listing()
        code, _, err = self.run_cli({"add": [{"dst": "rec.json"}]})
        self.assertEqual(code, 0, err)
        self.assertEqual(listing(), before)

    def test_move_takes_only_descendants_of_the_source_directory(self):
        self.seed({"a/directory/extra.md": b"extra\n"})
        code, text, err = self.run_cli({"move": [{"src": "a/dir", "dst": "b/dir"}]})
        self.assertEqual(code, 0, err)
        self.assertEqual(text, "R100\ta/dir/one.md\tb/dir/one.md\nR100\ta/dir/sub/two.md\tb/dir/sub/two.md\n")

    def test_index_mode_change_is_refused(self):
        self.git("update-index", "--chmod=+x", "a/keep.md")
        self.assert_refused({"remove": ["a/gone.md"]}, 2, "index")


class ReadOnlyGit(unittest.TestCase):
    def test_only_read_only_git_subcommands_run(self):
        for argv in (("add", "-A"), ("add", "--", "x"), ("mv", "a", "b"), ("rm", "--cached", "x"),
                     ("commit", "-m", "x"), ("hash-object", "-w", "--stdin"),
                     ("-c", "x=y", "ls-files"), ("update-index", "--add", "x")):
            with self.subTest(argv=argv), mock.patch.object(AL.subprocess, "run") as run:
                with self.assertRaises(AL.PlanError):
                    AL.git("/nonexistent", *argv)
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
