"""Build one dry-run unit plan, and the check-plans and check-routes findings, from given values
(ICM v2.1 Part 2, Step 217).

Pure core of move_unit (its I/O shell is Step 209). It makes no filesystem call, runs no process or Git
command, reads no clock or environment and moves nothing: it takes rows and values (TSV texts with the
name of the file they came from, a Step 201 manifest's bytes, a Step 206 match, a Step 207 report,
Step 216 rows, observed paths) and returns the plan or the findings. Any malformed or ambiguous input is
a fdsafe.Refusal that names the input; nothing is guessed or repaired.

build_plan (DESIGN.md:473-475): one entry with its ID, digest, actions ("moves", the form Step 272 reads),
bytes, roots, risks, checks, rollback (the inverted move list, A/H-SLICE.md:52) and the exact approval
command. Every unit is a HOLD row of MOVE-REQUIREMENTS (SPEC.md:83, :732) and moves whole. Its target is
the candidate under experiments/<id>/ only when the Step 206 match is exact for that ID and the candidate
is not observed as existing; otherwise it is the row's exact V target, unchanged (SPEC.md:161,
DESIGN.md:254). An existing V target is a collision stop (DESIGN.md:292). The plan never carries an
overwrite, delete or commit action.

check_plans (Step 215): findings for a reader occurrence with no repair or historical row, a repair whose old_text does not
occur exactly once on its line (overlapping occurrences count), a row whose new_text is not under the
target of the entry move that holds the occurrence's old path, a row with no occurrence, a repeated row,
and a row whose old path no entry moves.

check_routes (Steps 241-242): findings over a producer route table (child, producer, owner, target): one
row per observed child, owner run, audit or build-receipt with a producer and an exact target outside the
source, or hold with the source's V target plus the child; no two targets equal or nested.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import posixpath
import re
import sys
from collections.abc import Mapping

from ops.migrate import dup_find_core, fdsafe
from ops.migrate.unit_manifest import canonical

Refusal = fdsafe.Refusal

REQUIREMENT_HEADER = ("requirement_id", "source", "target", "action", "observed_bytes", "class", "lane",
                      "check_id", "admission", "prd_ids")
REPAIR_HEADER = ("file", "line", "old_text", "new_text", "step")
HISTORICAL_HEADER = ("file", "line", "old_text")
ROUTE_HEADER = ("child", "producer", "owner", "target")
PLAN_FINDING_COLUMNS = ("kind", "file", "line", "old_text", "detail")
ROUTE_FINDING_COLUMNS = ("kind", "child", "detail")
OWNERS = frozenset(("run", "audit", "build-receipt"))
REPAIR_STEPS = frozenset({*range(261, 270), 387})
UNIT_KEYS = frozenset(("requirement_id", "manifest_path", "manifest_bytes", "registry", "candidate",
                       "readers", "comparison"))
MATCH_KEYS = frozenset(("unit", "result", "experiment_id", "candidates", "unknown", "evidence"))
GIT_ROOT_KEYS = frozenset(("path", "head", "branch", "dirty"))
STALE_KEYS = frozenset(("file", "line", "old_text", "old"))
UNVERIFIED_REQUIRED, UNVERIFIED_OPTIONAL = frozenset(("file", "reason")), frozenset(("line", "text"))
COMPARISON_KEYS = frozenset(("source", "relpath", "class", "equal_to", "differing_from", "same_inode", "hint"))
HINT_KEYS = frozenset(("sha256", "agrees"))
MOVE_KEYS = frozenset(("id", "prd_ids", "action", "source", "target", "kind", "bytes",
                       "before_sha256", "source_manifest", "lane", "reader_check_ids"))
OCCURRENCE_KEYS = frozenset(("file", "line", "old_text", "old", "text"))
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
MV_RE = re.compile(r"MV-[0-9]{3}")
DIGITS = re.compile(r"0|[1-9][0-9]*")
CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def _refuse(where: str, reason: str):
    raise Refusal(where, reason)


def _seq(value, where: str) -> list:
    if not isinstance(value, (list, tuple)):
        _refuse(where, f"expected a list, got {type(value).__name__}")
    return list(value)


def _map(value, where: str) -> Mapping:
    if not isinstance(value, Mapping):
        _refuse(where, f"expected an object, got {type(value).__name__}")
    return value


def _keys(row: Mapping, required: frozenset, where: str, optional: frozenset = frozenset()) -> None:
    missing, unknown = required - row.keys(), row.keys() - required - optional
    if missing or unknown:
        _refuse(where, f"missing field(s) {sorted(missing)}, unknown field(s) {sorted(map(str, unknown))}")


def _utf8(value: str) -> bool:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _text(value, where: str) -> str:
    if not isinstance(value, str) or not value or "\0" in value or not _utf8(value):
        _refuse(where, f"expected a non-empty UTF-8 string, got {value!r}")
    return value


def _id(value, where: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        _refuse(where, f"expected an ID, got {value!r}")
    return value


def _int(token: str, where: str) -> int:
    """Decimal text -> int. [LAW:single-enforcer] the one digit-limit check for manifest and TSV integers;
    [LAW:one-source-of-truth] the bound is the interpreter's own limit (0 means none)."""
    digits, limit = len(token.lstrip("-")), sys.get_int_max_str_digits()
    if 0 < limit < digits:
        _refuse(where, f"holds an integer of {digits} digits, over the interpreter limit of {limit}")
    return int(token)


