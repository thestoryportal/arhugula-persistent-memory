"""Tests for move_unit run: the I/O shell of Step 210 over move_run_core (Step 218).

The shell observes the plan, its approval, the source bytes (a fresh Step 201 inventory), the targets and
the worktree, passes them to the core, writes the six custody documents and admitted.tsv, and runs only the
actions the core returns. Every test builds its own fixture repo M in a temporary directory; no real corpus
path is read for writing.

RED list for a filesystem tool, per bound object (each input file and its folder, the source and its parent,
the target base, the custody folder, M/.git and its config): swap_for_symlink between scan and open,
fifo_in_place, an injected EIO at each call class (open, scandir, read, write, fstat, close, F_GETPATH,
mkdir, rename) and ENOSPC on a write, one_byte_writes for the custody files, rename_and_rebind for each held
folder, raise_unexpected showing a non-OSError propagates, and refusals naming the path and errno name.
Git: the T201 ruling 2 and 7-9 refusals and a config swap while Git runs. "Never" sentences: audit tests
show no delete, chmod, extra mkdir, extra write, extra process or commit, and no input opened by path.
"""
from __future__ import annotations

import contextlib
import datetime
import errno
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe, move_unit, record_split, unit_manifest
from ops.migrate import move_run_core as run_core

GETPATH = FK.GETPATH
CODE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHECK = os.path.join(CODE, "state", "icm21_check.py")
STAGE = os.path.join(CODE, "ops", "git", "stage_check.py")
REQ_HEADER = "requirement_id\tsource\ttarget\taction\tobserved_bytes\tclass\tlane\tcheck_id\tadmission\tprd_ids"
PHASE_HEADER = "source_relative\ttarget_relative\tobserved_sha256"
CUSTODY = ("leaves.json", "routes.tsv", "repairs.json", "journal.jsonl", "executor.json", "retention.json",
           "admitted.tsv")
GIT_ALLOWED = {"config", "rev-parse", "ls-files", "update-index", "rm", "add"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(repo: str, *args: str) -> bytes:
    return subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                          env=clean_env(), check=True, capture_output=True).stdout


def named(path):
    """A fault_kit match: the call's first argument is this name or path."""
    return lambda first, *args, **kwargs: first == path


def instant(delta: datetime.timedelta) -> str:
    return (datetime.datetime.now(datetime.timezone.utc) + delta).strftime("%Y-%m-%dT%H:%M:%SZ")


REAL_RENAME = os.rename
NOREPLACE = fdsafe._rename_noreplace


@contextlib.contextmanager
def noreplace_at_os_rename():
    """Route fdsafe's exclusive rename through os.rename, so fault_kit's "rename" target wraps it (as
    test_fdsafe_named.py does); the kit's own path moves keep the plain rename."""
    def os_rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
        if src_dir_fd is None and dst_dir_fd is None:
            return REAL_RENAME(src, dst)
        return NOREPLACE(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
    with mock.patch.object(os, "rename", os_rename), \
            mock.patch.object(fdsafe, "_rename_noreplace", lambda *a, **k: os.rename(*a, **k)):
        yield


_events: list | None = None
WATCHED = frozenset({
    "open", "os.mkdir", "os.rename", "os.symlink", "os.link", "os.remove", "os.rmdir", "os.truncate", "os.chmod",
    "os.chflags", "os.chown", "os.utime", "shutil.copyfile", "shutil.move", "shutil.rmtree", "subprocess.Popen",
    "os.system", "os.posix_spawn", "os.exec", "os.spawn", "os.fork"})
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND


def _audit(event, args):
    if _events is not None and event in WATCHED:
        _events.append((event, args))


sys.addaudithook(_audit)  # an audit hook cannot be removed, so it records only inside recording()


@contextlib.contextmanager
def recording():
    global _events
    _events = []
    try:
        yield _events
    finally:
        _events = None


class Unit:
    """One fixture unit: its source folder and files, which of them Git tracks, and its plan inputs."""

    def __init__(self, name, rid, source, vtarget, files, tracked=(), exact=False):
        self.name, self.rid, self.source, self.vtarget = name, rid, source, vtarget
        self.files, self.tracked, self.exact = files, tracked, exact


class Fixture:
    """Root M (a Git repo with README.md and experiments/c10r/README.md committed), units, every run input,
    and the custody folder M/program/migrations/icm21/units/S220."""

    def __init__(self, base: str, kind: str = "in-m"):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="fx", dir=base))
        self.m = self.mk("m")
        git(self.m, "init", "-q", "--template=", "-b", "master")
        self.put("m/README.md", b"readme\n")
        self.put("m/experiments/c10r/README.md", b"c10r\n")
        self.custody = self.mk("m/program/migrations/icm21/units/S220")
        self.decoy = self.mk("decoy")
        self.gen = 0
        self.put("decoy/a.json", b'{"decoy": true}\n')
        if kind == "in-m":
            self.units = [Unit("u1", "MV-101", f"{self.m}/old/u1", f"{self.base}/v/old/u1",
                               {"a.json": b'{"a": 1}\n', "notes.txt": b"notes\n", "b.bin": b"\x00\x01\x02"},
                               tracked=("a.json",), exact=True)]
        else:
            self.units = [Unit("u3", "MV-103", f"{self.m}/old/u3", f"{self.base}/v/old/u3",
                               {"x.json": b'{"x": 3}\n'}, tracked=("x.json",)),
                          Unit("u2", "MV-102", f"{self.base}/p/u2", f"{self.base}/v/p/u2", {"c.log": b"log\n"})]
        for unit in self.units:
            for rel, data in unit.files.items():
                self.put(os.path.join(unit.source, rel), data)
        git(self.m, "add", "--", "README.md", "experiments/c10r/README.md",
            *[os.path.relpath(f"{u.source}/{rel}", self.m) for u in self.units for rel in u.tracked])
        git(self.m, "commit", "-q", "-m", "fixture")
        self.seal()

    def mk(self, rel: str) -> str:
        path = os.path.join(self.base, rel)
        os.makedirs(path)
        return path

    def put(self, path: str, data: bytes) -> str:
        path = os.path.join(self.base, path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "xb") as fh:
            fh.write(data)
        return path

    def json_file(self, name: str, obj) -> str:
        return self.put(os.path.join(self.inp, name), json.dumps(obj).encode())

    def rewrite(self, path: str, data: bytes) -> None:
        with open(path, "wb") as fh:
            fh.write(data)

    def candidate(self, unit: Unit) -> str:
        return f"{self.m}/experiments/c10r/runs/{unit.name}"

    def seal(self) -> None:
        """Every run input from the state now: manifests, splits, the Step 209 plan, its approval."""
        self.gen += 1
        self.inp = self.mk(f"in{self.gen}")
        rows = [REQ_HEADER]
        specs = []
        self.splits = {}
        for unit in self.units:
            manifest = os.path.join(self.inp, f"manifest-{unit.name}.json")
            split = os.path.join(self.inp, f"split-{unit.name}.json")
            with contextlib.redirect_stdout(io.StringIO()):
                assert unit_manifest.main(["--root", unit.source, "--out", manifest]) == 0
                assert record_split.main(["--root", unit.source, "--out", split]) == 0
            self.splits[unit.source] = split
            total = sum(len(d) for d in unit.files.values())
            rows.append("\t".join([unit.rid, unit.source, unit.vtarget, "HOLD", str(total), "legacy-science-unit",
                                   "legacy-preservation", "C-HOLD", "G4+G5; reader hold", "ICM-R4"]))
            match = {"root": self.m, "matches": [
                {"unit": unit.name, "result": "exact" if unit.exact else "none",
                 "experiment_id": "c10r" if unit.exact else None, "candidates": ["c10r"] if unit.exact else [],
                 "unknown": [], "evidence": []}]}
            specs.append({"requirement_id": unit.rid, "manifest": manifest,
                          "registry": self.json_file(f"match-{unit.name}.json", match),
                          "readers": self.json_file(f"readers-{unit.name}.json", {"stale": [], "unverified": []}),
                          "comparison": None, "candidate": self.candidate(unit) if unit.exact else None})
        self.req = self.put(os.path.join(self.inp, "req.tsv"), ("\n".join(rows) + "\n").encode())
        units_file = self.json_file("units.json", specs)
        out = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
        with contextlib.redirect_stdout(out):
            assert move_unit.main(["plan", "--entry", "S220", "--root", self.m, "--requirements", self.req,
                                   "--units", units_file]) == 0
        out.flush()
        self.plan_bytes = out.buffer.getvalue()
        self.plan_doc = json.loads(self.plan_bytes)
        self.plan = self.put(os.path.join(self.inp, "plan.json"), self.plan_bytes)
        self.approval = self.json_file("approval.json", self.approval_doc())
        self.run_units = self.json_file("run-units.json", [])
        self.phase = self.put(os.path.join(self.inp, "phase.tsv"), (PHASE_HEADER + "\n").encode())
        self.plans = self.json_file("plans.json", {"entries": [self.plan_doc]})

    def approval_doc(self, **over) -> dict:
        doc = {"approval_id": "approval-0001", "plan_id": "S220", "plan_sha256": sha(self.plan_bytes), "gate": "G4",
               "approved_by": "operator", "approved_at": instant(-datetime.timedelta(hours=1)),
               "expires_at": instant(datetime.timedelta(days=1)), "decision": "approved"}
        doc.update(over)
        return doc

    def target(self, unit: Unit) -> str:
        return next(u["target"] for u in self.plan_doc["units"] if u["source"] == unit.source)

    def args(self, *extra, splits=None) -> list:
        pairs = [part for source, path in (splits or self.splits).items() for part in ("--split", source, path)]
        return ["run", "--root", self.m, "--plan", self.plan, "--approval", self.approval, *pairs,
                "--run-units", self.run_units, "--custody-dir", self.custody, *extra]

    def custody_files(self) -> list:
        return sorted(os.listdir(self.custody))

    def observed(self) -> str:
        """The post LeafManifest: a fresh inventory of each unit source and target that exists now."""
        leaves = []
        for i, unit in enumerate(self.units):
            for j, path in enumerate((unit.source, self.target(unit))):
                if os.path.lexists(path):
                    out = os.path.join(self.base, f"obs-{i}-{j}-{len(os.listdir(self.base))}.json")
                    with contextlib.redirect_stdout(io.StringIO()):
                        assert unit_manifest.main(["--root", path, "--out", out]) == 0
                    with open(out, "rb") as fh:
                        leaves += json.loads(fh.read())["leaves"]
        return self.put(os.path.join(self.base, f"observed-{len(os.listdir(self.base))}.json"),
                        json.dumps({"schema_version": 1, "leaves": leaves}).encode())

    def moves_check(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-B", CHECK, "moves", "--root", self.m, "--requirements", self.req, "--phase-files",
             self.phase, "--plans", self.plans, "--entry", "S220", "--manifest",
             os.path.join(self.custody, "executor.json"), "--retention", os.path.join(self.custody, "retention.json"),
             "--observed", self.observed(), "--stage", "post"],
            capture_output=True, text=True, env=dict(clean_env(), PYTHONPATH=CODE), timeout=120)

    def stage_check(self) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", STAGE, "--repo", self.m, "--admitted",
                               os.path.join(self.custody, "admitted.tsv")],
                              capture_output=True, text=True, env=clean_env(), timeout=60)


