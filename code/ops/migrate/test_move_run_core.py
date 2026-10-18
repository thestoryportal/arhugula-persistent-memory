"""Tests for move_run_core: the pure core of move_unit run (Step 218; its I/O shell is Step 210).

The core takes one approved unit plan (the Step 217 build_plan document) and the state the shell
observed (approval, fresh Step 201 manifests, Step 212 splits, tracked paths, worktree, targets,
run units, a clock reading) and returns the ordered actions and the unit's custody documents, or
refuses with fdsafe.Refusal naming the input. RED list for a pure function: malformed input of each
field, boundary values and unexpected types; the negative controls of the step (unapproved plan,
corrupted byte, collision, split run, linked worktree) are rows.
"""
from __future__ import annotations

import builtins
import contextlib
import copy
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from typing import NamedTuple
from unittest import mock

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as plan_core
from ops.migrate import move_run_core as core

M = "/m"
PLAN_PATH = "/m/program/migrations/icm21/phase5-plans/S220.json"
APPROVAL_PATH = "/m/program/migrations/icm21/approvals/S220.json"
CUSTODY = "/m/program/migrations/icm21/units/S220"
NOW = "2026-10-18T12:00:00Z"
WORKTREE = {"top": M, "git_dir": "/m/.git", "common_dir": "/m/.git"}
HEADER = "requirement_id\tsource\ttarget\taction\tobserved_bytes\tclass\tlane\tcheck_id\tadmission\tprd_ids"
RECORD, BULK, PAYLOAD = "tracked-record", "attested-bulk", "governed-payload"
ALLOWED = {"mkdir", "mv", "git-mv", "git-rm-cached", "git-add"}
BIG = b"9" * 5000                          # over the interpreter integer digit limit (4300)
DEEP = b"[" * 100000 + b"]" * 100000      # past the recursion limit of json.loads


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class Leaf(NamedTuple):
    rel: str
    data: bytes | None = b"abc"   # None: a symlink
    link: str | None = None
    cls: str = RECORD


class Spec(NamedTuple):
    name: str
    rid: str
    source: str
    vtarget: str
    exact: bool
    base: str
    leaves: tuple
    tracked: tuple = ()


U1 = Spec("u1", "MV-101", "/m/old/u1", "/v/preserved/old-u1", True, "/m/experiments/c10r",
          (Leaf("a.json", b"{}"), Leaf("b.bin", b"\x00\x01", cls=PAYLOAD), Leaf("link", None, "a.json")),
          ("a.json",))
U2 = Spec("u2", "MV-102", "/v/p/u2", "/v/preserved/u2", False, "/v", (Leaf("c.log", b"log\n"),))
T1, T2 = "/m/experiments/c10r/runs/u1", "/v/preserved/u2"


def record(source: str, leaf: Leaf) -> dict:
    path = f"{source}/{leaf.rel}"
    inode = int(sha(path.encode())[:8], 16)
    if leaf.data is None:
        text = leaf.link.encode()
        return {"source": path, "kind": "symlink", "bytes": len(text), "sha256": sha(text), "link_text": leaf.link,
                "device": 16777230, "inode": inode, "nlink": 1}
    return {"source": path, "kind": "file", "bytes": len(leaf.data), "sha256": sha(leaf.data), "link_text": None,
            "device": 16777230, "inode": inode, "nlink": 1}


def manifest_doc(spec: Spec) -> dict:
    return {"schema_version": 1, "root": spec.source, "leaves": [record(spec.source, l) for l in spec.leaves],
            "git_roots": []}


def split_doc(spec: Spec, records: list) -> dict:
    rows = []
    for leaf, rec in zip(spec.leaves, records):
        if leaf.data is None:
            rows.append({"path": leaf.rel, "class": RECORD, "kind": "link", "size": None, "sha256": None,
                         "link": leaf.link})
        else:
            rows.append({"path": leaf.rel, "class": leaf.cls, "kind": "file", "size": rec["bytes"],
                         "sha256": rec["sha256"], "link": None})
    return {"root": spec.source, "leaves": rows}


def split_bytes(doc: dict) -> bytes:
    return (json.dumps(doc, indent=1, sort_keys=True) + "\n").encode()  # as record_split renders it


def req_row(spec: Spec) -> str:
    return "\t".join([spec.rid, spec.source, spec.vtarget, "HOLD", "0", "legacy-science-unit",
                      "legacy-preservation", "C-HOLD", "G4+G5; reader hold", "ICM-R4"])


def reseal(doc: dict) -> dict:
    body = {k: v for k, v in doc.items() if k not in ("digest", "approval")}
    digest = sha(canonical(body))
    return {**body, "digest": digest, "approval": f"G4 approve {body['id']} sha256:{digest}"}


def approval_doc(plan_bytes: bytes, plan_id="S220", **over) -> dict:
    doc = {"approval_id": "approval-0123456789ab", "plan_id": plan_id, "plan_sha256": sha(plan_bytes),
           "gate": "G4", "approved_by": "operator", "approved_at": "2026-10-18T11:00:00.123456+00:00",
           "expires_at": "2026-10-19T11:00:00+00:00", "decision": "approved"}
    doc.update(over)
    return doc


def scenario(specs=(U1, U2), plan_edit=None, approval_over=None, manifest_edit=None, split_edit=None):
    """(kwargs for core.run_unit, the plan document, {source: manifest dict})."""
    manifests = {s.source: manifest_doc(s) for s in specs}
    units = []
    for s in specs:
        name = s.name
        units.append({"requirement_id": s.rid, "manifest_path": f"/m/program/units/{name}.json",
                      "manifest_bytes": canonical(manifests[s.source]),
                      "registry": ({"unit": name, "result": "exact", "experiment_id": "c10r", "candidates": ["c10r"],
                                    "unknown": [], "evidence": []} if s.exact else
                                   {"unit": name, "result": "none", "experiment_id": None, "candidates": [],
                                    "unknown": [], "evidence": []}),
                      "candidate": f"/m/experiments/c10r/runs/{name}" if s.exact else None,
                      "readers": {"stale": [], "unverified": []}, "comparison": None})
    plan = plan_core.build_plan(entry_id="S220", root=M,
                                requirement_tables=[("/m/MOVE-REQUIREMENTS.tsv",
                                                     "\n".join([HEADER, *map(req_row, specs)]) + "\n")],
                                units=units, existing_targets=[])
    by_target = {u["source"]: u["target"] for u in plan["units"]}  # before any edit: the observed targets
    if plan_edit is not None:
        plan = copy.deepcopy(plan)
        plan_edit(plan)
        plan = reseal(plan)
    plan_bytes = canonical(plan)
    fresh = copy.deepcopy(manifests)
    if manifest_edit is not None:
        manifest_edit(fresh)
    splits = {s.source: split_doc(s, manifests[s.source]["leaves"]) for s in specs}
    if split_edit is not None:
        split_edit(splits)
    kw = dict(root=M, plan=(PLAN_PATH, plan_bytes),
              approval=(APPROVAL_PATH, canonical(approval_doc(plan_bytes, **(approval_over or {})))),
              now=NOW,
              units=[{"source": s.source, "manifest": canonical(fresh[s.source]), "split": split_bytes(splits[s.source])}
                     for s in specs],
              tracked=[f"{s.source}/{rel}" for s in specs for rel in s.tracked],
              worktree=dict(WORKTREE),
              targets=[{"target": by_target[s.source], "exists": False, "base": s.base} for s in specs],
              run_units=[s.source for s in specs],
              custody_dir=CUSTODY)
    return kw, plan, manifests