def _line(value, where: str) -> int:
    if type(value) is not int or value < 1:
        _refuse(where, f"expected a line number >= 1, got {value!r}")
    return value


def _normal(value) -> bool:
    # normpath keeps a leading "//", so that is refused on its own.
    return (isinstance(value, str) and value.startswith("/") and not value.startswith("//") and "\0" not in value
            and posixpath.normpath(value) == value and _utf8(value))


def _path(value, where: str) -> str:
    if not _normal(value):
        _refuse(where, f"expected an absolute normalized path, got {value!r}")
    return value


def _exact(value) -> bool:
    """An exact target: absolute, normalized and with no angle-bracket placeholder (DESIGN.md:252)."""
    return _normal(value) and "<" not in value and ">" not in value


def _under(path: str, base: str) -> bool:
    return path == base or path.startswith(base.rstrip("/") + "/")


def _overlap(a: str, b: str) -> bool:
    return _under(a, b) or _under(b, a)


def _strings(value) -> bool:
    """A list of strings: the shape of Step 216's path lists and Step 201's dirty records."""
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _absolute(root: str, text: str) -> str:
    """A reader's spelling of a path, made absolute against the repo root ('./' spellings included)."""
    if text.startswith("/"):
        return text
    return root + "/" + (text[2:] if text.startswith("./") else text)


def _count(text: str, sub: str) -> int:
    return sum(1 for i in range(len(text)) if text.startswith(sub, i))


def tsv_lines(text: str, name: str) -> list[str]:
    """Parse LF or CRLF text into lines, with one ending per file."""
    # [LAW:single-enforcer] Annex and plan readers share this line-ending boundary.
    if not text.endswith("\n"):
        _refuse(name, "is empty or does not end with a newline")
    lines = text[:-1].split("\n")
    crlf = lines[0].endswith("\r")
    for number, line in enumerate(lines, 1):
        if line.endswith("\r") != crlf:
            _refuse(f"{name}:{number}", "mixes LF and CRLF line endings")
    # [LAW:parse-dont-validate] Return CR-free lines; field parsers own other embedded controls.
    lines = [line[:-1] for line in lines] if crlf else lines
    for number, line in enumerate(lines, 1):
        if "\r" in line:
            _refuse(f"{name}:{number}", "holds a CR that is not part of a line end")
    return lines


def _tsv(table, header: tuple, where: str) -> tuple[str, list[tuple[str, dict]]]:
    """(name, text) of one TSV file -> (name, [(name:line, row)]). LF or CRLF, one ending per file."""
    pair = _seq(table, where)
    if len(pair) != 2 or not isinstance(pair[0], str) or not pair[0] or not isinstance(pair[1], str):
        _refuse(where, "expected a (name, text) pair")
    name, text = pair
    rows = []
    for number, line in enumerate(tsv_lines(text, name), 1):
        at = f"{name}:{number}"
        cells = line.split("\t")
        if any(CONTROL.search(cell) for cell in cells):
            _refuse(at, "a cell holds a control character")
        if len(cells) != len(header):
            _refuse(at, f"expected {len(header)} cells, got {len(cells)}")
        if number == 1:
            if tuple(cells) != header:
                _refuse(at, f"expected the header {list(header)}")
            continue
        rows.append((at, dict(zip(header, cells))))
    return name, rows


