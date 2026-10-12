#!/usr/bin/env python3
"""C2-band FALSIFIER — does the minimum-collinearity band [8-12] reduce cross-entity read
corruption vs the default band [4-8], at fixed N=100, SEQUENTIAL write?

This is a FALSIFIER, not an optimizer. C2 (CORPUS/20) found same-relation key collinearity is
U-shaped in depth with a MINIMUM at L8-12. The mechanistic prediction: editing in the
low-collinearity band leaves untouched-entity read distributions LESS perturbed → HIGHER
`unt_cross_loc` (locality = 100·mean(1 − JS(post,pre)/ln2); higher = less corruption).
A clean "no improvement" FALSIFIES the editing-relevance of the collinearity→corruption mechanism
(C2 lead) — a real negative result, not a failure to optimize.

WHY SEQUENTIAL (not batch): the A1 batch/Genesis path ALREADY eliminates cross-entity corruption
(baseline batch unt_cross_loc≈98.5% — at ceiling, zero headroom → a band comparison there is a
metric-ceiling artifact, not a test of C2). C2's collinearity→corruption mechanism is a
SEQUENTIAL-regime claim; sequential baseline [4-8] sits at ≈54.8% cross-loc (N=100) — ~45pp of
real headroom for the band to move. Measuring the wrong regime would hide the effect where
falsification lives (memory: match-metric-to-the-claim).

Metric discipline (memory: match-metric-to-the-claim): both bands are scored by the SAME
`unt_cross_loc` on the SAME held-out probes (fixed screen/seed), each a paired post-vs-pre JS
diff — so shared bias cancels and the comparison is band-vs-band on identical units. The GUARD
(edit retention/expression ≥95 on both arms) ensures we are not comparing corruption at
different edit-success levels (the obvious confound).

Runs g6_scale_n_param.py twice as isolated subprocesses (clean HF/torch state per arm), then
emits results/c2band_compare_result.json with the top-rung (N=100) comparison + guard fields.

NOTE: band [8-12] needs covariance for L9-12 (not cached) — the first run computes them
(standing-auth: PRE-APPROVED). Budget the wrapper timeout accordingly.
"""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT", "/workspace"))
G6 = ROOT / "experiments/scale/g6_scale_n_param.py"
HP_BASE = ROOT / "configs/hparams/qwen25_3b_memit_hparams.json"            # [4,5,6,7,8]
HP_BAND = ROOT / "configs/hparams/qwen25_3b_memit_hparams_band812.json"    # [8,9,10,11,12]
OUT = ROOT / "results/c2band_compare_result.json"

ARMS = [("base", HP_BASE, "_c2band_base"), ("band812", HP_BAND, "_c2band_812")]

def run_arm(hparams: Path, tag: str):
    # SEQUENTIAL write — the regime where cross-entity corruption has headroom (see module docstring).
    env = {**os.environ, "HPARAMS": str(hparams), "WRITE_MODE": "sequential",
           "RESULT_TAG": tag, "RUNGS": os.environ.get("RUNGS", "13,25,50"),
           "LLMDB_ROOT": str(ROOT)}
    log = ROOT / f"logs/c2band{tag}.log"
    print(f"[compare] running arm tag={tag} hparams={hparams.name} → {log.name}", flush=True)
    with open(log, "w") as lf:
        p = subprocess.run([sys.executable, "-u", str(G6)], env=env, cwd=ROOT,
                           stdout=lf, stderr=subprocess.STDOUT)
    rj = ROOT / f"results/g6_scale_n_result{tag}.json"   # sequential output path
    if p.returncode != 0 or not rj.exists():
        raise RuntimeError(f"arm {tag} failed rc={p.returncode} json_exists={rj.exists()} (see {log})")
    d = json.loads(rj.read_text())
    top = d["rungs"][-1]   # N=100 rung
    return {"unt_cross_loc": top["unt_cross_loc"], "unt_within_loc": top["unt_within_loc"],
            "unt_global_loc": top["unt_global_loc"], "retention": top["all_record_retention"],
            "expression": top["apply_time_expr"], "heldout_top1": top["heldout_top1"],
            "band": d["config"]["band"], "n": top["n"]}

def main():
    arms = {}
    for name, hp, tag in ARMS:
        if not hp.exists():
            print(f"FATAL: hparams missing {hp}", file=sys.stderr); return 2
        arms[name] = run_arm(hp, tag)
    b, k = arms["base"], arms["band812"]
    out = {
        "experiment": "C2-band falsifier (collinearity→corruption editing-relevance, SEQUENTIAL regime)",
        "write_mode": "sequential",
        "bands": {"baseline": b["band"], "band812": k["band"]},
        "n": k["n"],
        "unt_cross_loc_baseline": b["unt_cross_loc"],
        "unt_cross_loc_band812": k["unt_cross_loc"],
        # positive = band812 has HIGHER locality = LESS cross-entity corruption than baseline
        "corruption_reduction_pp": round(k["unt_cross_loc"] - b["unt_cross_loc"], 2),
        "within_loc_baseline": b["unt_within_loc"], "within_loc_band812": k["unt_within_loc"],
        "heldout_baseline": b["heldout_top1"], "heldout_band812": k["heldout_top1"],
        # guard = WORST arm's edit success (both must clear ≥95 or the comparison is confounded)
        "retention": min(b["retention"], k["retention"]),
        "expression": min(b["expression"], k["expression"]),
        "retention_baseline": b["retention"], "retention_band812": k["retention"],
        "arms_raw": arms,
    }
    OUT.write_text(json.dumps(out, indent=2))
    print(f"[compare] wrote {OUT}", flush=True)
    print(f"[compare] cross-loc base={b['unt_cross_loc']}% band812={k['unt_cross_loc']}% "
          f"Δ={out['corruption_reduction_pp']}pp | guard ret={out['retention']} expr={out['expression']}", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
