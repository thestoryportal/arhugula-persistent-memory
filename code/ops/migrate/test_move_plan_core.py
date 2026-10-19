"""Tests for move_plan_core: the pure core of move_unit plan, check-plans and check-routes (Step 217).

The core takes rows and values (TSV texts with their names, manifest bytes, Step 206 matches, Step 207
reports, Step 216 rows, observed paths) and returns the plan or the findings. RED list for a pure
function: malformed input of each field, boundary values and unexpected types; each refuses with
fdsafe.Refusal, which names the offending input.
"""
from __future__ import annotations

import builtins
import contextlib
import copy
import hashlib
import io
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as core

_INODES = itertools.count(100)
M = "/m"
HEADER = "requirement_id\tsource\ttarget\taction\tobserved_bytes\tclass\tlane\tcheck_id\tadmission\tprd_ids"
DEFAULT = object()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def req_row(rid, source, target, action="HOLD", observed=3):
    return "\t".join([rid, source, target, action, str(observed), "legacy-science-unit",
                      "legacy-preservation", "C-HOLD", "G4+G5; reader hold", "ICM-R4"])


def table(*rows, name="/m/plans/MOVE-REQUIREMENTS.tsv", eol="\n"):
    return (name, eol.join([HEADER, *rows]) + eol)


def leaf(root, rel, data=b"abc"):
    return {"source": f"{root}/{rel}", "kind": "file", "bytes": len(data), "sha256": sha(data),
            "link_text": None, "device": 16777230, "inode": next(_INODES), "nlink": 1}


def manifest_bytes(root, *leaves, git_roots=()):
    return canonical({"schema_version": 1, "root": root, "leaves": list(leaves), "git_roots": list(git_roots)})


def match(unit, result="none", experiment_id=None, candidates=()):
    return {"unit": unit, "result": result, "experiment_id": experiment_id,
            "candidates": list(candidates), "unknown": [], "evidence": []}


def exact(unit, eid="c10r"):
    return match(unit, "exact", eid, [eid])


def unit(name="u1", rid="MV-101", data=b"abc", registry=DEFAULT, candidate=DEFAULT, readers=None,
         comparison=DEFAULT, git_roots=()):
    root = f"/p/{name}"
    lf = leaf(root, "a.json", data)
    return {"requirement_id": rid, "manifest_path": f"/m/program/units/{name}.json",
            "manifest_bytes": manifest_bytes(root, lf, git_roots=git_roots),
            "registry": exact(name) if registry is DEFAULT else registry,
            "candidate": f"/m/experiments/c10r/runs/{name}" if candidate is DEFAULT else candidate,
            "readers": readers or {"stale": [], "unverified": []},
            "comparison": ([{"source": lf["source"], "relpath": "a.json", "class": "unique", "equal_to": [],
                             "differing_from": [], "same_inode": [], "hint": None}]
                           if comparison is DEFAULT else comparison)}


def plan(units=DEFAULT, tables=DEFAULT, existing=(), entry_id="S220", root=M):
    tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1"), req_row("MV-102", "/p/u2", "/v/p/u2"))] \
        if tables is DEFAULT else tables
    return core.build_plan(entry_id=entry_id, root=root, requirement_tables=tables,
                           units=[unit()] if units is DEFAULT else units,
                           existing_targets=list(existing) if isinstance(existing, (list, tuple)) else existing)


def risks(result, kind):
    return [r for r in result["risks"] if r["kind"] == kind]