def rebind(kw: dict, edit) -> dict:
    """kw for a one-unit scenario whose fresh manifest leaves edit() changed, with the plan and approval
    resealed to bind the new manifest bytes (so the edit is observed evidence, not a changed pre-digest)."""
    manifest = json.loads(kw["units"][0]["manifest"])
    edit(manifest["leaves"])
    data = canonical(manifest)
    plan = json.loads(kw["plan"][1])
    plan["units"][0]["manifest"]["sha256"] = sha(data)
    plan["moves"][0]["source_manifest"]["sha256"] = plan["moves"][0]["before_sha256"] = sha(data)
    plan_bytes = canonical(reseal(plan))
    units = copy.deepcopy(kw["units"])
    units[0]["manifest"] = data
    return {**kw, "units": units, "plan": (PLAN_PATH, plan_bytes),
            "approval": (APPROVAL_PATH, canonical(approval_doc(plan_bytes)))}


def run(**over):
    kw = scenario()[0]
    kw.update(over)
    return core.run_unit(**kw)


def docs(result) -> dict:
    return {d["path"]: d["bytes"] for d in result["documents"]}


def act(op, action, source=None, target=None):
    return {"operation_id": op, "action": action, "source": source, "target": target}


class Actions(unittest.TestCase):
    def test_tracked_unit_inside_m_is_git_mv_then_untracked_records_are_added(self):
        result = run()
        self.assertEqual(result["actions"], [
            act("MV-101", "mkdir", target="/m/experiments/c10r/runs"),
            act("MV-101", "git-mv", "/m/old/u1", T1),
            act("MV-101", "git-add", target=f"{T1}/link"),
            act("MV-102", "mkdir", target="/v/preserved"),
            act("MV-102", "mv", "/v/p/u2", T2),
        ])

    def test_untracked_unit_inside_m_is_mv_then_every_record_is_added(self):
        kw = scenario([U1._replace(tracked=())])[0]
        self.assertEqual(core.run_unit(**kw)["actions"], [
            act("MV-101", "mkdir", target="/m/experiments/c10r/runs"),
            act("MV-101", "mv", "/m/old/u1", T1),
            act("MV-101", "git-add", target=f"{T1}/a.json"),
            act("MV-101", "git-add", target=f"{T1}/link"),
        ])

    def test_tracked_unit_leaving_m_is_mv_then_git_rm_cached(self):
        u3 = Spec("u3", "MV-103", "/m/old/u3", "/v/preserved/u3", False, "/v/preserved",
                  (Leaf("x.json", b"[]"), Leaf("y.txt", b"y")), ("x.json",))
        kw = scenario([u3])[0]
        self.assertEqual(core.run_unit(**kw)["actions"], [
            act("MV-103", "mv", "/m/old/u3", "/v/preserved/u3"),
            act("MV-103", "git-rm-cached", source="/m/old/u3"),
        ])

    def test_untracked_unit_leaving_m_is_a_plain_mv(self):
        u3 = Spec("u3", "MV-103", "/m/old/u3", "/v/preserved/u3", False, "/v/preserved", (Leaf("x.json", b"[]"),))
        kw = scenario([u3])[0]
        self.assertEqual(core.run_unit(**kw)["actions"], [act("MV-103", "mv", "/m/old/u3", "/v/preserved/u3")])

    def test_unit_entering_m_from_outside_adds_records_only(self):
        u4 = Spec("u4", "MV-104", "/v/p/u4", "/v/preserved/u4", True, "/m/experiments/c10r/runs",
                  (Leaf("r.ipynb", b"{}"), Leaf("w.bin", b"\x00", cls=BULK), Leaf("p.bin", b"\x01", cls=PAYLOAD)))
        kw = scenario([u4])[0]
        self.assertEqual(core.run_unit(**kw)["actions"], [
            act("MV-104", "mv", "/v/p/u4", "/m/experiments/c10r/runs/u4"),
            act("MV-104", "git-add", target="/m/experiments/c10r/runs/u4/r.ipynb"),
        ])

    def test_missing_folders_are_made_parent_first_and_once(self):
        u5 = Spec("u5", "MV-105", "/m/old/u5", "/v/x", True, "/m", (Leaf("e.json", b"1"),))
        u1 = U1._replace(base="/m")
        kw = scenario([u1, u5])[0]
        made = [a["target"] for a in core.run_unit(**kw)["actions"] if a["action"] == "mkdir"]
        self.assertEqual(made, ["/m/experiments", "/m/experiments/c10r", "/m/experiments/c10r/runs"])

    def test_an_existing_parent_needs_no_folder(self):
        kw = scenario([U1._replace(base="/m/experiments/c10r/runs")])[0]
        self.assertNotIn("mkdir", [a["action"] for a in core.run_unit(**kw)["actions"]])

    def test_no_overwrite_delete_or_commit_action_is_ever_returned(self):
        u3 = Spec("u3", "MV-103", "/m/old/u3", "/v/preserved/u3", False, "/v/preserved",
                  (Leaf("x.json", b"[]"),), ("x.json",))
        u4 = Spec("u4", "MV-104", "/v/p/u4", "/v/preserved/u4", True, "/m/experiments/c10r/runs", (Leaf("r.json", b"{}"),))
        for specs in ([U1, U2], [U1._replace(tracked=())], [u3], [u4]):
            with self.subTest(specs=[s.name for s in specs]):
                actions = core.run_unit(**scenario(specs)[0])["actions"]
                self.assertLessEqual({a["action"] for a in actions}, ALLOWED)
                for a in actions:
                    self.assertEqual(set(a), {"operation_id", "action", "source", "target"})
                    for word in ("overwrite", "delete", "commit", "unlink", "replace", "force"):
                        self.assertNotIn(word, a["action"])

    def test_actions_carry_the_mv_id_of_their_unit(self):
        ops = {a["operation_id"] for a in run()["actions"]}
        self.assertEqual(ops, {"MV-101", "MV-102"})


