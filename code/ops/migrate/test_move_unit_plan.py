"""Tests for move_unit plan, check-plans and check-routes: the I/O shell of Step 209 over move_plan_core (Step 217).

The shell reads its inputs through fdsafe, passes them to the core and prints the core's plan or findings
unchanged. RED list for a filesystem tool: every fault_kit attack that applies to each bound object (each
input file and the directory that holds it, --root, --source, and each reader file a report names); an
injected error at each call class the shell makes (open, fstat, read, close, F_GETPATH, scandir, and lstat
through a local helper, because fault_kit has no lstat target), naming the path and the errno; an unexpected
exception propagating. The tool creates no file, so one_byte_writes, ENOSPC, mkdir, rename and output-parent
attacks have no target here; the audit tests show it opens nothing to write, changes nothing and runs no
process.
"""
from __future__ import annotations

import contextlib
import errno
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import dup_find_core, fdsafe, move_unit, unit_manifest
from ops.migrate import move_plan_core as core

GETPATH = FK.GETPATH
CODE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOL = os.path.join(CODE, "ops", "migrate", "move_unit.py")
DATA = b'{"a": 1}\n'
REQ_HEADER = "requirement_id\tsource\ttarget\taction\tobserved_bytes\tclass\tlane\tcheck_id\tadmission\tprd_ids"
REPAIR_HEADER = "file\tline\told_text\tnew_text\tstep"
ROUTE_HEADER = "child\tproducer\towner\ttarget"


def canonical_line(obj) -> str:
    return unit_manifest.canonical(obj).decode("utf-8") + "\n"


def req_row(rid, source, target, observed, action="HOLD"):
    return "\t".join([rid, source, target, action, str(observed), "legacy-science-unit", "legacy-preservation",
                      "C-HOLD", "G4+G5; reader hold", "ICM-R4"])


def named(path):
    """A fault_kit match: the call's first argument is this name or path."""
    return lambda first, *args, **kwargs: first == path


@contextlib.contextmanager
def lstat_error(err, path):
    """fault_kit has no lstat target: raise OSError(err) at the first os.lstat whose first argument is path."""
    real, calls = os.lstat, []

    def hooked(first, *args, **kwargs):
        if first == path and not calls:
            calls.append(first)
            raise OSError(err, os.strerror(err))
        return real(first, *args, **kwargs)
    with mock.patch.object(os, "lstat", hooked):
        yield calls
    if not calls:
        raise AssertionError(f"lstat_error: no os.lstat of {path!r}")


@contextlib.contextmanager
def stat_error(err, name):
    """Raise OSError(err) at the first os.stat of name relative to a held directory (dir_fd), as the target
    observation calls it."""
    real, calls = os.stat, []

    def hooked(first, *args, **kwargs):
        if first == name and "dir_fd" in kwargs and not calls:
            calls.append(first)
            raise OSError(err, os.strerror(err))
        return real(first, *args, **kwargs)
    with mock.patch.object(os, "stat", hooked):
        yield calls
    if not calls:
        raise AssertionError(f"stat_error: no os.stat of {name!r} with dir_fd")


_events: list | None = None  # audit events while recording runs; None outside it
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


class Fixture:
    """A fresh tree: root M with experiments/c10r/runs and docs/a.md, one unit P/u1 with its Step 201 manifest,
    every plan, check-plans and check-routes input file, and a results folder with two children."""

    def __init__(self, base: str):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="fx", dir=base))
        self.m = self.mk("m")
        self.mk("m/experiments/c10r/runs")
        self.docs = self.mk("m/docs")
        self.src = self.mk("p/u1")
        self.write(os.path.join(self.src, "a.json"), DATA)
        self.inp = self.mk("in")
        self.mdir = self.mk("manifests")
        self.other = self.mk("other")
        self.decoy = self.write(os.path.join(self.base, "decoy"), b"decoy\n")
        self.candidate = f"{self.m}/experiments/c10r/runs/u1"
        self.v_target = f"{self.base}/v/p/u1"
        self.manifest = os.path.join(self.mdir, "u1.json")
        with contextlib.redirect_stdout(io.StringIO()):
            assert unit_manifest.main(["--root", self.src, "--out", self.manifest]) == 0
        with open(self.manifest, "rb") as fh:
            self.manifest_bytes = fh.read()
        self.old = f"{self.src}/a.json"
        self.reader = self.write(os.path.join(self.docs, "a.md"), f"intro\nsee {self.old} here\n".encode())
        self.req_text = f"{REQ_HEADER}\n{req_row('MV-101', self.src, self.v_target, len(DATA))}\n"
        self.req = self.write(os.path.join(self.inp, "req.tsv"), self.req_text.encode())
        self.match_doc = {"root": self.m, "matches": [{"unit": "u1", "result": "exact", "experiment_id": "c10r",
                                                       "candidates": ["c10r"], "unknown": [], "evidence": []}]}
        self.match = self.json("match.json", self.match_doc)
        self.stale = {"file": "docs/a.md", "line": 2, "old_text": self.old, "old": self.old}
        self.readers_doc = {"stale": [self.stale], "unverified": []}
        self.readers = self.json("readers.json", self.readers_doc)
        ref = self.mk("p/ref")
        self.write(os.path.join(ref, "a.json"), DATA)
        ref_manifest = os.path.join(self.base, "ref.json")
        with contextlib.redirect_stdout(io.StringIO()):
            assert unit_manifest.main(["--root", ref, "--out", ref_manifest]) == 0
        with open(ref_manifest, "rb") as fh:
            self.dup_doc = dup_find_core.classify(json.loads(self.manifest_bytes), [json.loads(fh.read())])
        self.dup = self.json("dup.json", self.dup_doc)
        self.units_doc = [self.spec()]
        self.units = self.json("units.json", self.units_doc)
        # [LAW:one-source-of-truth] Check the same wire Moves that the real plan command emits.
        out = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
        with contextlib.redirect_stdout(out):
            assert move_unit.main(self.plan_args()) == 0
        out.flush()
        self.plans_doc = {"entries": [json.loads(out.buffer.getvalue())]}
        self.plans = self.json("plans.json", self.plans_doc)
        self.repairs_text = f"{REPAIR_HEADER}\ndocs/a.md\t2\t{self.old}\t{self.candidate}/a.json\t261\n"
        self.repairs = self.write(os.path.join(self.inp, "repairs.tsv"), self.repairs_text.encode())
        self.historical_text = "file\tline\told_text\n"
        self.historical = self.write(os.path.join(self.inp, "historical.tsv"), self.historical_text.encode())
        self.source = self.mk("results")
        self.mk("results/r1")
        self.write(os.path.join(self.source, "r2.json"), b"{}\n")
        self.hold = f"{self.base}/v/results"
        self.routes_text = (f"{ROUTE_HEADER}\nr1\tstage_run.py\trun\t{self.m}/experiments/c10r/runs/r1\n"
                            f"r2.json\t\thold\t{self.hold}/r2.json\n")
        self.routes = self.write(os.path.join(self.inp, "routes.tsv"), self.routes_text.encode())

    def mk(self, rel: str) -> str:
        path = os.path.join(self.base, rel)
        os.makedirs(path)
        return path

    def write(self, path: str, data: bytes) -> str:
        with open(path, "xb") as fh:
            fh.write(data)
        return path

    def json(self, name: str, obj) -> str:
        return self.write(os.path.join(self.inp, name), json.dumps(obj).encode("utf-8"))

    def rewrite(self, path: str, data: bytes) -> None:
        with open(path, "wb") as fh:
            fh.write(data)

    def spec(self, **change) -> dict:
        return {"requirement_id": "MV-101", "manifest": self.manifest, "registry": self.match,
                "readers": self.readers, "comparison": self.dup, "candidate": self.candidate, **change}

    def core_unit(self, **change) -> dict:
        return {"requirement_id": "MV-101", "manifest_path": self.manifest, "manifest_bytes": self.manifest_bytes,
                "registry": self.match_doc["matches"][0], "candidate": self.candidate,
                "readers": self.readers_doc, "comparison": self.dup_doc, **change}

    def plan_args(self, *extra) -> list:
        return ["plan", "--entry", "S220", "--root", self.m, "--requirements", self.req, "--units", self.units,
                *extra]

    def expected_plan(self, existing=(), units=None, tables=None) -> dict:
        return core.build_plan(entry_id="S220", root=self.m,
                               requirement_tables=tables or [(self.req, self.req_text)],
                               units=units or [self.core_unit()], existing_targets=list(existing))

    def check_plans_args(self, *extra) -> list:
        return ["check-plans", "--root", self.m, "--plans", self.plans, "--repairs", self.repairs,
                "--historical", self.historical, "--readers", self.readers, *extra]

    def expected_findings(self, occurrences=None) -> tuple:
        line = f"see {self.old} here"
        return core.check_plans(root=self.m, entries=self.plans_doc["entries"],
                                occurrences=occurrences or [{**self.stale, "text": line}],
                                repairs=(self.repairs, self.repairs_text),
                                historical=(self.historical, self.historical_text))

    def check_routes_args(self, *extra) -> list:
        return ["check-routes", "--routes", self.routes, "--source", self.source, "--hold-target", self.hold, *extra]


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="moveunit"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.fx = Fixture(self.tmp)

    def fresh(self) -> Fixture:
        return Fixture(self.tmp)

    def main(self, *argv):
        out, err = io.TextIOWrapper(io.BytesIO(), encoding="utf-8"), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = move_unit.main(list(argv))
        out.flush()
        return code, out.buffer.getvalue().decode("utf-8"), err.getvalue()

    def assert_refused(self, result, path, *words):
        code, out, err = result
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")
        self.assertEqual(len(err.splitlines()), 1, err)
        self.assertNotIn("Traceback", err)
        self.assertIn(repr(path), err)
        for word in words:
            self.assertIn(word, err)

    def cli(self, *argv, cwd=None):
        env = dict(os.environ, PYTHONPATH=CODE)
        return subprocess.run([sys.executable, "-B", TOOL, *argv], capture_output=True, text=True, env=env,
                              cwd=cwd, timeout=60)


