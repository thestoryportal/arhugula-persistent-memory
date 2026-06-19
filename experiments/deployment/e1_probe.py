import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""E1: probe a LARQL vindex over the b3 probe set; greedy top-1 next token via INFER.
Runs ALL probes in ONE `larql lql` session (single vindex load) to avoid per-prompt reload.
Usage: python e1_probe.py <vindex_path> <out_pred_json> [--limit N]
Parses INFER TOP 1 output, writes [{prompt,kind,target,top1}] aligned to b3_probes order.
"""
import sys, json, subprocess, re, os

VINDEX = sys.argv[1]
OUT = sys.argv[2]
LIMIT = None
if "--limit" in sys.argv:
    LIMIT = int(sys.argv[sys.argv.index("--limit") + 1])

LARQL = f"{LLMDB_ROOT}/external_prior_art/larql/target/release/larql"
probes = json.load(open(f"{LLMDB_ROOT}/configs/probes/b3_probes.json"))
allp = probes["edited"] + probes["native"]
if LIMIT:
    allp = allp[:LIMIT]

# Build one LQL script: USE then one INFER per prompt, with a unique marker before each
# so we can re-align output to prompts deterministically.
lines = [f'USE "{VINDEX}";']
for i, p in enumerate(allp):
    pr = p["prompt"].replace('"', '\\"')
    lines.append(f'INFER "{pr}" TOP 1;')
script = "\n".join(lines) + "\n"

env = dict(os.environ, OPENBLAS_NUM_THREADS="8", OMP_NUM_THREADS="8")
res = subprocess.run([LARQL, "lql", script], capture_output=True, text=True,
                     env=env, cwd=f"{LLMDB_ROOT}/external_prior_art/larql", timeout=3600)
raw = res.stdout + "\n" + res.stderr
open(OUT + ".rawout.txt", "w").write(raw)
print("RAW saved to", OUT + ".rawout.txt", "len", len(raw))
print("---- first 60 lines of raw (inspect INFER format) ----")
for ln in raw.splitlines()[:60]:
    print(ln)