class Documents(unittest.TestCase):
    def setUp(self):
        self.kw, self.plan, self.manifests = scenario()
        self.result = core.run_unit(**self.kw)
        self.docs = docs(self.result)

    def doc(self, name):
        return self.docs[f"{CUSTODY}/{name}"]

    def test_documents_are_written_bound_first_and_retention_last(self):
        self.assertEqual([d["path"] for d in self.result["documents"]],
                         [f"{CUSTODY}/{n}" for n in ("leaves.json", "routes.tsv", "repairs.json", "journal.jsonl",
                                                     "executor.json", "retention.json")])

    def test_retention_follows_the_spec_shape_minus_metadata_and_binds_each_document(self):
        retention = json.loads(self.doc("retention.json"))
        self.assertEqual(set(retention), {"schema_version", "leaves", "routes", "repairs", "executor", "containers"})
        self.assertEqual(retention["schema_version"], 1)
        self.assertEqual(retention["containers"], [])
        for key, name in (("leaves", "leaves.json"), ("routes", "routes.tsv"), ("repairs", "repairs.json"),
                          ("executor", "executor.json")):
            self.assertEqual(retention[key], {"path": f"{CUSTODY}/{name}", "sha256": sha(self.doc(name))})
        self.assertEqual(self.doc("retention.json"), canonical(retention))

    def test_leaves_are_the_fresh_manifest_leaves_without_root_or_git_roots(self):
        leaves = json.loads(self.doc("leaves.json"))
        self.assertEqual(leaves, {"schema_version": 1, "leaves": self.manifests[U1.source]["leaves"]
                                  + self.manifests[U2.source]["leaves"]})

    def test_routes_name_each_leaf_its_target_kind_bytes_mv_id_and_split_class(self):
        lines = self.doc("routes.tsv").decode().split("\n")
        self.assertEqual(lines[0], "requirement_id\tsource\ttarget\tkind\tobserved_bytes\taction\tlane\tscientific_role")
        self.assertEqual(lines[1:], [
            f"MV-101\t/m/old/u1/a.json\t{T1}/a.json\tfile\t2\tMOVE\tlegacy-preservation\ttracked-record",
            f"MV-101\t/m/old/u1/b.bin\t{T1}/b.bin\tfile\t2\tMOVE\tlegacy-preservation\tgoverned-payload",
            f"MV-101\t/m/old/u1/link\t{T1}/link\tsymlink\t6\tMOVE\tlegacy-preservation\ttracked-record",
            f"MV-102\t/v/p/u2/c.log\t{T2}/c.log\tfile\t4\tMOVE\tlegacy-preservation\ttracked-record",
            ""])

    def test_repairs_are_an_empty_repair_set(self):
        self.assertEqual(self.doc("repairs.json"), b'{"repairs":[],"schema_version":1}')

    def test_journal_is_the_ordered_actions_one_json_line_each(self):
        self.assertEqual(self.doc("journal.jsonl"), b"".join(canonical(a) + b"\n" for a in self.result["actions"]))

    def test_executor_has_one_operation_per_mv_id_bound_to_plan_approval_and_journal(self):
        executor = json.loads(self.doc("executor.json"))
        plan_bytes, approval_bytes = self.kw["plan"][1], self.kw["approval"][1]
        self.assertEqual(executor, {"schema_version": 1, "operations": [
            {"operation_id": rid, "prd_ids": ["ICM-R4"],
             "plan": {"path": PLAN_PATH, "sha256": sha(plan_bytes)},
             "approval": {"path": APPROVAL_PATH, "sha256": sha(approval_bytes)},
             "journal": {"path": f"{CUSTODY}/journal.jsonl", "sha256": sha(self.doc("journal.jsonl"))},
             "verification": None, "readers": None, "acceptance": None, "rollback": None}
            for rid in ("MV-101", "MV-102")]})
        self.assertEqual([op["operation_id"] for op in executor["operations"]], self.plan["replaces"])

    def test_output_is_deterministic_and_inputs_are_not_changed(self):
        kw = scenario()[0]
        before = copy.deepcopy(kw)
        self.assertEqual(core.run_unit(**kw), core.run_unit(**kw))
        self.assertEqual(kw, before)
        self.assertEqual(core.run_unit(**kw), self.result)

    def test_tuples_are_accepted_for_sequences(self):
        kw = scenario()[0]
        for key in ("units", "tracked", "targets", "run_units"):
            kw[key] = tuple(kw[key])
        self.assertEqual(core.run_unit(**kw), self.result)


def _consumer():
    """The Step 204 / Step 202 consumer modules, from code/state (the wire contract's own checker)."""
    state = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "state")
    if state not in sys.path:
        sys.path.insert(0, state)
    import icm21_check
    import icm21_retained
    return icm21_check, icm21_retained


class Consumer(unittest.TestCase):
    """The documents pass the merged checkers that read them: check_retained (post stage) and the wire schema."""

    @classmethod
    def setUpClass(cls):
        cls.check, cls.retained = _consumer()

    def setUp(self):
        self.kw, self.plan, self.manifests = scenario()
        self.result = core.run_unit(**self.kw)
        self.docs = docs(self.result)
        self.docs[APPROVAL_PATH] = self.kw["approval"][1]
        self.retention = json.loads(self.docs[f"{CUSTODY}/retention.json"])
        targets = {u["source"]: u["target"] for u in self.plan["units"]}
        self.post = []
        for source, m in self.manifests.items():
            for leaf in m["leaves"]:
                self.post.append({**leaf, "source": targets[source] + leaf["source"][len(source):]})

    def observed(self, leaves):
        return {"schema_version": 1, "leaves": leaves}

    def test_executor_is_wire_executor_evidence(self):
        self.check.validate_wire("ExecutorEvidence", json.loads(self.docs[f"{CUSTODY}/executor.json"]),
                                 self.retained.wire_schema(), {})

    def test_documents_parse_with_the_consumer_parsers(self):
        R = self.retained
        self.assertEqual(set(self.retention), R.RETENTION_KEYS)
        self.assertEqual(len(R.leaf_manifest(json.loads(self.docs[f"{CUSTODY}/leaves.json"]), "admitted")), 4)
        self.assertEqual(len(R.route_table(self.docs[f"{CUSTODY}/routes.tsv"])), 4)
        self.assertEqual(R.repair_set(json.loads(self.docs[f"{CUSTODY}/repairs.json"])), {})
        self.assertEqual(R.approved_plans(self.retention["executor"], self.docs), set())  # G4: no rewrite approved

    def test_a_completed_move_passes_check_retained(self):
        self.assertEqual(self.retained.check_retained(M, self.retention, self.docs, self.observed(self.post)), ())

    def test_a_leaf_left_at_its_source_fails_check_retained(self):
        leaves = [leaf for leaf in self.post if not leaf["source"].endswith("/a.json")]
        leaves.append(self.manifests[U1.source]["leaves"][0])
        found = self.retained.check_retained(M, self.retention, self.docs, self.observed(leaves))
        self.assertIn("FAIL", {f["status"] for f in found})

    def test_a_corrupted_byte_after_the_move_fails_check_retained(self):
        leaves = copy.deepcopy(self.post)
        leaves[0]["sha256"] = sha(b"corrupt")
        found = self.retained.check_retained(M, self.retention, self.docs, self.observed(leaves))
        self.assertIn("FAIL", {f["status"] for f in found})


class Refuses(unittest.TestCase):
    def refuses(self, kw, where, reason):
        with self.assertRaises(fdsafe.Refusal) as caught:
            core.run_unit(**kw)
        self.assertIn(where, caught.exception.path)
        self.assertIn(reason, str(caught.exception))
        return caught.exception

    def over(self, **over):
        kw = scenario()[0]
        kw.update(over)
        return kw


class NegativeControls(Refuses):
    """The step's named refusals and its SPEC.md:711 negative controls, as rows."""

    def test_rows(self):
        def corrupt(fresh):
            fresh[U1.source]["leaves"][0]["sha256"] = sha(b"corrupted")

        rows = [
            ("unapproved: decision", scenario(approval_over={"decision": "rejected"})[0], APPROVAL_PATH, "not approved"),
            ("unapproved: gate", scenario(approval_over={"gate": "G5"})[0], APPROVAL_PATH, "gate"),
            ("corrupted byte", scenario(manifest_edit=corrupt)[0], U1.source, "pre-digest"),
            ("collision", self.over(targets=[{"target": T1, "exists": True, "base": "/m/experiments/c10r"},
                                             {"target": T2, "exists": False, "base": "/v"}]), T1, "already exists"),
            ("split run", self.over(run_units=["/m/old"]), U1.source, "splits run unit /m/old"),
            ("linked worktree", self.over(worktree={"top": M, "git_dir": "/m/.git/worktrees/x",
                                                    "common_dir": "/m/.git"}), "worktree", "linked worktree"),
        ]
        for name, kw, where, reason in rows:
            with self.subTest(name):
                self.refuses(kw, where, reason)