class Plan(Base):
    def test_plan_is_the_core_plan_unchanged_on_one_canonical_line(self):
        code, out, err = self.main(*self.fx.plan_args())
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, canonical_line(self.fx.expected_plan()))
        row = dict(zip(REQ_HEADER.split("\t"), self.fx.req_text.splitlines()[1].split("\t")))
        digest = hashlib.sha256(self.fx.manifest_bytes).hexdigest()
        # [LAW:behavior-not-structure] Bind every wire field to the fixture inputs, independently of the core.
        self.assertEqual(json.loads(out)["moves"], [{
            "id": "MV-101", "action": "MOVE", "source": self.fx.src, "target": self.fx.candidate,
            "kind": "directory", "bytes": len(DATA), "before_sha256": digest,
            "source_manifest": {"path": self.fx.manifest, "sha256": digest},
            "lane": row["lane"], "prd_ids": row["prd_ids"].split(","), "reader_check_ids": [],
        }])

    def test_existing_candidate_is_observed_and_keeps_the_v_target(self):
        os.mkdir(self.fx.candidate)
        code, out, err = self.main(*self.fx.plan_args())
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, canonical_line(self.fx.expected_plan(existing=[self.fx.candidate])))
        self.assertEqual(json.loads(out)["moves"][0]["target"], self.fx.v_target)
        self.assertIn("candidate-exists", [r["kind"] for r in json.loads(out)["risks"]])

    def test_existing_v_target_behind_an_existing_candidate_refuses(self):
        os.mkdir(self.fx.candidate)
        os.makedirs(self.fx.v_target)
        self.assert_refused(self.main(*self.fx.plan_args()), "MV-101", "already exists")

    def test_existing_v_target_of_an_unmatched_unit_refuses(self):
        self.fx.rewrite(self.fx.match, json.dumps(
            {"root": self.fx.m, "matches": [{"unit": "u1", "result": "none", "experiment_id": None,
                                             "candidates": [], "unknown": [], "evidence": []}]}).encode())
        os.makedirs(self.fx.v_target)
        self.assert_refused(self.main(*self.fx.plan_args()), "MV-101", "already exists")

    def test_absent_targets_are_not_existing(self):
        self.fx.rewrite(self.fx.units, json.dumps([self.fx.spec(candidate=None)]).encode())
        code, out, err = self.main(*self.fx.plan_args())
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, canonical_line(self.fx.expected_plan(units=[self.fx.core_unit(candidate=None)])))
        self.assertEqual(json.loads(out)["moves"][0]["target"], self.fx.v_target)

    def test_null_comparison_is_passed_as_no_comparison(self):
        self.fx.rewrite(self.fx.units, json.dumps([self.fx.spec(comparison=None)]).encode())
        code, out, err = self.main(*self.fx.plan_args())
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, canonical_line(self.fx.expected_plan(units=[self.fx.core_unit(comparison=None)])))
        self.assertIn("no-comparison", [r["kind"] for r in json.loads(out)["risks"]])

    def test_every_requirements_file_and_every_unit_is_read(self):
        fx = self.fx
        src2 = fx.mk("p/u2")
        fx.write(os.path.join(src2, "b.txt"), b"bb")
        man2 = os.path.join(fx.mdir, "u2.json")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(unit_manifest.main(["--root", src2, "--out", man2]), 0)
        with open(man2, "rb") as fh:
            man2_bytes = fh.read()
        text2 = f"{REQ_HEADER}\n{req_row('MV-157', src2, fx.base + '/v/p/u2', 2)}\n"
        req2 = fx.write(os.path.join(fx.inp, "amend.tsv"), text2.encode())
        match2 = {"root": fx.m, "matches": [{"unit": "u2", "result": "none", "experiment_id": None,
                                             "candidates": [], "unknown": [], "evidence": []}]}
        readers2 = {"stale": [], "unverified": [{"file": "docs/b.md", "reason": "binary"}]}
        spec2 = {"requirement_id": "MV-157", "manifest": man2, "registry": fx.json("match2.json", match2),
                 "readers": fx.json("readers2.json", readers2), "comparison": None, "candidate": None}
        fx.rewrite(fx.units, json.dumps([fx.spec(), spec2]).encode())
        code, out, err = self.main(*fx.plan_args("--requirements", req2))
        self.assertEqual((code, err), (0, ""))
        unit2 = {"requirement_id": "MV-157", "manifest_path": man2, "manifest_bytes": man2_bytes,
                 "registry": match2["matches"][0], "candidate": None, "readers": readers2, "comparison": None}
        expected = fx.expected_plan(units=[fx.core_unit(), unit2],
                                    tables=[(fx.req, fx.req_text), (req2, text2)])
        self.assertEqual(out, canonical_line(expected))
        self.assertEqual(json.loads(out)["replaces"], ["MV-101", "MV-157"])

    def test_relative_paths_are_read_from_the_cwd(self):
        cwd = os.getcwd()
        os.chdir(self.fx.base)
        self.addCleanup(os.chdir, cwd)
        self.fx.rewrite(self.fx.units, json.dumps([self.fx.spec(
            manifest="manifests/u1.json", registry="in/match.json", readers="in/readers.json",
            comparison="in/dup.json")]).encode())
        code, out, err = self.main("plan", "--entry", "S220", "--root", "m", "--requirements", "in/req.tsv",
                                   "--units", "in/units.json")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, canonical_line(self.fx.expected_plan()))

    def test_core_refusal_exits_2_with_one_line(self):
        self.fx.rewrite(self.fx.req, self.fx.req_text.replace("\tHOLD\t", "\tMOVE\t").encode())
        self.assert_refused(self.main(*self.fx.plan_args()), "MV-101", "not HOLD")

    def test_a_candidate_below_a_file_refuses_with_its_errno(self):
        os.rmdir(os.path.join(self.fx.m, "experiments/c10r/runs"))
        self.fx.write(os.path.join(self.fx.m, "experiments/c10r/runs"), b"")
        self.assert_refused(self.main(*self.fx.plan_args()), self.fx.candidate, "[ENOTDIR]")

    def test_target_lstat_error_names_the_target_and_errno(self):
        with stat_error(errno.EIO, os.path.basename(self.fx.candidate)):
            result = self.main(*self.fx.plan_args())
        self.assert_refused(result, self.fx.candidate, "[EIO]")

    def test_root_that_is_not_a_directory_refuses(self):
        self.assert_refused(self.main(*self.fx.plan_args()[:4], self.fx.req, *self.fx.plan_args()[5:]),
                            self.fx.req, "[ENOTDIR]")

    def test_root_reached_through_a_link_refuses(self):
        link = os.path.join(self.tmp, "linked")
        os.symlink(self.fx.base, link)
        argv = self.fx.plan_args()
        argv[argv.index("--root") + 1] = os.path.join(link, "m")
        self.assert_refused(self.main(*argv), os.path.join(link, "m"), "a component is a link")
        argv[argv.index("--root") + 1] = link
        self.assert_refused(self.main(*argv), link, "[ENOTDIR]")

    def test_cli_prints_the_plan_and_exits_0(self):
        proc = self.cli(*self.fx.plan_args())
        self.assertEqual((proc.returncode, proc.stderr), (0, ""))
        self.assertEqual(proc.stdout, canonical_line(self.fx.expected_plan()))

    def test_cli_refusal_is_one_line_exit_2_without_traceback(self):
        missing = os.path.join(self.fx.inp, "missing.tsv")
        argv = self.fx.plan_args()
        argv[argv.index("--requirements") + 1] = missing
        proc = self.cli(*argv)
        self.assertEqual((proc.returncode, proc.stdout), (2, ""))
        self.assertEqual(proc.stderr, f"{missing!r}: No such file or directory [ENOENT]\n")