def _requirements(tables) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for i, table in enumerate(_seq(tables, "requirement_tables")):
        for at, row in _tsv(table, REQUIREMENT_HEADER, f"requirement_tables[{i}]")[1]:
            if not MV_RE.fullmatch(row["requirement_id"]):
                _refuse(at, f"requirement_id {row['requirement_id']!r} is not MV-NNN")
            if row["requirement_id"] in out:
                _refuse(at, f"duplicate requirement {row['requirement_id']}")
            if not DIGITS.fullmatch(row["observed_bytes"]):
                _refuse(at, f"observed_bytes {row['observed_bytes']!r} is not a byte count")
            _text(row["action"], at)
            # [LAW:parse-dont-validate] Parse annex shape here; the wire schema owns PRD values.
            lane = _id(row["lane"], f"{at}.lane")
            prd_ids = row["prd_ids"].split(",")
            if "" in prd_ids or len(set(prd_ids)) != len(prd_ids):
                _refuse(f"{at}.prd_ids", "empty or repeated item")
            out[row["requirement_id"]] = {"source": _path(row["source"], at), "target": _path(row["target"], at),
                                          "action": row["action"],
                                          "observed_bytes": _int(row["observed_bytes"], at),
                                          "lane": lane, "prd_ids": prd_ids}
    return out


def _manifest(data, where: str) -> tuple[str, list, list[str], str]:
    """Step 201 manifest bytes -> (root, leaves, nested git root paths, sha256 of the bytes)."""
    if not isinstance(data, bytes):
        _refuse(where, f"expected the manifest bytes, got {type(data).__name__}")
    try:
        doc = json.loads(data.decode("utf-8"), parse_int=lambda token: _int(token, where))
    except UnicodeDecodeError:
        _refuse(where, "is not UTF-8")
    except json.JSONDecodeError as exc:
        _refuse(where, f"is not JSON ({exc.msg})")
    except RecursionError:  # [LAW:single-enforcer] caught only here and at the re-encode below
        _refuse(where, "nests too deeply")
    doc = _map(doc, where)
    if "git_roots" not in doc:
        _refuse(where, "has no git_roots; not a Step 201 manifest")
    root, leaves = dup_find_core._manifest(doc, where)
    try:
        same = canonical(doc) == data
    except UnicodeEncodeError:
        same = False
    except RecursionError:
        _refuse(where, "nests too deeply")
    if not same:
        _refuse(where, "is not the canonical JSON that Step 201 writes")
    git = []
    for j, g in enumerate(_seq(doc["git_roots"], f"{where}.git_roots")):
        gwhere = f"{where}.git_roots[{j}]"
        g = _map(g, gwhere)
        _keys(g, GIT_ROOT_KEYS, gwhere)
        if not _under(_path(g["path"], gwhere), root):
            _refuse(gwhere, f"git root {g['path']!r} is not inside {root!r}")
        for field in ("head", "branch"):
            if not isinstance(g[field], (str, type(None))):
                _refuse(f"{gwhere}.{field}", f"expected a string or null, got {type(g[field]).__name__}")
        if not _strings(g["dirty"]):
            _refuse(f"{gwhere}.dirty", f"expected a list of status records, got {g['dirty']!r}")
        git.append(g["path"])
    return root, leaves, git, hashlib.sha256(data).hexdigest()


def _registry(value, where: str, source: str) -> tuple[str, str | None, list[str]]:
    m = _map(value, where)
    _keys(m, MATCH_KEYS, where)
    unit = m["unit"]
    if not isinstance(unit, str) or not fnmatch.fnmatchcase(posixpath.basename(source), unit):
        _refuse(where, f"match is for unit {unit!r}, not {posixpath.basename(source)!r}")
    candidates = [_id(c, f"{where}.candidates") for c in _seq(m["candidates"], f"{where}.candidates")]
    unknown = _seq(m["unknown"], f"{where}.unknown")
    _seq(m["evidence"], f"{where}.evidence")
    result, eid = m["result"], m["experiment_id"]
    if result == "exact":
        if candidates != [_id(eid, f"{where}.experiment_id")] or unknown:
            _refuse(where, "an exact match names exactly one known experiment ID")
    elif result in ("ambiguous", "none"):
        if eid is not None:
            _refuse(where, f"a {result} match names no experiment ID")
    else:
        _refuse(where, f"result must be exact, ambiguous or none, got {result!r}")
    return result, eid, candidates