class ApprovalRefuses(Refuses):
    def test_approval_of_another_plan_or_version(self):
        self.refuses(scenario(approval_over={"plan_id": "S221"})[0], APPROVAL_PATH, "plan_id")
        self.refuses(scenario(approval_over={"plan_sha256": sha(b"other")})[0], APPROVAL_PATH, "plan_sha256")

    def test_expired_or_not_yet_valid(self):
        self.refuses(scenario(approval_over={"expires_at": NOW})[0], APPROVAL_PATH, "expired")
        self.refuses(scenario(approval_over={"approved_at": "2026-10-18T12:00:00.000001Z"})[0], APPROVAL_PATH,
                     "after now")

    def test_boundaries_admit(self):
        core.run_unit(**scenario(approval_over={"approved_at": NOW, "expires_at": "2026-10-18T12:00:00.000001Z"})[0])

    def test_fields(self):
        for key, value in (("approval_id", ""), ("approved_by", ""), ("approved_by", 7), ("approval_id", None)):
            with self.subTest(key=key, value=value):
                self.refuses(scenario(approval_over={key: value})[0], APPROVAL_PATH, key)

    def test_keys(self):
        kw = scenario()[0]
        doc = json.loads(kw["approval"][1])
        for edit in (lambda d: d.pop("gate"), lambda d: d.update(extra=1)):
            with self.subTest(edit=edit):
                d = copy.deepcopy(doc)
                edit(d)
                self.refuses({**kw, "approval": (APPROVAL_PATH, canonical(d))}, APPROVAL_PATH, "field")

    def test_instants(self):
        for bad in ("2026-13-01T00:00:00Z", "2026-02-30T00:00:00Z", "2026-10-18T24:00:00Z", "2026-10-18T12:00:00",
                    "2026-10-18T12:00:00+01:00", "2026-10-18 12:00:00Z", "2026-10-18T12:00:00.1234567Z", 20261018,
                    "0000-01-01T00:00:00Z", "2026-10-18T12:60:00Z", "2026-10-18T12:00:60Z"):
            with self.subTest(bad=bad):
                self.refuses(scenario(approval_over={"expires_at": bad})[0], APPROVAL_PATH, "expires_at")
                self.refuses(self.over(now=bad), "now", "UTC instant")

    def test_short_or_empty_instant_fields(self):
        for bad in ("26-10-18T12:00:00Z", "2026-1-18T12:00:00Z", "2026-10-1T12:00:00Z", "2026-10-18T1:00:00Z",
                    "2026-10-18T12:0:00Z", "2026-10-18T12:00:0Z", "2026-10-18T12:00:00.Z", "-10-18T12:00:00Z",
                    "2026--18T12:00:00Z", "2026-10-T12:00:00Z", "2026-10-18T:00:00Z", "2026-10-18T12::00Z",
                    "2026-10-18T12:00:Z"):
            with self.subTest(bad=bad):
                self.refuses(self.over(now=bad), "now", "UTC instant")

    def test_leap_day_and_z_forms_are_instants(self):
        core.run_unit(**scenario(approval_over={"expires_at": "2028-02-29T00:00:00Z"})[0])

    def test_approval_bytes(self):
        kw = scenario()[0]
        for data, reason in ((b"{", "not JSON"), (b"\xff", "not UTF-8"), (b"[]", "object"),
                             (b'{"a":1,"a":2}', "twice"), (b'{"a":NaN}', "NaN"), ("/m/x.json", "bytes")):
            with self.subTest(data=data):
                self.refuses({**kw, "approval": (APPROVAL_PATH, data)}, APPROVAL_PATH, reason)

    def test_approval_pair(self):
        kw = scenario()[0]
        for value in ((APPROVAL_PATH,), [APPROVAL_PATH, b"{}", 1], None, ("rel/a.json", kw["approval"][1])):
            with self.subTest(value=value):
                self.refuses({**kw, "approval": value}, "approval", "")


    def test_an_oversized_integer_or_deep_nesting_in_the_approval(self):
        kw = scenario()[0]
        for data, reason in ((b'{"approval_id":' + BIG + b'}', "5000 digits"),
                             (b'{"a":' + DEEP + b'}', "nests too deeply")):
            with self.subTest(reason=reason):
                self.refuses({**kw, "approval": (APPROVAL_PATH, data)}, APPROVAL_PATH, reason)

    def test_a_negative_integer_at_the_digit_limit_parses(self):
        kw = scenario()[0]
        data = kw["approval"][1].replace(b'"approval-0123456789ab"', b"-" + b"9" * 4300)  # the sign is no digit
        self.refuses({**kw, "approval": (APPROVAL_PATH, data)}, APPROVAL_PATH, "approval_id must be")