class PlanInputs(Base):
    def refuse_units(self, doc, *words):
        self.fx.rewrite(self.fx.units, json.dumps(doc).encode())
        self.assert_refused(self.main(*self.fx.plan_args()), self.fx.units, *words)

    def test_units_file_shapes_refuse(self):
        fx = self.fx
        cases = [{}, [1], [{k: v for k, v in fx.spec().items() if k != "readers"}], [fx.spec(extra=1)],
                 [fx.spec(manifest=5)], [fx.spec(registry=None)], [fx.spec(readers=["x"])],
                 [fx.spec(comparison=5)], [fx.spec(manifest="")]]
        for doc in cases:
            with self.subTest(doc=doc):
                self.refuse_units(doc)

    def test_empty_units_list_is_the_core_refusal(self):
        self.fx.rewrite(self.fx.units, b"[]")
        self.assert_refused(self.main(*self.fx.plan_args()), "units", "at least one unit")

    def test_unit_paths_are_parsed_like_cli_paths(self):
        for bad, word in (("in//match.json", "normalized"), ("in/./match.json", "normalized"), ("in/", "normalized"),
                          ("//in/match.json", "normalized"), ("", "normalized"), ("in/m\tatch.json", "holds a NUL"),
                          ("in/m\x00atch.json", "holds a NUL"), ("in/m\ratch.json", "holds a NUL"),
                          ("in/m\natch.json", "holds a NUL")):
            for key in ("manifest", "registry", "readers", "comparison"):
                with self.subTest(bad=bad, key=key):
                    self.fx.rewrite(self.fx.units, json.dumps([self.fx.spec(**{key: bad})]).encode())
                    self.assert_refused(self.main(*self.fx.plan_args()), self.fx.units, word, repr(bad))

    def test_registry_document_shapes_refuse(self):
        fx = self.fx
        one = fx.match_doc["matches"][0]
        for doc in ({"root": fx.m, "matches": []}, {"root": fx.m, "matches": [one, one]}, {"root": fx.m},
                    {"root": fx.m, "matches": [one], "x": 1}, {"root": fx.m, "matches": one}, [one]):
            with self.subTest(doc=doc):
                fx.rewrite(fx.match, json.dumps(doc).encode())
                self.assert_refused(self.main(*fx.plan_args()), fx.match)

    def test_registry_matches_of_the_wrong_type_refuse(self):
        # MAESTRO T209 RULING-2 ruling 6 (M21): a one-key object or a one-character string has length 1 too.
        fx = self.fx
        for matches in ({"unit": "u1"}, "x"):
            with self.subTest(matches=matches):
                fx.rewrite(fx.match, json.dumps({"root": fx.m, "matches": matches}).encode())
                self.assert_refused(self.main(*fx.plan_args()), fx.match, "holding exactly one match")

    def test_json_inputs_must_be_strict_utf8_json(self):
        for data, word in ((b"\xff[]", "UTF-8"), (b"[", "JSON"), (b'{"stale": [], "stale": []}', "duplicate key"),
                           (b"[NaN]", "NaN"), (b"[Infinity]", "Infinity")):
            for attr in ("units", "match", "readers", "dup"):
                with self.subTest(data=data, attr=attr):
                    fx = self.fresh()
                    fx.rewrite(getattr(fx, attr), data)
                    self.assert_refused(self.main(*fx.plan_args()), getattr(fx, attr), word)

    def test_a_duplicate_key_is_named_exactly(self):
        self.fx.rewrite(self.fx.readers, b'{"stale": [], "stale": []}')
        code, out, err = self.main(*self.fx.plan_args())
        self.assertEqual((code, out, err), (2, "", f"{self.fx.readers!r}: duplicate key 'stale'\n"))

    def test_a_json_escaped_lone_surrogate_refuses(self):
        for attr in ("units", "match", "readers", "dup"):
            with self.subTest(attr=attr):
                fx = self.fresh()
                fx.rewrite(getattr(fx, attr), b'["\\udcff"]')
                self.assert_refused(self.main(*fx.plan_args()), getattr(fx, attr), "holds a lone surrogate")

    def test_cwd_error_for_a_relative_path_names_the_path_and_errno(self):
        argv = self.fx.plan_args()
        argv[argv.index("--units") + 1] = "units.json"
        with mock.patch.object(os, "getcwd", side_effect=OSError(errno.EIO, os.strerror(errno.EIO))):
            result = self.main(*argv)
        self.assert_refused(result, "units.json", "[EIO]")

    def test_requirements_must_be_utf8(self):
        self.fx.rewrite(self.fx.req, b"\xff" + self.fx.req_text.encode())
        self.assert_refused(self.main(*self.fx.plan_args()), self.fx.req, "UTF-8")

    def test_manifest_bytes_are_passed_raw_to_the_core(self):
        self.fx.rewrite(self.fx.manifest, self.fx.manifest_bytes + b"\n")
        self.assert_refused(self.main(*self.fx.plan_args()), "units[0].manifest_bytes", "canonical")


class Arguments(Base):
    def test_cli_strings_with_control_characters_or_lone_surrogates_refuse(self):
        for bad in ("S2\x0020", "S2\t20", "S2\n20", "S2\r20", "S2\r\n20", "S2\udcff20"):
            with self.subTest(bad=bad):
                argv = self.fx.plan_args()
                argv[argv.index("--entry") + 1] = bad
                self.assert_refused(self.main(*argv), bad, "holds a NUL, tab, CR, LF or lone surrogate")
        for bad in (self.fx.hold + "\n", self.fx.hold + "\udcff"):
            with self.subTest(bad=bad):
                argv = self.fx.check_routes_args()
                argv[argv.index("--hold-target") + 1] = bad
                self.assert_refused(self.main(*argv), bad, "holds a NUL, tab, CR, LF or lone surrogate")
        for bad in (self.fx.m + "\r", self.fx.m + "\t", self.fx.m + "\udcff"):
            with self.subTest(bad=bad):
                argv = self.fx.check_plans_args()
                argv[argv.index("--root") + 1] = bad
                self.assert_refused(self.main(*argv), bad, "holds a NUL, tab, CR, LF or lone surrogate")

    def test_non_normalized_paths_refuse(self):
        m = self.fx.m
        for bad in (m + "/", m + "/./", m.replace("/m", "//m"), m + "/../m", "/" + m, ""):
            with self.subTest(bad=bad):
                argv = self.fx.check_plans_args()
                argv[argv.index("--root") + 1] = bad
                self.assert_refused(self.main(*argv), bad, "is not a normalized path")

    def test_a_missing_subcommand_or_option_is_exit_2(self):
        for argv in ([], ["plan"], ["check-plans", "--root", self.fx.m], ["move", "--root", self.fx.m]):
            with self.subTest(argv=argv):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                    move_unit.main(argv)
                self.assertEqual(caught.exception.code, 2)