class BuildPlan(unittest.TestCase):
    def test_exact_registry_and_absent_candidate_place_the_unit_at_the_candidate(self):
        p = plan()
        self.assertEqual(p["moves"], [{"source": "/p/u1", "target": "/m/experiments/c10r/runs/u1",
            "id": "MV-101", "prd_ids": ["ICM-R4"], "action": "MOVE", "kind": "directory",
            "bytes": 3, "before_sha256": p["units"][0]["manifest"]["sha256"],
            "source_manifest": p["units"][0]["manifest"], "lane": "legacy-preservation",
            "reader_check_ids": []}])
        u = p["units"][0]
        self.assertEqual((u["basis"], u["experiment_id"], u["target"]),
                         ("registry", "c10r", "/m/experiments/c10r/runs/u1"))
        self.assertEqual(p["id"], "S220")
        self.assertEqual(p["replaces"], ["MV-101"])
        self.assertEqual(p["risks"], [])

    def test_registry_none_keeps_the_exact_v_target(self):
        p = plan([unit(registry=match("u1"))])
        self.assertEqual(p["moves"][0]["target"], "/v/p/u1")
        self.assertEqual(p["units"][0]["basis"], "v-target")
        self.assertIsNone(p["units"][0]["experiment_id"])
        self.assertEqual(risks(p, "registry-none"), [{"requirement_id": "MV-101", "kind": "registry-none",
                                                     "items": []}])

    def test_registry_ambiguous_keeps_the_v_target_and_lists_the_candidates(self):
        p = plan([unit(registry=match("u1", "ambiguous", None, ["c10r", "c9"]))])
        self.assertEqual(p["moves"][0]["target"], "/v/p/u1")
        self.assertEqual(risks(p, "registry-ambiguous")[0]["items"], ["c10r", "c9"])

    def test_existing_candidate_keeps_the_v_target(self):
        p = plan(existing=["/m/experiments/c10r/runs/u1"])
        self.assertEqual(p["moves"][0]["target"], "/v/p/u1")
        self.assertEqual(p["units"][0]["basis"], "v-target")
        self.assertEqual(risks(p, "candidate-exists")[0]["items"], ["/m/experiments/c10r/runs/u1"])

    def test_exact_registry_without_candidate_keeps_the_v_target(self):
        p = plan([unit(candidate=None)])
        self.assertEqual(p["moves"][0]["target"], "/v/p/u1")
        self.assertEqual(len(risks(p, "no-candidate")), 1)

    def test_candidate_is_ignored_when_the_registry_is_not_exact(self):
        p = plan([unit(registry=match("u1"), candidate="/m/experiments/other/runs/u1")])
        self.assertEqual(p["moves"][0]["target"], "/v/p/u1")

    def test_other_existing_paths_do_not_block(self):
        p = plan(existing=["/m/experiments/c10r/runs/u1x", "/m/experiments/c10r/runs"])
        self.assertEqual(p["moves"][0]["target"], "/m/experiments/c10r/runs/u1")

    def test_a_crlf_annex_and_an_lf_amendment_are_both_read(self):
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1"), eol="\r\n"),
                  table(req_row("MV-102", "/p/u2", "/v/p/u2"), name="/m/plans/AMENDMENT-1.tsv")]
        p = plan([unit(registry=match("u1")), unit("u2", "MV-102", registry=match("u2"))], tables=tables)
        self.assertEqual([m["target"] for m in p["moves"]], ["/v/p/u1", "/v/p/u2"])

    def test_two_units_sorted_moves_bytes_roots_and_inverted_rollback(self):
        p = plan([unit("u2", "MV-102", b"12345"), unit()])
        self.assertEqual(p["replaces"], ["MV-101", "MV-102"])
        self.assertEqual([m["source"] for m in p["moves"]], ["/p/u1", "/p/u2"])
        self.assertEqual(p["rollback"], [{"source": "/m/experiments/c10r/runs/u2", "target": "/p/u2"},
                                         {"source": "/m/experiments/c10r/runs/u1", "target": "/p/u1"}])
        self.assertEqual(p["bytes"], 8)
        self.assertEqual([u["bytes"] for u in p["units"]], [3, 5])
        self.assertEqual([u["leaves"] for u in p["units"]], [1, 1])
        self.assertEqual(p["roots"], {"sources": ["/p/u1", "/p/u2"],
                                      "targets": ["/m/experiments/c10r/runs/u1", "/m/experiments/c10r/runs/u2"]})

    def test_manifest_is_named_by_path_and_the_sha256_of_its_bytes(self):
        u = unit()
        p = plan([u])
        self.assertEqual(p["units"][0]["manifest"], {"path": u["manifest_path"],
                                                     "sha256": sha(u["manifest_bytes"])})
        self.assertEqual(p["units"][0]["source"], "/p/u1")

    def test_digest_is_the_sha256_of_the_canonical_plan_body_and_approval_names_it(self):
        p = plan()
        body = {k: v for k, v in p.items() if k not in ("digest", "approval")}
        self.assertEqual(p["digest"], sha(canonical(body)))
        self.assertEqual(p["approval"], f"G4 approve S220 sha256:{p['digest']}")
        self.assertEqual(set(p), {"schema_version", "id", "replaces", "units", "moves", "bytes", "roots",
                                  "risks", "checks", "rollback", "digest", "approval"})

    def test_digest_is_stable_and_changes_with_any_input(self):
        units = [unit()]
        first = plan(copy.deepcopy(units))["digest"]
        self.assertEqual(first, plan(copy.deepcopy(units))["digest"])
        self.assertNotEqual(first, plan(copy.deepcopy(units), entry_id="S221")["digest"])
        changed = copy.deepcopy(units)
        changed[0]["candidate"] = "/m/experiments/c10r/runs/other"
        self.assertNotEqual(first, plan(changed)["digest"])

    def test_checks_name_each_unit_and_the_staging_check(self):
        self.assertEqual(plan()["checks"], ["MV-101 C-MOVE", "MV-101 manifest-digest", "MV-101 target-absent",
                                            "stage-check"])

    def test_bytes_differing_from_the_annex_are_a_risk(self):
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1", observed=4))]
        p = plan(tables=tables)
        self.assertEqual(risks(p, "bytes-drift")[0]["items"], ["annex 4", "manifest 3"])
        self.assertEqual(p["units"][0]["observed_bytes"], 4)
        self.assertEqual(risks(plan(), "bytes-drift"), [])

    def test_readers_and_unverified_readers_are_risks(self):
        readers = {"stale": [{"file": "code/x.py", "line": 3, "old_text": "/p/u1/a.json", "old": "/p/u1"},
                             {"file": "code/x.py", "line": 9, "old_text": "/p/u1", "old": "/p/u1"}],
                   "unverified": [{"file": "code/y.py", "reason": "dynamic", "line": 2, "text": "/p/u"},
                                  {"file": "img.bin", "reason": "binary"}]}
        p = plan([unit(readers=readers)])
        self.assertEqual(risks(p, "readers")[0]["items"], ["code/x.py:3", "code/x.py:9"])
        self.assertEqual(risks(p, "unverified-readers")[0]["items"], ["code/y.py:2 dynamic", "img.bin binary"])

    def test_relative_reader_old_path_is_bound_against_the_root(self):
        tables = [table(req_row("MV-101", "/m/results/u1", "/v/m/results/u1"))]
        u = unit()
        lf = leaf("/m/results/u1", "a.json")
        u.update(manifest_bytes=manifest_bytes("/m/results/u1", lf), comparison=None, candidate=None,
                 readers={"stale": [{"file": "a.md", "line": 1, "old_text": "results/u1", "old": "results/u1"}],
                          "unverified": []})
        p = plan([u], tables=tables)
        self.assertEqual(risks(p, "readers")[0]["items"], ["a.md:1"])

    def test_nested_git_roots_are_a_risk(self):
        g = [{"path": "/p/u1", "head": None, "branch": None, "dirty": []},
             {"path": "/p/u1/sub", "head": "a" * 40, "branch": "refs/heads/main", "dirty": [" M x"]}]
        self.assertEqual(risks(plan([unit(git_roots=g)]), "nested-git")[0]["items"], ["/p/u1", "/p/u1/sub"])

    def test_comparison_classes_and_a_missing_comparison_are_risks(self):
        u = unit()
        u["comparison"][0]["class"] = "differing"
        self.assertEqual(risks(plan([u]), "differing")[0]["items"], ["/p/u1/a.json"])
        u["comparison"][0]["class"] = "equal"
        self.assertEqual(risks(plan([u]), "equal")[0]["items"], ["/p/u1/a.json"])
        self.assertEqual(len(risks(plan([unit(comparison=None)]), "no-comparison")), 1)

    def test_plan_has_no_delete_overwrite_or_commit_action(self):
        text = json.dumps(plan([unit(comparison=None)]))
        for word in ("delete", "overwrite", "commit", "purge", "unlink", "\"rm\""):
            self.assertNotIn(word, text)

    def test_inputs_are_not_mutated(self):
        units = [unit(), unit("u2", "MV-102")]
        before = copy.deepcopy(units)
        plan(units)
        self.assertEqual(units, before)

    def test_id_characters(self):
        for good in ("9S", "S_a.b-C9", "Sz"):
            self.assertEqual(plan(entry_id=good)["id"], good)
        p = plan([unit(registry=exact("u1", "C9.r_x-1"), candidate="/m/experiments/C9.r_x-1/runs/u1")])
        self.assertEqual(p["units"][0]["experiment_id"], "C9.r_x-1")

    def test_tuples_are_accepted_for_sequences(self):
        tables = (table(req_row("MV-101", "/p/u1", "/v/p/u1")),)
        p = core.build_plan(entry_id="S220", root=M, requirement_tables=tables, units=(unit(),),
                            existing_targets=())
        self.assertEqual(p["moves"][0]["source"], "/p/u1")