def _readers(value, where: str, root: str, source: str) -> tuple[list[str], list[str]]:
    report = _map(value, where)
    _keys(report, frozenset(("stale", "unverified")), where)
    stale = []
    for j, row in enumerate(_seq(report["stale"], f"{where}.stale")):
        rwhere = f"{where}.stale[{j}]"
        row = _map(row, rwhere)
        _keys(row, STALE_KEYS, rwhere)
        file, line = _text(row["file"], rwhere), _line(row["line"], rwhere)
        _text(row["old_text"], rwhere)
        old = _absolute(root, _text(row["old"], rwhere))
        if not _normal(old) or not _under(old, source):
            _refuse(rwhere, f"old path {row['old']!r} is not in this unit {source!r}")
        stale.append(f"{file}:{line}")
    unverified = []
    for j, row in enumerate(_seq(report["unverified"], f"{where}.unverified")):
        rwhere = f"{where}.unverified[{j}]"
        row = _map(row, rwhere)
        _keys(row, UNVERIFIED_REQUIRED, rwhere, UNVERIFIED_OPTIONAL)
        file, reason = _text(row["file"], rwhere), _text(row["reason"], rwhere)
        at = f"{file}:{_line(row['line'], rwhere)}" if "line" in row else file
        unverified.append(f"{at} {reason}")
    return sorted(set(stale)), sorted(set(unverified))


def _comparison(value, where: str, leaves: list) -> dict[str, list[str]] | None:
    """Step 216 rows covering every leaf once -> {class: sources}, or None when no comparison was made."""
    if value is None:
        return None
    sources = {leaf[0] for leaf in leaves}
    seen: dict[str, str] = {}
    for j, row in enumerate(_seq(value, where)):
        rwhere = f"{where}[{j}]"
        row = _map(row, rwhere)
        _keys(row, COMPARISON_KEYS, rwhere)
        source = row["source"]
        if not isinstance(source, str):
            _refuse(f"{rwhere}.source", f"expected a path string, got {type(source).__name__}")
        if source not in sources or source in seen:
            _refuse(rwhere, f"{source!r} is not a manifest leaf, or is compared twice")
        if row["class"] not in ("equal", "differing", "unique"):
            _refuse(rwhere, f"unknown class {row['class']!r}")
        if not isinstance(row["relpath"], str):
            _refuse(f"{rwhere}.relpath", f"expected a string, got {type(row['relpath']).__name__}")
        for field in ("equal_to", "differing_from", "same_inode"):
            if not _strings(row[field]):
                _refuse(f"{rwhere}.{field}", f"expected a list of path strings, got {row[field]!r}")
        if row["hint"] is not None:
            hint = _map(row["hint"], f"{rwhere}.hint")
            _keys(hint, HINT_KEYS, f"{rwhere}.hint")
            if not isinstance(hint["sha256"], str) or type(hint["agrees"]) is not bool:
                _refuse(f"{rwhere}.hint", f"expected null or {{sha256: string, agrees: bool}}, got {hint!r}")
        seen[source] = row["class"]
    if len(seen) != len(sources):
        _refuse(where, "does not cover every manifest leaf")
    out: dict[str, list[str]] = {}
    for source, cls in seen.items():
        out.setdefault(cls, []).append(source)
    return {cls: sorted(paths) for cls, paths in out.items()}


