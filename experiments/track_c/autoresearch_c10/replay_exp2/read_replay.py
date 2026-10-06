#!/usr/bin/env python3
"""Read the frozen D-C10r-exp2ctl control without importing the model."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

BASE_COMMIT = "92acd0378d23f4935df9a8bccc0137b36695a40f"
TEMPLATE_SHA = "e8605172dce0"
COLLISION_HEADS = frozenset(
    ("Drennik", "Vythorn", "Vorlex", "Kessivar", "Halquin", "Marsduq", "Glimsto", "Fluvane")
)
IMPORT_LOG = """import hashlib
import json
import os
import sys

_REPLAY_EDIT_PATH = os.path.abspath(__file__)
_REPLAY_EDIT_SHA256 = hashlib.sha256(open(_REPLAY_EDIT_PATH, "rb").read()).hexdigest()

"""
CONTEXT_LOG = """    _replay_templates_sha = hashlib.sha256(json.dumps(ctx).encode()).hexdigest()
    print(f"executed_edit_py_sha256: {_REPLAY_EDIT_SHA256}", flush=True)
    print(f"edit_context_templates_sha256: {_replay_templates_sha}", flush=True)
    with open(os.path.join(os.path.dirname(_REPLAY_EDIT_PATH), "replay_launch.json")) as _replay_f:
        _replay_launch = json.load(_replay_f)
    _replay_record = {
        "executed_edit_py_sha256": _REPLAY_EDIT_SHA256,
        "edit_context_templates_sha256": _replay_templates_sha,
        "edit_context_templates": ctx,
        "launch": _replay_launch,
    }
    _replay_run_dir = sys._getframe(1).f_locals["run_dir"]
    with open(os.path.join(_replay_run_dir, "replay_provenance.jsonl"), "a") as _replay_f:
        _replay_f.write(json.dumps(_replay_record) + "\\n")