class BuildPlanRefuses(unittest.TestCase):
    def refuses(self, names=None, **kw):
        with self.assertRaises(fdsafe.Refusal) as caught:
            plan(**kw)
        if names is not None:
            self.assertEqual(caught.exception.path, names)
            self.assertIn(repr(names), str(caught.exception))
        return caught.exception

    def test_entry_id(self):
        for bad in ("", "S 220", None, 220, "-S"):
            self.refuses("entry_id", entry_id=bad)

    def test_root(self):
        for bad in ("m", "/m/", "/m/../m", "//m", None, b"/m", "/m\0"):
            self.refuses("root", root=bad)

    def test_requirement_table_shapes(self):
        for bad in (None, "x", [("n",)], [("n", "t", "x")], [(1, "t")], [("n", b"t")]):
            self.refuses(tables=bad)

    def test_requirement_table_text(self):
        good = req_row("MV-101", "/p/u1", "/v/p/u1")
        cases = {
            "no final newline": ("n", HEADER + "\n" + good),
            "empty": ("n", ""),
            "wrong header": ("n", HEADER.replace("source", "src") + "\n" + good + "\n"),
            "short row": ("n", HEADER + "\n" + good.rsplit("\t", 1)[0] + "\n"),
            "long row": ("n", HEADER + "\n" + good + "\tx\n"),
            "mixed endings": ("n", HEADER + "\r\n" + good + "\n"),
            "bare cr": ("n", HEADER + "\n" + good.replace("ICM", "IC\rM") + "\n"),
            "control char": ("n", HEADER + "\n" + good.replace("ICM", "IC\x01M") + "\n"),
            "delete char": ("n", HEADER + "\n" + good.replace("ICM", "IC\x7fM") + "\n"),
            "surrogate source": ("n", HEADER + "\n" + good.replace("/p/u1", "/p/u\udcff") + "\n"),
            "bad id": ("n", HEADER + "\n" + good.replace("MV-101", "MV-1") + "\n"),
            "relative source": ("n", HEADER + "\n" + good.replace("\t/p/u1\t", "\tp/u1\t") + "\n"),
            "relative target": ("n", HEADER + "\n" + good.replace("/v/p/u1", "v/p/u1") + "\n"),
            "bytes not digits": ("n", HEADER + "\n" + req_row("MV-101", "/p/u1", "/v/p/u1", observed="3k") + "\n"),
            "bytes leading zero": ("n", HEADER + "\n" + req_row("MV-101", "/p/u1", "/v/p/u1", observed="03") + "\n"),
            "empty action": ("n", HEADER + "\n" + req_row("MV-101", "/p/u1", "/v/p/u1", action="") + "\n"),
        }
        for label, tab in cases.items():
            with self.subTest(label):
                self.refuses(tables=[tab])

    def test_unselected_requirement_row_with_an_empty_action(self):
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1"), req_row("MV-102", "/p/u2", "/v/p/u2", action=""))]
        refusal = self.refuses("/m/plans/MOVE-REQUIREMENTS.tsv:3", tables=tables)
        self.assertIn("expected a non-empty UTF-8 string, got ''", str(refusal))

    def test_table_refusal_names_the_table_and_line(self):
        bad = ("/m/t.tsv", HEADER + "\n" + req_row("MV-1", "/p/u1", "/v/p/u1") + "\n")
        self.assertEqual(self.refuses(tables=[bad]).path, "/m/t.tsv:2")

    def test_duplicate_requirement_across_tables(self):
        row = req_row("MV-101", "/p/u1", "/v/p/u1")
        self.refuses("/m/b.tsv:2", tables=[table(row, name="/m/a.tsv"), table(row, name="/m/b.tsv")])

    def test_units_shape(self):
        for bad in ([], None, "u", [None], [[1]]):
            self.refuses(units=bad)

    def test_unit_keys(self):
        u = unit()
        del u["candidate"]
        self.refuses("units[0]", units=[u])
        u = unit()
        u["extra"] = 1
        self.refuses("units[0]", units=[u])

    def test_unknown_or_non_hold_requirement(self):
        self.refuses("units[0].requirement_id", units=[unit(rid="MV-999")])
        self.refuses("units[0].requirement_id", units=[unit(rid=101)])
        self.refuses("MV-101", tables=[table(req_row("MV-101", "/p/u1", "/v/p/u1", action="MOVE"))])

    def test_manifest_bytes(self):
        good = unit()["manifest_bytes"]
        doc = json.loads(good)
        cases = {"not bytes": good.decode(), "not utf-8": b"\xff" + good, "not json": b"{",
                 "not canonical": json.dumps(doc, indent=1, sort_keys=True).encode(),
                 "trailing newline": good + b"\n",
                 "no git_roots": canonical({k: v for k, v in doc.items() if k != "git_roots"}),
                 "schema 2": canonical({**doc, "schema_version": 2}),
                 "leaf outside root": canonical({**doc, "leaves": [leaf("/p/u2", "a.json")]}),
                 "surrogate": canonical(doc).replace(b"a.json", b"a\\udcff.json"),
                 "surrogate in git_roots": canonical({**doc, "git_roots": [
                     {"path": "/p/u1", "head": None, "branch": None, "dirty": ["X"]}]}).replace(b'"X"', b'"\\udcff"')}
        for label, data in cases.items():
            with self.subTest(label):
                u = unit()
                u["manifest_bytes"] = data
                self.refuses(units=[u])

    def test_invalid_utf8_manifest_is_named_as_such(self):
        u = unit()
        u["manifest_bytes"] = u["manifest_bytes"].replace(b"a.json", b"a\xff.json")
        self.assertIn("is not UTF-8", str(self.refuses("units[0].manifest_bytes", units=[u])))

    def test_manifest_root_must_be_the_requirement_source(self):
        u = unit()
        u["manifest_bytes"] = manifest_bytes("/p/u2", leaf("/p/u2", "a.json"))
        self.refuses("MV-101", units=[u])

    def test_git_roots(self):
        for bad in ("x", [None], [{"path": "/p/other", "head": None, "branch": None, "dirty": []}],
                    [{"path": "/p/u1", "head": None, "branch": None}], [{"path": 1, "head": None, "branch": None,
                                                                        "dirty": []}]):
            u = unit()
            doc = json.loads(u["manifest_bytes"])
            doc["git_roots"] = bad
            u["manifest_bytes"] = canonical(doc)
            with self.subTest(bad=bad):
                self.refuses(units=[u])

    def test_manifest_path(self):
        for bad in ("program/u.json", None, "/p/u1/manifest.json", "/p/u1"):
            u = unit()
            u["manifest_path"] = bad
            with self.subTest(bad=bad):
                self.refuses("units[0].manifest_path", units=[u])

    def test_registry(self):
        cases = [None, {**exact("u1"), "extra": 1}, {k: v for k, v in exact("u1").items() if k != "unit"},
                 {**exact("u1"), "result": "maybe"}, {**exact("u1"), "experiment_id": None},
                 {**exact("u1"), "candidates": ["c10r", "c9"]}, {**exact("u1"), "unknown": ["c10r"]},
                 {**exact("u1"), "experiment_id": "c 10"},
                 match("u1", "none", "c10r"), {**match("u1"), "candidates": "c10r"},
                 {**match("u1"), "evidence": None}, exact("u2"), {**exact("u1"), "unit": 7}]
        for bad in cases:
            with self.subTest(bad=bad):
                self.refuses(units=[unit(registry=bad)])

    def test_registry_family_pattern_matches_the_unit_name(self):
        p = plan([unit(registry=exact("u*"))])
        self.assertEqual(p["units"][0]["basis"], "registry")

    def test_candidate(self):
        for bad in ("experiments/c10r/runs/u1", 5, "/m/experiments/c9/runs/u1", "/m/experiments/c10r",
                    "/m/experiments/c10rx/u1", "/m/experiments/c10r/runs/<unit>", "/m/experiments/c10r/a/../b"):
            with self.subTest(bad=bad):
                self.refuses(units=[unit(candidate=bad)])

    def test_existing_v_target_is_a_collision_stop(self):
        self.refuses("MV-101", units=[unit(registry=match("u1"))], existing=["/v/p/u1"])
        self.refuses("MV-101", existing=["/v/p/u1", "/m/experiments/c10r/runs/u1"])

    def test_v_target_with_angle_brackets_is_not_bound(self):
        self.refuses("MV-101", units=[unit(registry=match("u1"))],
                     tables=[table(req_row("MV-101", "/p/u1", "/v/<unit>"))])

    def test_existing_targets(self):
        for bad in (None, "/v/p/u1", ["v/p/u1"], [None]):
            self.refuses(existing=bad)

    def test_readers(self):
        ok = {"file": "code/x.py", "line": 3, "old_text": "/p/u1", "old": "/p/u1"}
        cases = [{"stale": []}, {"stale": [], "unverified": [], "x": []}, {"stale": None, "unverified": []},
                 {"stale": [{**ok, "line": 0}], "unverified": []}, {"stale": [{**ok, "line": True}], "unverified": []},
                 {"stale": [{**ok, "line": "3"}], "unverified": []},
                 {"stale": [{**ok, "old": "/p/u2"}], "unverified": []},
                 {"stale": [{**ok, "old": "/p/u1x"}], "unverified": []},
                 {"stale": [{**ok, "file": ""}], "unverified": []},
                 {"stale": [{**ok, "file": "x\udcff.py"}], "unverified": []},
                 {"stale": [], "unverified": [{"file": "x", "reason": "bin\udcff"}]},
                 {"stale": [{k: v for k, v in ok.items() if k != "old_text"}], "unverified": []},
                 {"stale": [], "unverified": [{"file": "x"}]},
                 {"stale": [], "unverified": [{"file": "x", "reason": "binary", "why": 1}]}, "x"]
        for bad in cases:
            with self.subTest(bad=bad):
                u = unit()
                u["readers"] = bad
                self.refuses(units=[u])

    def test_stale_reader_with_an_empty_old_text(self):
        u = unit()
        u["readers"] = {"stale": [{"file": "x.py", "line": 1, "old_text": "", "old": "/p/u1"}], "unverified": []}
        refusal = self.refuses("units[0].readers.stale[0]", units=[u])
        self.assertIn("expected a non-empty UTF-8 string, got ''", str(refusal))

    def test_comparison(self):
        row = unit()["comparison"][0]
        cases = [[], "x", [{**row, "source": "/p/u1/b.json"}], [row, row], [{**row, "class": "same"}],
                 [{k: v for k, v in row.items() if k != "hint"}], [None]]
        for bad in cases:
            with self.subTest(bad=bad):
                self.refuses(units=[unit(comparison=bad)])

    def test_two_units_for_one_requirement(self):
        self.refuses("MV-101", units=[unit(), unit()])

    def test_overlapping_sources(self):
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1"), req_row("MV-102", "/p/u1/inner", "/v/inner"))]
        inner = unit("u1/inner", "MV-102", registry=match("inner"))
        self.refuses(units=[unit(registry=match("u1")), inner], tables=tables)

    def test_two_units_with_one_target(self):
        self.refuses(units=[unit(), unit("u2", "MV-102", candidate="/m/experiments/c10r/runs/u1")])

    def test_target_nested_in_another_target_or_source(self):
        self.refuses(units=[unit(), unit("u2", "MV-102", candidate="/m/experiments/c10r/runs/u1/u2")])
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1"), req_row("MV-102", "/p/u2", "/p/u1/u2"))]
        self.refuses(units=[unit(), unit("u2", "MV-102", registry=match("u2"))], tables=tables)

    def test_target_inside_its_own_source(self):
        tables = [table(req_row("MV-101", "/p/u1", "/p/u1/keep"))]
        self.refuses("MV-101", units=[unit(registry=match("u1"))], tables=tables)