def _unit(value, where: str, root: str, table: dict, existing: frozenset) -> tuple[dict, list[dict], dict]:
    row = _map(value, where)
    _keys(row, UNIT_KEYS, where)
    rid = row["requirement_id"]
    if not isinstance(rid, str) or rid not in table:
        _refuse(f"{where}.requirement_id", f"no MOVE-REQUIREMENTS row {rid!r}")
    req = table[rid]
    if req["action"] != "HOLD":
        _refuse(rid, f"is {req['action']}, not HOLD; only a HOLD row is replaced by a unit plan")
    source = req["source"]
    mroot, leaves, git, digest = _manifest(row["manifest_bytes"], f"{where}.manifest_bytes")
    if mroot != source:
        _refuse(rid, f"manifest root {mroot!r} is not the requirement source {source!r}")
    manifest_path = _path(row["manifest_path"], f"{where}.manifest_path")
    if _under(manifest_path, source):
        _refuse(f"{where}.manifest_path", "the manifest lies inside the unit it describes")
    result, eid, candidates = _registry(row["registry"], f"{where}.registry", source)
    candidate = row["candidate"]
    if candidate is not None:
        _path(candidate, f"{where}.candidate")
    stale, unverified = _readers(row["readers"], f"{where}.readers", root, source)
    compared = _comparison(row["comparison"], f"{where}.comparison", leaves)

    risks: dict[str, list[str]] = {}
    target, basis = req["target"], "v-target"
    if result != "exact":
        risks[f"registry-{result}"] = candidates
    elif candidate is None:
        risks["no-candidate"] = []
    else:
        base = f"{root}/experiments/{eid}"
        if not _exact(candidate) or not _under(candidate, base) or candidate == base:
            _refuse(f"{where}.candidate", f"{candidate!r} is not an exact path below {base!r}")
        if candidate in existing:
            risks["candidate-exists"] = [candidate]
        else:
            target, basis = candidate, "registry"
    if basis == "v-target":
        if not _exact(target):
            _refuse(rid, f"V target {target!r} is not exact; the hold stays in place")
        if target in existing:
            _refuse(rid, f"V target {target!r} already exists; stop and keep the source unchanged")
    if _overlap(target, source):
        _refuse(rid, f"target {target!r} overlaps its own source")

    total = sum(leaf[2][1] for leaf in leaves)
    if total != req["observed_bytes"]:
        risks["bytes-drift"] = [f"annex {req['observed_bytes']}", f"manifest {total}"]
    for kind, items in (("readers", stale), ("unverified-readers", unverified), ("nested-git", git)):
        if items:
            risks[kind] = items
    if compared is None:
        risks["no-comparison"] = []
    else:
        for cls in ("equal", "differing"):
            if cls in compared:
                risks[cls] = compared[cls]
    planned = {"requirement_id": rid, "source": source, "target": target, "basis": basis,
               "experiment_id": eid if basis == "registry" else None,
               "manifest": {"path": manifest_path, "sha256": digest},
               "leaves": len(leaves), "bytes": total, "observed_bytes": req["observed_bytes"]}
    # [LAW:one-source-of-truth] A root leaf supplies its kind; folders retain their manifest-derived default.
    kinds = {leaf[0]: leaf[2][0] for leaf in leaves}
    move = {"id": rid, "prd_ids": req["prd_ids"], "action": "MOVE",
            "source": source, "target": target, "kind": kinds.get(source, "git-root" if source in git else "directory"),
            "bytes": total, "before_sha256": digest, "source_manifest": planned["manifest"],
            "lane": req["lane"], "reader_check_ids": []}
    return planned, [{"requirement_id": rid, "kind": k, "items": sorted(v)}
                     for k, v in risks.items()], move


def build_plan(*, entry_id, root, requirement_tables, units, existing_targets) -> dict:
    """One dry-run plan entry for whole-unit moves of the HOLD rows its units name."""
    eid = _id(entry_id, "entry_id")
    root = _path(root, "root")
    table = _requirements(requirement_tables)
    existing = frozenset(_path(p, "existing_targets") for p in _seq(existing_targets, "existing_targets"))
    raw = _seq(units, "units")
    if not raw:
        _refuse("units", "an entry places at least one unit")
    planned, risks, moves = [], [], []
    for i, value in enumerate(raw):
        u, r, move = _unit(value, f"units[{i}]", root, table, existing)
        for other in planned:  # a requirement named twice has one source, so it overlaps itself
            if _overlap(u["source"], other["source"]) or _overlap(u["target"], other["target"]) \
                    or _overlap(u["target"], other["source"]) or _overlap(u["source"], other["target"]):
                _refuse(u["requirement_id"], f"overlaps {other['requirement_id']} (source or target)")
        planned.append(u)
        moves.append(move)
        risks += r
    planned.sort(key=lambda u: u["source"])  # code point order is UTF-8 byte order
    moves.sort(key=lambda move: move["source"])
    body = {
        "schema_version": 1,
        "id": eid,
        "replaces": sorted(u["requirement_id"] for u in planned),
        "units": planned,
        "moves": moves,
        "bytes": sum(u["bytes"] for u in planned),
        "roots": {"sources": [m["source"] for m in moves],
                  "targets": sorted(m["target"] for m in moves)},
        "risks": sorted(risks, key=lambda r: (r["requirement_id"], r["kind"])),
        "checks": sorted([f"{u['requirement_id']} {c}" for u in planned
                          for c in ("manifest-digest", "target-absent", "C-MOVE")] + ["stage-check"]),
        "rollback": [{"source": m["target"], "target": m["source"]} for m in reversed(moves)],
    }
    digest = hashlib.sha256(canonical(body)).hexdigest()
    return {**body, "digest": digest, "approval": f"G4 approve {eid} sha256:{digest}"}