class Base(unittest.TestCase):
    kind = "in-m"

    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="moverun"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.fx = Fixture(self.tmp, self.kind)
        self.u = self.fx.units[0]

    def main(self, *argv):
        out, err = io.TextIOWrapper(io.BytesIO(), encoding="utf-8"), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = move_unit.main(list(argv))
        out.flush()
        return code, out.buffer.getvalue().decode("utf-8"), err.getvalue()

    def run_ok(self, *extra):
        code, out, err = self.main(*self.fx.args(*extra))
        self.assertEqual((code, err), (0, ""))
        return json.loads(out)

    def assert_refused(self, result, path, *words):
        code, out, err = result
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")
        self.assertEqual(len(err.splitlines()), 1, err)
        self.assertNotIn("Traceback", err)
        self.assertIn(repr(path), err)
        for word in words:
            self.assertIn(word, err)

    def assert_unmoved(self, staged=True):
        """No unit moved and Git staged nothing: no target exists (and, when M's .git is intact, nothing is
        staged)."""
        for unit in self.fx.units:
            self.assertFalse(os.path.lexists(self.fx.target(unit)), unit.source)
        if staged:
            self.assertEqual(git(self.fx.m, "diff", "--cached", "--name-status"), b"")

    def assert_sources_in_place(self):
        for unit in self.fx.units:
            for rel, data in unit.files.items():
                with open(os.path.join(unit.source, rel), "rb") as fh:
                    self.assertEqual(fh.read(), data)

    def refuses_unmoved(self, path, *words, argv=None):
        self.assert_refused(self.main(*(argv or self.fx.args())), path, *words)
        self.assert_unmoved()