"""


def expected_edit(source):
    """One authoritative permitted patch, shared by setup and launch."""
    replacements = (
        ("import torch\n\n", "import torch\n\n" + IMPORT_LOG),
        ("PRESERVE_WEIGHT = 1.0", "PRESERVE_WEIGHT = 0.0"),
        (
            "    ctx = get_context_templates(model, tok)\n",
            "    ctx = get_context_templates(model, tok)\n" + CONTEXT_LOG,
        ),
    )
    for old, new in replacements:
        if source.count(old) != 1:
            raise ValueError(f"pinned source anchor is not unique: {old!r}")
        source = source.replace(old, new, 1)
    return source


def git(dest, *args):
    result = subprocess.run(
        ["git", "-C", str(dest), *args], check=True, capture_output=True, text=True
    )
    return result.stdout


def inspect_replay(dest):
    """Validate bytes, rather than trusting a diff-OK flag."""
    dest = Path(dest).resolve()
    if git(dest, "rev-parse", "HEAD").strip() != BASE_COMMIT:
        raise ValueError("replay HEAD is not the pinned experiment-2 commit")
    if Path(git(dest, "rev-parse", "--absolute-git-dir").strip()).resolve() != dest / ".git":
        raise ValueError("replay is not a standalone checkout")
    if (dest / ".git/objects/info/alternates").exists():
        raise ValueError("replay borrows another repository's objects")
    source = git(dest, "show", f"{BASE_COMMIT}:edit.py")
    expected = expected_edit(source).encode()
    if (dest / "edit.py").read_bytes() != expected:
        raise ValueError("edit.py differs beyond the zero weight and exact logging additions")
    for name in ("prepare.py", "c10e_bandknob.py"):
        if (dest / name).read_bytes() != git(dest, "show", f"{BASE_COMMIT}:{name}").encode():
            raise ValueError(f"fixed evaluation changed: {name}")
    diff = git(dest, "diff", "--no-ext-diff", "--no-textconv", BASE_COMMIT, "--", "edit.py")
    if not diff:
        raise ValueError("replay diff is empty")
    return {
        "base_commit": BASE_COMMIT,
        "edit_py_sha256": hashlib.sha256(expected).hexdigest(),
        "diff_sha256": hashlib.sha256(diff.encode()).hexdigest(),
        "diff": diff,
    }


def classify(count):
    if type(count) is not int or not 0 <= count <= 72:
        raise ValueError("heldout_full must be an integer in [0, 72]")
    if count <= 11:
        return "SUPPORTS-PRESERVE"
    if count <= 17:
        return "PARTIAL-PRESERVE"
    return "ARTIFACT-SUSPECT"


def provenance_checks(score_path):
    path = score_path.parent / "replay_provenance.jsonl"
    if not path.is_file():
        return (False, f"MISSING {path}", False, "MISSING executed-source record", [])
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not records:
        return (False, "EMPTY provenance log", False, "MISSING executed-source record", [])
    try:
        expected = inspect_replay(score_path.parent.parent.parent)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        hashes = [r.get("executed_edit_py_sha256") for r in records]
        return (False, str(exc), False, hashes, records)
    diff_ok = all(r.get("launch") == expected for r in records)
    hashes = [r.get("executed_edit_py_sha256") for r in records]
    source_ok = all(h == expected["edit_py_sha256"] for h in hashes)
    context_ok = all(
        r.get("edit_context_templates_sha256")
        == hashlib.sha256(json.dumps(r["edit_context_templates"]).encode()).hexdigest()
        for r in records
    )
    return (
        diff_ok,
        {"only_permitted_lines": diff_ok, "sha256": expected["diff_sha256"]},
        source_ok and context_ok,
        {"executed_sha256": hashes, "context_hashes_consistent": context_ok},
        records,
    )


def read_score(path):
    score = json.loads(path.read_text())
    summary, gates = score["summary"], score["gates"]
    count = summary["heldout_full"]
    classify(count)
    report_keys = (
        "canon", "first_token", "A1", "A2", "L1_flips", "frame_flips",
        "described_as", "L3", "ppl_post", "scope_ok", "law5_ok", "dw_total", "guards",
    )
    for key in report_keys:
        value = summary[key]
        if type(value) is float and not math.isfinite(value):
            raise ValueError(f"non-finite reported value: {key}")
    rows = score["arms"]["A7_coined_coined"]["rows"]
    if len(rows) != 24 or len({row["subj"] for row in rows}) != 24:
        raise ValueError("expected 24 distinct scored subjects")
    for row in rows:
        hits = row["para_full_hits"]
        if len(hits) != 3 or any(type(hit) is not bool for hit in hits):
            raise ValueError("para_full_hits must contain three booleans per fact")
    if sum(sum(row["para_full_hits"]) for row in rows) != count:
        raise ValueError("heldout_full disagrees with per-fact hit flags")
    collision = [r for r in rows if r["val"].split()[0] in COLLISION_HEADS]
    other = [r for r in rows if r["val"].split()[0] not in COLLISION_HEADS]
    if (len(collision), len(other)) != (16, 8):
        raise ValueError("expected the registered 16 collision facts and other 8")
    try:
        diff_ok, diff_value, source_ok, source_value, records = provenance_checks(path)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        diff_ok, source_ok = False, False
        diff_value = source_value = str(exc)
        records = []
    checks = (
        ("law5_ok", summary["law5_ok"] is True, summary["law5_ok"]),
        ("scope_ok", summary["scope_ok"] is True, summary["scope_ok"]),
        ("scorer_templates_sha", gates["templates_sha"] == TEMPLATE_SHA, gates["templates_sha"]),
        ("A1_in_[68,71]", type(summary["A1"]) is int and 68 <= summary["A1"] <= 71, summary["A1"]),
        ("A2_in_[68,71]", type(summary["A2"]) is int and 68 <= summary["A2"] <= 71, summary["A2"]),
        ("prelaunch_diff_only_permitted", diff_ok, diff_value),
        ("executed_source_hash_recorded", source_ok, source_value),
    )
    for name, ok, value in checks:
        print(f"VALIDITY {name}: {'PASS' if ok else 'FAIL'} value={json.dumps(value, sort_keys=True)}")
    failures = [name for name, ok, _ in checks if not ok]
    if failures:
        print(f"NON-BINDING count-only label: {classify(count)} (failed validity: {', '.join(failures)})")
    print(f"REPORTED heldout_full={count}")
    for key in report_keys:
        print(f"REPORTED {key}={json.dumps(summary[key])}")
    print(f"REPORTED H0_equals_7={json.dumps(count == 7)}")
    for i, record in enumerate(records):
        print(f"REPORTED edit_context_templates_sha256[{i}]={record.get('edit_context_templates_sha256')}")
    for name, group in (("COLLISION", collision), ("OTHER", other)):
        print(f"{name}: facts={len(group)} full_hits={sum(sum(r['para_full_hits']) for r in group)}/{3 * len(group)}")
        for row in group:
            print(f"  {row['subj']} -> {row['val']}: para_full_hits={json.dumps(row['para_full_hits'])}")
    if not all(ok for _, ok, _ in checks):
        print("INVALID")
        print("HALT: validity failure; no reading label")
        return 2
    print(f"LABEL: {classify(count)}")
    return 0


def main():
    if len(sys.argv) != 2:
        print("usage: read_replay.py SCORE_JSON", file=sys.stderr)
        return 2
    try:
        return read_score(Path(sys.argv[1]).resolve())
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print("INVALID")
        print(f"HALT: {exc}; no reading label")
        return 2


if __name__ == "__main__":
    sys.exit(main())
