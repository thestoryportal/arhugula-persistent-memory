"""record_split classes a nested Git root as governed payload (Step 369, ruling R6).

Every leaf below a nested `.git` folder is a governed payload with its unit_manifest kind, size and
sha256 ("Never git add a nested repo"); every other leaf keeps the class it has today; a `.git` that is
a file (gitlink) still refuses, as unit_manifest refuses it; and move_run_core.run_unit accepts the
split of such a unit, because its leaves are exactly the Step 201 manifest leaves.

Both tools run as their module entry in a child process, on a unit holding a real repo made by `git init`.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ops.migrate import dup_find_core
from ops.migrate import move_plan_core as plan_core
from ops.migrate import move_run_core as core
from ops.migrate import record_split as R
from ops.migrate import test_move_run_core as RC
from test_record_split import before_open, fstat_reports

# [LAW:one-source-of-truth] The child imports the very code tree this process imported.
CODE = Path(R.__file__).resolve().parents[2]
GIT_ENV = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def child(module: str, *args) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(CODE)}
    return subprocess.run([sys.executable, "-B", "-m", module, *map(str, args)], env=env,
                          capture_output=True, text=True, timeout=120)


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false",
                    *args], cwd=repo, env={**os.environ, **GIT_ENV}, check=True, capture_output=True, timeout=60)


class NestedGitUnit(unittest.TestCase):
    """A unit beside its outputs: unit/ holds ordinary leaves and inner/, a committed nested repo."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        # unit_manifest refuses a root reached through a link (/var -> /private/var on macOS).
        self.base = Path(os.path.realpath(tmp.name))
        self.unit = self.base / "unit"
        self.put("notes.txt", b"plain text\n")
        self.put("weights.bin", b"\x00\x01\x02")
        self.put("model.json", b"\x00binary named as a record")
        self.cache = self.put("cache.bin", b"\x00regenerable")
        os.symlink("notes.txt", self.unit / "alias")
        self.put("inner/README.md", b"nested repo work tree\n")
        self.put("inner/blob.bin", b"\x00\xff")
        git(self.unit / "inner", "init", "-q")
        git(self.unit / "inner", "add", "-A")
        git(self.unit / "inner", "commit", "-q", "-m", "init")
        # Text and a record-kind name inside .git: payload all the same.
        self.put("inner/.git/info/sizes.json", b"{}\n")

    def put(self, rel: str, data: bytes) -> bytes:
        p = self.unit / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return data

    def attest(self, *paths_and_digests) -> Path:
        p = self.base / "att.json"
        p.write_text(json.dumps({"attested_by": "operator", "regenerate": "python make_cache.py",
                                 "leaves": [{"path": k, "sha256": v} for k, v in paths_and_digests]}))
        return p

    def split_cli(self, *extra) -> subprocess.CompletedProcess:
        return child("ops.migrate.record_split", "--root", self.unit, "--out", self.base / "split.json", *extra)

    def split(self) -> bytes:
        proc = self.split_cli("--attestation", self.attest(("cache.bin", sha(self.cache))))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return (self.base / "split.json").read_bytes()

    def manifest(self) -> bytes:
        out = self.base / "manifest.json"
        proc = child("ops.migrate.unit_manifest", "--root", self.unit, "--out", out)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return out.read_bytes()

    def rows(self) -> dict:
        return {row["path"]: row for row in json.loads(self.split())["leaves"]}

    def manifest_leaves(self) -> dict:
        return {dup_find_core.leaf_relpath(leaf["source"], str(self.unit)): leaf
                for leaf in json.loads(self.manifest())["leaves"]}

    def assertRefusedNaming(self, proc, name: str):
        self.assertEqual(proc.returncode, 2, proc.stderr)
        lines = proc.stderr.strip().splitlines()
        self.assertEqual(len(lines), 1, proc.stderr)
        self.assertTrue(lines[0].startswith("record_split: refused: "), proc.stderr)
        self.assertIn(name, lines[0])
        self.assertFalse((self.base / "split.json").exists())