class PositiveControl(Base):
    def test_one_unit_moves_and_both_checks_pass(self):
        result = self.run_ok()
        target = self.fx.target(self.u)
        self.assertEqual(target, self.fx.candidate(self.u))
        self.assertFalse(os.path.lexists(self.u.source))
        for rel, data in self.u.files.items():
            with open(os.path.join(target, rel), "rb") as fh:
                self.assertEqual(fh.read(), data)
        self.assertEqual(self.fx.custody_files(), sorted(CUSTODY))
        self.assertEqual(result["custody"], [os.path.join(self.fx.custody, name) for name in CUSTODY])
        check = self.fx.moves_check()
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(json.loads(check.stdout)["status"], "PASS")
        staged = self.fx.stage_check()
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)

    def test_moves_check_fails_when_the_move_is_skipped(self):
        with mock.patch.dict(move_unit.ACTIONS, {"git-mv": lambda state, action: None}):
            self.main(*self.fx.args())
        self.assertTrue(os.path.isdir(self.u.source))
        check = self.fx.moves_check()
        self.assertEqual(check.returncode, 1, check.stdout + check.stderr)
        self.assertIn("C-MOVE", check.stdout)

    def test_stage_check_fails_when_the_record_add_is_skipped(self):
        with mock.patch.dict(move_unit.ACTIONS, {"git-add": lambda state, action: None}):
            self.run_ok()
        self.assertEqual(self.fx.moves_check().returncode, 0)
        staged = self.fx.stage_check()
        self.assertEqual(staged.returncode, 1, staged.stdout)
        self.assertIn("notes.txt", staged.stdout)

    def test_custody_files_are_the_core_documents_and_the_admitted_rows(self):
        seen = []
        real = run_core.run_unit

        def spy(**kw):
            seen.append(real(**kw))
            return seen[-1]
        with mock.patch.object(move_unit.run_core, "run_unit", spy):
            result = self.run_ok()
        documents = seen[0]["documents"]
        self.assertEqual(result["actions"], seen[0]["actions"])
        for doc in documents:
            with open(doc["path"], "rb") as fh:
                self.assertEqual(fh.read(), doc["bytes"], doc["path"])
        with open(os.path.join(self.fx.custody, "admitted.tsv"), "rb") as fh:
            self.assertEqual(fh.read(), b"R100\told/u1/a.json\texperiments/c10r/runs/u1/a.json\n"
                                        b"A\texperiments/c10r/runs/u1/notes.txt\n")
        self.assertEqual([a["action"] for a in seen[0]["actions"]], ["mkdir", "git-mv", "git-add"])

    def test_the_actions_run_in_core_order_and_nothing_else_runs(self):
        with recording() as events:
            self.run_ok()
        gits = [args[1] for event, args in events if event == "subprocess.Popen"]
        commands = [list(argv[argv.index("core.fsmonitor=false") + 1:]) for argv in gits]
        for argv in gits:
            self.assertEqual(list(argv[:4]), ["git", "--no-optional-locks", "-c", "core.fsmonitor=false"])
        self.assertEqual(commands, [
            ["config", "--file", "-", "--no-includes", "--null", "--list"],
            ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-dir", "--git-common-dir"],
            ["ls-files", "-z", "--full-name", "--", "old/u1"],
            ["ls-files", "-s", "-z", "--full-name", "--", "old/u1"],
            ["update-index", "-z", "--index-info"],
            ["add", "--", "experiments/c10r/runs/u1/notes.txt"]])
        self.assertEqual([args[0] for event, args in events if event == "os.mkdir"], ["runs"])
        others = {event for event, _ in events} - {"open", "subprocess.Popen", "os.mkdir"}
        self.assertEqual(others, set())
        created = [args[0] for event, args in events if event == "open" and isinstance(args[0], str)
                   and args[0] != os.devnull and args[2] & WRITE_FLAGS]
        self.assertEqual(created, list(CUSTODY))

    def test_every_input_and_folder_is_opened_through_a_held_folder(self):
        with recording() as events:
            self.run_ok()
        for event, args in events:
            if event == "open":
                path, flags = args[0], args[2]
                # an int is a pipe fd that subprocess wraps
                self.assertTrue(isinstance(path, int) or "/" not in path or flags & os.O_DIRECTORY
                                or path == os.devnull, args)

    def test_git_runs_without_global_config_and_with_lazy_fetch_off(self):
        seen = []
        real = subprocess.run

        def spy(argv, **kw):
            seen.append(kw["env"])
            return real(argv, **kw)
        with mock.patch.object(move_unit.subprocess, "run", spy):
            self.run_ok()
        for env in seen:
            self.assertEqual({k: env[k] for k in ("GIT_NO_LAZY_FETCH", "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL",
                                                  "GIT_DIR", "GIT_WORK_TREE", "GIT_LITERAL_PATHSPECS")},
                             {"GIT_NO_LAZY_FETCH": "1", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                              "GIT_DIR": f"{self.fx.m}/.git", "GIT_WORK_TREE": self.fx.m,
                              "GIT_LITERAL_PATHSPECS": "1"})

    def test_a_glob_name_is_a_literal_path(self):
        self.fx.put(os.path.join(self.u.source, "*.txt"), b"star\n")
        self.u.files["*.txt"] = b"star\n"
        self.fx.seal()
        self.run_ok()
        staged = self.fx.stage_check()
        self.assertEqual(staged.returncode, 0, staged.stdout)
        self.assertIn(b"A\texperiments/c10r/runs/u1/*.txt", git(self.fx.m, "diff", "--cached", "--name-status"))

    def test_relative_input_paths_are_read_from_the_cwd(self):
        cwd = os.getcwd()
        os.chdir(self.fx.base)
        self.addCleanup(os.chdir, cwd)
        argv = [os.path.relpath(a, self.fx.base) if a in (self.fx.plan, self.fx.approval, self.fx.run_units)
                else a for a in self.fx.args()]
        code, out, err = self.main(*argv)
        self.assertEqual((code, err), (0, ""))


class OutsideM(Base):
    kind = "outside"

    def test_untracked_unit_moves_with_mv_and_a_tracked_unit_leaving_m_is_removed_from_the_index(self):
        result = self.run_ok()
        self.assertEqual([(a["action"], a["operation_id"]) for a in result["actions"]],
                         [("mkdir", "MV-103"), ("mkdir", "MV-103"), ("mv", "MV-103"), ("git-rm-cached", "MV-103"),
                          ("mkdir", "MV-102"), ("mv", "MV-102")])
        for unit in self.fx.units:
            self.assertFalse(os.path.lexists(unit.source))
            self.assertEqual(sorted(os.listdir(self.fx.target(unit))), sorted(unit.files))
        with open(os.path.join(self.fx.custody, "admitted.tsv"), "rb") as fh:
            self.assertEqual(fh.read(), b"D\told/u3/x.json\n")
        staged = self.fx.stage_check()
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        check = self.fx.moves_check()
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_a_plan_unit_without_a_split_refuses(self):
        u3, u2 = self.fx.units
        argv = self.fx.args(splits={u2.source: self.fx.splits[u2.source]})
        self.refuses_unmoved(f"{u3.source} split", "expected the document bytes", argv=argv)

    def test_mv_is_fdsafe_rename_with_only_the_unit_folders_as_roots(self):
        calls = []
        real = fdsafe.rename

        def spy(sp, sn, dp, dn, roots):
            calls.append((sp.path, sn, dp.path, dn, [r.path for r in roots]))
            return real(sp, sn, dp, dn, roots)
        with mock.patch.object(move_unit.fdsafe, "rename", spy):
            self.run_ok()
        b = self.fx.base
        self.assertEqual(calls, [(f"{b}/m/old", "u3", f"{b}/v/old", "u3", [f"{b}/m/old", f"{b}/v/old"]),
                                 (f"{b}/p", "u2", f"{b}/v/p", "u2", [f"{b}/p", f"{b}/v/p"])])

    def test_injected_eio_at_rename_names_both_paths(self):
        with noreplace_at_os_rename(), FK.inject_oserror("rename", 1, errno.EIO):
            result = self.main(*self.fx.args())
        u3 = self.fx.units[0]
        self.assert_refused(result, f"{u3.source} -> {self.fx.target(u3)}", "[EIO]")
        self.assertTrue(os.path.isdir(u3.source))

    def test_source_swapped_for_a_link_at_the_rename_refuses(self):
        u2 = self.fx.units[1]
        with FK.swap_for_symlink("open", 1, u2.source, self.fx.decoy, match=named("u2")) as fault:
            result = self.main(*self.fx.args())
        self.assert_refused(result, u2.source, "[ELOOP]")
        self.assertFalse(os.path.lexists(self.fx.target(u2)))
        self.assertTrue(os.path.isdir(fault.parked))
        self.assertTrue(os.path.isdir(self.fx.decoy))

    def test_source_replaced_after_its_inventory_is_not_moved(self):
        u2 = self.fx.units[1]
        other = self.fx.mk("other-u2")
        real = move_unit._inventory

        def swap_after(source):
            out = real(source)
            if source == u2.source:
                os.rename(source, os.path.join(self.fx.base, "parked-u2"))
                os.rename(other, source)
            return out
        with noreplace_at_os_rename(), mock.patch.object(move_unit, "_inventory", swap_after):
            result = self.main(*self.fx.args())
        self.assert_refused(result, u2.source, "not the directory inventoried")
        self.assertFalse(os.path.lexists(self.fx.target(u2)))

    def test_source_replaced_between_check_and_rename_is_named_and_left(self):
        u2 = self.fx.units[1]
        other = self.fx.mk("other-u2")
        real = fdsafe.rename

        def swap_then_rename(sp, sn, dp, dn, roots):
            if sn == "u2":
                os.rename(u2.source, os.path.join(self.fx.base, "parked-u2"))
                os.rename(other, u2.source)
            return real(sp, sn, dp, dn, roots)
        with mock.patch.object(move_unit.fdsafe, "rename", swap_then_rename):
            result = self.main(*self.fx.args())
        self.assert_refused(result, self.fx.target(u2), "not the directory inventoried")
        self.assertTrue(os.path.isdir(self.fx.target(u2)))  # moved, never deleted
        self.assertTrue(os.path.isdir(os.path.join(self.fx.base, "parked-u2")))

    def test_rebound_source_parent_refuses_the_rename(self):
        u2 = self.fx.units[1]
        with FK.rename_and_rebind("mkdir", 3, os.path.dirname(u2.source), when="after") as fault:
            result = self.main(*self.fx.args())
        self.assertEqual(result[0], 2, result[2])
        self.assertIn(repr(os.path.dirname(u2.source)), result[2])
        self.assertTrue(os.path.isdir(os.path.join(fault.parked, "u2")))
        self.assertFalse(os.path.lexists(self.fx.target(u2)))