def occ(file="code/x.py", line=3, old_text="/p/u1/a.json", old="/p/u1", text=None):
    return {"file": file, "line": line, "old_text": old_text, "old": old,
            "text": f"P = '{old_text}'" if text is None else text}


REPAIR_HEADER = "file\tline\told_text\tnew_text\tstep"


def repairs(*rows, name="/m/program/repairs.tsv"):
    return (name, "\n".join([REPAIR_HEADER, *("\t".join(map(str, r)) for r in rows)]) + "\n")


def historical(*rows, name="/m/program/historical.tsv"):
    return (name, "\n".join(["file\tline\told_text", *("\t".join(map(str, r)) for r in rows)]) + "\n")


ENTRY = {"id": "S220", "moves": [{"source": "/p/u1", "target": "/m/experiments/c10r/runs/u1",
    "id": "MV-101", "prd_ids": ["ICM-R4"], "action": "MOVE", "kind": "directory",
    "bytes": 3, "before_sha256": "a" * 64,
    "source_manifest": {"path": "/m/manifest.json", "sha256": "a" * 64},
    "lane": "legacy-preservation", "reader_check_ids": []}]}


def check_plans(occurrences, rep, entries=None):
    return core.check_plans(root=M, entries=[ENTRY] if entries is None else entries,
                            occurrences=occurrences, repairs=rep, historical=historical())