class PlanRefuses(Refuses):
    def plan(self, edit, where, reason, reseal_it=True):
        if reseal_it:
            kw = scenario(plan_edit=edit)[0]
        else:
            kw, plan, _ = scenario()
            doc = copy.deepcopy(plan)
            edit(doc)
            data = canonical(doc)
            kw.update(plan=(PLAN_PATH, data), approval=(APPROVAL_PATH, canonical(approval_doc(data))))
        return self.refuses(kw, where, reason)

    def test_digest_and_approval_string(self):
        self.plan(lambda d: d.update(bytes=999), PLAN_PATH, "is not the sha256 of the plan body", reseal_it=False)
        self.plan(lambda d: d.update(approval="G4 approve S220 sha256:" + "0" * 64), PLAN_PATH, "approval string",
                  reseal_it=False)

    def test_keys_and_schema(self):
        self.plan(lambda d: d.update(extra=1), PLAN_PATH, "field")
        self.plan(lambda d: d.pop("rollback"), PLAN_PATH, "field")
        self.plan(lambda d: d.update(schema_version=2), PLAN_PATH, "schema_version")
        self.plan(lambda d: d.update(schema_version=True), PLAN_PATH, "schema_version")
        self.plan(lambda d: d.update(id="bad id"), PLAN_PATH, "ID")

    def test_moves_and_replaces_must_derive_from_units(self):
        self.plan(lambda d: d["moves"].reverse(), PLAN_PATH, "moves")
        self.plan(lambda d: d["moves"][0].update(target="/m/elsewhere"), PLAN_PATH, "moves")
        self.plan(lambda d: d.update(replaces=["MV-101"]), PLAN_PATH, "replaces")

    def test_units(self):
        def unit(**over):
            def edit(d):
                d["units"][0].update(over)
            return edit

        self.plan(lambda d: d.update(units=[], moves=[], replaces=[]), PLAN_PATH, "at least one unit")
        self.plan(lambda d: d.update(units={}), PLAN_PATH, "list")
        self.plan(lambda d: d["units"][0].pop("basis"), "units[0]", "field")
        self.plan(unit(requirement_id="MV-1"), "units[0]", "MV-NNN")
        self.plan(lambda d: d["units"][0].update(manifest={"path": "/m/x.json"}), "units[0].manifest", "field")
        self.plan(lambda d: d["units"][0]["manifest"].update(sha256="ABC"), "units[0].manifest", "sha256")
        self.plan(lambda d: d["units"][0]["manifest"].update(path="m/x.json"), "units[0].manifest", "path")
        self.plan(unit(leaves=True), "units[0]", "leaves")
        self.plan(unit(bytes=-1), "units[0]", "bytes")

    def _move(self, i, **over):
        def edit(d):
            d["units"][i].update(over)
            d["moves"][i].update(over)
        return edit

    def test_paths(self):
        self.plan(self._move(0, source="/m/old/../u1"), "units[0]", "normalized")
        self.plan(self._move(0, target="/m/experiments/<id>/u1"), "units[0]", "not exact")
        self.plan(self._move(0, target="/m/old/u1/inner"), "units[0]", "overlaps its own source")
        self.plan(self._move(0, target="/m/old"), "units[0]", "overlaps its own source")

    def test_two_units_that_overlap(self):
        self.plan(self._move(1, target=T1 + "/x"), "units[1]", "overlaps")
        self.plan(self._move(1, target="/m/old/u1/y"), "units[1]", "overlaps")
        self.plan(self._move(1, source="/m/experiments/c10r/runs/u1/z"), "units[1]", "overlaps")

    def test_plan_bytes(self):
        kw = scenario()[0]
        for data, reason in ((b"{", "not JSON"), (b"\xff", "not UTF-8"), (b'"x"', "object"),
                             (b'{"id":"a","id":"b"}', "twice"), (b'{"a":Infinity}', "Infinity"),
                             (b'{"a":"\\ud800"}', "surrogate"), (PLAN_PATH, "bytes"), (None, "bytes")):
            with self.subTest(data=data):
                self.refuses({**kw, "plan": (PLAN_PATH, data)}, PLAN_PATH, reason)

    def test_plan_path(self):
        kw = scenario()[0]
        self.refuses({**kw, "plan": ("plans/S220.json", kw["plan"][1])}, "plan", "absolute")

    def test_repeated_mv_ids(self):
        def edit(d):
            d["units"][1]["requirement_id"] = d["moves"][1]["id"] = "MV-101"
            d["replaces"] = ["MV-101", "MV-101"]
        self.plan(edit, PLAN_PATH, "unique MV ids")

    def test_manifest_sha256_shape(self):
        for bad in ("abc", "a" * 63, "a" * 65, "g" * 64, 5):
            with self.subTest(bad=bad):
                self.plan(lambda d: d["units"][0]["manifest"].update(sha256=bad), "units[0].manifest", "sha256")

    def test_leaf_count_and_bytes_must_match_the_fresh_manifest(self):
        self.plan(lambda d: d["units"][0].update(leaves=4), U1.source, "leaves")
        self.plan(lambda d: d["units"][0].update(bytes=11), U1.source, "bytes")


    def test_an_oversized_integer_or_deep_nesting_in_the_plan(self):
        kw = scenario()[0]
        for data, reason in ((BIG, "5000 digits"), (DEEP, "nests too deeply")):
            with self.subTest(reason=reason):
                self.refuses({**kw, "plan": (PLAN_PATH, data)}, PLAN_PATH, reason)

    def test_no_interpreter_digit_limit_admits_any_integer(self):
        old = sys.get_int_max_str_digits()
        self.addCleanup(sys.set_int_max_str_digits, old)
        sys.set_int_max_str_digits(0)
        self.assertEqual(len(run()["actions"]), 5)
        units = copy.deepcopy(scenario()[0]["units"])
        units[0]["split"] = units[0]["split"].replace(b'"size": 2', b'"size": ' + BIG, 1)
        self.refuses(self.over(units=units), "split", "disagrees")


class UnitRefuses(Refuses):
    def test_corrupted_byte_names_both_digests(self):
        def corrupt(fresh):
            fresh[U2.source]["leaves"][0]["bytes"] = 5

        kw, plan, _ = scenario(manifest_edit=corrupt)
        err = self.refuses(kw, U2.source, "pre-digest")
        self.assertIn(plan["units"][1]["manifest"]["sha256"], str(err))

    def test_manifest_root_must_be_the_source(self):
        def edit(d):
            d["units"][0]["source"] = d["moves"][0]["source"] = "/m/old/u0"
        kw = scenario(plan_edit=edit)[0]
        kw["units"][0]["source"] = "/m/old/u0"
        self.refuses(kw, "units[0].manifest", "root")

    def test_manifest_not_bytes_or_not_a_manifest(self):
        kw = scenario()[0]
        for value in ("/m/program/units/u1.json", None):
            with self.subTest(value=value):
                k = copy.deepcopy(kw)
                k["units"][0]["manifest"] = value
                self.refuses(k, U1.source, "bytes")

    def test_unit_list(self):
        kw = scenario()[0]
        self.refuses({**kw, "units": kw["units"][:1]}, "units", "exactly once")
        self.refuses({**kw, "units": kw["units"] + kw["units"][:1]}, "units", "exactly once")
        extra = dict(kw["units"][0], source="/m/old/u9")
        self.refuses({**kw, "units": kw["units"] + [extra]}, "units", "exactly once")
        self.refuses({**kw, "units": "x"}, "units", "list")
        bad = copy.deepcopy(kw["units"])
        bad[0]["extra"] = 1
        self.refuses({**kw, "units": bad}, "units[0]", "field")
        bad = copy.deepcopy(kw["units"])
        bad[0]["source"] = 5
        self.refuses({**kw, "units": bad}, "units[0]", "path")

    def test_control_characters_in_leaf_paths(self):
        spec = U2._replace(leaves=(Leaf("c\tlog", b"x"),))
        self.refuses(scenario([spec])[0], "/v/p/u2/c\tlog", "control character")
        spec = U2._replace(leaves=(Leaf("c\nlog", b"x"),))
        self.refuses(scenario([spec])[0], "/v/p/u2/c\nlog", "control character")


    def test_control_characters_in_plan_targets(self):
        for target in ("/v/preserved/u\t2", "/v/preserved/u\n2"):
            def edit(plan, target=target):
                for unit in plan["units"]:
                    if unit["source"] == U2.source:
                        unit["target"] = target
                for move, unit in zip(plan["moves"], plan["units"]):
                    move["target"] = unit["target"]
            kw = scenario(plan_edit=edit)[0]
            kw["targets"] = [r if r["target"] != T2 else {**r, "target": target} for r in kw["targets"]]
            with self.subTest(target=target):
                self.refuses(kw, target + "/c.log", "holds a control character")