class NegativeControls(Base):
    def test_a_corrupted_byte_refuses_and_keeps_the_source(self):
        self.fx.rewrite(os.path.join(self.u.source, "a.json"), b'{"a": 2}\n')
        self.refuses_unmoved(self.u.source, "changed pre-digest")
        self.assertEqual(self.fx.custody_files(), [])

    def test_a_collision_refuses(self):
        os.makedirs(self.fx.target(self.u))
        self.assert_refused(self.main(*self.fx.args()), self.fx.target(self.u), "already exists")
        self.assert_sources_in_place()
        self.assertEqual(os.listdir(self.fx.target(self.u)), [])
        self.assertEqual(self.fx.custody_files(), [])

    def test_a_file_at_the_target_refuses(self):
        os.makedirs(os.path.dirname(self.fx.target(self.u)))
        self.fx.put(self.fx.target(self.u), b"occupied\n")
        self.assert_refused(self.main(*self.fx.args()), self.fx.target(self.u), "already exists")
        self.assert_sources_in_place()

    def test_a_link_at_the_target_refuses(self):
        os.makedirs(os.path.dirname(self.fx.target(self.u)))
        os.symlink(self.fx.decoy, self.fx.target(self.u))
        self.assert_refused(self.main(*self.fx.args()), self.fx.target(self.u), "link")
        self.assert_sources_in_place()

    def test_a_split_run_refuses(self):
        self.fx.rewrite(self.fx.run_units, json.dumps([f"{self.fx.m}/old"]).encode())
        self.refuses_unmoved(self.u.source, "splits run unit")

    def test_an_unapproved_plan_refuses(self):
        self.fx.rewrite(self.fx.approval, json.dumps(self.fx.approval_doc(decision="rejected")).encode())
        self.refuses_unmoved(self.fx.approval, "not approved")

    def test_an_expired_approval_refuses(self):
        self.fx.rewrite(self.fx.approval, json.dumps(self.fx.approval_doc(
            expires_at=instant(-datetime.timedelta(minutes=1)))).encode())
        self.refuses_unmoved(self.fx.approval, "expired")

    def test_a_changed_plan_refuses(self):
        self.fx.rewrite(self.fx.plan, self.fx.plan_bytes.rstrip(b"\n"))
        self.refuses_unmoved(self.fx.approval, "does not bind the plan bytes")

    def test_a_linked_worktree_refuses(self):
        other = os.path.join(self.fx.base, "other")
        git(self.fx.base, "init", "-q", other)
        self.fx.put(os.path.join(self.fx.m, ".git", "commondir"), f"{other}/.git\n".encode())
        self.assert_refused(self.main(*self.fx.args()), "worktree", "linked worktree")
        self.assert_unmoved(staged=False)
        self.assert_sources_in_place()

    def test_a_dot_git_file_refuses(self):
        os.rename(os.path.join(self.fx.m, ".git"), os.path.join(self.fx.base, "gitdir"))
        self.fx.put(os.path.join(self.fx.m, ".git"), f"gitdir: {self.fx.base}/gitdir\n".encode())
        self.assert_refused(self.main(*self.fx.args()), f"{self.fx.m}/.git", "[ENOTDIR]")
        self.assert_sources_in_place()

    def test_a_split_for_no_plan_unit_refuses(self):
        splits = dict(self.fx.splits, **{f"{self.fx.m}/old/u9": self.fx.splits[self.u.source]})
        self.refuses_unmoved(f"{self.fx.m}/old/u9", "no unit of the plan", argv=self.fx.args(splits=splits))

    def test_a_unit_source_split_twice_refuses(self):
        argv = self.fx.args() + ["--split", self.u.source, self.fx.splits[self.u.source]]
        self.refuses_unmoved("--split", "twice", argv=argv)

    def test_a_relative_root_or_custody_folder_refuses(self):
        for flag in ("--root", "--custody-dir"):
            with self.subTest(flag=flag):
                argv = self.fx.args()
                argv[argv.index(flag) + 1] = "m"
                self.refuses_unmoved("m", "not an absolute path", argv=argv)

    def test_a_control_character_in_a_path_refuses(self):
        argv = self.fx.args()
        argv[argv.index("--plan") + 1] = self.fx.plan + "\t"
        self.refuses_unmoved(self.fx.plan + "\t", "tab", argv=argv)

    def test_an_existing_custody_file_is_never_overwritten(self):
        kept = self.fx.put(os.path.join(self.fx.custody, "retention.json"), b"kept\n")
        self.refuses_unmoved(kept, "[EEXIST]")
        with open(kept, "rb") as fh:
            self.assertEqual(fh.read(), b"kept\n")
        self.assertEqual(self.fx.custody_files(), sorted(CUSTODY[:5] + ("retention.json",)))

    def test_custody_inside_the_source_folder_refuses(self):
        inside = self.fx.mk("m/old/custody")
        argv = self.fx.args()
        argv[argv.index("--custody-dir") + 1] = inside
        self.refuses_unmoved(os.path.join(inside, "leaves.json"), "inside root", argv=argv)
        self.assertEqual(os.listdir(inside), [])

    def test_custody_inside_the_target_folder_refuses(self):
        inside = self.fx.mk("m/experiments/c10r/runs/custody")
        argv = self.fx.args()
        argv[argv.index("--custody-dir") + 1] = inside
        self.refuses_unmoved(os.path.join(inside, "leaves.json"), "inside root", argv=argv)

    def test_a_failing_git_command_refuses_with_its_exit(self):
        self.fx.put(os.path.join(self.fx.m, ".gitignore"), b"*.txt\n")
        git(self.fx.m, "add", ".gitignore")
        git(self.fx.m, "commit", "-q", "-m", "ignore")
        code, out, err = self.main(*self.fx.args())
        self.assertEqual(code, 2, err)
        self.assertIn("git add -- experiments/c10r/runs/u1/notes.txt", err)
        self.assertIn("exited 1", err)
        self.assertEqual(len(err.splitlines()), 1, err)

    def test_admitted_rows_are_strict_utf8(self):
        # The parse steps refuse a lone surrogate before it reaches a row (move_run_core._json for plan paths,
        # _utf8 for git ls-files names), so this witness calls the row builder directly: a lossy encode would
        # write a row no staged path can equal.
        action = {"operation_id": "MV-101", "action": "git-add", "source": None, "target": "/m/a\udcff"}
        with self.assertRaises(UnicodeEncodeError):
            move_unit._admitted("/m", [action], [])

    def test_no_delete_chmod_or_commit(self):
        with recording() as events:
            self.run_ok()
        self.assertFalse({"os.remove", "os.rmdir", "os.chmod", "shutil.rmtree", "os.system"}
                         & {event for event, _ in events})
        for event, args in events:
            if event == "subprocess.Popen":
                self.assertIn(args[1][4], GIT_ALLOWED, args)
        self.assertEqual(git(self.fx.m, "rev-list", "--count", "HEAD"), b"1\n")


