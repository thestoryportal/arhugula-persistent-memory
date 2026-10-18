"""Turn one approved unit plan and its observed state into ordered actions and custody documents
(ICM v2.1 Part 2, Step 218).

Pure core of move_unit run (its I/O shell is Step 210). It makes no filesystem call, runs no process or
Git command and reads no clock or environment: the shell observes, passes the observations in as values
and runs only the actions returned. Any malformed, ambiguous or refusing input is a fdsafe.Refusal that
names the input; nothing is guessed or repaired, and a refusal returns no action, so the source stays
unchanged.

Inputs (each parsed once, at the top of run_unit):
- plan: (path, bytes) of one Step 217 build_plan document. Its digest must be the sha256 of its body and
  its approval string must name that digest; moves and replaces must be the units' own.
- approval: (path, bytes) of the native approval JSON (corpusctl core.py:367 keys). It must be a G4
  "approved" decision for this plan id and these plan bytes, with approved_at <= now < expires_at.
- now: the shell's clock reading, a UTC instant (Z or +00:00).
- units: one {source, manifest, split} per plan unit: the fresh Step 201 manifest bytes (their sha256
  must be the plan's pre-digest) and the Step 212 record_split document bytes covering every leaf.
- tracked: absolute paths `git ls-files` lists under the unit sources; each is a manifest leaf in M.
- worktree: {top, git_dir, common_dir} from `git rev-parse`; only the main checkout of root is admitted.
- targets: one {target, exists, base} per plan target: base is its nearest existing ancestor folder.
- run_units: observed run-unit roots; a unit inside one of them would split that run (SPEC.md:711).
- custody_dir: the folder the shell writes the documents in, outside every source and target.

Actions (A/H-SLICE.md:33-43), in plan order, each {operation_id (the MV id), action, source, target}:
mkdir for each missing target folder (parent first, once); then `git-mv` for a unit that holds a tracked
file and stays in M, else `mv`; then `git-rm-cached` (git rm --cached -r -- SRC) for a tracked unit that
leaves M, and `git-add` for each untracked tracked-record leaf that lands in M. There is no overwrite,
delete or commit action.

Documents (SPEC.md:190-196 minus MetadataSet, as A/H-SLICE.md item 9 drops it): leaves.json
(LeafManifest), routes.tsv (MOVE-LEAVES rows), repairs.json (an empty RepairSet: a unit move edits no
content), journal.jsonl (the ordered actions), executor.json (ExecutorEvidence: one OperationEvidence per
MV id) and retention.json (RetentionManifest binding the other five by path and sha256).
"""
from __future__ import annotations

import calendar
import hashlib
import json
import posixpath
import re
import sys
from pathlib import PurePosixPath
from typing import NamedTuple

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as plan_core
from ops.migrate.unit_manifest import canonical

# [LAW:no-shared-mutable-globals] exception: icm21_moves imports its code/state siblings by bare name, so that
# folder joins the process import path once, here at import, before any run.
sys.path.append(posixpath.join(posixpath.dirname(posixpath.dirname(posixpath.dirname(__file__))), "state"))
import icm21_moves  # noqa: E402

Refusal = fdsafe.Refusal
_refuse, _seq, _map, _keys, _id, _path = (plan_core._refuse, plan_core._seq, plan_core._map, plan_core._keys,
                                          plan_core._id, plan_core._path)

PLAN_KEYS = frozenset(("schema_version", "id", "replaces", "units", "moves", "bytes", "roots", "risks", "checks",
                       "rollback", "digest", "approval"))
PLAN_UNIT_KEYS = frozenset(("requirement_id", "source", "target", "basis", "experiment_id", "manifest", "leaves",
                            "bytes", "observed_bytes"))
BINDING_KEYS = frozenset(("path", "sha256"))
APPROVAL_KEYS = frozenset(("approval_id", "plan_id", "plan_sha256", "gate", "approved_by", "approved_at",
                           "expires_at", "decision"))
