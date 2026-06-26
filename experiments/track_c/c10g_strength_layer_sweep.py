import os, sys, json
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")

os.environ.setdefault("DECISION_ID", "D-C10g-strengthlayers")
os.environ.setdefault("PREREG", f"{LLMDB_ROOT}/docs/C10_STRENGTH_LAYER_SWEEP_PREREG.md")
os.environ.setdefault("OUT", f"{LLMDB_ROOT}/results/c10g_strength_layer_sweep.json")
os.environ.setdefault("RUN_LABEL", "C10 edit-strength / layer-count sweep")

import c10e_bandknob as c10

CANDIDATES = [
    ("wide_band412_strength150", f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams_band412_strength150.json"),
    ("wide_band412_lowcov2500", f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams_band412_lowcov2500.json"),
    ("deep_band41218", f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams_band41218.json"),
]


def arm_counts(recipe, arm_name):
    detail = recipe.get("detail", {}).get(arm_name, [])
    n = len(detail)
    npar = len(c10.PTEST)
    return {
        "canon_full_hits": sum(1 for row in detail if row["canon_full"]),
        "canon_total": n,
        "para_full_hits": sum(sum(row["para_full_hits"]) for row in detail),
        "para_first_hits": sum(sum(row["para_first_hits"]) for row in detail),
        "para_total": n * npar,
    }


def candidate_verdict(results, name):
    recipes = results["recipes"]
    b = recipes["baseline"]["arms"]["A7_coined_coined"]
    k = recipes[name]["arms"]["A7_coined_coined"]
    a1 = recipes[name]["arms"]["A1_single"]["para_full"]
    a2 = recipes[name]["arms"]["A2_coherent2"]["para_full"]
    control_min = min(a1, a2)
    dc = round(k["canon_full"] - b["canon_full"], 1)
    dp = round(k["para_full"] - b["para_full"], 1)
    counts = {
        "baseline_A7": arm_counts(recipes["baseline"], "A7_coined_coined"),
        f"{name}_A7": arm_counts(recipes[name], "A7_coined_coined"),
        f"{name}_A1": arm_counts(recipes[name], "A1_single"),
        f"{name}_A2": arm_counts(recipes[name], "A2_coherent2"),
    }
    if control_min < 80:
        label = "TRADEOFF_NOT_CLEAN_RESCUE"
        text = "candidate damages A1/A2 controls below 80; any A7 gain is not a clean C10 rescue"
    elif k["para_full"] >= 85:
        label = "USABILITY_RESCUE_LEAD_NOT_PROMOTED"
        text = "candidate reaches the C10 usability bar in this scoped run; replication and downstream checks required"
    elif dp >= 25 and k["para_full"] >= 40:
        label = "BEHAVIORAL_LEAD_NOT_CLOSURE"
        text = "candidate materially improves held-out read expression but remains below C10 closure"
    elif dc >= 20 and k["para_full"] < 40:
        label = "W_REALIZATION_ONLY_NON_RESCUE"
        text = "candidate improves canonical trained-prompt fit only; behavioral readout remains unusable"
    elif dp < 15 and k["para_full"] < 40:
        label = "NO_MATERIAL_BEHAVIORAL_RESCUE"
        text = "candidate does not materially improve the binding held-out behavioral readout"
    else:
        label = "AMBIGUOUS_NONPROMOTIONAL"
        text = "valid scoped signal but below behavioral lead thresholds; not promotional without replication"
    return {
        "label": label,
        "text": text,
        "A7": k,
        "delta_A7": {"canon_full_pp": dc, "para_full_pp": dp},
        "control_min_para_full": control_min,
        "counts": counts,
    }


def sweep_verdict(results):
    recipes = results["recipes"]
    invalid = []
    if not all(r.get("law5_gate", {}).get("ok") for r in recipes.values()):
        invalid.append("LAW#5 failed for at least one recipe")
    b = recipes["baseline"]["arms"]["A7_coined_coined"]
    if not (b["canon_full"] <= 55 and b["para_full"] <= 35):
        invalid.append("baseline A7 did not reproduce failure envelope")
    if recipes["baseline"]["arms"]["A1_single"]["para_full"] < 80:
        invalid.append("baseline A1 sanity below 80")
    if recipes["baseline"]["arms"]["A2_coherent2"]["para_full"] < 80:
        invalid.append("baseline A2 coherent2 below 80")

    candidate_results = {name: candidate_verdict(results, name) for name, _ in CANDIDATES}
    if invalid:
        label = "INVALID"
        text = "; ".join(invalid)
    elif any(v["label"] == "USABILITY_RESCUE_LEAD_NOT_PROMOTED" for v in candidate_results.values()):
        label = "USABILITY_RESCUE_LEAD_NOT_PROMOTED"
        text = "at least one candidate reaches the scoped C10 usability bar; not promoted without replication/downstream checks"
    elif any(v["label"] == "BEHAVIORAL_LEAD_NOT_CLOSURE" for v in candidate_results.values()):
        label = "BEHAVIORAL_LEAD_NOT_CLOSURE"
        text = "at least one candidate materially improves held-out read expression; C10 remains open"
    else:
        best = max(candidate_results.items(), key=lambda kv: kv[1]["delta_A7"]["para_full_pp"])
        if best[1]["label"] == "TRADEOFF_NOT_CLEAN_RESCUE":
            label = "TRADEOFF_NOT_CLEAN_RESCUE"
            text = "best A7 behavioral gain comes with damaged A1/A2 controls; not a clean rescue"
        elif any(v["label"] == "W_REALIZATION_ONLY_NON_RESCUE" for v in candidate_results.values()):
            label = "W_REALIZATION_ONLY_NON_RESCUE"
            text = "at least one candidate improves canonical fit only; behavioral read criterion remains unmet"
        elif all(v["label"] == "NO_MATERIAL_BEHAVIORAL_RESCUE" for v in candidate_results.values()):
            label = "NO_MATERIAL_KNOB_RESCUE"
            text = "all valid candidates fail to materially improve the binding held-out behavioral readout"
        else:
            label = "MIXED_NONPROMOTIONAL"
            text = "valid but ambiguous sub-threshold signals; no candidate reaches a behavioral lead threshold"
    return {
        "label": label,
        "text": text,
        "invalid_reasons": invalid,
        "baseline_A7": b,
        "baseline_counts": arm_counts(recipes["baseline"], "A7_coined_coined"),
        "candidates": candidate_results,
        "stopping_rule": "After these three pre-registered candidates, move to AnyEdit or accept-bounded unless a candidate reaches a behavioral lead threshold.",
    }


def main():
    base_report = c10.pre_base_report()
    print("\n=== STIMULUS BASE CHECK ===", flush=True)
    for k, v in base_report.items():
        print(f"  {k:18} base={v['base']}/{c10.N} ntok={v['mean_ntok']} range={v['ntok_range']}", flush=True)
    if any(v["base"] > c10.N * 0.15 for v in base_report.values()):
        print("STIMULUS HALT: pre-edit base leak >15%", flush=True)
        return 0

    results = {
        "decision_id": "D-C10g-strengthlayers",
        "prereg": f"{LLMDB_ROOT}/docs/C10_STRENGTH_LAYER_SWEEP_PREREG.md",
        "run": "C10 edit-strength / layer-count sweep",
        "class": "FALSIFIER-resolver / bounded MEMIT-knob characterization; NOT promotable",
        "scope": "Qwen2.5-3B / AlphaEdit / capital / A1-A2-A7 / N=24 / 1-seed / HF-fp16",
        "stimulus": {"CANON": c10.CANON, "PTEST": c10.PTEST, "FICTION": c10.FICTION, **{f"V_{k}": v for k, v in c10.ARMS.items()}},
        "base_report": base_report,
        "candidate_order": [name for name, _ in CANDIDATES],
        "recipes": {"baseline": c10.run_recipe("baseline", c10.HP_BASE)},
    }
    for name, hp_path in CANDIDATES:
        results["recipes"][name] = c10.run_recipe(name, hp_path)

    results["verdict"] = sweep_verdict(results)
    out = f"{LLMDB_ROOT}/results/c10g_strength_layer_sweep.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n=== C10g STRENGTH/LAYER SWEEP SUMMARY ===", flush=True)
    print(json.dumps(results["verdict"], indent=2), flush=True)
    print(f"\nwrote {out}", flush=True)
    print("C10G_DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