class GitConfig(Base):
    # [LAW:behavior-not-structure] config and repo attacks must refuse while preserving sources.
    def refuses_config(self, path, *words, staged=True):
        self.assert_refused(self.main(*self.fx.args()), path, *words)
        self.assert_unmoved(staged)
        self.assert_sources_in_place()

    def test_refused_config_keys(self):
        config = f"{self.fx.m}/.git/config"
        for key, value in (("include.path", "/elsewhere"), ("includeIf.gitdir:/x/.path", "/elsewhere"),
                           ("core.hooksPath", "/elsewhere"), ("core.fsmonitor", "/bin/true"),
                           ("extensions.worktreeConfig", "true"), ("remote.origin.promisor", "true"),
                           ("remote.origin.partialclonefilter", "blob:none"), ("filter.x.clean", "cat")):
            with self.subTest(key=key):
                fx = Fixture(self.tmp)
                git(fx.m, "config", key, value)
                self.fx = fx
                self.refuses_config(f"{fx.m}/.git/config", "sets", key.lower().split(".")[0])
        self.assertTrue(config)

    def test_allowed_config_keys_pass(self):
        git(self.fx.m, "config", "remote.origin.url", "/nowhere")
        git(self.fx.m, "config", "branch.master.remote", "origin")
        self.run_ok()

    def test_config_worktree_refuses(self):
        self.fx.put(os.path.join(self.fx.m, ".git", "config.worktree"), b"")
        self.refuses_config(f"{self.fx.m}/.git/config.worktree", "second config")

    def test_link_inside_dot_git_refuses(self):
        os.mkdir(os.path.join(self.fx.m, ".git", "info"))
        os.symlink(self.fx.decoy, os.path.join(self.fx.m, ".git", "info", "link"))
        self.refuses_config(f"{self.fx.m}/.git/info/link", "link or special file")

    def test_fifo_inside_dot_git_refuses(self):
        os.mkdir(os.path.join(self.fx.m, ".git", "info"))
        os.mkfifo(os.path.join(self.fx.m, ".git", "info", "fifo"))
        self.refuses_config(f"{self.fx.m}/.git/info/fifo", "link or special file")

    def test_config_swapped_while_git_runs_refuses(self):
        config = f"{self.fx.m}/.git/config"
        real = subprocess.run

        def swap(argv, **kw):
            out = real(argv, **kw)
            if "ls-files" in argv:
                copy = config + ".new"
                shutil.copyfile(config, copy)
                os.replace(copy, config)
            return out
        with mock.patch.object(move_unit.subprocess, "run", swap):
            self.refuses_config(config, "changed while Git ran")

    def test_config_edited_with_mtime_restored_refuses_on_ctime(self):
        config = f"{self.fx.m}/.git/config"
        real = subprocess.run

        def edit(argv, **kw):
            out = real(argv, **kw)
            if "rev-parse" in argv:
                st = os.stat(config)
                with open(config, "r+b") as fh:
                    data = fh.read()
                    self.assertIn(b"filemode = true", data)
                    fh.seek(0)
                    fh.write(data.replace(b"filemode = true", b"filemode = TRUE", 1))
                os.utime(config, ns=(st.st_atime_ns, st.st_mtime_ns))
                after = os.stat(config)
                self.assertEqual((after.st_ino, after.st_size, after.st_mtime_ns),
                                 (st.st_ino, st.st_size, st.st_mtime_ns))
                self.assertNotEqual(after.st_ctime_ns, st.st_ctime_ns)
            return out
        with mock.patch.object(move_unit.subprocess, "run", edit):
            self.refuses_config(config, "changed while Git ran")

    def test_dot_git_swapped_with_same_config_inode_refuses(self):
        dotgit = f"{self.fx.m}/.git"
        copy = self.fx.base + "/git-copy"
        shutil.copytree(dotgit, copy, symlinks=True)
        os.remove(copy + "/config")
        os.link(dotgit + "/config", copy + "/config")
        real = subprocess.run

        def swap(argv, **kw):
            out = real(argv, **kw)
            if "rev-parse" in argv:
                os.rename(dotgit, dotgit + "-old")
                os.rename(copy, dotgit)
            return out
        with mock.patch.object(move_unit.subprocess, "run", swap):
            self.refuses_config(dotgit, "changed while Git ran")

    def test_dot_git_swapped_while_git_runs_refuses(self):
        dotgit = f"{self.fx.m}/.git"
        real = subprocess.run

        def swap(argv, **kw):
            out = real(argv, **kw)
            if "rev-parse" in argv:
                os.rename(dotgit, dotgit + "-old")
                shutil.copytree(dotgit + "-old", dotgit, symlinks=True)
            return out
        with mock.patch.object(move_unit.subprocess, "run", swap):
            self.assert_refused(self.main(*self.fx.args()), f"{dotgit}/config", "changed while Git ran")
        self.assert_sources_in_place()

    def test_config_swapped_for_a_fifo_between_walk_and_open_refuses(self):
        config = f"{self.fx.m}/.git/config"
        with FK.fifo_in_place(config, name="open", match=named("config")):
            self.refuses_config(config, "not a regular file", staged=False)

    def test_unreadable_git_exits_as_a_refusal(self):
        with mock.patch.dict(os.environ, {"PATH": "/nonexistent"}):
            code, out, err = self.main(*self.fx.args())
        self.assertEqual(code, 2, err)
        self.assertIn("git config", err)
        self.assert_sources_in_place()