class CheckPlans(Base):
    def test_clean_repairs_exit_0_with_no_findings(self):
        code, out, err = self.main(*self.fx.check_plans_args())
        self.assertEqual((code, err, out), (0, "", "[]\n"))
        self.assertEqual(self.fx.expected_findings(), ())

    def test_an_occurrence_with_no_row_exits_1_with_the_core_findings(self):
        self.fx.rewrite(self.fx.repairs, f"{REPAIR_HEADER}\n".encode())
        self.fx.repairs_text = f"{REPAIR_HEADER}\n"
        code, out, err = self.main(*self.fx.check_plans_args())
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(out, canonical_line(self.fx.expected_findings()))
        self.assertEqual([f[0] for f in json.loads(out)], ["no-row"])

    def test_the_line_text_comes_from_the_reader_file(self):
        self.fx.rewrite(self.fx.reader, f"intro\nsee {self.fx.old} and {self.fx.old}\n".encode())
        code, out, err = self.main(*self.fx.check_plans_args())
        self.assertEqual((code, err), (1, ""))
        line = f"see {self.fx.old} and {self.fx.old}"
        self.assertEqual(out, canonical_line(self.fx.expected_findings([{**self.fx.stale, "text": line}])))
        self.assertEqual([f[0] for f in json.loads(out)], ["not-once"])

    def test_a_crlf_line_keeps_its_carriage_return(self):
        self.fx.rewrite(self.fx.reader, f"intro\r\nsee {self.fx.old}\r\n".encode())
        code, out, err = self.main(*self.fx.check_plans_args())
        self.assertEqual((code, err, out), (0, "", "[]\n"))

    def test_crlf_text_reaches_the_core_unchanged(self):
        # [LAW:behavior-not-structure] compare the actual text crossing the I/O boundary.
        self.fx.rewrite(self.fx.reader, f"intro\r\nsee {self.fx.old}\r\n".encode())
        with mock.patch.object(core, "check_plans", wraps=core.check_plans) as checked:
            result = self.main(*self.fx.check_plans_args())
        self.assertEqual(result, (0, "[]\n", ""))
        self.assertEqual(checked.call_args.kwargs["occurrences"][0]["text"], f"see {self.fx.old}\r")

    def test_every_readers_report_is_read(self):
        fx = self.fx
        fx.write(os.path.join(fx.docs, "b.md"), f"{fx.old}\n".encode())
        row = {"file": "docs/b.md", "line": 1, "old_text": fx.old, "old": fx.old}
        second = fx.json("readers2.json", {"stale": [row], "unverified": []})
        code, out, err = self.main(*fx.check_plans_args("--readers", second))
        self.assertEqual((code, err), (1, ""))
        occurrences = [{**fx.stale, "text": f"see {fx.old} here"}, {**row, "text": fx.old}]
        self.assertEqual(out, canonical_line(fx.expected_findings(occurrences)))
        self.assertEqual([(f[0], f[1]) for f in json.loads(out)], [("no-row", "docs/b.md")])

    def test_unverified_rows_are_not_occurrences(self):
        self.fx.rewrite(self.fx.readers, json.dumps(
            {"stale": [self.fx.stale], "unverified": [{"file": "docs/zz.md", "reason": "binary"}]}).encode())
        code, out, err = self.main(*self.fx.check_plans_args())
        self.assertEqual((code, err, out), (0, "", "[]\n"))

    def test_reader_rows_that_cannot_be_read_refuse(self):
        fx = self.fx
        cases = [({"file": fx.reader}, "docs"), ({"file": "../m/docs/a.md"}, "docs"), ({"file": "docs//a.md"}, "docs"),
                 ({"file": "docs/./a.md"}, "docs"), ({"file": 5}, "file"), ({"line": "2"}, "line"),
                 ({"line": True}, "line"), ({"line": 0}, "line"), ({"line": 2.0}, "line")]
        for change, _ in cases:
            with self.subTest(change=change):
                fx.rewrite(fx.readers, json.dumps({"stale": [{**fx.stale, **change}], "unverified": []}).encode())
                self.assert_refused(self.main(*fx.check_plans_args()), fx.readers)

    def test_report_shapes_refuse(self):
        fx = self.fx
        missing = {k: v for k, v in fx.stale.items() if k != "old"}
        for doc in ([], {"stale": []}, {"stale": [], "unverified": [], "x": 1}, {"stale": {}, "unverified": []},
                    {"stale": [1], "unverified": []}, {"stale": [missing], "unverified": []},
                    {"stale": [{**fx.stale, "x": 1}], "unverified": []}):
            with self.subTest(doc=doc):
                fx.rewrite(fx.readers, json.dumps(doc).encode())
                self.assert_refused(self.main(*fx.check_plans_args()), fx.readers)

    def test_a_line_past_the_end_of_the_reader_refuses(self):
        self.fx.rewrite(self.fx.readers, json.dumps({"stale": [{**self.fx.stale, "line": 4}],
                                                     "unverified": []}).encode())
        self.assert_refused(self.main(*self.fx.check_plans_args()), f"{self.fx.reader}:4", "no line 4")

    def test_a_reader_line_that_is_not_utf8_refuses(self):
        self.fx.rewrite(self.fx.reader, b"intro\nsee " + self.fx.old.encode() + b" \xff\n")
        self.assert_refused(self.main(*self.fx.check_plans_args()), f"{self.fx.reader}:2", "UTF-8")

    def test_old_text_not_on_its_line_is_the_core_refusal(self):
        self.fx.rewrite(self.fx.reader, b"intro\nnothing here\n")
        self.assert_refused(self.main(*self.fx.check_plans_args()), "occurrences[0]", "not in the text")

    def test_plans_document_shapes_refuse(self):
        fx = self.fx
        for doc in ([], {}, {"entries": [], "schema_version": 1}, fx.plans_doc["entries"][0]):
            with self.subTest(doc=doc):
                fx.rewrite(fx.plans, json.dumps(doc).encode())
                self.assert_refused(self.main(*fx.check_plans_args()), fx.plans)

    def test_empty_entries_is_the_core_refusal(self):
        self.fx.rewrite(self.fx.plans, b'{"entries": []}')
        self.assert_refused(self.main(*self.fx.check_plans_args()), "entries", "never an empty PASS")

    def test_repairs_must_be_utf8(self):
        self.fx.rewrite(self.fx.repairs, b"\xff" + self.fx.repairs_text.encode())
        self.assert_refused(self.main(*self.fx.check_plans_args()), self.fx.repairs, "UTF-8")

    def test_relative_root_and_inputs_are_read_from_the_cwd(self):
        cwd = os.getcwd()
        os.chdir(self.fx.base)
        self.addCleanup(os.chdir, cwd)
        self.fx.rewrite(self.fx.repairs, f"{REPAIR_HEADER}\n".encode())
        self.fx.repairs_text = f"{REPAIR_HEADER}\n"
        code, out, err = self.main("check-plans", "--root", "m", "--plans", "in/plans.json",
                                   "--repairs", "in/repairs.tsv", "--historical", "in/historical.tsv",
                                   "--readers", "in/readers.json")
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(out, canonical_line(self.fx.expected_findings()))

    def test_cli_exits_1_on_a_finding(self):
        self.fx.rewrite(self.fx.repairs, f"{REPAIR_HEADER}\n".encode())
        self.fx.repairs_text = f"{REPAIR_HEADER}\n"
        proc = self.cli(*self.fx.check_plans_args())
        self.assertEqual((proc.returncode, proc.stderr), (1, ""))
        self.assertEqual(proc.stdout, canonical_line(self.fx.expected_findings()))