class CheckPlans(unittest.TestCase):
    def test_every_occurrence_with_one_good_row_gives_no_finding(self):
        rows = [("code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1/a.json", 261),
                ("code/y.py", 1, "/p/u1", "experiments/c10r/runs/u1", 269),
                ("code/z.py", 2, "/p/u1", "./experiments/c10r/runs/u1/b", 262)]
        found = check_plans([occ(), occ("code/y.py", 1, "/p/u1"), occ("code/z.py", 2, "/p/u1")], repairs(*rows))
        self.assertEqual(found, ())

    def test_zero_rows_and_zero_occurrences_give_no_finding(self):
        self.assertEqual(check_plans([], repairs()), ())

    def test_occurrence_with_no_row(self):
        found = check_plans([occ()], repairs())
        self.assertEqual(found, (("no-row", "code/x.py", 3, "/p/u1/a.json", "no repairs row for /p/u1"),))
        self.assertEqual(core.PLAN_FINDING_COLUMNS, ("kind", "file", "line", "old_text", "detail"))

    def test_old_text_twice_on_its_line(self):
        o = occ(text="a = '/p/u1/a.json' + '/p/u1/a.json'")
        found = check_plans([o, o], repairs(("code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1", 261)))
        self.assertEqual([f[0] for f in found], ["not-once"])
        self.assertIn("2 times", found[0][4])

    def test_overlapping_old_text_counts_twice(self):
        o = occ(old_text="/p/u1/aa", text="x /p/u1/aa/p/u1/aa")
        found = check_plans([o], repairs(("code/x.py", 3, "/p/u1/aa", "/m/experiments/c10r/runs/u1/aa", 261)))
        self.assertEqual([f[0] for f in found], ["not-once"])

    def test_truly_overlapping_old_text_counts_twice(self):
        entries = [{"id": "S220", "moves": [{**ENTRY["moves"][0], "source": "/p/p", "target": "/v/p/p"}]}]
        o = occ(old_text="/p/p", old="/p/p", text="path=/p/p/p")
        found = check_plans([o], repairs(("code/x.py", 3, "/p/p", "/v/p/p", 261)), entries=entries)
        self.assertEqual(found, (("not-once", "code/x.py", 3, "/p/p", "old_text occurs 2 times on its line"),))

    def test_new_text_not_under_the_entry_target(self):
        for new in ("/m/experiments/c10r/runs/u1x", "/v/p/u1", "experiments/c10r/runs", "../m/experiments/c10r/runs/u1",
                    "/m/experiments/c10r/runs/u1/../u2", "/m/experiments/c10r/runs/u1/", "experiments//c10r/runs/u1"):
            with self.subTest(new=new):
                found = check_plans([occ()], repairs(("code/x.py", 3, "/p/u1/a.json", new, 261)))
                self.assertEqual([f[0] for f in found], ["not-under-target"])
                self.assertIn("/m/experiments/c10r/runs/u1", found[0][4])

    def test_new_text_equal_to_the_target_is_under_it(self):
        found = check_plans([occ()], repairs(("code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1", 261)))
        self.assertEqual(found, ())

    def test_row_with_no_occurrence(self):
        found = check_plans([], repairs(("code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1", 261)))
        self.assertEqual([f[0] for f in found], ["no-occurrence"])

    def test_duplicate_row(self):
        row = ("code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1", 261)
        found = check_plans([occ()], repairs(row, row))
        self.assertEqual([f[0] for f in found], ["duplicate-row"])

    def test_old_path_no_entry_moves(self):
        o = occ(old_text="/p/u9", old="/p/u9")
        found = check_plans([o], repairs(("code/x.py", 3, "/p/u9", "/m/x", 261)))
        self.assertEqual(found, (("no-entry", "code/x.py", 3, "/p/u9", "no entry moves /p/u9"),))

    def test_longest_move_source_names_the_target(self):
        entries = [ENTRY, {"id": "S221", "moves": [{**ENTRY["moves"][0], "source": "/p/u1/inner", "target": "/v/inner"}]}]
        o = occ(old_text="/p/u1/inner/a", old="/p/u1/inner")
        found = check_plans([o], repairs(("code/x.py", 3, "/p/u1/inner/a", "/v/inner/a", 261)), entries)
        self.assertEqual(found, ())
        found = check_plans([o], repairs(("code/x.py", 3, "/p/u1/inner/a", "/m/experiments/c10r/runs/u1/inner/a",
                                          261)), entries)
        self.assertEqual([f[0] for f in found], ["not-under-target"])

    def test_relative_old_path_is_resolved_against_the_root(self):
        entries = [{"id": "S241", "moves": [{**ENTRY["moves"][0], "source": "/m/results/u1", "target": "/v/m/results/u1"}]}]
        o = occ(old_text="results/u1", old="results/u1")
        self.assertEqual(check_plans([o], repairs(("code/x.py", 3, "results/u1", "/v/m/results/u1", 261)), entries), ())

    def test_findings_are_sorted(self):
        found = check_plans([occ("b.py"), occ("a.py")], repairs())
        self.assertEqual([f[1] for f in found], ["a.py", "b.py"])