class Attacks(Base):
    """fault_kit attacks on every object the shell binds."""

    def inputs(self):
        return {"plan": self.fx.plan, "approval": self.fx.approval, "split": self.fx.splits[self.u.source],
                "run-units": self.fx.run_units}

    def test_input_file_swapped_for_a_link_refuses(self):
        for label, path in self.inputs().items():
            with self.subTest(label=label):
                self.setUp()
                path = self.inputs()[label]
                with FK.swap_for_symlink("open", 1, path, f"{self.fx.decoy}/a.json",
                                         match=named(os.path.basename(path))):
                    result = self.main(*self.fx.args())
                self.assert_refused(result, path, "[ELOOP]")
                self.assert_unmoved()

    def test_folder_swapped_for_a_link_refuses(self):
        def folders():
            return {"source": self.u.source, "source parent": os.path.dirname(self.u.source),
                    "target base": f"{self.fx.m}/experiments/c10r", "dot git": f"{self.fx.m}/.git",
                    "custody": self.fx.custody, "input folder": self.fx.inp}
        for label in folders():
            with self.subTest(label=label):
                self.setUp()
                path = folders()[label]
                with FK.swap_for_symlink("open", 1, path, self.fx.decoy, match=named(path)):
                    result = self.main(*self.fx.args())
                self.assert_refused(result, path)
                self.assertRegex(result[2], r"\[(ELOOP|ENOTDIR)\]")  # O_DIRECTORY | O_NOFOLLOW on a link
                self.assert_unmoved(staged=label != "dot git")
                self.assertEqual(self.fx.custody_files() if label != "custody" else [], [])

    def test_config_swapped_for_a_link_refuses(self):
        config = f"{self.fx.m}/.git/config"
        with FK.swap_for_symlink("open", 1, config, f"{self.fx.decoy}/a.json", match=named("config")):
            self.assert_refused(self.main(*self.fx.args()), config, "[ELOOP]")
        self.assert_unmoved(staged=False)

    def test_fifo_in_place_of_each_leaf_and_folder_refuses(self):
        def objects():
            """label: (the object put as a FIFO, the path the refusal names)."""
            c10r = f"{self.fx.m}/experiments/c10r"
            return {**{k: (v, v) for k, v in self.inputs().items()},
                    "config": (f"{self.fx.m}/.git/config",) * 2, "source": (self.u.source,) * 2,
                    "source parent": (os.path.dirname(self.u.source),) * 2,
                    "target base": (c10r, f"{c10r}/runs"),  # the first folder held below the FIFO
                    "dot git": (f"{self.fx.m}/.git",) * 2, "custody": (self.fx.custody,) * 2}
        for label in objects():
            with self.subTest(label=label):
                self.setUp()
                path, refused = objects()[label]
                with FK.fifo_in_place(path):
                    code, out, err = self.main(*self.fx.args())
                self.assertEqual(code, 2, err)
                self.assertIn(repr(refused), err)
                self.assertNotIn("Traceback", err)
                for unit in self.fx.units:
                    self.assertFalse(os.path.lexists(self.fx.target(unit)))

    def test_injected_errors_name_the_path_and_the_errno(self):
        leaves = "leaves.json (left in place, incomplete)"
        cases = [("open", errno.EIO, lambda fx: named("plan.json"), lambda fx: fx.plan),
                 ("fstat", errno.EIO, lambda fx: None, lambda fx: fx.plan),
                 ("read", errno.EIO, lambda fx: None, lambda fx: fx.plan),
                 ("close", errno.EIO, lambda fx: None, lambda fx: fx.plan),
                 (GETPATH, errno.EIO, lambda fx: None, lambda fx: fx.inp),
                 ("scandir", errno.EIO, lambda fx: None, lambda fx: f"{fx.m}/.git"),
                 ("open", errno.EIO, lambda fx: named("config"), lambda fx: f"{fx.m}/.git/config"),
                 ("open", errno.EIO, lambda fx: named(fx.units[0].source), lambda fx: fx.units[0].source),
                 ("open", errno.EIO, lambda fx: named(fx.custody), lambda fx: fx.custody),
                 ("write", errno.EIO, lambda fx: None, lambda fx: f"{fx.custody}/{leaves}"),
                 ("write", errno.ENOSPC, lambda fx: None, lambda fx: f"{fx.custody}/{leaves}"),
                 ("mkdir", errno.EIO, lambda fx: None, lambda fx: f"{fx.m}/experiments/c10r/runs")]
        for name, err, match, path in cases:
            with self.subTest(name=name, path=path(self.fx), err=err):
                self.setUp()
                with FK.inject_oserror(name, 1, err, match=match(self.fx)):
                    result = self.main(*self.fx.args())
                self.assert_refused(result, path(self.fx), f"[{errno.errorcode[err]}]")
                self.assert_unmoved()

    def test_injected_close_error_after_a_custody_write_names_the_kept_file(self):
        real, calls = os.write, []

        def note(fd, data):
            calls.append(fd)
            return real(fd, data)
        with mock.patch.object(os, "write", note), \
                FK.inject_oserror("close", 1, errno.EIO, match=lambda fd: bool(calls) and fd == calls[0]):
            result = self.main(*self.fx.args())
        self.assert_refused(result, f"{self.fx.custody}/leaves.json (created, left in place)", "[EIO]")
        self.assertEqual(self.fx.custody_files(), ["leaves.json"])
        self.assert_unmoved()

    def test_one_byte_writes_give_the_same_custody_bytes(self):
        seen = []
        real = run_core.run_unit

        def spy(**kw):
            seen.append(real(**kw))
            return seen[-1]
        with mock.patch.object(move_unit.run_core, "run_unit", spy), FK.one_byte_writes():
            self.run_ok()
        for doc in seen[0]["documents"]:
            with open(doc["path"], "rb") as fh:
                self.assertEqual(fh.read(), doc["bytes"])
        with open(os.path.join(self.fx.custody, "admitted.tsv"), "rb") as fh:
            self.assertEqual(fh.read(), b"R100\told/u1/a.json\texperiments/c10r/runs/u1/a.json\n"
                                        b"A\texperiments/c10r/runs/u1/notes.txt\n")

    def test_rebound_custody_folder_refuses_and_keeps_the_file(self):
        with FK.rename_and_rebind("write", 1, self.fx.custody) as fault:
            result = self.main(*self.fx.args())
        self.assert_refused(result, f"{fault.parked}/leaves.json", "moved during the write", "left in place")
        self.assertEqual(os.listdir(fault.parked), ["leaves.json"])
        self.assertEqual(os.listdir(self.fx.custody), [])
        self.assert_unmoved()

    def test_rebound_target_base_refuses_the_mkdir(self):
        base = f"{self.fx.m}/experiments/c10r"
        with FK.rename_and_rebind("mkdir", 1, base) as fault:
            result = self.main(*self.fx.args())
        self.assertEqual(result[0], 2, result[2])
        self.assertIn("runs", result[2])
        self.assertTrue(os.path.isdir(os.path.join(fault.parked, "runs")))  # kept, never deleted
        self.assert_unmoved()

    def test_rebound_source_parent_refuses_the_git_mv(self):
        parent = os.path.dirname(self.u.source)
        with FK.rename_and_rebind("mkdir", 1, parent, when="after") as fault:
            result = self.main(*self.fx.args())
        self.assert_refused(result, parent, "was moved")
        self.assertTrue(os.path.isdir(os.path.join(fault.parked, "u1")))
        self.assertEqual(git(self.fx.m, "diff", "--cached", "--name-status"), b"")

    def test_rebound_target_parent_refuses_the_git_mv(self):
        runs = f"{self.fx.m}/experiments/c10r/runs"
        real = fdsafe.mkdir

        def made_then_rebound(parent, name):
            held = real(parent, name)
            os.rename(runs, runs + "-parked")
            os.mkdir(runs)
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_rebound):
            result = self.main(*self.fx.args())
        self.assert_refused(result, runs, "is held at")
        self.assert_unmoved()
        self.assert_sources_in_place()

    def test_target_created_before_the_git_mv_refuses(self):
        target = self.fx.target(self.u)
        real = fdsafe.mkdir

        def made_then_occupied(parent, name):
            held = real(parent, name)
            os.mkdir(target)
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_occupied):
            result = self.main(*self.fx.args())
        self.assert_refused(result, target, "[EEXIST]")
        self.assertEqual(os.listdir(target), [])
        self.assert_sources_in_place()

    def test_source_replaced_before_the_git_mv_is_not_moved(self):
        other = self.fx.mk("other-u1")
        real = fdsafe.mkdir

        def made_then_swapped(parent, name):
            held = real(parent, name)
            os.rename(self.u.source, os.path.join(self.fx.base, "parked-u1"))
            os.rename(other, self.u.source)
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_swapped):
            result = self.main(*self.fx.args())
        self.assert_refused(result, self.u.source, "not the directory inventoried")
        self.assert_unmoved()

    def test_source_replaced_during_the_git_mv_is_named(self):
        target = self.fx.target(self.u)
        real = subprocess.run

        def swap(argv, **kw):
            out = real(argv, **kw)
            if "update-index" in argv:
                os.rename(target, os.path.join(self.fx.base, "parked-u1"))
                os.mkdir(target)
            return out
        with mock.patch.object(move_unit.subprocess, "run", swap):
            result = self.main(*self.fx.args())
        self.assert_refused(result, target, "not the directory inventoried")
        self.assertTrue(os.path.isdir(os.path.join(self.fx.base, "parked-u1")))

    def test_rebound_dot_git_refuses(self):
        with FK.rename_and_rebind("open", 1, f"{self.fx.m}/.git", when="after", match=named("config")):
            result = self.main(*self.fx.args())
        self.assertEqual(result[0], 2, result[2])
        self.assertIn(f"'{self.fx.m}/.git", result[2])
        self.assertNotIn("Traceback", result[2])
        self.assert_sources_in_place()

    def test_unexpected_exceptions_propagate(self):
        for name, exc in (("scandir", ValueError), ("open", KeyError), ("mkdir", RuntimeError),
                          ("write", ValueError)):
            with self.subTest(name=name, exc=exc.__name__):
                self.setUp()
                with FK.raise_unexpected(name, 1, exc), self.assertRaises(exc) as caught:
                    self.main(*self.fx.args())
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)

    def test_injected_eio_at_the_config_fstat_names_the_config(self):
        config = f"{self.fx.m}/.git/config"

        def is_config(fd):
            return fdsafe.live_path(fd, "probe").endswith("/.git/config")
        with FK.inject_oserror("fstat", 1, errno.EIO, match=is_config):
            self.assert_refused(self.main(*self.fx.args()), config, "[EIO]")
        self.assert_unmoved()

    def test_injected_eio_at_the_git_fstat_names_git(self):
        git_path = f"{self.fx.m}/.git"

        def is_git(fd):
            return fdsafe.live_path(fd, "probe").endswith("/.git")
        with FK.inject_oserror("fstat", 1, errno.EIO, match=is_git):
            self.assert_refused(self.main(*self.fx.args()), git_path, "[EIO]")
        self.assert_unmoved()

    def test_an_os_error_inside_the_inventory_names_the_source(self):
        with FK.inject_oserror("open", 1, errno.EIO, match=named("a.json")):
            self.assert_refused(self.main(*self.fx.args()), self.u.source, "[EIO]")
        self.assert_unmoved()

    def test_an_inventory_refusal_names_the_source(self):
        os.mkfifo(os.path.join(self.u.source, "fifo"))
        self.assert_refused(self.main(*self.fx.args()), self.u.source, "unsupported object kind")
        self.assert_unmoved()

    def test_an_unexpected_error_inside_the_inventory_propagates(self):
        with FK.raise_unexpected("open", 1, RuntimeError, match=named("a.json")), \
                self.assertRaises(RuntimeError) as caught:
            self.main(*self.fx.args())
        self.assertIs(type(caught.exception), RuntimeError)

    def test_an_unexpected_error_while_holding_a_target_folder_propagates(self):
        runs = f"{self.fx.m}/experiments/c10r/runs"
        with FK.raise_unexpected("open", 1, RuntimeError, match=named(runs)), \
                self.assertRaises(RuntimeError) as caught:
            self.main(*self.fx.args())
        self.assertIs(type(caught.exception), RuntimeError)
        self.assert_unmoved()

    def test_a_source_gone_before_its_move_names_it(self):
        real = fdsafe.mkdir

        def made_then_gone(parent, name):
            held = real(parent, name)
            os.rename(self.u.source, os.path.join(self.fx.base, "parked-u1"))
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_gone):
            self.assert_refused(self.main(*self.fx.args()), self.u.source, "[ENOENT]")
        self.assert_unmoved()

    def test_cli_refusal_is_one_line_without_a_traceback(self):
        self.fx.rewrite(os.path.join(self.u.source, "a.json"), b'{"a": 2}\n')
        env = dict(clean_env(), PYTHONPATH=CODE)
        proc = subprocess.run([sys.executable, "-B", os.path.join(CODE, "ops", "migrate", "move_unit.py"),
                               *self.fx.args()], capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(len(proc.stderr.splitlines()), 1, proc.stderr)
        self.assertIn(repr(self.u.source), proc.stderr)


if __name__ == "__main__":
    unittest.main()


class LateInputParents(Base):
    def test_late_parent_attacks_refuse_for_every_input(self):
        from test_move_unit_plan import after_open_then

        for attr in ("plan", "approval", "run_units", "split"):
            for kind in ("rebind", "link"):
                with self.subTest(attr=attr, kind=kind):
                    self.setUp()
                    leaf = next(iter(self.fx.splits.values())) if attr == "split" else getattr(self.fx, attr)
                    parent = os.path.dirname(leaf)
                    if kind == "link":
                        replacement = os.path.join(self.fx.decoy, "replacement")
                        shutil.copytree(parent, replacement)
                        attack = FK.swap_for_symlink("open", 1, parent, replacement,
                                                     when="after", match=named(os.path.basename(leaf)))
                    else:
                        attack = FK.rename_and_rebind("open", 1, parent,
                                                     when="after", match=named(os.path.basename(leaf)))
                    with attack as fault:
                        def restore():
                            if kind == "rebind":
                                shutil.copytree(fault.parked, parent, dirs_exist_ok=True)
                        with after_open_then(os.path.basename(leaf), restore):
                            result = self.main(*self.fx.args())
                    self.assertEqual(fault.fired, 1)
                    self.assert_refused(result, parent)
                    self.assert_unmoved()
                    self.assert_sources_in_place()
                    self.assertEqual(self.fx.custody_files(), [])


class LateWindows(Base):
    # [LAW:behavior-not-structure] inject changes at effects and assert refusal and preserved state.
    def test_w1a_source_leaf_swapped_during_mkdir(self):
        leaf = self.u.source + "/notes.txt"
        with FK.swap_for_symlink("mkdir", 1, leaf, self.fx.decoy + "/a.json", when="after") as fault:
            result = self.main(*self.fx.args())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, self.u.source)
        self.assert_unmoved()
        self.assertTrue(os.path.isdir(self.u.source))
        self.assertEqual(os.readlink(leaf), self.fx.decoy + "/a.json")
        for rel in ("a.json", "b.bin"):
            with open(self.u.source + "/" + rel, "rb") as fh:
                self.assertEqual(fh.read(), self.u.files[rel])

    def test_w1b_target_leaf_swapped_after_rename(self):
        target = self.fx.target(self.u)
        real = move_unit.fdsafe.rename

        def moved_then_swapped(*args):
            result = real(*args)
            leaf = target + "/notes.txt"
            os.rename(leaf, self.fx.base + "/parked-notes")
            os.symlink(self.fx.decoy + "/a.json", leaf)
            return result
        with mock.patch.object(move_unit.fdsafe, "rename", moved_then_swapped):
            result = self.main(*self.fx.args())
        self.assert_refused(result, target)
        self.assertTrue(os.path.islink(target + "/notes.txt"))

    def test_w2_attributes_link_during_mkdir(self):
        os.mkdir(os.path.join(self.fx.m, ".git", "info"))
        attrs = self.fx.put("m/.git/info/attributes", b"")
        outside = self.fx.put("decoy/attributes", b"*.txt text eol=lf\n")
        before = git(self.fx.m, "ls-files", "-z")
        with FK.swap_for_symlink("mkdir", 1, attrs, outside, when="after") as fault:
            result = self.main(*self.fx.args())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, attrs, "link or special file")
        self.assert_unmoved()
        self.assert_sources_in_place()
        self.assertEqual(git(self.fx.m, "ls-files", "-z"), before)

    def test_w3_config_edited_in_place_during_mkdir(self):
        config = self.fx.m + "/.git/config"
        outside = self.fx.put("decoy/attributes", b"*.txt text eol=lf\n")
        inode = os.stat(config).st_ino
        before = git(self.fx.m, "ls-files", "-s", "-z")
        real = move_unit.fdsafe.mkdir

        def made_then_edited(parent, name):
            held = real(parent, name)
            with open(config, "ab") as fh:
                fh.write(("[core]\n\tattributesFile = " + outside + "\n").encode())
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_edited):
            result = self.main(*self.fx.args())
        self.assertEqual(os.stat(config).st_ino, inode)
        self.assert_refused(result, config, "changed before Git ran")
        self.assert_unmoved()
        self.assert_sources_in_place()
        self.assertEqual(git(self.fx.m, "ls-files", "-s", "-z"), before)

    def test_w4_target_created_before_rename(self):
        target = self.fx.target(self.u)
        real = move_unit.fdsafe.rename

        def occupied_then_rename(*args):
            os.mkdir(target)
            self.fx.put(target + "/keep", b"keep")
            return real(*args)
        with mock.patch.object(move_unit.fdsafe, "rename", occupied_then_rename):
            result = self.main(*self.fx.args())
        self.assert_refused(result, target, "already exists", "[EEXIST]")
        self.assert_sources_in_place()
        self.assertEqual(os.listdir(target), ["keep"])
        with open(target + "/keep", "rb") as fh:
            self.assertEqual(fh.read(), b"keep")

    def test_w5_index_changed_during_mkdir(self):
        real = move_unit.fdsafe.mkdir

        def made_then_staged(parent, name):
            held = real(parent, name)
            added = self.fx.put(self.u.source + "/new.txt", b"new\n")
            git(self.fx.m, "add", "--", added)
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_staged):
            result = self.main(*self.fx.args())
        self.assert_refused(result, self.u.source, "index under it changed")
        self.assert_unmoved(staged=False)
        self.assert_sources_in_place()

    def test_w5_unmerged_index_entry_during_mkdir(self):
        real = move_unit.fdsafe.mkdir

        def made_then_unmerged(parent, name):
            held = real(parent, name)
            mode, object_name, _, _ = git(self.fx.m, "ls-files", "-s", "--", "old/u1/a.json").decode().split()
            records = (f"0 {'0' * 40}\told/u1/a.json\n"
                       f"{mode} {object_name} 1\told/u1/a.json\n"
                       f"{mode} {object_name} 2\told/u1/a.json\n")
            subprocess.run(["git", "-C", self.fx.m, "update-index", "--index-info"],
                           input=records.encode(), env=clean_env(), check=True, capture_output=True)
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_unmerged):
            result = self.main(*self.fx.args())
        self.assert_refused(result, self.u.source, "index under it changed")
        self.assert_unmoved(staged=False)
        self.assert_sources_in_place()