def _entry_moves(entries, root: str) -> dict[str, str]:
    """Every move of every entry: {source: target}. A source moved twice is ambiguous."""
    raw = _seq(entries, "entries")
    if not raw:
        _refuse("entries", "the plans document has no entries (never an empty PASS)")
    moves: dict[str, str] = {}
    ids = set()
    for i, entry in enumerate(raw):
        where = f"entries[{i}]"
        entry = _map(entry, where)
        if "id" not in entry or "moves" not in entry:
            _refuse(where, "an entry has an id and moves")
        eid = _id(entry["id"], f"{where}.id")
        if eid in ids:
            _refuse(f"{where}.id", f"duplicate entry {eid}")
        ids.add(eid)
        listed = _seq(entry["moves"], f"{where}.moves")
        if not listed:
            _refuse(f"{where}.moves", "an entry moves at least one source")
        for j, move in enumerate(listed):
            mwhere = f"{where}.moves[{j}]"
            move = _map(move, mwhere)
            _keys(move, MOVE_KEYS, mwhere)
            source = _path(move["source"], f"{mwhere}.source")
            if source in moves:
                _refuse(f"{mwhere}.source", f"{source!r} is moved by two moves")
            moves[source] = _path(move["target"], f"{mwhere}.target")
    return moves


def _target_of(old: str, moves: dict[str, str]) -> str | None:
    holders = [s for s in moves if _under(old, s)]
    return moves[max(holders, key=len)] if holders else None


def check_plans(*, root, entries, occurrences, repairs, historical) -> tuple:
    """Sorted findings for repair and historical coverage of reader occurrences."""
    root = _path(root, "root")
    moves = _entry_moves(entries, root)
    found = []
    by_key: dict[tuple, list[str]] = {}
    texts: dict[tuple, str] = {}
    for i, o in enumerate(_seq(occurrences, "occurrences")):
        where = f"occurrences[{i}]"
        o = _map(o, where)
        _keys(o, OCCURRENCE_KEYS, where)
        file, line = _text(o["file"], where), _line(o["line"], where)
        old_text, text = _text(o["old_text"], where), o["text"]
        if not isinstance(text, str) or old_text not in text:
            _refuse(where, f"old_text {old_text!r} is not in the text of its line")
        if texts.setdefault((file, line), text) != text:
            _refuse(where, f"{file}:{line} is given two different texts")
        old = _absolute(root, _text(o["old"], where))
        if not _normal(old):
            _refuse(where, f"old path {o['old']!r} is not a normalized path")
        by_key.setdefault((file, line, old_text), []).append(old)
    # [LAW:types-are-the-program] None means a historical row has no replacement text.
    rows: dict[tuple, tuple[str, str | None]] = {}
    for table, header, label in ((repairs, REPAIR_HEADER, "repairs"),
                                 (historical, HISTORICAL_HEADER, "historical")):
        name, parsed = _tsv(table, header, label)
        for at, row in parsed:
            file, old_text = (_text(row[k], f"{at}.{k}") for k in ("file", "old_text"))
            if not DIGITS.fullmatch(row["line"]):
                _refuse(at, "line and step are decimal numbers")
            line = _line(_int(row["line"], at), at)
            new_text = None
            if label == "repairs":
                new_text = _text(row["new_text"], f"{at}.new_text")
                if not DIGITS.fullmatch(row["step"]):
                    _refuse(at, "line and step are decimal numbers")
                step = _int(row["step"], at)
                if step not in REPAIR_STEPS:
                    # [LAW:one-source-of-truth] Refusals describe the same set that admits rows.
                    runs = []
                    for allowed in sorted(REPAIR_STEPS):
                        if runs and allowed == runs[-1][1] + 1:
                            runs[-1][1] = allowed
                        else:
                            runs.append([allowed, allowed])
                    parts = [str(a) if a == b else f"{a}-{b}" for a, b in runs]
                    _refuse(at, f"repair step {step} is not one of {', '.join(parts)}")
            key = (file, line, old_text)
            # [LAW:one-source-of-truth] One index detects repeats within and across tables.
            if key in rows:
                found.append(("duplicate-row", *key, f"repeats a row of {name}"))
                continue
            rows[key] = (name, new_text)
    # [LAW:no-silent-failure] Neither table covering a reader must remain a finding.
    for key, olds in by_key.items():
        if key not in rows:
            found.append(("no-row", *key, f"no repairs row for {olds[0]}"))
    for key, (name, new_text) in rows.items():
        if key not in by_key:
            found.append(("no-occurrence", *key, "no reader occurrence matches this row"))
            continue
        if new_text is not None:
            n = _count(texts[key[:2]], key[2])
            if n != 1:
                found.append(("not-once", *key, f"old_text occurs {n} times on its line"))
        for old in sorted(set(by_key[key])):
            target = _target_of(old, moves)
            if target is None:
                found.append(("no-entry", *key, f"no entry moves {old}"))
                continue
            if new_text is not None:
                new = _absolute(root, new_text)
                if not _normal(new) or not _under(new, target):
                    found.append(("not-under-target", *key, f"new_text {new_text} is not under {target}"))
    return tuple(sorted(found))


