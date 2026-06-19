#!/usr/bin/env python3
"""Honest held-out evaluator for the band-[8-12] cross-entity-isolation search.

Reads config.json (the band + mom2_uw the autoresearch agent edits), runs the
PROVEN sequential edit harness (run_edit.py = g6_scale_n_param.py copy) at that
band on Qwen2.5-3B (N=100, 50 entities x 2 fields), and prints a JSON metric.

HONESTY / anti-Goodhart design:
  * METRIC = held-out same-relation top-1 measured with EXACT match (not the
    lenient prefix-match `correct()` = the NEW-3 confound). Higher = less
    cross-entity corruption. Baseline band [4-8] sequential ~= 41.7% (prefix);
    exact will be lower — the first run establishes the real baseline.
  * GUARD (must stay TRUE or the experiment is INVALID, regardless of metric):
    retention >= 95% AND apply-time expression >= 95%. This blocks the obvious
    cheat — a band that "looks clean" only because the edits never took.
  * Held-out entities are NEVER edited (the harness edits the first N entities
    and probes a disjoint held-out set), so the metric can't be trained on.

Output (stdout, last line = JSON the loop parses):
  {"metric_value": <heldout edited-rel EXACT top-1 %>, "retention": ...,
   "expression": ..., "valid": true|false, "layers": [...], "baseline_4_8": 41.7}

NOTE: a band whose covariance is not yet cached (e.g. L9-12) triggers a one-time
covariance computation on first run (slow, ~minutes/layer). Band [4-8] is cached
(use it to validate this evaluator reproduces the known baseline).
"""
import os, sys, json, subprocess, tempfile

LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
HERE = os.path.dirname(os.path.abspath(__file__))
REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"

cfg = json.load(open(os.path.join(HERE, "config.json")))
layers = cfg["layers"]
mom2 = cfg.get("mom2_update_weight", 5000)

# build a full hparams JSON from the 3B template + the searched band/mom2
hp = json.load(open(f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"))
hp["layers"] = layers
hp["mom2_update_weight"] = mom2
tmp_hp = tempfile.NamedTemporaryFile("w", suffix="_bandsearch_hparams.json", delete=False)
json.dump(hp, tmp_hp); tmp_hp.close()

env = dict(os.environ,
           MODEL_ID="Qwen/Qwen2.5-3B", MODEL_REV=REV,
           HPARAMS=tmp_hp.name,
           SCREEN=f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json",
           WRITE_MODE="sequential", RESULT_TAG="_bandsearch",
           HF_HOME=f"{LLMDB_ROOT}/hf_cache", HF_HUB_OFFLINE="1",
           PYTHONUNBUFFERED="1")
# allow a quick smoke via REDUCED N (e.g. SMOKE_N=10) when validating the plumbing
if os.environ.get("SMOKE_N"):
    env["N_ENTITIES"] = os.environ["SMOKE_N"]; env["RUNGS"] = os.environ["SMOKE_N"]

print(f"[evaluate] band={layers} mom2_uw={mom2} -> running sequential edit ...", file=sys.stderr, flush=True)
r = subprocess.run([sys.executable, os.path.join(HERE, "run_edit.py")],
                   env=env, capture_output=True, text=True, timeout=14400)
if r.returncode != 0:
    print(r.stdout[-2000:], file=sys.stderr); print(r.stderr[-2000:], file=sys.stderr)
    print(json.dumps({"metric_value": None, "valid": False, "error": "run_edit failed", "layers": layers}))
    sys.exit(1)

res = json.load(open(f"{LLMDB_ROOT}/results/g6_scale_n_result_bandsearch.json"))
final = res["rungs"][-1]                       # the N=100 rung
heldout = final["heldout_top1"]["edited_rel"]
metric = heldout.get("top1_exact_vs_truth", heldout["top1_correct_vs_truth"])  # EXACT preferred
retention = final["all_record_retention"]
expression = final["apply_time_expr"]
valid = (retention >= 95.0) and (expression >= 95.0)

out = {"metric_value": metric, "retention": retention, "expression": expression,
       "valid": valid, "layers": layers, "mom2_update_weight": mom2,
       "heldout_prefix_for_reference": heldout["top1_correct_vs_truth"],
       "baseline_4_8_prefix": 41.7,
       "guard": "retention>=95 AND expression>=95"}
print(json.dumps(out))