class CheckPlansRefuses(unittest.TestCase):
    def refuses(self, occurrences=(), rep=DEFAULT, entries=DEFAULT, root=M, names=None):
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.check_plans(root=root, entries=[ENTRY] if entries is DEFAULT else entries,
                             occurrences=list(occurrences), repairs=repairs() if rep is DEFAULT else rep, historical=historical())
        if names is not None:
            self.assertEqual(caught.exception.path, names)
        return caught.exception

    def test_root(self):
        self.refuses(root="m", names="root")

    def test_entries(self):
        for bad in ([], None, [None], [{"id": "S1"}], [{"id": "", "moves": []}], [{"id": "S1", "moves": None}],
                    [{"id": "S1", "moves": [{**ENTRY["moves"][0], "source": "p", "target": "/v"}]}],
                    [{"id": "S1", "moves": [{**ENTRY["moves"][0], "source": "/p", "target": "/v", "x": 1}]}],
                    [ENTRY, {"id": "S221", "moves": [{**ENTRY["moves"][0], "source": "/p/u1", "target": "/v/u1"}]}], [ENTRY, ENTRY],
                    [{**ENTRY, "id": ""}], [{**ENTRY, "id": 5}], [{**ENTRY, "id": "S 1"}], [{"id": "S1", "moves": []}],
                    [ENTRY, {"id": "S220", "moves": [{**ENTRY["moves"][0], "source": "/p/u2", "target": "/v/u2"}]}]):
            with self.subTest(bad=bad):
                self.refuses(entries=bad)

    def test_occurrences(self):
        for bad in ([None], [{**occ(), "x": 1}], [{k: v for k, v in occ().items() if k != "text"}],
                    [occ(line=0)], [occ(line=False)], [occ(old="p/../u1")], [occ(text="no match here")],
                    [occ(), occ(old_text="/p/u1", text="other text /p/u1")], [occ(text=7)], [occ(file="")]):
            with self.subTest(bad=bad):
                self.refuses(bad)
        with self.assertRaises(fdsafe.Refusal):
            core.check_plans(root=M, entries=[ENTRY], occurrences="x", repairs=repairs(), historical=historical())

    def test_repairs_rows(self):
        good = ["code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1", 261]
        for i, bad in [(1, "0"), (1, "03"), (1, "x"), (1, ""), (4, "260"), (4, "270"), (4, "26a"), (0, ""),
                       (2, ""), (3, "")]:
            row = list(good)
            row[i] = bad
            with self.subTest(i=i, bad=bad):
                self.refuses([occ()], repairs(row))

    def test_repairs_text(self):
        for bad in (("n", "file\tline\n"), ("n", REPAIR_HEADER), ("n", ""), None, ("n",), (1, "x\n"),
                    ("n", REPAIR_HEADER + "\na\t1\tb\tc\n")):
            with self.subTest(bad=bad):
                self.refuses(rep=bad)

    def test_row_refusal_names_the_file_and_line(self):
        self.refuses([occ()], repairs(["code/x.py", "x", "/p/u1/a.json", "/m/t", 261], name="/m/r.tsv"),
                     names="/m/r.tsv:2")


ROUTE_HEADER = "child\tproducer\towner\ttarget"
SRC, HOLD_T = "/m/results", "/v/m/results"


def routes(*rows, name="/m/program/results-routes.tsv"):
    return (name, "\n".join([ROUTE_HEADER, *("\t".join(r) for r in rows)]) + "\n")


GOOD_ROUTES = [("a", "c10_sweep.py", "run", "/m/experiments/c10r/runs/a"),
               ("b", "audit_tool", "audit", "/m/audits/b"),
               ("c", "build.sh", "build-receipt", "/m/program/receipts/c"),
               ("d", "", "hold", "/v/m/results/d")]


def check_routes(rows, children=("a", "b", "c", "d")):
    return core.check_routes(routes=routes(*rows), source=SRC, children=list(children), hold_target=HOLD_T)


def kinds(found):
    return [f[0] for f in found]


class CheckRoutes(unittest.TestCase):
    def test_one_good_row_per_child_gives_no_finding(self):
        self.assertEqual(check_routes(GOOD_ROUTES), ())
        self.assertEqual(core.ROUTE_FINDING_COLUMNS, ("kind", "child", "detail"))

    def test_child_with_no_row(self):
        self.assertEqual(check_routes(GOOD_ROUTES[:3]), (("no-row", "d", "no route row"),))

    def test_row_for_an_unknown_child(self):
        found = check_routes(GOOD_ROUTES + [("e", "", "hold", "/v/m/results/e")])
        self.assertEqual(found, (("unknown-child", "e", "/m/results has no child e"),))

    def test_duplicate_child(self):
        self.assertEqual(kinds(check_routes(GOOD_ROUTES + [GOOD_ROUTES[0]])), ["duplicate-child"])

    def test_bad_owner_and_missing_producer(self):
        rows = list(GOOD_ROUTES)
        rows[0] = ("a", "c10_sweep.py", "Run", "/m/experiments/c10r/runs/a")
        self.assertEqual(kinds(check_routes(rows)), ["bad-owner"])
        rows[0] = ("a", "", "run", "/m/experiments/c10r/runs/a")
        self.assertEqual(kinds(check_routes(rows)), ["no-producer"])

    def test_inexact_targets(self):
        for bad in ("experiments/c10r/runs/a", "/m/experiments/<id>/a", "/m/experiments/c10r/runs/a/",
                    "/m/x/../a", "", "/m/a>b"):
            rows = list(GOOD_ROUTES)
            rows[0] = ("a", "p", "run", bad)
            with self.subTest(bad=bad):
                self.assertEqual(kinds(check_routes(rows)), ["inexact-target"])

    def hold_row_for(self, child):
        return core.check_routes(routes=routes((child, "", "hold", f"{HOLD_T}/{child}")), source=SRC,
                                 children=[child], hold_target=HOLD_T)

    def test_hold_row_child_with_open_and_close_brackets_is_inexact(self):
        self.assertEqual(self.hold_row_for("<x>"),
                         (("inexact-target", "<x>", "the hold target /v/m/results/<x> is not exact"),))

    def test_hold_row_child_ending_in_an_open_bracket_is_inexact(self):
        self.assertEqual(self.hold_row_for("x<"),
                         (("inexact-target", "x<", "the hold target /v/m/results/x< is not exact"),))

    def test_hold_row_child_ending_in_a_close_bracket_is_inexact(self):
        self.assertEqual(self.hold_row_for("x>"),
                         (("inexact-target", "x>", "the hold target /v/m/results/x> is not exact"),))

    def test_hold_row_plain_child_with_its_exact_target_gives_no_finding(self):
        self.assertEqual(self.hold_row_for("x"), ())

    def test_hold_row_needs_the_v_target_of_its_child(self):
        for bad in ("/v/m/results", "/v/m/results/e", "/v/m/results/d/x", "/m/results/d"):
            rows = list(GOOD_ROUTES)
            rows[3] = ("d", "", "hold", bad)
            with self.subTest(bad=bad):
                self.assertEqual(kinds(check_routes(rows)), ["hold-target"])

    def test_target_in_or_over_the_source(self):
        for bad in ("/m/results/a", "/m/results"):
            rows = list(GOOD_ROUTES)
            rows[0] = ("a", "p", "run", bad)
            with self.subTest(bad=bad):
                self.assertEqual(kinds(check_routes(rows)), ["target-in-source"])
        rows = [("a", "p", "run", "/m")] + GOOD_ROUTES[1:]
        self.assertIn(("target-in-source", "a", "target /m overlaps the source /m/results"), check_routes(rows))

    def test_target_collisions(self):
        rows = list(GOOD_ROUTES)
        rows[1] = ("b", "p", "audit", "/m/experiments/c10r/runs/a")
        self.assertEqual(check_routes(rows), (("target-collision", "a", "/m/experiments/c10r/runs/a"),
                                              ("target-collision", "b", "/m/experiments/c10r/runs/a")))
        rows[1] = ("b", "p", "audit", "/m/experiments/c10r/runs/a/b")
        self.assertEqual(kinds(check_routes(rows)), ["target-collision", "target-collision"])
        rows[1] = ("b", "p", "audit", "/m/experiments/c10r/runs/ab")
        self.assertEqual(check_routes(rows), ())

    def test_a_child_name_tsv_cannot_hold_is_reported_as_missing(self):
        self.assertEqual(check_routes(GOOD_ROUTES, ("a", "b", "c", "d", "bad\tname")),
                         (("no-row", "bad\tname", "no route row"),))


