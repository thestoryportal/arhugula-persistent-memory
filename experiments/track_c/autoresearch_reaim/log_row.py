#!/usr/bin/env python3
"""Append one results.tsv row from an iteration's run.json (or a crash). Keep/discard by program.md's policy, mechanically.
Usage: log_row.py <tag> <iter> "<description>"      — exits 0; prints the row and the current best."""
import sys, os, json, hashlib
LLMDB_ROOT = os.environ["LLMDB_ROOT"]
GUARDS = {"A1": (">=", 68), "A2": (">=", 68), "L1_flips": ("<=", 1), "frame_flips": ("<=", 2), "described_as": (">=", 85.0), "L3": (">=", 29), "ppl_post": ("<=", 22.2), "law5_ok": ("==", True), "cap_ok": ("==", True)}
KEEP_GAIN = 3
TAG, ITER, DESC = sys.argv[1], int(sys.argv[2]), sys.argv[3].replace("\t", " ")
D = f"{LLMDB_ROOT}/results/autoresearch_reaim/{TAG}"; TSV = f"{D}/results.tsv"
if not os.path.exists(TSV):
    open(TSV, "w").write("iter\tknobs_sha\theldout_full\tguards\tstatus\tdw_ratio\tdescription\n")
rows = [l.rstrip("\n").split("\t") for l in open(TSV).read().splitlines()[1:]]
best = max((int(r[2]) for r in rows if r[4] == "keep"), default=None)
it = f"{D}/iter_{ITER:02d}"
sha = hashlib.sha256(open(f"{it}/knobs.json", "rb").read()).hexdigest()[:8] if os.path.exists(f"{it}/knobs.json") else "--------"
if not os.path.exists(f"{it}/run.json"):
    row = [str(ITER), sha, "0", "crash", "crash", "0", DESC]
else:
    s = json.load(open(f"{it}/run.json"))["summary"]
    failing = [g for g, (op, thr) in GUARDS.items() if not {">=": s[g] >= thr, "<=": s[g] <= thr, "==": s[g] == thr}[op]]
    ok = not failing
    status = "invalid" if not ok else ("keep" if best is None or s["heldout_full"] >= best + KEEP_GAIN else "discard")
    row = [str(ITER), sha, str(s["heldout_full"]), "ok" if ok else ",".join(failing), status, f"{s['dw_ratio']:.2f}", DESC]
open(TSV, "a").write("\t".join(row) + "\n")
print("\t".join(row)); print(f"best kept heldout_full so far: {best if row[4] != 'keep' else row[2]}")