class CheckRoutes(Base):
    def expected(self, children=("r1", "r2.json")):
        return core.check_routes(routes=(self.fx.routes, self.fx.routes_text), source=self.fx.source,
                                 children=list(children), hold_target=self.fx.hold)

    def test_a_complete_table_exits_0(self):
        code, out, err = self.main(*self.fx.check_routes_args())
        self.assertEqual((code, err, out), (0, "", "[]\n"))
        self.assertEqual(self.expected(), ())

    def test_children_are_the_observed_entries_of_the_source(self):
        self.fx.write(os.path.join(self.fx.source, ".DS_Store"), b"")
        os.symlink("/", os.path.join(self.fx.source, "ln"))
        code, out, err = self.main(*self.fx.check_routes_args())
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(out, canonical_line(self.expected([".DS_Store", "ln", "r1", "r2.json"])))
        self.assertEqual([(f[0], f[1]) for f in json.loads(out)], [("no-row", ".DS_Store"), ("no-row", "ln")])

    def test_relative_source_is_read_from_the_cwd(self):
        cwd = os.getcwd()
        os.chdir(self.fx.base)
        self.addCleanup(os.chdir, cwd)
        code, out, err = self.main("check-routes", "--routes", "in/routes.tsv", "--source", "results",
                                   "--hold-target", self.fx.hold)
        self.assertEqual((code, err, out), (0, "", "[]\n"))

    def test_core_findings_and_refusals_pass_through(self):
        code, out, err = self.main(*self.fx.check_routes_args()[:-1], self.fx.source + "/hold")
        self.assert_refused((code, out, err), "hold_target", "overlaps the source")

    def test_routes_must_be_utf8(self):
        self.fx.rewrite(self.fx.routes, b"\xff" + self.fx.routes_text.encode())
        self.assert_refused(self.main(*self.fx.check_routes_args()), self.fx.routes, "UTF-8")

    def test_source_reached_through_a_link_refuses(self):
        link = os.path.join(self.tmp, "linked")
        os.symlink(self.fx.base, link)
        argv = self.fx.check_routes_args()
        argv[argv.index("--source") + 1] = os.path.join(link, "results")
        self.assert_refused(self.main(*argv), os.path.join(link, "results"), "a component is a link")

    def test_source_moved_after_the_scan_refuses(self):
        with FK.rename_and_rebind("scandir", 1, self.fx.source, when="after"):
            result = self.main(*self.fx.check_routes_args())
        self.assert_refused(result, self.fx.source, "moved while it was held")

    def test_cli_exits_1_on_a_finding(self):
        self.fx.write(os.path.join(self.fx.source, "r3"), b"")
        proc = self.cli(*self.fx.check_routes_args())
        self.assertEqual((proc.returncode, proc.stderr), (1, ""))
        self.assertEqual(proc.stdout, canonical_line(self.expected(["r1", "r2.json", "r3"])))


# Bound objects per subcommand: (fixture attribute, kind). Leaves are opened by name through a held parent.
LEAVES = {"plan": ("req", "units", "manifest", "match", "readers", "dup"),
          "check-plans": ("plans", "repairs", "historical", "readers", "reader"),
          "check-routes": ("routes",)}
DIRS = {"plan": ("m", "inp", "mdir"), "check-plans": ("m", "inp", "docs"), "check-routes": ("inp", "source")}
ARGS = {"plan": Fixture.plan_args, "check-plans": Fixture.check_plans_args, "check-routes": Fixture.check_routes_args}


class Attacks(Base):
    def cases(self, table):
        for cmd, attrs in table.items():
            for attr in attrs:
                fx = self.fresh()
                with self.subTest(cmd=cmd, attr=attr):
                    yield fx, getattr(fx, attr), ARGS[cmd](fx)

    def test_leaf_swapped_for_a_symlink_between_scan_and_open_refuses(self):
        for fx, path, argv in self.cases(LEAVES):
            with FK.swap_for_symlink("open", 1, path, fx.decoy, match=named(os.path.basename(path))):
                result = self.main(*argv)
            self.assert_refused(result, path, "[ELOOP]")

    def test_directory_swapped_for_a_symlink_refuses(self):
        for fx, path, argv in self.cases(DIRS):
            with FK.swap_for_symlink("open", 1, path, fx.other, match=named(path)):
                result = self.main(*argv)
            self.assert_refused(result, path)
            self.assertRegex(result[2], r"\[(ENOTDIR|ELOOP)\]$")  # macOS: O_DIRECTORY on a link is ENOTDIR

    def test_fifo_in_place_of_a_leaf_refuses_without_blocking(self):
        for fx, path, argv in self.cases(LEAVES):
            with FK.fifo_in_place(path):
                result = self.main(*argv)
            self.assert_refused(result, path, "is not a regular file")

    def test_fifo_in_place_of_a_directory_refuses_without_blocking(self):
        for fx, path, argv in self.cases(DIRS):
            with FK.fifo_in_place(path):
                result = self.main(*argv)
            self.assert_refused(result, path, "[ENOTDIR]")

    def test_directory_renamed_and_rebound_refuses(self):
        for fx, path, argv in self.cases(DIRS):
            with FK.rename_and_rebind("open", 1, path, when="after", match=named(path)):
                result = self.main(*argv)
            self.assert_refused(result, path, "a component is a link")

    def test_late_parent_attacks_refuse_for_every_input(self):
        # [LAW:behavior-not-structure] the same late attack must refuse at every input boundary.
        for cmd, attrs in LEAVES.items():
            for attr in attrs:
                for kind in ("rebind", "link"):
                    with self.subTest(cmd=cmd, attr=attr, kind=kind):
                        fx = self.fresh()
                        leaf = getattr(fx, attr)
                        parent = os.path.dirname(leaf)
                        if kind == "link":
                            replacement = os.path.join(fx.other, "replacement")
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
                                result = self.main(*ARGS[cmd](fx))
                        self.assertEqual(fault.fired, 1)
                        self.assert_refused(result, parent)

    def test_leaf_open_errors_name_the_path_and_errno(self):
        for fx, path, argv in self.cases(LEAVES):
            for err in (errno.EIO, errno.EBADF):
                with FK.inject_oserror("open", 1, err, match=named(os.path.basename(path))):
                    result = self.main(*argv)
                self.assert_refused(result, path, f"[{errno.errorcode[err]}]")

    def test_directory_open_errors_name_the_path_and_errno(self):
        for fx, path, argv in self.cases(DIRS):
            with FK.inject_oserror("open", 1, errno.EIO, match=named(path)):
                result = self.main(*argv)
            self.assert_refused(result, path, "[EIO]")

    def test_leaf_lstat_errors_name_the_path_and_errno(self):
        for fx, path, argv in self.cases(LEAVES):
            with lstat_error(errno.EIO, os.path.basename(path)):
                result = self.main(*argv)
            self.assert_refused(result, path, "[EIO]")

    def test_call_class_errors_name_the_path_and_errno(self):
        fx = self.fx
        # [LAW:behavior-not-structure] parent-close faults select the opened fd, not close order.
        cases = [("plan", "fstat", 1, fx.req), ("plan", "read", 1, fx.req), ("plan", GETPATH, 1, fx.m),
                 ("plan", "close", 1, fx.req), ("plan", "close-of", 1, fx.inp), ("plan", "close", 16, fx.m),
                 ("check-plans", "fstat", 1, fx.plans), ("check-plans", "read", 1, fx.plans),
                 ("check-plans", GETPATH, 1, fx.m), ("check-plans", "close", 1, fx.plans),
                 ("check-plans", "close-of", 1, fx.inp), ("check-plans", "close", 11, fx.m),
                 ("check-routes", "fstat", 1, fx.routes), ("check-routes", "read", 1, fx.routes),
                 ("check-routes", GETPATH, 1, fx.inp), ("check-routes", "close", 1, fx.routes),
                 ("check-routes", "close-of", 1, fx.inp), ("check-routes", "scandir", 1, fx.source),
                 ("check-routes", GETPATH, 3, fx.source), ("check-routes", "close-of", 1, fx.source)]
        for cmd, target, n, path in cases:
            for err in (errno.EIO, errno.EBADF):
                with self.subTest(cmd=cmd, target=target, n=n, err=err):
                    if target == "close-of":
                        real, held = os.open, {}

                        def opened(first, *args, **kwargs):
                            fd = real(first, *args, **kwargs)
                            held[fd] = first
                            return fd
                        with mock.patch.object(os, "open", opened), \
                                FK.inject_oserror("close", 1, err, match=lambda fd: held.get(fd) == path):
                            result = self.main(*ARGS[cmd](fx))
                    else:
                        with FK.inject_oserror(target, n, err):
                            result = self.main(*ARGS[cmd](fx))
                    self.assert_refused(result, path, f"[{errno.errorcode[err]}]")

    def test_a_failing_target_prefix_close_names_the_prefix(self):
        # MAESTRO T209 RULING-2 ruling 6 (M56).
        fx = self.fx
        runs = os.path.dirname(fx.candidate)
        real, fds = os.open, {}

        def opened(first, *args, **kwargs):
            fd = real(first, *args, **kwargs)
            if first == "runs" and "dir_fd" in kwargs:
                fds["runs"] = fd
            return fd
        with mock.patch.object(os, "open", opened):
            with FK.inject_oserror("close", 1, errno.EIO, match=lambda fd: fd == fds.get("runs")):
                result = self.main(*fx.plan_args())
        self.assert_refused(result, runs, "[EIO]")

    def test_unexpected_exceptions_propagate(self):
        for cmd, target in (("plan", "read"), ("plan", "open"), ("check-plans", "read"),
                            ("check-routes", "scandir"), ("check-routes", "read")):
            for exc in FK.UNEXPECTED:
                with self.subTest(cmd=cmd, target=target, exc=exc.__name__):
                    with FK.raise_unexpected(target, 1, exc):
                        with self.assertRaises(exc) as caught:
                            self.main(*ARGS[cmd](self.fx))
                    self.assertNotIsInstance(caught.exception, fdsafe.Refusal)

    def test_unexpected_exception_from_a_target_lstat_propagates(self):
        real = os.stat

        def hooked(first, *args, **kwargs):
            if first == os.path.basename(self.fx.candidate) and "dir_fd" in kwargs:
                raise RuntimeError("unexpected")
            return real(first, *args, **kwargs)
        with mock.patch.object(os, "stat", hooked), self.assertRaises(RuntimeError):
            self.main(*self.fx.plan_args())