class LinkBoundary(Refuses):
    """SPEC.md:711: a link that crosses the unit boundary refuses the unit (icm21_moves.link_boundary_failures)."""

    def links(self, *leaves):
        return scenario([U1._replace(leaves=leaves, tracked=())])[0]

    def test_a_symlink_leaving_or_looping_refuses_the_unit(self):
        for text, reason in (("../outside", "link crosses the unit boundary: /m/old/u1/link"),
                             ("/outside", "link crosses the unit boundary: /m/old/u1/link"),
                             ("link", "ambiguous link (loop): /m/old/u1/link")):
            with self.subTest(text=text):
                err = self.refuses(self.links(Leaf("a.json", b"{}"), Leaf("link", None, text)), U1.source, reason)
                self.assertEqual(err.path, U1.source)

    def test_the_refusal_names_the_first_failure_in_check_order(self):
        kw = self.links(Leaf("a", None, "/x"), Leaf("b", None, "b"))
        err = self.refuses(kw, U1.source, "link crosses the unit boundary: /m/old/u1/a")
        self.assertNotIn("/m/old/u1/b", str(err))

    def test_a_hard_link_with_a_name_outside_the_unit_refuses(self):
        def outside(leaves):
            leaves[0]["nlink"] = 2

        kw = rebind(scenario([U2])[0], outside)
        err = self.refuses(kw, U2.source, "hard link crosses the unit boundary: /v/p/u2/c.log")
        self.assertEqual(err.path, U2.source)

    def test_links_that_stay_inside_the_unit_return_actions(self):
        kw = self.links(Leaf("a.json", b"{}"), Leaf("d/link", None, "../a.json"))
        self.assertIn(act("MV-101", "mv", "/m/old/u1", T1), core.run_unit(**kw)["actions"])

        def pair(leaves):
            for leaf in leaves:
                leaf.update(inode=leaves[0]["inode"], nlink=2)

        kw = rebind(scenario([U2._replace(leaves=(Leaf("c.log", b"x"), Leaf("d.log", b"x")))])[0], pair)
        self.assertEqual(core.run_unit(**kw)["actions"],
                         [act("MV-102", "mkdir", target="/v/preserved"), act("MV-102", "mv", "/v/p/u2", T2)])


class ZeroSizes(unittest.TestCase):
    """Zero is a legal size: a unit of zero-byte files and a unit with no leaves both move."""

    def test_zero_byte_and_zero_leaf_units_return_actions(self):
        for leaves in ((Leaf("zero", b""), Leaf("empty", b"")), ()):
            with self.subTest(leaves=len(leaves)):
                kw = scenario([U2._replace(leaves=leaves)])[0]
                self.assertEqual(core.run_unit(**kw)["actions"],
                                 [act("MV-102", "mkdir", target="/v/preserved"), act("MV-102", "mv", "/v/p/u2", T2)])


class SplitRefuses(Refuses):
    def split(self, edit, where, reason):
        return self.refuses(scenario(split_edit=edit)[0], where, reason)

    def leaf(self, **over):
        def edit(s):
            s[U1.source]["leaves"][0].update(over)
        return edit

    def test_rows(self):
        rows = [
            ("root", lambda s: s[U1.source].update(root="/m/old/other"), "root"),
            ("keys", lambda s: s[U1.source].update(extra=1), "field"),
            ("leaf keys", lambda s: s[U1.source]["leaves"][0].pop("link"), "field"),
            ("missing leaf", lambda s: s[U1.source]["leaves"].pop(1), "does not cover"),
            ("unknown leaf", self.leaf(path="zz.json"), "not a manifest leaf"),
            ("duplicate", lambda s: s[U1.source]["leaves"].append(dict(s[U1.source]["leaves"][0])), "twice"),
            ("class", self.leaf(**{"class": "record"}), "class"),
            ("size", self.leaf(size=3), "disagrees"),
            ("sha", self.leaf(sha256=sha(b"no")), "disagrees"),
            ("kind file as link", self.leaf(kind="link", size=None, sha256=None, link="x"), "disagrees"),
            ("link text", lambda s: s[U1.source]["leaves"][2].update(link="b.bin"), "disagrees"),
            ("link as file", lambda s: s[U1.source]["leaves"][2].update(kind="file", size=6, sha256=sha(b"a.json"),
                                                                     link=None), "disagrees"),
            ("absolute path", self.leaf(path="/m/old/u1/a.json"), "relative path"),
            ("parent path", self.leaf(path="../u1/a.json"), "relative path"),
            ("dot path", self.leaf(path="./a.json"), "relative path"),
            ("empty path", self.leaf(path=""), "relative path"),
            ("leaves not a list", lambda s: s[U1.source].update(leaves={}), "list"),
        ]
        for name, edit, reason in rows:
            with self.subTest(name):
                self.split(edit, "split", reason)

    def test_split_bytes(self):
        kw = scenario()[0]
        for value, reason in ((b"[1]", "object"), (b"{", "not JSON"), ("/m/split.json", "bytes")):
            with self.subTest(value=value):
                k = copy.deepcopy(kw)
                k["units"][0]["split"] = value
                self.refuses(k, U1.source, reason)

    def test_a_socket_leaf_has_no_split_row(self):
        doc = manifest_doc(U2)
        doc["leaves"].append({"source": "/v/p/u2/sock", "kind": "socket", "bytes": 0, "sha256": sha(b""),
                              "link_text": None, "device": 1, "inode": 2, "nlink": 1})
        k = scenario([U2])[0]
        plan_doc = json.loads(k["plan"][1])
        plan_doc["units"][0]["manifest"]["sha256"] = sha(canonical(doc))
        plan_doc["moves"][0]["source_manifest"]["sha256"] = plan_doc["moves"][0]["before_sha256"] = sha(canonical(doc))
        plan_doc["units"][0]["leaves"] = 2
        plan_doc = reseal(plan_doc)
        data = canonical(plan_doc)
        k.update(plan=(PLAN_PATH, data), approval=(APPROVAL_PATH, canonical(approval_doc(data))))
        k["units"][0]["manifest"] = canonical(doc)
        self.refuses(k, "split", "does not cover")


    def test_non_string_class_or_kind(self):
        for field, value in (("class", []), ("class", {}), ("kind", []), ("kind", {"a": 1})):
            with self.subTest(field=field, value=value):
                self.split(self.leaf(**{field: value}), "split", field)

    def test_an_oversized_size(self):
        units = copy.deepcopy(scenario()[0]["units"])
        units[0]["split"] = units[0]["split"].replace(b'"size": 2', b'"size": ' + BIG, 1)
        self.refuses(self.over(units=units), "split", "5000 digits")

    def test_a_size_equal_in_value_but_not_an_integer(self):
        self.split(self.leaf(size=2.0), "split", "disagrees")  # a.json holds 2 bytes
        one = U1._replace(leaves=(Leaf("a.json", b"1"),) + U1.leaves[1:])
        self.refuses(scenario([one, U2], split_edit=self.leaf(size=True))[0], "split", "disagrees")