class GitLeavesArePayload(NestedGitUnit):
    def test_every_leaf_below_nested_git_is_governed_payload_with_its_manifest_kind_size_and_sha256(self):
        rows, leaves = self.rows(), self.manifest_leaves()
        in_git = {rel for rel in leaves if rel.startswith("inner/.git/")}
        self.assertIn("inner/.git/HEAD", in_git)
        self.assertIn("inner/.git/info/sizes.json", in_git)
        self.assertIn("inner/.git/index", in_git)
        self.assertEqual({rel for rel in rows if "/.git/" in "/" + rel}, in_git)
        for rel in sorted(in_git):
            with self.subTest(leaf=rel):
                leaf = leaves[rel]
                self.assertEqual(leaf["kind"], "file")
                self.assertEqual(rows[rel], {"path": rel, "class": R.PAYLOAD, "kind": "file", "size": leaf["bytes"],
                                             "sha256": leaf["sha256"], "link": None})

    def test_an_attestation_naming_a_git_leaf_refuses(self):
        head = (self.unit / "inner/.git/HEAD").read_bytes()
        proc = self.split_cli("--attestation", self.attest(("inner/.git/HEAD", sha(head))))
        self.assertRefusedNaming(proc, "inner/.git/HEAD")


class OtherLeavesKeepTheirClass(NestedGitUnit):
    def test_leaves_outside_nested_git_get_the_class_they_get_today(self):
        rows = self.rows()
        outside = {rel: (row["class"], row["kind"]) for rel, row in rows.items() if not rel.startswith("inner/.git/")}
        self.assertEqual(outside, {
            "notes.txt": (R.TRACKED, "file"),
            "weights.bin": (R.PAYLOAD, "file"),
            "model.json": (R.TRACKED, "file"),
            "cache.bin": (R.BULK, "file"),
            "alias": (R.TRACKED, "link"),
            "inner/README.md": (R.TRACKED, "file"),
            "inner/blob.bin": (R.PAYLOAD, "file"),
        })
        self.assertEqual(rows["alias"]["link"], "notes.txt")


class GitlinkStillRefuses(NestedGitUnit):
    def test_a_git_file_or_link_refuses_in_both_tools(self):
        cases = {"gitlink file": lambda p: p.write_bytes(b"gitdir: ../../elsewhere/.git\n"),
                 "link to a git dir": lambda p: os.symlink(self.unit / "inner/.git", p),
                 "relative in-unit link": lambda p: os.symlink("../inner/.git", p)}
        (self.unit / "wt").mkdir()
        for name, make in cases.items():
            with self.subTest(case=name):
                make(self.unit / "wt/.git")
                try:
                    # [LAW:behavior-not-structure] A generic link refusal cannot prove .git admission.
                    self.assertRefusedNaming(self.split_cli(), "nested .git at 'wt/.git' is not a directory")
                    proc = child("ops.migrate.unit_manifest", "--root", self.unit, "--out", self.base / "m.json")
                    report = json.loads(proc.stdout)
                    self.assertEqual((proc.returncode, report["status"]), (1, "FAIL"), proc.stderr)
                    self.assertIn("wt/.git", report["reason"])
                finally:
                    os.unlink(self.unit / "wt/.git")

    def test_a_link_inside_nested_git_refuses(self):
        os.symlink("HEAD", self.unit / "inner/.git/HEAD.alias")
        self.assertRefusedNaming(
            self.split_cli(), "'inner/.git/HEAD.alias' inside a nested .git is a link or special file")