@contextlib.contextmanager
def root_replaced_at_open(name, root):
    """At the first os.open of name, move root away and put a copy of it (a different real directory) at its
    path, so every later path-based read succeeds against the copy while the held fd names the moved one."""
    real, done = os.open, []

    def hooked(first, *args, **kwargs):
        if first == name and not done:
            done.append(first)
            os.rename(root, root + ".moved")
            shutil.copytree(root + ".moved", root, symlinks=True)
        return real(first, *args, **kwargs)
    with mock.patch.object(os, "open", hooked):
        yield
    if not done:
        raise AssertionError(f"root_replaced_at_open: no os.open of {name!r}")


class HeldRootAndTargets(Base):
    """MAESTRO T209 ruling 1 (one held --root per run, live check before the core) and ruling 2 (a target is
    observed prefix by prefix without following a link)."""

    def test_k1_check_plans_root_replaced_before_a_reader_file_is_read_refuses(self):
        with root_replaced_at_open("readers.json", self.fx.m):
            result = self.main(*self.fx.check_plans_args())
        self.assert_refused(result, self.fx.docs, f"is not below the held root {self.fx.m!r}")

    def test_k1b_check_plans_root_replaced_after_the_last_reader_file_read_refuses(self):
        fx = self.fx
        real_open, real_close, fds, done = os.open, os.close, {}, []

        def opened(path, *args, **kwargs):
            fd = real_open(path, *args, **kwargs)
            fds[fd] = path
            return fd

        def closed(fd):
            result = real_close(fd)
            if fds.get(fd) == fx.docs and not done:
                done.append(fd)
                os.rename(fx.m, fx.m + ".moved")
                shutil.copytree(fx.m + ".moved", fx.m)
            return result
        with mock.patch.object(os, "open", opened), mock.patch.object(os, "close", closed):
            result = self.main(*fx.check_plans_args())
        self.assertEqual(len(done), 1)
        self.assert_refused(result, fx.m, "was moved while it was held")

    def test_k2_plan_root_replaced_before_the_target_observation_refuses(self):
        with root_replaced_at_open("dup.json", self.fx.m):
            result = self.main(*self.fx.plan_args())
        self.assert_refused(result, self.fx.m, "was moved while it was held")

    def link_ancestor(self, fx, real_dir, link, *make):
        os.rename(link, real_dir)
        for rel in make:
            os.makedirs(os.path.join(real_dir, rel))
        os.symlink(real_dir, link)

    def unmatched(self, fx):
        fx.rewrite(fx.units, json.dumps([fx.spec(candidate=None)]).encode())

    def test_k3_a_link_ancestor_to_a_directory_holding_the_target_refuses(self):
        fx = self.fx
        link = os.path.join(fx.m, "experiments", "c10r")
        self.link_ancestor(fx, os.path.join(fx.base, "c10r_real"), link, "runs/u1")
        self.assert_refused(self.main(*fx.plan_args()), fx.candidate, f"component {link!r} is a link")
        fx = self.fresh()
        self.unmatched(fx)
        os.makedirs(os.path.join(fx.base, "v_real", "p", "u1"))
        os.symlink(os.path.join(fx.base, "v_real"), os.path.join(fx.base, "v"))
        self.assert_refused(self.main(*fx.plan_args()), fx.v_target, f"component {fx.base + '/v'!r} is a link")

    def test_k4_a_link_ancestor_to_a_directory_without_the_target_refuses(self):
        fx = self.fx
        link = os.path.join(fx.m, "experiments", "c10r")
        self.link_ancestor(fx, os.path.join(fx.base, "c10r_real"), link)
        self.assert_refused(self.main(*fx.plan_args()), fx.candidate, f"component {link!r} is a link")
        fx = self.fresh()
        self.unmatched(fx)
        os.makedirs(os.path.join(fx.base, "v_real"))
        os.symlink(os.path.join(fx.base, "v_real"), os.path.join(fx.base, "v"))
        self.assert_refused(self.main(*fx.plan_args()), fx.v_target, f"component {fx.base + '/v'!r} is a link")


@contextlib.contextmanager
def swapped_after_observed(prefix, action):
    """Run action() right after the first no-follow observation of prefix, whether by its full path (os.lstat)
    or by its name relative to a held parent (os.stat with dir_fd)."""
    real_lstat, real_stat, done = os.lstat, os.stat, []
    name = os.path.basename(prefix)

    def after(result):
        if not done:
            done.append(1)
            action()
        return result

    def lstat(first, *args, **kwargs):
        result = real_lstat(first, *args, **kwargs)
        return after(result) if first == prefix else result

    def stat_(first, *args, **kwargs):
        result = real_stat(first, *args, **kwargs)
        observed = first == prefix or (first == name and "dir_fd" in kwargs)
        return after(result) if observed and kwargs.get("follow_symlinks") is False else result
    with mock.patch.object(os, "lstat", lstat), mock.patch.object(os, "stat", stat_):
        yield
    if not done:
        raise AssertionError(f"swapped_after_observed: {prefix!r} was never observed")


class HeldIdentity(Base):
    """MAESTRO T209 ruling 4: D1 (a target prefix swapped for a link after its own observation) and D2 (--root
    moved away and back around a reader file read) both refuse."""

    def test_k5_a_target_prefix_swapped_for_a_link_after_its_observation_refuses(self):
        fx = self.fx
        c10r = os.path.join(fx.m, "experiments", "c10r")
        os.makedirs(os.path.join(fx.base, "c10r_real", "runs", "u1"))

        def to_link():
            os.rename(c10r, c10r + ".gone")
            os.symlink(os.path.join(fx.base, "c10r_real"), c10r)
        with swapped_after_observed(c10r, to_link):
            result = self.main(*fx.plan_args())
        self.assert_refused(result, fx.candidate)
        self.assertRegex(result[2], r"\[(ENOTDIR|ELOOP)\]$")  # macOS: O_DIRECTORY on a link is ENOTDIR

    def test_k6_root_moved_away_and_back_around_a_reader_file_read_refuses(self):
        fx = self.fx
        real_open, real_close, fds, state = os.open, os.close, {}, set()

        def opened(path, *args, **kwargs):
            if path == fx.docs and "away" not in state:
                state.add("away")
                os.rename(fx.m, fx.m + ".away")
                shutil.copytree(fx.m + ".away", fx.m)
                fx.rewrite(fx.reader, f"intro\nforged {fx.old}\n".encode())
            fd = real_open(path, *args, **kwargs)
            fds[fd] = path
            return fd

        def closed(fd):
            result = real_close(fd)
            if fds.get(fd) == fx.docs and "back" not in state:
                state.add("back")
                shutil.rmtree(fx.m)
                os.rename(fx.m + ".away", fx.m)
            return result
        with mock.patch.object(os, "open", opened), mock.patch.object(os, "close", closed):
            result = self.main(*fx.check_plans_args())
        self.assertEqual(state, {"away", "back"})
        self.assert_refused(result, fx.docs, f"is not below the held root {fx.m!r}")

    def test_identity_check_errors_name_the_path_and_errno(self):
        # fstat 1-8 check plans.json, repairs.tsv, historical.tsv and readers.json; 9 is the root's.
        with FK.inject_oserror("fstat", 9, errno.EIO):
            result = self.main(*self.fx.check_plans_args())
        self.assert_refused(result, self.fx.m, "[EIO]")
        real = os.stat

        def hooked(first, *args, **kwargs):
            if first == "." and "dir_fd" in kwargs:
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(first, *args, **kwargs)
        with mock.patch.object(os, "stat", hooked):
            result = self.main(*self.fx.check_plans_args())
        self.assert_refused(result, self.fx.docs, "[EIO]")