UNIT_KEYS = frozenset(("source", "manifest", "split"))
SPLIT_KEYS = frozenset(("root", "leaves"))
SPLIT_LEAF_KEYS = frozenset(("path", "class", "kind", "size", "sha256", "link"))
WORKTREE_KEYS = frozenset(("top", "git_dir", "common_dir"))
TARGET_KEYS = frozenset(("target", "exists", "base"))
RECORD = "tracked-record"
CLASSES = frozenset((RECORD, "attested-bulk", "governed-payload"))
SPLIT_KINDS = {"file": "file", "link": "symlink"}
ROUTE_HEADER = ("requirement_id", "source", "target", "kind", "observed_bytes", "action", "lane", "scientific_role")
PRD_IDS = ["ICM-R4"]
SHA_RE = re.compile(r"[0-9a-f]{64}")
INSTANT = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]{1,6}))?"
                     r"(?:Z|\+00:00)")


class Unit(NamedTuple):
    rid: str
    source: str
    target: str
    manifest_sha256: str
    leaves: int
    bytes: int


class Plan(NamedTuple):
    id: str
    binding: dict
    units: tuple


class Observed(NamedTuple):
    """One plan unit with its fresh leaves and each leaf's Step 212 class."""
    unit: Unit
    leaves: list
    classes: dict


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _inside(path: str, base: str) -> bool:
    return path != base and plan_core._under(path, base)


def _pair(value, where: str) -> tuple:
    pair = _seq(value, where)
    if len(pair) != 2:
        _refuse(where, "expected a (path, bytes) pair")
    return _path(pair[0], where), pair[1]


