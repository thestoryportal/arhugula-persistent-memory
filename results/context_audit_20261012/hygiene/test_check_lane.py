"""Behavioral fixtures; all Git objects and writes stay in temporary directories."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import zlib

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("checker", HERE / "check_lane.py")


def git_object(root, kind, body):
    raw = kind.encode() + b" " + str(len(body)).encode() + b"\0" + body
    digest = hashlib.sha1(raw).hexdigest()
    path = root / ".git/objects" / digest[:2] / digest[2:]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(zlib.compress(raw))
    return digest


def tree(root, folder):
    chunks = []
    for path in sorted(folder.iterdir(), key=lambda p: p.name + ("/" if p.is_dir() else "")):
        if path.name == ".git":
            continue
        mode = b"40000" if path.is_dir() else b"100644"
        digest = tree(root, path) if path.is_dir() else git_object(root, "blob", path.read_bytes())
        chunks.append(mode + b" " + path.name.encode() + b"\0" + bytes.fromhex(digest))
    return git_object(root, "tree", b"".join(chunks))


def snapshot(root):
    digest = tree(root, root)
    commit = git_object(root, "commit", ("tree " + digest + "\nauthor Fixture <fixture@local> 0 +0000\ncommitter Fixture <fixture@local> 0 +0000\n\nfixture\n").encode())
    (root / ".git/refs/heads/fixture").write_text(commit + "\n")
    subprocess.run(["git", "-C", str(root), "read-tree", commit], check=True, capture_output=True)
    return commit


class CheckLaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.checker)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.wt = Path(self.tmp.name) / "wt"
        self.wt.mkdir()
        (self.wt / ".git/refs/heads").mkdir(parents=True)
        (self.wt / ".git/HEAD").write_text("ref: refs/heads/fixture\n")
        (self.wt / ".git/config").write_text("[core]\n repositoryformatversion = 0\n bare = false\n")
        self.write("allowed.md", "initial\n")
        self.write("memory_mirror/MEMORY.md", "index\n")
        self.base = snapshot(self.wt)
        self.lane = {"id": "FIX", "kind": "repo", "base_commit": self.base,
                     "allowlist": ["allowed.md", "memory_mirror/note.md", "memory_mirror/MEMORY.md"]}
        self.plan = Path(self.tmp.name) / "lanes.json"

    def write(self, path, value):
        target = self.wt / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value)

    def run_check(self):
        self.plan.write_text(json.dumps({"lanes": [self.lane]}))
        return self.checker.check_lane("FIX", self.wt, self.plan)

    def assert_failure(self, marker):
        failures = self.run_check()
        self.assertTrue(any(marker in line for line in failures), failures)

    def test_scope_pass(self):
        self.write("allowed.md", "changed\n")
        self.assertEqual([], self.run_check())

    def test_scope_fail_untracked(self):
        self.write("outside.md", "new\n")
        self.assert_failure("SCOPE")

    def test_scope_fail_committed_since_base(self):
        self.write("outside.md", "new\n")
        snapshot(self.wt)
        self.assert_failure("SCOPE")

    def test_frontmatter_pass(self):
        self.write("memory_mirror/note.md", "---\nname: Note\ndescription: A rule\nmetadata:\n  type: feedback\n---\nBody\n")
        self.assertEqual([], self.run_check())

    def test_frontmatter_fail(self):
        self.write("memory_mirror/note.md", "---\nname: Note\ndescription: A rule\n---\nBody\n")
        self.assert_failure("FRONTMATTER")

    def test_frontmatter_empty_fail(self):
        self.write("memory_mirror/note.md", '---\nname: ""\ndescription: A rule\nmetadata.type: feedback\n---\n')
        self.assert_failure("FRONTMATTER")

    def test_wiki_pass(self):
        self.write("allowed.md", "[[memory_mirror/MEMORY|index]]\n")
        self.assertEqual([], self.run_check())

    def test_wiki_fail(self):
        self.write("allowed.md", "[[absent]]\n")
        self.assert_failure("LINK")

    def test_relative_pass(self):
        self.write("allowed.md", "[index](memory_mirror/MEMORY.md#section)\n")
        self.assertEqual([], self.run_check())

    def test_relative_fail(self):
        self.write("allowed.md", "[bad](missing.md)\n")
        self.assert_failure("LINK")

    def test_reference_link_fail(self):
        self.write("allowed.md", "[bad][ref]\n\n[ref]: missing.md\n")
        self.assert_failure("LINK")

    def test_body_code_link_fail(self):
        self.write("allowed.md", "Body pointer `[[missing]]` must resolve.\n")
        self.assert_failure("LINK")

    def test_cap_pass_boundary(self):
        self.write("memory_mirror/MEMORY.md", "x" * 24400)
        self.assertEqual([], self.run_check())

    def test_cap_fail_bytes(self):
        self.write("memory_mirror/MEMORY.md", "é" * 12201)
        self.assert_failure("CAP")

    def test_host_pass(self):
        staged = "results/context_audit_20261012/hygiene/host_staging/.claude/CLAUDE.md"
        self.lane.update(kind="host", allowlist=[staged])
        self.write(staged, "[target](target.md)\n")
        self.write("results/context_audit_20261012/hygiene/host_staging/.claude/target.md", "target\n")
        self.lane["allowlist"].append("results/context_audit_20261012/hygiene/host_staging/.claude/target.md")
        self.assertEqual([], self.run_check())

    def test_host_fail_extra_stage(self):
        prefix = "results/context_audit_20261012/hygiene/host_staging/"
        self.lane.update(kind="host", allowlist=[prefix + ".claude/CLAUDE.md"])
        self.write(prefix + ".claude/extra.md", "extra\n")
        self.assert_failure("SCOPE")

    def test_host_fail_frontmatter(self):
        staged = "results/context_audit_20261012/hygiene/host_staging/.claude/projects/example/memory/note.md"
        self.lane.update(kind="host", allowlist=[staged])
        self.write(staged, "No metadata\n")
        self.assert_failure("FRONTMATTER")

    def test_host_cap_fail(self):
        staged = "results/context_audit_20261012/hygiene/host_staging/.claude/projects/example/memory/MEMORY.md"
        self.lane.update(kind="host", allowlist=[staged])
        self.write(staged, "x" * 24401)
        self.assert_failure("CAP")

    def test_host_links_do_not_use_live_home(self):
        staged = "results/context_audit_20261012/hygiene/host_staging/.claude/projects/example/memory/note.md"
        self.lane.update(kind="host", allowlist=[staged])
        self.write(staged, "---\nname: N\ndescription: D\nmetadata.type: feedback\n---\n[[missing]]\n")
        self.assert_failure("LINK")

    def test_symlink_escape_fail(self):
        external = Path(self.tmp.name) / "external.md"
        external.write_text("outside\n")
        (self.wt / "allowed.md").unlink()
        (self.wt / "allowed.md").symlink_to(external)
        self.assert_failure("SYMLINK")

    def test_missing_base_fails_closed(self):
        self.lane["base_commit"] = "f" * 40
        self.assert_failure("BASE")

    def freeze_dispatch(self, receipt):
        relative = "results/context_audit_20261012/hygiene/dispatch/FIX.json"
        body = json.dumps(receipt).encode()
        target = self.wt / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        digest = git_object(self.wt, "blob", body)
        ref = self.wt / ".git/refs/context_hygiene/dispatch/FIX"
        ref.parent.mkdir(parents=True, exist_ok=True)
        ref.write_text(digest + "\n")
        self.lane["requires_dispatch"] = True

    def test_dispatch_pass_frozen(self):
        self.freeze_dispatch({"lane": "FIX", "base_commit": self.base})
        self.write("allowed.md", "changed\n")
        self.assertEqual([], self.run_check())

    def test_dispatch_fail_mutated_base(self):
        self.write("outside.md", "new\n")
        moved = snapshot(self.wt)
        self.freeze_dispatch({"lane": "FIX", "base_commit": self.base})
        self.write("results/context_audit_20261012/hygiene/dispatch/FIX.json",
                   json.dumps({"lane": "FIX", "base_commit": moved}))
        self.assert_failure("BASE")

    def test_required_dispatch_missing_fail(self):
        self.lane["requires_dispatch"] = True
        self.assert_failure("BASE")

    def test_relative_basename_cannot_use_wiki_fallback(self):
        self.write("allowed.md", "[index](MEMORY.md)\n")
        self.assert_failure("LINK")

    def test_parenthesized_relative_fail(self):
        self.write("allowed.md", "[missing](missing(foo).md)\n")
        self.assert_failure("LINK")

    def test_python_comment_link_fail(self):
        self.lane["allowlist"].append("allowed.py")
        self.write("allowed.py", "# [[missing]]\nvalue = 1\n")
        self.assert_failure("LINK")

    def test_python_fixture_string_is_not_body_link(self):
        self.lane["allowlist"].append("allowed.py")
        self.write("allowed.py", "fixture = '[[intentionally_missing]]'\n")
        self.assertEqual([], self.run_check())

    def test_yaml_empty_block_scalar_fail(self):
        self.write("memory_mirror/note.md", "---\nname: |\ndescription: D\nmetadata:\n  type: feedback\n---\n")
        self.assert_failure("FRONTMATTER")

    def test_yaml_nonempty_block_scalar_pass(self):
        self.write("memory_mirror/note.md", "---\nname: |\n  Real name\ndescription: D\nmetadata:\n  type: feedback\n---\n")
        self.assertEqual([], self.run_check())

    def test_flat_metadata_is_not_mapping(self):
        self.write("memory_mirror/note.md", "---\nname: N\ndescription: D\nmetadata.type: feedback\n---\n")
        self.assert_failure("FRONTMATTER")

    def test_private_immutable_seed_pass(self):
        seed = "results/context_audit_20261012/hygiene/host_staging/.codex/config.toml"
        self.write(seed, "private fixture\n")
        self.lane["private_paths"] = [seed]
        self.freeze_dispatch({"lane": "FIX", "base_commit": self.base,
                              "private_seed_hashes": {seed: hashlib.sha256((self.wt / seed).read_bytes()).hexdigest()}})
        self.assertEqual([], self.run_check())

    def test_private_seed_mutation_fail(self):
        seed = "results/context_audit_20261012/hygiene/host_staging/.codex/config.toml"
        self.write(seed, "private fixture\n")
        self.lane["private_paths"] = [seed]
        self.freeze_dispatch({"lane": "FIX", "base_commit": self.base,
                              "private_seed_hashes": {seed: hashlib.sha256((self.wt / seed).read_bytes()).hexdigest()}})
        self.write(seed, "changed outside owner\n")
        self.assert_failure("SCOPE")

    def test_duplicate_metadata_fail(self):
        self.write("memory_mirror/note.md", "---\nname: N\ndescription: D\nmetadata:\n  type: feedback\nmetadata: null\n---\n")
        self.assert_failure("FRONTMATTER")

    def test_deleted_private_seed_fail(self):
        seed = "results/context_audit_20261012/hygiene/host_staging/.codex/config.toml"
        self.write(seed, "private fixture\n")
        self.lane["private_paths"] = [seed]
        self.freeze_dispatch({"lane": "FIX", "base_commit": self.base,
                              "private_seed_hashes": {seed: hashlib.sha256((self.wt / seed).read_bytes()).hexdigest()}})
        (self.wt / seed).unlink()
        self.assert_failure("BASE")

    def test_quoted_flow_metadata_pass(self):
        self.write("memory_mirror/note.md", '---\nname: N\ndescription: D\nmetadata: {"type": "feedback"}\n---\n')
        self.assertEqual([], self.run_check())


if __name__ == "__main__":
    unittest.main(verbosity=2)