class ObservationRefuses(Refuses):
    def test_tracked(self):
        self.refuses(self.over(tracked=["/m/old/u1/nope"]), "/m/old/u1/nope", "not a manifest leaf")
        self.refuses(self.over(tracked=["/v/p/u2/c.log"]), "/v/p/u2/c.log", "outside the root")
        self.refuses(self.over(tracked=["/m/old/u1/a.json", "/m/old/u1/a.json"]), "/m/old/u1/a.json", "twice")
        self.refuses(self.over(tracked="/m/old/u1/a.json"), "tracked", "list")
        self.refuses(self.over(tracked=["/m/old/u1/./a.json"]), "tracked", "normalized")

    def test_worktree(self):
        rows = [({"top": "/m/sub", "git_dir": "/m/.git", "common_dir": "/m/.git"}, "main checkout"),
                ({"top": M, "git_dir": "/n/.git", "common_dir": "/n/.git"}, "main checkout"),
                ({"top": M, "git_dir": "/m/.git"}, "field"),
                ({"top": M, "git_dir": "/m/.git", "common_dir": "m/.git"}, "normalized"),
                ("linked", "object")]
        for value, reason in rows:
            with self.subTest(value=value):
                self.refuses(self.over(worktree=value), "worktree", reason)

    def test_targets(self):
        good = scenario()[0]["targets"]
        rows = [
            (good[:1], "targets", "exactly once"),
            (good + good[:1], "targets", "exactly once"),
            (good + [{"target": "/m/x", "exists": False, "base": "/m"}], "targets", "exactly once"),
            ([dict(good[0], exists=1), good[1]], "targets[0]", "exists"),
            ([dict(good[0], base=T1), good[1]], T1, "ancestor"),
            ([dict(good[0], base="/m/experiments/c10"), good[1]], T1, "ancestor"),
            ([dict(good[0], base="/m/experiments/c10r/"), good[1]], "targets[0]", "normalized"),
            ([{"target": T1, "exists": False}, good[1]], "targets[0]", "field"),
            ("x", "targets", "list"),
        ]
        for value, where, reason in rows:
            with self.subTest(value=value):
                self.refuses(self.over(targets=value), where, reason)

    def test_observations_that_disagree_on_a_folder(self):
        u5 = Spec("u5", "MV-105", "/m/old/u5", "/v/x", True, "/m/experiments/c10r/runs", (Leaf("e.json", b"1"),))
        kw = scenario([U1._replace(base="/m/experiments"), u5])[0]
        self.refuses(kw, "/m/experiments/c10r", "observed both")

    def test_run_units(self):
        core.run_unit(**self.over(run_units=["/m/old/u1", "/m/old/u1/inner", "/m/other", "/m/old/u10"]))
        self.refuses(self.over(run_units=["/m"]), U1.source, "splits run unit /m")
        self.refuses(self.over(run_units=["/v/p"]), U2.source, "splits run unit /v/p")
        self.refuses(self.over(run_units=["m/old"]), "run_units", "normalized")
        self.refuses(self.over(run_units=None), "run_units", "list")

    def test_custody_dir(self):
        for value in (U1.source, U1.source + "/custody", "/m/old", T1 + "/c", "/v"):
            with self.subTest(value=value):
                self.refuses(self.over(custody_dir=value), "custody_dir", "overlaps")
        self.refuses(self.over(custody_dir="/m/units/"), "custody_dir", "normalized")

    def test_a_unit_that_holds_the_root(self):
        self.refuses(self.over(root=U1.source, worktree={"top": U1.source, "git_dir": U1.source + "/.git",
                                                         "common_dir": U1.source + "/.git"}, tracked=[]),
                     U1.source, "holds the root")
        root = T1 + "/inner"
        self.refuses(self.over(root=root, worktree={"top": root, "git_dir": root + "/.git",
                                                    "common_dir": root + "/.git"}, tracked=[]),
                     U1.source, "holds the root")

    def test_a_missing_folder_above_a_source(self):
        u6 = Spec("u6", "MV-106", "/m/new/a/u6", "/m/new/b/u6", False, "/m", (Leaf("e.json", b"1"),))
        self.refuses(scenario([u6])[0], "/m/new", "observed both")

    def test_root(self):
        self.refuses(self.over(root="/m/"), "root", "normalized")

    def test_refusal_names_the_input_on_one_line(self):
        err = self.refuses(self.over(run_units=["/m/old"]), U1.source, "splits")
        self.assertIsNone(err.errno)
        self.assertEqual(len(str(err).splitlines()), 1)
        self.assertTrue(str(err).startswith(repr(U1.source)))


class Purity(unittest.TestCase):
    def test_core_makes_no_filesystem_or_subprocess_call(self):
        def forbidden(*args, **kwargs):
            raise AssertionError(f"filesystem or process call: {args!r}")

        kw = scenario()[0]
        names = ["open", "stat", "lstat", "fstat", "scandir", "listdir", "readlink", "getcwd", "access", "walk",
                 "rename", "replace", "mkdir", "makedirs", "unlink", "remove", "rmdir", "chmod", "system",
                 "path.exists", "path.lexists", "path.isdir", "path.isfile", "path.islink", "path.realpath",
                 "path.abspath", "getenv"]
        with contextlib.ExitStack() as stack:
            for name in names:
                target = os.path if name.startswith("path.") else os
                stack.enter_context(mock.patch.object(target, name.split(".")[-1], forbidden))
            for target, name in [(builtins, "open"), (io, "open"), (subprocess, "run"), (subprocess, "Popen"),
                                 (shutil, "move"), (shutil, "copy"), (shutil, "rmtree")]:
                stack.enter_context(mock.patch.object(target, name, forbidden))
            stack.enter_context(mock.patch.object(os, "environ", {}))
            result = core.run_unit(**kw)
        self.assertEqual(len(result["actions"]), 5)

    def test_module_names_no_filesystem_entry_point(self):
        text = core.__loader__.get_source(core.__name__)
        for token in ("import os", "open(", "import subprocess", "import shutil", "import time", "import datetime",
                      "os.environ", "getenv", "except Exception", "except ValueError", "except KeyError", "except:",
                      ".now(", "utcnow"):
            self.assertFalse(token in text, f"move_run_core names {token!r}")

    def test_unexpected_exceptions_propagate(self):
        kw = scenario()[0]
        for exc in (ValueError, KeyError, RuntimeError):
            with self.subTest(exc=exc), mock.patch.object(core.hashlib, "sha256", side_effect=exc("boom")):
                with self.assertRaises(exc) as caught:
                    core.run_unit(**kw)
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)


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

    def test_a_valid_run_makes_no_filesystem_or_process_call(self):
        kw = scenario()[0]
        warm = core.run_unit(**kw)  # warm-up outside the window: lazy imports may open files
        with self.window():
            seen = core.run_unit(**kw)
        self.assertEqual(seen, warm)

    def test_a_refused_run_makes_no_filesystem_or_process_call(self):
        kw = scenario()[0]
        kw["worktree"] = {"top": M, "git_dir": "/m/.git/worktrees/x", "common_dir": "/m/.git"}
        with self.window():
            with self.assertRaises(fdsafe.Refusal):
                core.run_unit(**kw)

    def test_a_path_in_place_of_bytes_is_refused_unopened(self):
        kw = scenario()[0]
        paths = {}
        for name, data in (("plan", kw["plan"][1]), ("approval", kw["approval"][1]),
                           ("manifest", kw["units"][0]["manifest"]), ("split", kw["units"][0]["split"])):
            path = os.path.join(self.scratch, name + ".json")
            with open(path, "wb") as f:
                f.write(data)
            paths[name] = path
        cases = [({**kw, "plan": (PLAN_PATH, paths["plan"])}, PLAN_PATH),
                 ({**kw, "approval": (APPROVAL_PATH, paths["approval"])}, APPROVAL_PATH)]
        for key in ("manifest", "split"):
            units = copy.deepcopy(kw["units"])
            units[0][key] = paths[key]
            cases.append(({**kw, "units": units}, U1.source))
        for case, where in cases:
            with self.subTest(where=where):
                with self.assertRaises(fdsafe.Refusal):  # warm-up outside the window
                    core.run_unit(**case)
                with self.window():
                    with self.assertRaises(fdsafe.Refusal) as caught:
                        core.run_unit(**case)
                self.assertIn(where, caught.exception.path)


