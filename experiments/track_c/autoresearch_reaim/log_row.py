#!/usr/bin/env python3
"""Append one results.tsv row from an iteration's run.json (or a crash), in the fork's 5-column shape (program.md):
commit	heldout_full	dw_ratio	status	description
keep = the metric improved (higher) over the best kept row with every guard true; equal or worse = discard; a failed guard =
invalid (treated as a discard; the failing guards are appended to the description); no run.json = crash.
Usage: log_row.py <tag> <iter> "<description>"  — exits 0; prints the row and the current best. [LAW:one-source-of-truth] guards live here once."""
import sys, os, json, hashlib
LLMDB_ROOT = os.environ["LLMDB_ROOT"]
GUARDS = {"A1": (">=", 68), "A2": (">=", 68), "L1_flips": ("<=", 1), "frame_flips": ("<=", 2), "described_as": (">=", 85.0), "L3": (">=", 29),
          "ppl_post": ("<=", 22.2), "law5_ok": ("==", True), "cap_ok": ("==", True)}
HEADER = "commit\theldout_full\tdw_ratio\tstatus\tdescription\n"
TAG, ITER, DESC = sys.argv[1], int(sys.argv[2]), sys.argv[3].replace("\t", " ")
D = f"{LLMDB_ROOT}/results/autoresearch_reaim/{TAG}"; TSV = f"{D}/results.tsv"
it = f"{D}/iter_{ITER:02d}"


def unit_sha():   # the editable unit's snapshot (run_iteration.py + knobs.json), taken by the launcher before the run; stands in for a git commit
    parts = [f"{it}/run_iteration.py", f"{it}/knobs.json"]
    if not all(os.path.exists(p) for p in parts): return "--------"
    h = hashlib.sha256()
    for p in parts: h.update(open(p, "rb").read())
    return h.hexdigest()[:8]


if not os.path.exists(TSV) or open(TSV).readline() != HEADER:   # fresh file, or a file from the earlier 7-column draft: rewrite in the fork's shape
    old = [l.rstrip("\n").split("\t") for l in open(TSV).read().splitlines()[1:]] if os.path.exists(TSV) else []
    with open(TSV, "w") as f:
        f.write(HEADER)
        for r in old:
            if len(r) == 7:   # iter, sha, metric, guards, status, dw, desc
                f.write("\t".join([r[1], r[2], r[5], r[4], r[6] + ("" if r[3] == "ok" else f" [guards failed: {r[3]}]")]) + "\n")
            elif len(r) == 5:
                f.write("\t".join(r) + "\n")
rows = [l.rstrip("\n").split("\t") for l in open(TSV).read().splitlines()[1:]]
best = max((int(r[1]) for r in rows if r[3] == "keep"), default=None)
if not os.path.exists(f"{it}/run.json"):
    row = [unit_sha(), "0", "0.00", "crash", DESC]
else:
    s = json.load(open(f"{it}/run.json"))["summary"]
    failing = [g for g, (op, thr) in GUARDS.items() if not {">=": s[g] >= thr, "<=": s[g] <= thr, "==": s[g] == thr}[op]]
    if failing: status, desc = "invalid", DESC + f" [guards failed: {','.join(failing)}]"
    else: status, desc = ("keep" if best is None or s["heldout_full"] > best else "discard"), DESC
    row = [unit_sha(), str(s["heldout_full"]), f"{s['dw_ratio']:.2f}", status, desc]
open(TSV, "a").write("\t".join(row) + "\n")
print("\t".join(row)); print(f"best kept heldout_full so far: {row[1] if row[3] == 'keep' else best}")