def _json(data, where: str):
    """The one parse of a JSON document: bytes, strict UTF-8, no repeated key, no NaN, no integer over the
    interpreter digit limit, no nesting past the recursion limit, no lone surrogate."""
    if not isinstance(data, bytes):
        _refuse(where, f"expected the document bytes, got {type(data).__name__}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        _refuse(where, "is not UTF-8")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                _refuse(where, f"names key {key!r} twice")
            out[key] = value
        return out

    def constant(token):
        _refuse(where, f"holds {token}")

    def integer(token):
        # [LAW:parse-dont-validate] refused inside the one parse, so no ValueError from int() escapes it.
        # [LAW:one-source-of-truth] the bound is the interpreter's own limit (0 means none), not a copy of it.
        digits, limit = len(token.lstrip("-")), sys.get_int_max_str_digits()
        if 0 < limit < digits:
            _refuse(where, f"holds an integer of {digits} digits, over the interpreter limit of {limit}")
        return int(token)

    # [LAW:single-enforcer] RecursionError is caught around these two calls only: the parse and its re-encode.
    try:
        doc = json.loads(text, object_pairs_hook=pairs, parse_constant=constant, parse_int=integer)
        canonical(doc)
    except json.JSONDecodeError as exc:
        _refuse(where, f"is not JSON ({exc.msg})")
    except UnicodeEncodeError:
        _refuse(where, "holds a lone surrogate")
    except RecursionError:
        _refuse(where, "nests too deeply")
    return doc


def _count(value, where: str, field: str) -> int:
    if type(value) is not int or value < 0:
        _refuse(where, f"{field} must be an integer >= 0, got {value!r}")
    return value


def _instant(value, where: str, field: str) -> tuple:
    """A UTC instant as a comparable tuple; no clock and no datetime parser is involved."""
    m = INSTANT.fullmatch(value) if isinstance(value, str) else None
    if m is None:
        _refuse(where, f"{field} is not a UTC instant: {value!r}")
    y, mo, d, h, mi, s = (int(g) for g in m.groups()[:6])
    if not (y >= 1 and 1 <= mo <= 12 and 1 <= d <= calendar.monthrange(y, mo)[1] and h < 24 and mi < 60 and s < 60):
        _refuse(where, f"{field} is not a UTC instant: {value!r}")
    return (y, mo, d, h, mi, s, int((m.group(7) or "").ljust(6, "0")))


def _plan_unit(value, where: str) -> Unit:
    row = _map(value, where)
    _keys(row, PLAN_UNIT_KEYS, where)
    rid = row["requirement_id"]
    if not isinstance(rid, str) or not plan_core.MV_RE.fullmatch(rid):
        _refuse(where, f"requirement_id {rid!r} is not MV-NNN")
    source, target = _path(row["source"], where), _path(row["target"], where)
    if not plan_core._exact(target):
        _refuse(where, f"target {target!r} is not exact")
    if plan_core._overlap(target, source):
        _refuse(where, f"target {target!r} overlaps its own source {source!r}")
    manifest = _map(row["manifest"], f"{where}.manifest")
    _keys(manifest, BINDING_KEYS, f"{where}.manifest")
    _path(manifest["path"], f"{where}.manifest")
    if not isinstance(manifest["sha256"], str) or not SHA_RE.fullmatch(manifest["sha256"]):
        _refuse(f"{where}.manifest", f"sha256 must be 64 lowercase hex digits, got {manifest['sha256']!r}")
    return Unit(rid, source, target, manifest["sha256"], _count(row["leaves"], where, "leaves"),
                _count(row["bytes"], where, "bytes"))


def _plan(value) -> Plan:
    path, data = _pair(value, "plan")
    doc = _map(_json(data, path), path)
    _keys(doc, PLAN_KEYS, path)
    if type(doc["schema_version"]) is not int or doc["schema_version"] != 1:
        _refuse(path, f"schema_version must be 1, got {doc['schema_version']!r}")
    eid = _id(doc["id"], path)
    body = {k: v for k, v in doc.items() if k not in ("digest", "approval")}
    digest = _sha(canonical(body))
    if doc["digest"] != digest:
        _refuse(path, f"digest {doc['digest']!r} is not the sha256 of the plan body {digest}")
    if doc["approval"] != f"G4 approve {eid} sha256:{digest}":
        _refuse(path, f"approval string {doc['approval']!r} does not name this plan and digest")
    raw = _seq(doc["units"], path)
    if not raw:
        _refuse(path, "a plan places at least one unit")
    units = tuple(_plan_unit(u, f"units[{i}]") for i, u in enumerate(raw))
    for i, unit in enumerate(units):
        for j, other in enumerate(units[:i]):
            if any(plan_core._overlap(a, b) for a in (unit.source, unit.target) for b in (other.source, other.target)):
                _refuse(f"units[{i}]", f"overlaps units[{j}] (source or target)")
    if doc["moves"] != [{"source": u.source, "target": u.target} for u in units]:
        _refuse(path, "moves are not the units' sources and targets in order")
    rids = [u.rid for u in units]
    if doc["replaces"] != sorted(rids) or len(set(rids)) != len(rids):
        _refuse(path, "replaces is not the units' unique MV ids")
    return Plan(eid, {"path": path, "sha256": _sha(data)}, units)


def _approval(value, plan: Plan, now: tuple) -> dict:
    path, data = _pair(value, "approval")
    doc = _map(_json(data, path), path)
    _keys(doc, APPROVAL_KEYS, path)
    for key in ("approval_id", "approved_by"):
        if not isinstance(doc[key], str) or not doc[key]:
            _refuse(path, f"{key} must be a non-empty string, got {doc[key]!r}")
    if doc["plan_id"] != plan.id:
        _refuse(path, f"plan_id {doc['plan_id']!r} is not the plan's id {plan.id!r}")
    if doc["plan_sha256"] != plan.binding["sha256"]:
        _refuse(path, f"plan_sha256 {doc['plan_sha256']!r} does not bind the plan bytes {plan.binding['sha256']}")
    if doc["gate"] != "G4":
        _refuse(path, f"gate {doc['gate']!r} is not G4")
    if doc["decision"] != "approved":
        _refuse(path, f"decision {doc['decision']!r}: the plan is not approved")
    if now < _instant(doc["approved_at"], path, "approved_at"):
        _refuse(path, "approved_at is after now")
    if now >= _instant(doc["expires_at"], path, "expires_at"):
        _refuse(path, f"the approval expired at {doc['expires_at']}")
    return {"path": path, "sha256": _sha(data)}


def _worktree(value, root: str) -> None:
    row = _map(value, "worktree")
    _keys(row, WORKTREE_KEYS, "worktree")
    top, git_dir, common = (_path(row[k], "worktree") for k in ("top", "git_dir", "common_dir"))
    if git_dir != common:
        _refuse("worktree", f"git_dir {git_dir!r} is not the common dir {common!r}: a linked worktree; never move "
                            "in a linked worktree (A/H-SLICE.md:37)")
    if top != root or common != posixpath.join(root, ".git"):
        _refuse("worktree", f"{top!r} with {common!r} is not the main checkout of {root!r}")


def _split(unit: Unit, data, leaves: list) -> dict:
    """{leaf source: Step 212 class}, from one split document that covers every manifest leaf once."""
    where = f"{unit.source} split"
    doc = _map(_json(data, where), where)
    _keys(doc, SPLIT_KEYS, where)
    if doc["root"] != unit.source:
        _refuse(where, f"root {doc['root']!r} is not the unit source")
    by_rel = {leaf["source"][len(unit.source) + 1:]: leaf for leaf in leaves}
    classes = {}
    for j, row in enumerate(_seq(doc["leaves"], where)):
        rwhere = f"{where}.leaves[{j}]"
        row = _map(row, rwhere)
        _keys(row, SPLIT_LEAF_KEYS, rwhere)
        rel = row["path"]
        if not isinstance(rel, str) or not rel or rel.startswith("/") or posixpath.normpath(rel) != rel \
                or rel.split("/")[0] == "..":
            _refuse(rwhere, f"path {rel!r} is not a relative path inside the unit")
        leaf = by_rel.get(rel)
        if leaf is None:
            _refuse(rwhere, f"{rel!r} is not a manifest leaf")
        if leaf["source"] in classes:
            _refuse(rwhere, f"{rel!r} is split twice")
        # [LAW:parse-dont-validate] a non-string class or kind is refused before a set or dict lookup can raise.
        if not isinstance(row["class"], str) or row["class"] not in CLASSES:
            _refuse(rwhere, f"class {row['class']!r} is not one of {sorted(CLASSES)}")
        if not isinstance(row["kind"], str):
            _refuse(rwhere, f"kind {row['kind']!r} is not a string")
        split = (SPLIT_KINDS.get(row["kind"]), row["size"], row["sha256"], row["link"])
        file = leaf["kind"] == "file"
        fresh = (leaf["kind"], leaf["bytes"] if file else None, leaf["sha256"] if file else None, leaf["link_text"])
        if canonical(split) != canonical(fresh):  # canonical JSON: true is not 1
            _refuse(rwhere, f"{rel!r} disagrees with its manifest leaf")
        classes[leaf["source"]] = row["class"]
    if len(classes) != len(leaves):
        _refuse(where, "does not cover every manifest leaf")
    return classes


def _observed(value, plan: Plan) -> tuple:
    rows: dict[str, list] = {}
    for i, row in enumerate(_seq(value, "units")):
        row = _map(row, f"units[{i}]")
        _keys(row, UNIT_KEYS, f"units[{i}]")
        rows.setdefault(_path(row["source"], f"units[{i}]"), []).append(row)
    if sorted(rows) != sorted(u.source for u in plan.units) or any(len(v) != 1 for v in rows.values()):
        _refuse("units", "must name each plan unit exactly once")
    out = []
    for i, unit in enumerate(plan.units):
        row = rows[unit.source][0]
        data = row["manifest"]
        if not isinstance(data, bytes):
            _refuse(unit.source, f"expected the fresh manifest bytes, got {type(data).__name__}")
        if _sha(data) != unit.manifest_sha256:
            _refuse(unit.source, f"changed pre-digest: the fresh manifest sha256 {_sha(data)} is not the plan's "
                                 f"{unit.manifest_sha256}; the source stays unchanged")
        root = plan_core._manifest(data, f"units[{i}].manifest")[0]
        if root != unit.source:
            _refuse(f"units[{i}].manifest", f"root {root!r} is not the unit source {unit.source!r}")
        leaves = json.loads(data)["leaves"]  # the canonical JSON _manifest has just checked
        if len(leaves) != unit.leaves:
            _refuse(unit.source, f"the plan counts {unit.leaves} leaves, the manifest has {len(leaves)}")
        if sum(leaf["bytes"] for leaf in leaves) != unit.bytes:
            _refuse(unit.source, f"the plan counts {unit.bytes} bytes, the manifest differs")
        for leaf in leaves:
            for path in (leaf["source"], unit.target + leaf["source"][len(unit.source):]):
                if plan_core.CONTROL.search(path):  # a route row is tab- and line-separated
                    _refuse(path, "holds a control character")
        out.append(Observed(unit, leaves, _split(unit, row["split"], leaves)))
    return tuple(out)


def _tracked(value, observed: tuple, root: str) -> frozenset:
    owner = {leaf["source"]: o.unit for o in observed for leaf in o.leaves}
    seen = set()
    for item in _seq(value, "tracked"):
        path = _path(item, "tracked")
        if path in seen:
            _refuse(path, "is listed twice")
        if path not in owner:
            _refuse(path, "is tracked but is not a manifest leaf of any unit")
        if not _inside(owner[path].source, root):
            _refuse(path, f"is tracked but its unit lies outside the root {root!r}")
        seen.add(path)
    return frozenset(seen)


def _folders(value, plan: Plan) -> dict:
    """{target: [missing folders, parent first]} from one observation per target; refuses a collision."""
    seen: dict[str, list] = {}
    for i, row in enumerate(_seq(value, "targets")):
        where = f"targets[{i}]"
        row = _map(row, where)
        _keys(row, TARGET_KEYS, where)
        target, base = _path(row["target"], where), _path(row["base"], where)
        if type(row["exists"]) is not bool:
            _refuse(where, f"exists must be true or false, got {row['exists']!r}")
        seen.setdefault(target, []).append((row["exists"], base))
    if sorted(seen) != sorted(u.target for u in plan.units) or any(len(v) != 1 for v in seen.values()):
        _refuse("targets", "must observe each plan target exactly once")
    chains = {}
    for unit in plan.units:
        exists, base = seen[unit.target][0]
        if exists:
            _refuse(unit.target, "already exists; stop and keep the source unchanged (DESIGN.md:292)")
        if not _inside(unit.target, base):
            _refuse(unit.target, f"base {base!r} is not an ancestor of the target")
        stem = base.rstrip("/")
        parts = unit.target[len(stem) + 1:].split("/")
        chains[unit.target] = [stem + "/" + "/".join(parts[:k]) for k in range(1, len(parts))]
    present = [seen[u.target][0][1] for u in plan.units] + [u.source for u in plan.units]
    for folder in sorted({f for chain in chains.values() for f in chain}):
        if any(plan_core._under(p, folder) for p in present):
            _refuse(folder, "is observed both missing and present (a base or source lies at or below it)")
    return chains


def _action(rid: str, action: str, source: str | None = None, target: str | None = None) -> dict:
    return {"operation_id": rid, "action": action, "source": source, "target": target}


def run_unit(*, root, plan, approval, now, units, tracked, worktree, targets, run_units, custody_dir) -> dict:
    """{actions: [...], documents: [{path, bytes}...]} for one approved plan, or a Refusal."""
    # [LAW:parse-dont-validate] every raw input is parsed here, once; the code below reads parsed values.
    root = _path(root, "root")
    parsed = _plan(plan)
    clock = _instant(now, "now", "now")
    approval_binding = _approval(approval, parsed, clock)
    _worktree(worktree, root)
    observed = _observed(units, parsed)
    tracked_leaves = _tracked(tracked, observed, root)
    chains = _folders(targets, parsed)
    runs = [_path(p, "run_units") for p in _seq(run_units, "run_units")]
    custody = _path(custody_dir, "custody_dir")
    for unit in parsed.units:
        if plan_core._under(root, unit.source) or plan_core._under(root, unit.target):
            _refuse(unit.source, f"the unit or its target {unit.target!r} holds the root {root!r}")
        for run in runs:
            if _inside(unit.source, run):
                _refuse(unit.source, f"the move splits run unit {run} (SPEC.md:711)")
        if plan_core._overlap(custody, unit.source) or plan_core._overlap(custody, unit.target):
            _refuse("custody_dir", f"{custody!r} overlaps {unit.source!r} or its target {unit.target!r}")
    for o in observed:
        # [LAW:single-enforcer] the link-boundary rule is icm21_moves'; this core refuses on its first finding.
        failures = icm21_moves.link_boundary_failures(
            [dict(leaf, source=PurePosixPath(leaf["source"])) for leaf in o.leaves], PurePosixPath(o.unit.source))
        if failures:
            _refuse(o.unit.source, failures[0])

    # [LAW:effects-at-boundaries] the actions are descriptions; Step 210 performs them.
    actions, made, routes = [], set(), []
    for o in observed:
        u = o.unit
        lands_in_m = _inside(u.target, root)
        holds_tracked = any(leaf["source"] in tracked_leaves for leaf in o.leaves)
        for folder in chains[u.target]:
            if folder not in made:
                made.add(folder)
                actions.append(_action(u.rid, "mkdir", target=folder))
        actions.append(_action(u.rid, "git-mv" if holds_tracked and lands_in_m else "mv", u.source, u.target))
        if holds_tracked and not lands_in_m:
            actions.append(_action(u.rid, "git-rm-cached", source=u.source))
        for leaf in o.leaves:
            target = u.target + leaf["source"][len(u.source):]
            routes.append((u.rid, leaf["source"], target, leaf["kind"], str(leaf["bytes"]), "MOVE", parsed.id,
                           o.classes[leaf["source"]]))
            if lands_in_m and o.classes[leaf["source"]] == RECORD and leaf["source"] not in tracked_leaves:
                actions.append(_action(u.rid, "git-add", target=target))

    def document(name: str, data: bytes) -> dict:
        return {"path": posixpath.join(custody, name), "bytes": data}

    def bind(doc: dict) -> dict:
        return {"path": doc["path"], "sha256": _sha(doc["bytes"])}

    leaves = document("leaves.json", canonical({"schema_version": 1, "leaves": [l for o in observed for l in o.leaves]}))
    route_doc = document("routes.tsv", "".join("\t".join(row) + "\n" for row in [ROUTE_HEADER, *routes]).encode())
    repairs = document("repairs.json", canonical({"schema_version": 1, "repairs": []}))
    journal = document("journal.jsonl", b"".join(canonical(a) + b"\n" for a in actions))
    executor = document("executor.json", canonical({"schema_version": 1, "operations": [
        {"operation_id": rid, "prd_ids": list(PRD_IDS), "plan": parsed.binding, "approval": approval_binding,
         "journal": bind(journal), "verification": None, "readers": None, "acceptance": None, "rollback": None}
        for rid in sorted(u.rid for u in parsed.units)]}))
    retention = document("retention.json", canonical({
        "schema_version": 1, "leaves": bind(leaves), "routes": bind(route_doc), "repairs": bind(repairs),
        "executor": bind(executor), "containers": []}))
    return {"actions": actions, "documents": [leaves, route_doc, repairs, journal, executor, retention]}