class GitStoreSafety(NestedGitUnit):
    def test_output_without_a_filename_is_refused_as_unnamed(self):
        self.assertRefusedNaming(self.split_cli("--out", "."), "names no file")

    def test_special_file_inside_git_refuses(self):
        os.mkfifo(self.unit / "inner/.git/pipe")
        self.assertRefusedNaming(
            self.split_cli(), "'inner/.git/pipe' inside a nested .git is a link or special file")

    def test_git_leaf_changed_after_digest_refuses(self):
        leaf = self.unit / "inner/.git/HEAD"
        real_digest = R._digest

        def append_after_read(at):
            result = real_digest(at)
            if at.path == str(leaf):
                with leaf.open("ab") as fh:
                    fh.write(b"more\n")
            return result

        with mock.patch.object(R, "_digest", append_after_read):
            with self.assertRaisesRegex(R.Refusal, r"inner/\.git/HEAD' changed while it was hashed"):
                R.split_unit(self.unit, [])

    def test_git_leaf_fd_changed_during_read_refuses(self):
        # [LAW:no-ambient-temporal-coupling] Count leaf fstats after HEAD opens, excluding directory fstats.
        with contextlib.ExitStack() as stack, before_open(
                lambda path, kwargs: path == "HEAD" and kwargs.get("dir_fd") is not None,
                lambda: stack.enter_context(fstat_reports(2, st_size=1))):
            with self.assertRaisesRegex(R.Refusal, r"inner/\.git/HEAD' changed while it was hashed"):
                R.split_unit(self.unit, [])

    def test_git_leaf_fd_on_another_device_refuses_before_hashing(self):
        hashers = mock.Mock(wraps=hashlib.sha256)
        with contextlib.ExitStack() as stack:
            def inject():
                stack.enter_context(fstat_reports(1, st_dev=1))
                stack.enter_context(mock.patch.object(hashlib, "sha256", hashers))

            with before_open(
                    lambda path, kwargs: path == "HEAD" and kwargs.get("dir_fd") is not None, inject):
                with self.assertRaisesRegex(R.Refusal, r"inner/\.git/HEAD' changed before it was hashed"):
                    R.split_unit(self.unit, [])
            self.assertEqual(hashers.call_count, 0, "inner/.git/HEAD changed before it was hashed")

    def test_git_leaf_removed_before_open_refuses(self):
        leaf = self.unit / "inner/.git/HEAD"
        with before_open(
                lambda path, kwargs: path == "HEAD" and kwargs.get("dir_fd") is not None, leaf.unlink):
            with self.assertRaisesRegex(R.Refusal, r"inner/\.git/HEAD' changed \(gone\) before it was hashed"):
                R.split_unit(self.unit, [])

    def test_git_leaf_swap_before_open_refuses_without_following_link(self):
        leaf = self.unit / "inner/.git/HEAD"
        outside = self.base / "outside"
        outside.write_bytes(b"secret")
        real_open = os.open
        fired = []

        def swap(path, flags, *args, **kwargs):
            if path == "HEAD" and kwargs.get("dir_fd") is not None and not fired:
                fired.append(True)
                leaf.rename(self.base / "saved-head")
                leaf.symlink_to(outside)
            return real_open(path, flags, *args, **kwargs)

        # [LAW:behavior-not-structure] Inject at the OS boundary; the real scanner must refuse.
        with mock.patch.object(os, "open", swap):
            with self.assertRaisesRegex(R.Refusal, "HEAD.*symlink") as caught:
                R.split_unit(self.unit, [])
        self.assertTrue(fired)
        self.assertIsInstance(caught.exception, R.Refusal)

class MoveRunAcceptsTheSplit(NestedGitUnit):
    def test_run_unit_accepts_the_split_and_adds_no_git_store_leaf(self):
        manifest, split = self.manifest(), self.split()
        source = str(self.unit)
        target = "/m/experiments/c10r/runs/unit"
        spec = RC.Spec("unit", "MV-369", source, "/v/preserved/unit", True, "/m/experiments/c10r", ())
        plan = plan_core.build_plan(
            entry_id="S220", root=RC.M,
            requirement_tables=[("/m/MOVE-REQUIREMENTS.tsv", RC.HEADER + "\n" + RC.req_row(spec) + "\n")],
            units=[{"requirement_id": spec.rid, "manifest_path": "/m/program/units/unit.json",
                    "manifest_bytes": manifest,
                    "registry": {"unit": "unit", "result": "exact", "experiment_id": "c10r", "candidates": ["c10r"],
                                 "unknown": [], "evidence": []},
                    "candidate": target, "readers": {"stale": [], "unverified": []}, "comparison": None}],
            existing_targets=[])
        plan_bytes = RC.canonical(plan)
        result = core.run_unit(
            root=RC.M, plan=(RC.PLAN_PATH, plan_bytes),
            approval=(RC.APPROVAL_PATH, RC.canonical(RC.approval_doc(plan_bytes))), now=RC.NOW,
            units=[{"source": source, "manifest": manifest, "split": split}], tracked=[],
            worktree=dict(RC.WORKTREE), targets=[{"target": target, "exists": False, "base": "/m/experiments/c10r"}],
            run_units=[source], custody_dir=RC.CUSTODY)
        rows = json.loads(split)["leaves"]
        records = sorted(f"{target}/{r['path']}" for r in rows if r["class"] == R.TRACKED)
        self.assertEqual(result["actions"], [
            RC.act("MV-369", "mkdir", target="/m/experiments/c10r/runs"),
            RC.act("MV-369", "mv", source, target),
            *(RC.act("MV-369", "git-add", target=t) for t in records)])
        self.assertFalse([t for t in records if "/.git/" in t])
        routes = [line.split("\t") for line in RC.docs(result)[f"{RC.CUSTODY}/routes.tsv"].decode().splitlines()[1:]]
        self.assertEqual(len(routes), len(json.loads(manifest)["leaves"]))
        git_routes = {r[1]: r[7] for r in routes if "/inner/.git/" in r[1]}
        self.assertTrue(git_routes)
        self.assertEqual(set(git_routes.values()), {R.PAYLOAD})


if __name__ == "__main__":
    unittest.main()