@contextlib.contextmanager
def after_open_then(name, action):
    """Run action() at the first os.read after the first os.open of name: the file is open and its parent
    has had its last use before the read."""
    real_open, real_read, state = os.open, os.read, []

    def opened(first, *args, **kwargs):
        fd = real_open(first, *args, **kwargs)
        if first == name and not state:
            state.append("open")
        return fd

    def read(fd, n):
        if state == ["open"]:
            state.append("done")
            action()
        return real_read(fd, n)
    with mock.patch.object(os, "open", opened), mock.patch.object(os, "read", read):
        yield
    if state != ["open", "done"]:
        raise AssertionError(f"after_open_then: no read after the open of {name!r} ({state})")


class HeldAfterUse(Base):
    """MAESTRO T209 RULING-2 ruling 5: every directory the tool holds is after-checked once its last use is
    past (still at its path, still below the held root by identity). K7-K10 are the reviewer's probes."""

    def test_k7_a_target_prefix_rebound_after_its_open_refuses(self):
        fx = self.fx
        runs = os.path.dirname(fx.candidate)
        real, done = os.stat, []

        def stat_(first, *args, **kwargs):
            if first == "u1" and "dir_fd" in kwargs and not done:
                done.append(first)
                os.mkdir(fx.candidate)  # the target now exists at its path, not in the parked directory
            return real(first, *args, **kwargs)
        with FK.rename_and_rebind("open", 1, runs, when="after", match=named("runs")):
            with mock.patch.object(os, "stat", stat_):
                result = self.main(*fx.plan_args())
        self.assertEqual(done, ["u1"])
        self.assert_refused(result, runs, "was moved while it was held")

    def test_k8_a_target_prefix_swapped_for_a_link_after_its_open_refuses(self):
        fx = self.fx
        runs = os.path.dirname(fx.candidate)
        outside = fx.mk("outside")
        os.mkdir(os.path.join(outside, "u1"))
        with FK.swap_for_symlink("open", 1, runs, outside, when="after", match=named("runs")):
            result = self.main(*fx.plan_args())
        self.assertTrue(os.path.isdir(fx.candidate))  # occupied through the link
        self.assert_refused(result, runs, "was moved while it was held")

    def test_k9_a_reader_parent_moved_outside_the_root_during_the_read_refuses(self):
        fx = self.fx
        with FK.rename_and_rebind("open", 1, fx.docs, when="after", match=named("a.md")) as fault:
            with after_open_then("a.md", lambda: os.rename(fault.parked, os.path.join(fx.other, "docs"))):
                result = self.main(*fx.check_plans_args())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, fx.docs, "was moved while it was held", fx.other)

    def test_k10_a_reader_parent_rebound_with_a_forged_reader_refuses(self):
        fx = self.fx
        forged = f"intro\n{fx.old} {fx.old}\n".encode()
        with FK.rename_and_rebind("open", 1, fx.docs, when="after", match=named("a.md")):
            with after_open_then("a.md", lambda: fx.write(fx.reader, forged)):
                result = self.main(*fx.check_plans_args())
        self.assert_refused(result, fx.docs, "was moved while it was held")
        self.assertEqual(self.main(*fx.check_plans_args())[0], 1)  # the forged reader is a finding when read

    def test_a_reader_parent_moved_into_a_new_root_refuses_by_identity(self):
        # The parent is back at its path, but under a different directory than the held root.
        fx = self.fx

        def move():
            os.rename(fx.m, fx.m + ".away")
            os.mkdir(fx.m)
            os.rename(os.path.join(fx.m + ".away", "docs"), fx.docs)
        with after_open_then("a.md", move):
            result = self.main(*fx.check_plans_args())
        self.assert_refused(result, fx.docs, f"is not below the held root {fx.m!r}")

    def test_a_v_target_prefix_rebound_after_its_open_refuses(self):
        fx = self.fx
        fx.rewrite(fx.units, json.dumps([fx.spec(candidate=None)]).encode())
        v = os.path.join(fx.base, "v")
        os.makedirs(os.path.join(v, "p"))
        with FK.rename_and_rebind("open", 1, v, when="after", match=named("v")):
            result = self.main(*fx.plan_args())
        self.assert_refused(result, v, "was moved while it was held")

    def test_plan_root_replaced_with_no_target_below_it_refuses(self):
        fx = self.fx
        fx.rewrite(fx.units, json.dumps([fx.spec(candidate=None)]).encode())
        with root_replaced_at_open("dup.json", fx.m):
            result = self.main(*fx.plan_args())
        self.assert_refused(result, fx.m, "was moved while it was held")


class ReadOnly(Base):
    def opened(self, events) -> set:
        return {str(args[0]) for event, args in events if event == "open"}

    def check(self, argv, expected_opens, code):
        with recording() as events:
            result = self.main(*argv)
            during = list(events)
            # Positive control: the same window records a write-open, a mkdir and a process.
            control = os.path.join(self.tmp, "control")
            os.mkdir(control)
            with open(os.path.join(control, "w"), "w"):
                pass
            subprocess.run(["/usr/bin/true"], check=True)
        self.assertEqual(result[0], code, result[2])
        kinds = {event for event, _ in events}
        self.assertLessEqual({"open", "os.mkdir", "subprocess.Popen"}, kinds)
        self.assertEqual([e for e in during if e[0] != "open"], [])
        writes = [args for event, args in during if event == "open"
                  and ((isinstance(args[1], str) and set(args[1]) & set("wax+"))
                       or (isinstance(args[2], int) and args[2] & WRITE_FLAGS))]
        self.assertEqual(writes, [])
        self.assertEqual(self.opened(during), set(expected_opens))
        os.unlink(os.path.join(control, "w"))
        os.rmdir(control)

    def test_plan_opens_only_its_inputs_to_read_and_changes_nothing(self):
        fx = self.fx
        os.mkdir(fx.candidate)
        # The target observation opens each directory above the candidate by name below --root, and "/" and
        # each directory above the V target (the fixture base, then an absent v).
        observed = {"experiments", "c10r", "runs", "/", *fx.base.strip("/").split("/")}
        self.check(fx.plan_args(), {fx.m, fx.inp, fx.mdir, "req.tsv", "units.json", "u1.json", "match.json",
                                    "readers.json", "dup.json", *observed}, 0)

    def test_check_plans_opens_only_its_inputs_to_read_and_changes_nothing(self):
        fx = self.fx
        self.check(fx.check_plans_args(), {fx.m, fx.inp, fx.docs, "plans.json", "repairs.tsv", "readers.json",
                                           "historical.tsv", "a.md"}, 0)

    def test_check_routes_opens_only_its_inputs_to_read_and_changes_nothing(self):
        fx = self.fx
        self.check(fx.check_routes_args(), {fx.inp, fx.source, "routes.tsv"}, 0)


class HeldParentIdentity(Base):
    """MAESTRO T209 RULING-5 rulings 13-15: an input parent's after-check refuses when its path now names another
    directory although the held fd still reports that path (macOS F_GETPATH keeps a removed directory's path),
    and an error in that identity check is a refusal naming the parent and the errno."""

    def test_an_input_parent_removed_and_remade_at_its_path_refuses(self):
        fx = self.fx
        aside = os.path.join(fx.other, "u1.json")

        def remake():
            os.rename(fx.manifest, aside)
            os.rmdir(fx.mdir)
            os.mkdir(fx.mdir)
            os.rename(aside, fx.manifest)
        with after_open_then("u1.json", remake):
            result = self.main(*fx.plan_args())
        self.assert_refused(result, fx.mdir, "was moved during the run")

    def test_an_input_parent_covered_by_another_device_at_its_path_refuses(self):
        # A volume mounted over the parent: the same inode number (volume roots are all 2), another st_dev.
        fx, real = self.fx, os.stat

        def stat_(first, *args, **kwargs):
            st = real(first, *args, **kwargs)
            if first != fx.mdir or "dir_fd" in kwargs:
                return st
            fields = list(st)
            fields[2] = st.st_dev + 1  # stat_result index 2 is st_dev; st_ino (index 1) is kept
            return os.stat_result(fields)
        with mock.patch.object(os, "stat", stat_):
            result = self.main(*fx.plan_args())
        self.assert_refused(result, fx.mdir, "was moved during the run")

    def test_an_input_parent_identity_error_names_the_path_and_errno(self):
        fx, real, calls = self.fx, os.stat, []

        def stat_(first, *args, **kwargs):
            if first == fx.mdir and "dir_fd" not in kwargs and not calls:
                calls.append(first)
                raise OSError(errno.EACCES, os.strerror(errno.EACCES))
            return real(first, *args, **kwargs)
        with mock.patch.object(os, "stat", stat_):
            result = self.main(*fx.plan_args())
        self.assertEqual(calls, [fx.mdir])
        self.assert_refused(result, fx.mdir, "[EACCES]")