def check_routes(*, routes, source, children, hold_target) -> tuple:
    """Findings (ROUTE_FINDING_COLUMNS tuples, sorted) for one producer route table of source's children."""
    source = _path(source, "source")
    hold_target = _path(hold_target, "hold_target")
    if not _exact(hold_target):
        _refuse("hold_target", f"{hold_target!r} is not exact")
    if _overlap(hold_target, source):
        _refuse("hold_target", f"{hold_target!r} overlaps the source {source!r}")
    kids = _seq(children, "children")
    if not kids:
        _refuse("children", "the source has no children (never an empty PASS)")
    for kid in kids:
        if not isinstance(kid, str) or kid in ("", ".", "..") or "/" in kid or "\0" in kid:
            _refuse("children", f"{kid!r} is not a child name")
    if len(set(kids)) != len(kids):
        _refuse("children", "a child is listed twice")
    known = set(kids)
    found = []
    seen: dict[str, str] = {}
    _, parsed = _tsv(routes, ROUTE_HEADER, "routes")
    for at, row in parsed:
        child, owner, target = _text(row["child"], f"{at}.child"), row["owner"], row["target"]
        if child in seen:
            found.append(("duplicate-child", child, f"{at} repeats the row for {child}"))
            continue
        if child not in known:
            found.append(("unknown-child", child, f"{source} has no child {child}"))
        if owner == "hold":
            if not _exact(f"{hold_target}/{child}"):
                found.append(("inexact-target", child, f"the hold target {hold_target}/{child} is not exact"))
            elif target != f"{hold_target}/{child}":
                found.append(("hold-target", child, f"a hold row targets {hold_target}/{child}, not {target}"))
        elif owner not in OWNERS:
            found.append(("bad-owner", child, f"owner {owner!r} is not run, audit, build-receipt or hold"))
        elif not row["producer"]:
            found.append(("no-producer", child, "a routed row names its producer"))
        elif not _exact(target):
            found.append(("inexact-target", child, f"target {target!r} is not an exact absolute path"))
        elif _overlap(target, source):
            found.append(("target-in-source", child, f"target {target} overlaps the source {source}"))
        seen[child] = target
    exact = [(child, target) for child, target in seen.items() if _exact(target)]
    for child, target in exact:
        if any(other != child and _overlap(target, t) for other, t in exact):
            found.append(("target-collision", child, target))
    for kid in kids:
        if kid not in seen:
            found.append(("no-row", kid, "no route row"))
    return tuple(sorted(found))