class CheckRoutesRefuses(unittest.TestCase):
    def refuses(self, rows=GOOD_ROUTES, children=("a", "b", "c", "d"), source=SRC, hold=HOLD_T, rt=DEFAULT,
                names=None):
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.check_routes(routes=routes(*rows) if rt is DEFAULT else rt, source=source,
                              children=children if children is None or isinstance(children, str) else list(children),
                              hold_target=hold)
        if names is not None:
            self.assertEqual(caught.exception.path, names)

    def test_children(self):
        for bad in ((), None, "abc", ("a", "a"), ("a/b",), (".",), ("..",), ("",), (1,), ("a\0",)):
            with self.subTest(bad=bad):
                self.refuses(children=bad, names="children")

    def test_source_and_hold_target(self):
        self.refuses(source="m/results", names="source")
        self.refuses(hold="v/m/results", names="hold_target")
        self.refuses(hold="/v/<results>", names="hold_target")

    def test_routes_text(self):
        for bad in (("n", "child\tproducer\n"), ("n", ROUTE_HEADER), None, ("n", ROUTE_HEADER + "\na\tb\n"),
                    ("n", ROUTE_HEADER + "\n\tp\trun\t/m/x\n")):
            with self.subTest(bad=bad):
                self.refuses(rt=bad)


class Purity(unittest.TestCase):
    def test_core_makes_no_filesystem_or_subprocess_call(self):
        def forbidden(*args, **kwargs):
            raise AssertionError(f"filesystem or process call: {args!r}")

        names = ["open", "stat", "lstat", "fstat", "scandir", "listdir", "readlink", "getcwd", "access",
                 "walk", "rename", "replace", "mkdir", "unlink", "remove", "path.exists", "path.lexists",
                 "path.isdir", "path.isfile", "path.islink", "path.realpath", "path.abspath", "getenv"]
        with contextlib.ExitStack() as stack:
            for name in names:
                target = os.path if name.startswith("path.") else os
                stack.enter_context(mock.patch.object(target, name.split(".")[-1], forbidden))
            for target, name in [(builtins, "open"), (io, "open"), (subprocess, "run"), (subprocess, "Popen"),
                                 (shutil, "move"), (shutil, "copy")]:
                stack.enter_context(mock.patch.object(target, name, forbidden))
            stack.enter_context(mock.patch.object(os, "environ", {}))
            p = plan([unit(), unit("u2", "MV-102", registry=match("u2"))], existing=["/m/experiments/x"])
            found = check_plans([occ()], repairs())
            routed = check_routes(GOOD_ROUTES)
        self.assertEqual(len(p["moves"]), 2)
        self.assertEqual(kinds(found), ["no-row"])
        self.assertEqual(routed, ())

    def test_module_names_no_filesystem_entry_point(self):
        text = core.__loader__.get_source(core.__name__)
        for token in ("import os", "open(", "import subprocess", "import shutil", "import time", "import datetime",
                      "os.environ", "getenv", "except Exception", "except ValueError", "except KeyError", "except:"):
            self.assertFalse(token in text, f"move_plan_core names {token!r}")

    def test_unexpected_exceptions_propagate(self):
        for exc in (ValueError, KeyError, RuntimeError):
            with self.subTest(exc=exc), mock.patch.object(core.hashlib, "sha256", side_effect=exc("boom")):
                with self.assertRaises(exc) as caught:
                    plan()
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)


class HoldTargetRefuses(unittest.TestCase):
    """A hold_target in, equal to or over the source is refused (so is a non-exact one, test_source_and_hold_target)."""

    def refuses(self, hold, target):
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.check_routes(routes=routes(("a", "", "hold", target)), source=SRC, children=["a"], hold_target=hold)
        self.assertEqual(caught.exception.path, "hold_target")

    def test_hold_target_equal_to_or_inside_the_source(self):
        self.refuses("/m/results", "/m/results/a")
        self.refuses("/m/results/keep", "/m/results/keep/a")

    def test_hold_target_over_the_source(self):
        self.refuses("/", "//a")
        self.refuses("/m", "/m/a")

    def test_hold_target_beside_the_source_is_accepted(self):
        found = core.check_routes(routes=routes(("a", "", "hold", "/m/resultsx/a")), source=SRC, children=["a"],
                                  hold_target="/m/resultsx")
        self.assertEqual(found, ())


class ProducerFieldTypesRefuse(unittest.TestCase):
    """Each Step 216 comparison field and Step 201 git_roots field has the type its producer emits."""

    def refuses_comparison(self, field, value):
        u = unit()
        u["comparison"][0][field] = value
        with self.assertRaises(fdsafe.Refusal) as caught:
            plan([u])
        self.assertEqual(caught.exception.path, f"units[0].comparison[0].{field}")

    def refuses_git(self, field, value):
        g = {"path": "/p/u1/sub", "head": None, "branch": None, "dirty": []}
        g[field] = value
        with self.assertRaises(fdsafe.Refusal) as caught:
            plan([unit(git_roots=[g])])
        self.assertEqual(caught.exception.path, f"units[0].manifest_bytes.git_roots[0].{field}")

    def test_comparison_source(self):
        for bad in ([], {}, 5, None):
            with self.subTest(bad=bad):
                self.refuses_comparison("source", bad)

    def test_comparison_relpath(self):
        for bad in (None, 5, []):
            with self.subTest(bad=bad):
                self.refuses_comparison("relpath", bad)

    def test_comparison_path_lists(self):
        for field in ("equal_to", "differing_from", "same_inode"):
            for bad in ("not a list", False, 3, None, {}, [1], ["/r/a.json", None]):
                with self.subTest(field=field, bad=bad):
                    self.refuses_comparison(field, bad)

    def test_comparison_hint(self):
        good = {"sha256": "a" * 64, "agrees": True}
        for bad in ([], "x", 5, {}, {"sha256": "a" * 64}, {**good, "x": 1}, {**good, "sha256": 5},
                    {**good, "agrees": 1}, {**good, "agrees": None}):
            with self.subTest(bad=bad):
                self.refuses_comparison("hint", bad)

    def test_comparison_fields_of_the_producer_types_are_accepted(self):
        u = unit()
        u["comparison"][0].update({"class": "equal", "equal_to": ["/r/a.json"], "differing_from": ["/r2/a.json"],
                                   "same_inode": ["/r/a.json"]})
        for hint in ({"sha256": "a" * 64, "agrees": True}, {"sha256": "b" * 64, "agrees": False}):
            u["comparison"][0]["hint"] = hint
            with self.subTest(hint=hint):
                self.assertEqual(risks(plan([u]), "equal")[0]["items"], ["/p/u1/a.json"])

    def test_git_root_head_and_branch(self):
        for field in ("head", "branch"):
            for bad in ([], 42, {}, True):
                with self.subTest(field=field, bad=bad):
                    self.refuses_git(field, bad)

    def test_git_root_dirty(self):
        for bad in ("not a list", None, {}, [1], [" M x", 2]):
            with self.subTest(bad=bad):
                self.refuses_git("dirty", bad)