class RefusalPathRendering(Base):
    """Filesystem names remain one stderr line at every reason interpolation."""

    def moved_parent(self, suffix):
        fx = self.fx
        moved = fx.mdir + suffix
        with after_open_then("u1.json", lambda: os.rename(fx.mdir, moved)):
            result = self.main(*fx.plan_args())
        self.assert_refused(result, fx.mdir, f"was moved while it was held (now {moved!r})")

    def test_live_parent_with_lf_is_one_line(self):
        self.moved_parent("\nrenamed")

    def test_live_parent_with_cr_is_one_line(self):
        self.moved_parent("\rrenamed")

    def test_candidate_with_lf_observation_error_is_one_line(self):
        fx = self.fx
        candidate = fx.candidate + "\nleaf"
        fx.rewrite(fx.units, json.dumps([fx.spec(candidate=candidate)]).encode())
        with stat_error(errno.EACCES, os.path.basename(candidate)):
            result = self.main(*fx.plan_args())
        self.assert_refused(result, candidate, f"(at {candidate!r})", "[EACCES]")

    def test_candidate_with_lf_link_is_one_line(self):
        fx = self.fx
        candidate = fx.candidate + "\nleaf"
        fx.rewrite(fx.units, json.dumps([fx.spec(candidate=candidate)]).encode())
        os.symlink(fx.other, candidate)
        self.assert_refused(self.main(*fx.plan_args()), candidate, f"component {candidate!r} is a link")

    def test_relative_root_under_lf_cwd_containment_is_one_line(self):
        fx = self.fx
        root = fx.m + "\nroot"
        os.rename(fx.m, root)
        argv = fx.check_plans_args()
        argv[argv.index("--root") + 1] = "."
        # [LAW:behavior-not-structure] cwd contributes bytes absent from the validated CLI spelling.
        with contextlib.chdir(root), root_replaced_at_open("readers.json", root):
            result = self.main(*argv)
        self.assert_refused(result, os.path.join(root, "docs"), f"is not below the held root {root!r}")


class IsolatedInputParents(Base):
    """Each input's own held parent must refuse independently of every other input."""

    def moved_input(self, command, attr):
        fx = self.fx
        old = getattr(fx, attr)
        parent = fx.mk("isolated-" + attr)
        leaf = os.path.join(parent, os.path.basename(old))
        os.rename(old, leaf)
        setattr(fx, attr, leaf)
        fx.rewrite(fx.units, json.dumps([fx.spec()]).encode())
        argv = ARGS[command](fx)
        self.assertEqual(self.main(*argv)[0], 0)
        # [LAW:behavior-not-structure] replacement bytes stay valid; only this parent's identity changes.
        with FK.rename_and_rebind("open", 1, parent, when="after", match=named(os.path.basename(leaf))) as fault:
            with after_open_then(os.path.basename(leaf),
                                 lambda: shutil.copytree(fault.parked, parent, dirs_exist_ok=True)):
                result = self.main(*argv)
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, parent, "was moved while it was held")

    def test_units_parent_moved_alone_refuses(self):
        self.moved_input("plan", "units")

    def test_registry_parent_moved_alone_refuses(self):
        self.moved_input("plan", "match")

    def test_readers_report_parent_moved_alone_refuses(self):
        self.moved_input("plan", "readers")

    def test_comparison_parent_moved_alone_refuses(self):
        self.moved_input("plan", "dup")

    def test_repairs_parent_moved_alone_refuses(self):
        self.moved_input("check-plans", "repairs")


class DecoderLimits(Base):
    """Decoder limits obey the same CLI refusal contract for either JSON input."""

    def refuse_limit(self, command, attr, data, reason):
        # [LAW:behavior-not-structure] Real file bytes cross the CLI boundary without decoder mocks.
        path = getattr(self.fx, attr)
        self.fx.rewrite(path, data)
        self.assert_refused(self.main(*ARGS[command](self.fx)), path, reason)

    def test_plan_units_deep_nesting_refuses(self):
        self.refuse_limit("plan", "units", b"[" * 200000, "nests too deeply")

    def test_plan_units_large_integer_refuses(self):
        self.refuse_limit("plan", "units", b"1" * 5000, "integer of 5000 digits")

    def test_check_plans_deep_nesting_refuses(self):
        self.refuse_limit("check-plans", "plans", b"[" * 200000, "nests too deeply")

    def test_check_plans_large_integer_refuses(self):
        self.refuse_limit("check-plans", "plans", b"1" * 5000, "integer of 5000 digits")


class RuledBoundaryCases(Base):
    """RULING-11: after-live parent swaps, cross-device root ABA, and final reader lines."""

    def test_k22_manifest_parent_symlink_after_live_refuses(self):
        fx, real_stat, fired = self.fx, os.stat, []

        def stat_(path, *args, **kwargs):
            # [LAW:no-ambient-temporal-coupling] Attack the stat boundary after live(), without sleeps.
            if path == fx.mdir and "dir_fd" not in kwargs and not fired:
                fired.append(path)
                os.rename(fx.mdir, fx.mdir + ".parked")
                os.symlink(fx.mdir + ".parked", fx.mdir)
            return real_stat(path, *args, **kwargs)

        with mock.patch.object(os, "stat", stat_):
            result = self.main(*fx.plan_args())
        self.assertEqual(fired, [fx.mdir])
        self.assertTrue(os.path.islink(fx.mdir))
        self.assert_refused(result, fx.mdir, "was moved during the run")

    def test_k23_root_aba_same_inode_other_device_refuses_before_reader(self):
        fx = self.fx
        real_open, real_close, real_stat = os.open, os.close, os.stat
        root_st = real_stat(fx.m)
        fds, state, readers, injected = {}, set(), [], []

        def opened(path, *args, **kwargs):
            if path == fx.docs and "away" not in state:
                state.add("away")
                os.rename(fx.m, fx.m + ".away")
                shutil.copytree(fx.m + ".away", fx.m)
                fx.rewrite(fx.reader, f"intro\nforged {fx.old} {fx.old}\n".encode())
            fd = real_open(path, *args, **kwargs)
            fds[fd] = path
            if path == "a.md":
                readers.append(fd)
            return fd

        def closed(fd):
            result = real_close(fd)
            if fds.get(fd) == fx.docs and "back" not in state:
                state.add("back")
                shutil.rmtree(fx.m)
                os.rename(fx.m + ".away", fx.m)
            return result

        def stat_(path, *args, **kwargs):
            st = real_stat(path, *args, **kwargs)
            if (path in ("..", "./..") and fds.get(kwargs.get("dir_fd")) == fx.docs
                    and state == {"away"}):
                # [LAW:behavior-not-structure] Inject mount identity; replacement bytes and I/O stay real.
                fields = list(st)
                fields[1], fields[2] = root_st.st_ino, root_st.st_dev + 1
                injected.append((fields[2], fields[1]))
                return os.stat_result(fields)
            return st

        with mock.patch.object(os, "open", opened), mock.patch.object(os, "close", closed), \
                mock.patch.object(os, "stat", stat_):
            result = self.main(*fx.check_plans_args())
        self.assertEqual(state, {"away", "back"})
        self.assertEqual(set(injected), {(root_st.st_dev + 1, root_st.st_ino)})
        self.assert_refused(result, fx.docs, f"is not below the held root {fx.m!r}")
        self.assertEqual(readers, [])

    def test_k24_reader_final_line_without_terminal_lf_is_valid(self):
        fx = self.fx
        fx.rewrite(fx.reader, f"intro\nsee {fx.old} here".encode())
        self.assertEqual(self.main(*fx.check_plans_args()), (0, "[]\n", ""))


if __name__ == "__main__":
    unittest.main()