class ValidatorShapeRefuses(unittest.TestCase):
    """Every untrusted object/list/path boundary refuses with its input path.

    Manifest edits are rebound into the plan and approval: a stale digest must not
    hide a missing delegated validation. Each row starts with an independent fixture.
    """

    def test_malformed_boundary_rows(self):
        manifest = "units[0].manifest"
        leaf = manifest + ".leaves[0]"
        git = manifest + ".git_roots[0]"
        split = U2.source + " split"
        source = U2.source + "/c.log"
        missing_git = manifest_doc(U2)
        del missing_git["git_roots"]
        # document, field path, malformed value, exact Refusal.path, reason
        rows = [
            ("kw", ("plan",), None, "plan", "list"),
            ("kw", ("plan",), [], "plan", "pair"),
            ("kw", ("plan",), ({}, b"{}"), "plan", "path"),
            ("kw", ("approval",), None, "approval", "list"),
            ("kw", ("approval",), [], "approval", "pair"),
            ("kw", ("approval",), ({}, b"{}"), "approval", "path"),
            ("plan", (), [], PLAN_PATH, "object"),
            ("plan", ("id",), {}, PLAN_PATH, "ID"),
            ("plan", ("units",), None, PLAN_PATH, "list"),
            ("plan", ("units", 0), None, "units[0]", "object"),
            ("plan", ("units", 0), [], "units[0]", "object"),
            ("plan", ("units", 0, "requirement_id"), {}, "units[0]", "MV-NNN"),
            ("plan", ("units", 0, "source"), {}, "units[0]", "path"),
            ("plan", ("units", 0, "target"), [], "units[0]", "path"),
            ("plan", ("units", 0, "manifest"), None, manifest, "object"),
            ("plan", ("units", 0, "manifest"), [], manifest, "object"),
            ("plan", ("units", 0, "manifest", "path"), {}, manifest, "path"),
            ("plan", ("units", 0, "leaves"), None, "units[0]", "leaves"),
            ("plan", ("units", 0, "bytes"), [], "units[0]", "bytes"),
            ("approval", (), [], APPROVAL_PATH, "object"),
            ("approval", ("approved_at",), None, APPROVAL_PATH, "UTC instant"),
            ("kw", ("worktree",), None, "worktree", "object"),
            ("kw", ("worktree", "top"), {}, "worktree", "path"),
            ("kw", ("worktree", "git_dir"), [], "worktree", "path"),
            ("kw", ("worktree", "common_dir"), None, "worktree", "path"),
            ("kw", ("units",), None, "units", "list"),
            ("kw", ("units", 0), None, "units[0]", "object"),
            ("kw", ("units", 0), [], "units[0]", "object"),
            ("kw", ("units", 0, "source"), {}, "units[0]", "path"),
            ("split", (), [], split, "object"),
            ("split", ("root",), {}, split, "root"),
            ("split", ("leaves",), None, split, "list"),
            ("split", ("leaves", 0), None, split + ".leaves[0]", "object"),
            ("split", ("leaves", 0), [], split + ".leaves[0]", "object"),
            ("split", ("leaves", 0, "path"), {}, split + ".leaves[0]", "relative path"),
            ("kw", ("tracked",), None, "tracked", "list"),
            ("kw", ("tracked",), [{}], "tracked", "path"),
            ("kw", ("targets",), None, "targets", "list"),
            ("kw", ("targets", 0), None, "targets[0]", "object"),
            ("kw", ("targets", 0), [], "targets[0]", "object"),
            ("kw", ("targets", 0, "target"), [], "targets[0]", "path"),
            ("kw", ("targets", 0, "base"), {}, "targets[0]", "path"),
            ("kw", ("run_units",), None, "run_units", "list"),
            ("kw", ("run_units",), [{}], "run_units", "path"),
            ("kw", ("root",), {}, "root", "path"),
            ("kw", ("custody_dir",), [], "custody_dir", "path"),
            ("manifest", (), missing_git, manifest, "has no git_roots; not a Step 201 manifest"),
            ("manifest", (), [], manifest, "object"),
            ("manifest", ("extra",), None, manifest, "unknown field"),
            ("manifest", ("schema_version",), None, manifest, "schema_version"),
            ("manifest", ("root",), {}, manifest, "path"),
            ("manifest", ("leaves",), None, manifest + ".leaves", "list"),
            ("manifest", ("leaves", 0), None, leaf, "object"),
            ("manifest", ("leaves", 0), [], leaf, "object"),
            ("manifest", ("leaves", 0, "extra"), None, source, "unknown field"),
            ("manifest", ("leaves", 0, "source"), {}, leaf, "path"),
            ("manifest", ("leaves", 0, "kind"), [], source, "kind"),
            ("manifest", ("leaves", 0, "bytes"), None, source, "bytes"),
            ("manifest", ("leaves", 0, "sha256"), {}, source, "sha256"),
            ("manifest", ("leaves", 0, "link_text"), [], source, "link_text"),
            ("manifest", ("leaves", 0, "device"), None, source, "device"),
            ("manifest", ("leaves", 0, "inode"), [], source, "inode"),
            ("manifest", ("leaves", 0, "nlink"), {}, source, "nlink"),
            ("manifest", ("git_roots",), None, manifest + ".git_roots", "list"),
            ("manifest", ("git_roots", 0), None, git, "object"),
            ("manifest", ("git_roots", 0), [], git, "object"),
            ("manifest", ("git_roots", 0, "extra"), None, git, "unknown field"),
            ("manifest", ("git_roots", 0, "path"), {}, git, "path"),
            ("manifest", ("git_roots", 0, "head"), [], git + ".head", "string or null"),
            ("manifest", ("git_roots", 0, "branch"), {}, git + ".branch", "string or null"),
            ("manifest", ("git_roots", 0, "dirty"), None, git + ".dirty", "list"),
            ("manifest", ("git_roots", 0, "dirty"), [None], git + ".dirty", "status records"),
        ]
        for document, path, value, where, reason in rows:
            with self.subTest(document=document, field=path, value=value):
                kw, plan, _ = scenario([U2])
                documents = {"kw": kw, "plan": plan, "approval": json.loads(kw["approval"][1]),
                             "split": json.loads(kw["units"][0]["split"]),
                             "manifest": json.loads(kw["units"][0]["manifest"])}
                if document == "manifest" and path[:1] == ("git_roots",) and len(path) > 1:
                    documents["manifest"]["git_roots"] = [
                        {"path": U2.source, "head": None, "branch": None, "dirty": []}]
                if path:
                    parent = documents[document]
                    for key in path[:-1]:
                        parent = parent[key]
                    parent[path[-1]] = copy.deepcopy(value)
                else:
                    documents[document] = copy.deepcopy(value)
                if document == "manifest":
                    data = canonical(documents["manifest"])
                    kw["units"][0]["manifest"] = data
                    plan["units"][0]["manifest"]["sha256"] = sha(data)
                if document in ("plan", "manifest"):
                    doc = documents["plan"]
                    data = canonical(reseal(doc) if isinstance(doc, dict) else doc)
                    kw["plan"] = (PLAN_PATH, data)
                    kw["approval"] = (APPROVAL_PATH, canonical(approval_doc(data)))
                if document == "approval":
                    kw["approval"] = (APPROVAL_PATH, canonical(documents["approval"]))
                if document == "split":
                    kw["units"][0]["split"] = canonical(documents["split"])
                with self.assertRaises(fdsafe.Refusal) as caught:
                    core.run_unit(**kw)
                self.assertEqual(caught.exception.path, where)
                self.assertIn(reason, str(caught.exception))


if __name__ == "__main__":
    unittest.main()