class SurvivingGuards(unittest.TestCase):
    """One test per pre-review survivor (reviews/T217/work/mutant-table.md); each asserts the original result."""

    def refuses(self, call, names):
        with self.assertRaises(fdsafe.Refusal) as caught:
            call()
        self.assertEqual(caught.exception.path, names)

    def test_m008_a_non_string_text_field_is_refused(self):
        readers = {"stale": [{"file": ["x"], "line": 1, "old_text": "/p/u1", "old": "/p/u1"}], "unverified": []}
        self.refuses(lambda: plan([unit(readers=readers)]), "units[0].readers.stale[0]")

    def test_m010_a_nul_in_a_text_field_is_refused(self):
        self.refuses(lambda: check_plans([occ(old_text="a\0", text="a\0")], repairs()), "occurrences[0]")

    def test_m023_a_path_that_is_not_utf8_is_refused(self):
        self.refuses(lambda: core.check_routes(routes=routes(("a", "p", "run", "/v/a")), source="/m\udcff",
                                               children=["a"], hold_target="/v/m"), "source")

    def test_m026_a_target_with_only_one_angle_bracket_is_inexact(self):
        for bad in ("/v/a<", "/v/a>"):
            with self.subTest(bad=bad):
                self.assertEqual(kinds(check_routes([("a", "p", "run", bad)], children=["a"])), ["inexact-target"])

    def test_m035_m036_a_table_name_that_is_not_a_non_empty_string_is_refused(self):
        for name in (1, ""):
            with self.subTest(name=name):
                self.refuses(lambda: plan(tables=[table(req_row("MV-101", "/p/u1", "/v/p/u1"), name=name)]),
                             "requirement_tables[0]")

    def test_m065_a_reader_old_path_that_is_not_normalized_is_refused(self):
        readers = {"stale": [{"file": "x", "line": 1, "old_text": "/p/u1/a/../b", "old": "/p/u1/a/../b"}],
                   "unverified": []}
        self.refuses(lambda: plan([unit(readers=readers)]), "units[0].readers.stale[0]")

    def test_m074_an_unhashable_requirement_id_is_refused(self):
        self.refuses(lambda: plan([unit(rid=[])]), "units[0].requirement_id")

    def test_m079_a_candidate_is_checked_even_when_the_registry_is_not_exact(self):
        self.refuses(lambda: plan([unit(registry=match("u1"), candidate=5)]), "units[0].candidate")

    def test_m100_a_source_inside_an_earlier_units_target_is_refused(self):
        src = "/m/experiments/c10r/runs/u1/inner"
        inner = unit("inner", "MV-102", registry=match("inner"), comparison=None)
        inner["manifest_bytes"] = manifest_bytes(src, leaf(src, "a.json"))
        tables = [table(req_row("MV-101", "/p/u1", "/v/p/u1"), req_row("MV-102", src, "/v/inner"))]
        self.refuses(lambda: plan([unit(), inner], tables=tables), "MV-102")

    def test_m103_an_entry_with_no_id_is_refused(self):
        self.refuses(lambda: check_plans([], repairs(), entries=[{"moves": ENTRY["moves"]}]), "entries[0]")


_AUDIT = {"installed": False, "on": False, "events": []}


def _audit(event, args):
    if _AUDIT["on"] and (event == "open" or event.startswith(("os.", "subprocess.", "shutil."))):
        _AUDIT["events"].append((event, args))


class AuditedPurity(unittest.TestCase):
    """PEP 578 audit events while the core runs: no open and no os, subprocess or shutil call."""

    def setUp(self):
        if not _AUDIT["installed"]:
            sys.addaudithook(_audit)  # a hook cannot be removed, so it records only inside window()
            _AUDIT["installed"] = True
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = scratch.name

    @contextlib.contextmanager
    def window(self):
        _AUDIT["events"] = []
        _AUDIT["on"] = True
        try:
            os.listdir(self.scratch)  # positive control: the hook is live inside the window
            yield
        finally:
            _AUDIT["on"] = False
        self.assertEqual(_AUDIT["events"], [("os.listdir", (self.scratch,))])

    def test_valid_calls_make_no_filesystem_or_process_call(self):
        units = [unit(), unit("u2", "MV-102", registry=match("u2"))]
        occurrences, rep = [occ()], repairs()
        calls = [lambda: plan(units, existing=["/m/experiments/x"]), lambda: check_plans(occurrences, rep),
                 lambda: check_routes(GOOD_ROUTES)]
        warm = [call() for call in calls]  # warm-up outside the window: lazy imports may open files
        with self.window():
            seen = [call() for call in calls]
        self.assertEqual(seen, warm)
        self.assertEqual(len(seen[0]["moves"]), 2)

    def test_a_manifest_path_in_place_of_its_bytes_is_refused_unopened(self):
        u = unit()
        path = os.path.join(self.scratch, "u1.json")
        with open(path, "wb") as f:
            f.write(u["manifest_bytes"])
        u["manifest_bytes"] = path
        self.assertTrue(os.path.isabs(path))
        with self.assertRaises(fdsafe.Refusal):  # warm-up outside the window
            plan([u])
        with self.window():
            with self.assertRaises(fdsafe.Refusal) as caught:
                plan([u])
        self.assertEqual(caught.exception.path, "units[0].manifest_bytes")


if __name__ == "__main__":
    unittest.main()