class OutsideLateWindows(Base):
    # [LAW:behavior-not-structure] late mv attacks assert refusal paths and preserved unit bytes.
    kind = "outside"

    def test_rebound_target_parent_refuses_the_mv(self):
        parent_path = os.path.dirname(self.fx.target(self.u))
        real = fdsafe.mkdir

        def made_then_rebound(parent, name):
            held = real(parent, name)
            if os.path.join(parent.path, name) == parent_path:
                os.rename(parent_path, parent_path + "-parked")
                os.mkdir(parent_path)
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_rebound):
            result = self.main(*self.fx.args())
        self.assert_refused(result, parent_path, "is held at")
        self.assert_unmoved()
        self.assert_sources_in_place()

    def test_w1a_mv_source_leaf_swapped_during_mkdir(self):
        leaf = self.u.source + "/x.json"
        with FK.swap_for_symlink("mkdir", 1, leaf, self.fx.decoy + "/a.json", when="after") as fault:
            result = self.main(*self.fx.args())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, self.u.source)
        self.assert_unmoved()
        self.assertEqual(os.readlink(leaf), self.fx.decoy + "/a.json")
        u2 = self.fx.units[1]
        for rel, data in u2.files.items():
            with open(os.path.join(u2.source, rel), "rb") as fh:
                self.assertEqual(fh.read(), data)

    def test_w1b_mv_target_leaf_swapped_after_rename(self):
        target = self.fx.target(self.u)
        real = fdsafe.rename

        def moved_then_swapped(src_parent, src_name, dst_parent, dst_name, roots):
            result = real(src_parent, src_name, dst_parent, dst_name, roots)
            if dst_name == os.path.basename(self.u.source):
                leaf = target + "/x.json"
                os.rename(leaf, self.fx.base + "/parked-x")
                os.symlink(self.fx.decoy + "/a.json", leaf)
            return result
        with mock.patch.object(move_unit.fdsafe, "rename", moved_then_swapped):
            result = self.main(*self.fx.args())
        self.assert_refused(result, target)
        self.assertEqual(os.readlink(target + "/x.json"), self.fx.decoy + "/a.json")
        u2 = self.fx.units[1]
        self.assertFalse(os.path.lexists(self.fx.target(u2)))
        for rel, data in u2.files.items():
            with open(os.path.join(u2.source, rel), "rb") as fh:
                self.assertEqual(fh.read(), data)

    def test_w5_index_changed_before_git_rm_cached(self):
        real = fdsafe.mkdir
        first_target = self.fx.base + "/v"

        def made_then_staged(parent, name):
            held = real(parent, name)
            if os.path.join(parent.path, name) == first_target:
                object_name = git(self.fx.m, "ls-files", "-s", "--", "old/u3/x.json").decode().split()[1]
                git(self.fx.m, "update-index", "--add", "--cacheinfo", f"100644,{object_name},old/u3/new.txt")
            return held
        with mock.patch.object(move_unit.fdsafe, "mkdir", made_then_staged):
            result = self.main(*self.fx.args())
        self.assert_refused(result, self.u.source, "index under it changed")
        target = self.fx.target(self.u)
        with open(target + "/x.json", "rb") as fh:
            self.assertEqual(fh.read(), self.u.files["x.json"])
        self.assertEqual(git(self.fx.m, "ls-files", "--", "old/u3"), b"old/u3/new.txt\nold/u3/x.json\n")
        u2 = self.fx.units[1]
        self.assertFalse(os.path.lexists(self.fx.target(u2)))
        for rel, data in u2.files.items():
            with open(os.path.join(u2.source, rel), "rb") as fh:
                self.assertEqual(fh.read(), data)
