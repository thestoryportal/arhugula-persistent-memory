#!/usr/bin/env python3
"""
re_evaluate_bands.py — S2.11-B re-evaluation pass

Applies multiple candidate consistency-band specifications to per-trial JSONs
from the S2.10 Stage 2 sweep, producing a revised sweep verdict per
probe_band_recalibration_spec.md v1.0 §5.

Inputs:
    Per-trial JSONs at /mnt/project/ or /mnt/user-data/uploads/ matching pattern
    stage_2_trial_L{config}_cfb-{fact}_r{replicate}.json
    OR
    L{config}/trials/cfb-{fact}_r{replicate}.json (sweep-archive layout)

Outputs:
    /mnt/user-data/outputs/revised_sweep_verdict_v1.json
    Schema per spec §5.3.

Decidability: mechanical AND/OR aggregation; no operator interpretation.
Reproducibility: idempotent under re-execution given identical input set.
"""
import json
import sys
import argparse
import datetime
import glob
import os
import re
from collections import defaultdict


# ============================================================
# Band predicates per probe_band_recalibration_spec.md v1.0 §3
# ============================================================
# A band predicate takes a probe dict (one of post_edit_probes.{probe_id})
# and a target_new string; returns True/False.

BAND_SPECS = {
    "B-A-0.5":   ("Current band (P > 0.5)",
                  lambda probe, tn: probe["p_target_new"] > 0.5),
    "B-A-0.1":   ("Absolute relaxed (P > 0.1)",
                  lambda probe, tn: probe["p_target_new"] > 0.1),
    "B-A-0.05":  ("Absolute relaxed (P > 0.05)",
                  lambda probe, tn: probe["p_target_new"] > 0.05),
    "B-A-0.01":  ("Absolute relaxed (P > 0.01) — PRIMARY recommendation",
                  lambda probe, tn: probe["p_target_new"] > 0.01),
    "B-A-0.005": ("Absolute relaxed (P > 0.005)",
                  lambda probe, tn: probe["p_target_new"] > 0.005),
    "B-A-0.001": ("Absolute relaxed (P > 0.001) — noise floor sanity",
                  lambda probe, tn: probe["p_target_new"] > 0.001),
    "B-B-5":     ("Rank — target_new in top-5",
                  lambda probe, tn: tn in [t["token_str"].strip()
                                            for t in probe["top_5"]]),
    "B-D-10":    ("Target dominance — P(target_new) > P(top_1) / 10",
                  lambda probe, tn: probe["p_target_new"] >
                                    probe["p_top_1"] / 10),
}

PRIMARY_BAND = "B-A-0.01"


# ============================================================
# Trial JSON discovery
# ============================================================

def discover_trial_jsons(roots):
    """
    Locate all per-trial JSONs under the given root directories.

    Recognizes two layouts:
      (a) flat: <root>/stage_2_trial_L{NN}_cfb-{NNN}_r{N}.json
      (b) archive: <root>/L{NN}/trials/cfb-{NNN}_r{N}.json
    """
    trials = []
    seen_paths = set()

    for root in roots:
        if not os.path.exists(root):
            continue

        # Layout (a): flat
        for path in sorted(glob.glob(os.path.join(
                root, "stage_2_trial_L*_cfb-*_r*.json"))):
            if path not in seen_paths:
                trials.append(path)
                seen_paths.add(path)

        # Layout (b): sweep-archive
        for path in sorted(glob.glob(os.path.join(
                root, "L*", "trials", "cfb-*_r*.json"))):
            if path not in seen_paths:
                trials.append(path)
                seen_paths.add(path)

        # Layout (c): operator may upload as stage_2_trial_*.json without L prefix
        # in which case config_id is parsed from inside the file
        for path in sorted(glob.glob(os.path.join(
                root, "stage_2_trial_*.json"))):
            if path not in seen_paths:
                trials.append(path)
                seen_paths.add(path)

    return trials


def parse_config_from_path_or_content(trial_path, trial_data):
    """
    Extract config_id (L01..L16) from path first, fall back to trial JSON content.
    """
    # Path-based: look for L\d{2} in path components
    m = re.search(r"L(\d{2})", trial_path)
    if m:
        return f"L{m.group(1)}"

    # Content-based: many trial JSONs include sweep metadata or config_id field
    if "config_id" in trial_data:
        return trial_data["config_id"]
    if "sweep_config" in trial_data and "config_id" in trial_data["sweep_config"]:
        return trial_data["sweep_config"]["config_id"]

    return None


# ============================================================
# Band evaluation pass
# ============================================================

def evaluate_trial_against_bands(trial_data):
    """
    For a single trial JSON, evaluate all band predicates against all 3
    consistency probes and return a per-band trial-pass dict.

    A trial passes a band iff all 3 cons probes pass under that band.
    """
    fact_id = trial_data["fact_id"]
    target_new = trial_data["memit_request"]["target_new"]["str"]
    pe = trial_data["post_edit_probes"]

    cons_probe_ids = [k for k in pe if k.startswith(f"p-{fact_id}-cons-")]
    cons_probe_ids = sorted(cons_probe_ids)

    if len(cons_probe_ids) != 3:
        raise ValueError(
            f"Expected 3 cons probes for {fact_id}, found {len(cons_probe_ids)}: "
            f"{cons_probe_ids}")

    per_band_per_probe = {}
    per_band_trial_pass = {}

    for band_id, (label, predicate) in BAND_SPECS.items():
        per_probe_pass = []
        for pid in cons_probe_ids:
            try:
                p = predicate(pe[pid], target_new)
                per_probe_pass.append(bool(p))
            except (KeyError, IndexError):
                per_probe_pass.append(False)

        per_band_per_probe[band_id] = per_probe_pass
        per_band_trial_pass[band_id] = all(per_probe_pass)

    return {
        "fact_id": fact_id,
        "target_new": target_new,
        "cons_probe_ids": cons_probe_ids,
        "per_band_per_probe_pass": per_band_per_probe,
        "per_band_trial_pass": per_band_trial_pass,
        # Forensic detail for diagnostic output
        "p_target_new_per_probe": {pid: pe[pid]["p_target_new"] for pid in cons_probe_ids},
        "top_1_token_per_probe": {pid: pe[pid]["top_1_token"].strip() for pid in cons_probe_ids},
    }


def aggregate_per_config(trials_by_config, sweep_verdict_struct=None):
    """
    Aggregate per-trial verdicts into per-config verdicts.

    Per-config consistency rule: ≥2/3 trials pass (per stage_2_sweep_design.md §5.1
    retained per recalibration_spec §2.3).

    Specificity / unmount verdicts are inherited from sweep_verdict.json
    per recalibration_spec §4.4 (those bands unchanged).
    """
    config_verdicts = {}

    # Build inheritance lookup from existing sweep_verdict.json
    inherited = {}
    if sweep_verdict_struct:
        for entry in sweep_verdict_struct.get("per_config_table", []):
            cid = entry["config_id"]
            ag = entry["criteria_summary"]["aggregate_pass"]
            inherited[cid] = {
                "specificity_post_edit": ag.get("specificity_post_edit"),
                "specificity_post_unmount": ag.get("specificity_post_unmount"),
                "unmount": ag.get("unmount"),
                "generalization": ag.get("generalization"),
                "hparams": entry.get("hparams"),
            }

    for cid, trial_records in sorted(trials_by_config.items()):
        per_band_trials_passing = defaultdict(int)
        per_band_trial_results = defaultdict(list)

        for trec in trial_records:
            for band_id, tpass in trec["per_band_trial_pass"].items():
                if tpass:
                    per_band_trials_passing[band_id] += 1
                per_band_trial_results[band_id].append({
                    "fact_id": trec["fact_id"],
                    "trial_pass": tpass,
                    "p_target_new_per_probe": trec["p_target_new_per_probe"],
                })

        per_band_config_verdict = {}
        for band_id in BAND_SPECS:
            n_pass = per_band_trials_passing[band_id]
            n_total = len(trial_records)
            cfg_pass = (n_pass >= 2) if n_total >= 2 else (n_pass >= 1)
            per_band_config_verdict[band_id] = {
                "trials_passing": n_pass,
                "trials_total": n_total,
                "config_pass": cfg_pass,
            }

        # Calibration corridor membership requires:
        # consistency-PASS (per band) AND specificity-pe AND specificity-pu AND unmount
        inh = inherited.get(cid, {})
        spec_pe = inh.get("specificity_post_edit", False)
        spec_pu = inh.get("specificity_post_unmount", False)
        unm = inh.get("unmount", False)

        for band_id in BAND_SPECS:
            cv = per_band_config_verdict[band_id]
            cv["specificity_post_edit_pass"] = spec_pe
            cv["specificity_post_unmount_pass"] = spec_pu
            cv["unmount_pass"] = unm
            cv["in_calibration_corridor"] = (
                cv["config_pass"] and spec_pe and spec_pu and unm
            )

        config_verdicts[cid] = {
            "hparams": inh.get("hparams"),
            "per_band": per_band_config_verdict,
            "n_trials": len(trial_records),
            "trial_details": dict(per_band_trial_results),
        }

    return config_verdicts


def aggregate_sweep(config_verdicts):
    """
    Sweep-level verdict per band: OR over per-config pass; corridor enumeration.
    """
    sweep_per_band = {}
    for band_id in BAND_SPECS:
        passing_configs = [cid for cid, cv in config_verdicts.items()
                           if cv["per_band"][band_id]["config_pass"]]
        corridor = [cid for cid, cv in config_verdicts.items()
                    if cv["per_band"][band_id]["in_calibration_corridor"]]
        sweep_per_band[band_id] = {
            "label": BAND_SPECS[band_id][0],
            "passing_configs": passing_configs,
            "calibration_corridor": corridor,
            "sweep_pass": len(passing_configs) > 0,
        }
    return sweep_per_band


def diagnostic_summary(sweep_per_band, config_verdicts):
    """Generate human-readable diagnostic text per spec §5.3."""
    n_configs = len(config_verdicts)
    lines = []
    lines.append(f"Re-evaluation pass over {n_configs} configs.")
    primary = sweep_per_band[PRIMARY_BAND]
    lines.append(f"PRIMARY band ({PRIMARY_BAND}): "
                 f"sweep_pass={primary['sweep_pass']}, "
                 f"corridor={primary['calibration_corridor']}")

    # Routing per spec §8
    if primary["sweep_pass"] and primary["calibration_corridor"]:
        lines.append(f"ROUTING (per spec §8.1): Class B is the defect. "
                     f"Corridor configs: {primary['calibration_corridor']}. "
                     f"Forward: S2.12 → Workstream 2 entry / Stage 2 promotion to 3×3.")
    elif sweep_per_band["B-A-0.001"]["sweep_pass"] and not primary["sweep_pass"]:
        lines.append("ROUTING (per spec §8.3): PARTIAL — pure-noise regime; "
                     "B-A-0.001 passes but B-A-0.01 does not. "
                     "Treated as FAIL for Class B isolation; routes to S2.12-A.")
    else:
        lines.append("ROUTING (per spec §8.2): Class B eliminated. "
                     "Forward: S2.12-A (corpus revision, CFB v1 → CFB v2).")

    # Asymmetric configs check
    primary_passing = primary["passing_configs"]
    if primary_passing:
        hparams = sorted(set(
            tuple(config_verdicts[c]["hparams"].items())
            for c in primary_passing if config_verdicts[c]["hparams"]))
        v_lrs = set()
        for c in primary_passing:
            h = config_verdicts[c]["hparams"]
            if h:
                v_lrs.add(h.get("v_lr"))
        if v_lrs and min(v_lrs) >= 1.5:
            lines.append("DETAIL (per spec §8.4): Asymmetric — primary band passes "
                         "only at high-strength configs (v_lr ≥ 1.5). Routes "
                         "Stage 2 promotion at qualifying corridor.")

    return " ".join(lines)


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Re-evaluate Stage 2 sweep against recalibrated probe bands "
                    "per probe_band_recalibration_spec.md v1.0")
    parser.add_argument("--input-roots", nargs="+",
                        default=["/mnt/user-data/uploads/", "/mnt/project/"],
                        help="Roots to search for trial JSONs")
    parser.add_argument("--sweep-verdict",
                        default="/mnt/project/stage_2_sweep_verdict.json",
                        help="Original sweep verdict for spec/unmount inheritance")
    parser.add_argument("--output",
                        default="/mnt/user-data/outputs/revised_sweep_verdict_v1.json",
                        help="Output path for revised verdict JSON")
    parser.add_argument("--require-min-trials", type=int, default=42,
                        help="Minimum trial count to consider re-evaluation complete "
                             "(14 configs × 3 trials = 42 expected)")
    args = parser.parse_args()

    # Step 0 — load sweep verdict for inherited bands
    if os.path.exists(args.sweep_verdict):
        with open(args.sweep_verdict) as f:
            sweep_verdict_struct = json.load(f)
    else:
        sweep_verdict_struct = None
        print(f"WARN: sweep_verdict.json not found at {args.sweep_verdict}; "
              "calibration corridor will not be derivable", file=sys.stderr)

    # Step 1 — discover trial JSONs
    trial_paths = discover_trial_jsons(args.input_roots)
    print(f"Discovered {len(trial_paths)} trial JSONs")
    for p in trial_paths:
        print(f"  {p}")

    if len(trial_paths) < args.require_min_trials:
        print(f"\nWARN: Only {len(trial_paths)} trials found; expected "
              f"{args.require_min_trials}. Re-evaluation will proceed but "
              "the verdict will be PARTIAL.", file=sys.stderr)

    # Step 2 — evaluate each trial; group by config_id
    trials_by_config = defaultdict(list)
    parse_failures = []

    for tpath in trial_paths:
        with open(tpath) as f:
            trial_data = json.load(f)
        cid = parse_config_from_path_or_content(tpath, trial_data)
        if cid is None:
            parse_failures.append(tpath)
            continue
        try:
            tres = evaluate_trial_against_bands(trial_data)
            tres["source_path"] = tpath
            tres["replicate"] = trial_data.get("replicate")
            trials_by_config[cid].append(tres)
        except Exception as e:
            print(f"WARN: failed to evaluate {tpath}: {e}", file=sys.stderr)
            parse_failures.append(tpath)

    print(f"\nGrouped trials into {len(trials_by_config)} configs:")
    for cid in sorted(trials_by_config):
        n = len(trials_by_config[cid])
        print(f"  {cid}: {n} trials")

    # Step 3 — aggregate per-config
    config_verdicts = aggregate_per_config(trials_by_config, sweep_verdict_struct)

    # Step 4 — aggregate sweep
    sweep_per_band = aggregate_sweep(config_verdicts)

    # Step 5 — diagnostic
    diag = diagnostic_summary(sweep_per_band, config_verdicts)
    print(f"\n{diag}\n")

    # Step 6 — emit output
    primary = sweep_per_band[PRIMARY_BAND]
    output = {
        "spec_ref": "probe_band_recalibration_spec.md v1.0",
        "evaluated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": {
            "trial_jsons_count": sum(len(v) for v in trials_by_config.values()),
            "config_count": len(trials_by_config),
            "configs_present": sorted(trials_by_config.keys()),
            "configs_expected": [f"L{i:02d}" for i in range(1, 15)],
            "anchor_at_L01": "L01" in trials_by_config,
            "input_roots": args.input_roots,
            "parse_failures": parse_failures,
        },
        "per_band_verdicts": {
            band_id: {
                "label": sweep_per_band[band_id]["label"],
                "per_config": [
                    {
                        "config_id": cid,
                        "hparams": config_verdicts[cid]["hparams"],
                        "trials_passing": config_verdicts[cid]["per_band"][band_id]["trials_passing"],
                        "trials_total": config_verdicts[cid]["per_band"][band_id]["trials_total"],
                        "config_pass": config_verdicts[cid]["per_band"][band_id]["config_pass"],
                        "in_calibration_corridor": config_verdicts[cid]["per_band"][band_id]["in_calibration_corridor"],
                    }
                    for cid in sorted(config_verdicts)
                ],
                "passing_configs": sweep_per_band[band_id]["passing_configs"],
                "calibration_corridor": sweep_per_band[band_id]["calibration_corridor"],
                "sweep_pass": sweep_per_band[band_id]["sweep_pass"],
            }
            for band_id in BAND_SPECS
        },
        "primary_band": PRIMARY_BAND,
        "primary_band_verdict": primary["sweep_pass"],
        "primary_band_corridor": primary["calibration_corridor"],
        "diagnostic_summary": diag,
        # Per-trial forensic detail
        "trial_forensic_table": [
            {
                "config_id": cid,
                "fact_id": trec["fact_id"],
                "replicate": trec["replicate"],
                "p_target_new_per_probe": trec["p_target_new_per_probe"],
                "top_1_token_per_probe": trec["top_1_token_per_probe"],
            }
            for cid in sorted(trials_by_config)
            for trec in trials_by_config[cid]
        ],
    }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Revised verdict written to {args.output}")

    # Cross-check sanity: original 0.5 band should reproduce S2.10 verdict
    if sweep_verdict_struct:
        original_pass_05 = sweep_verdict_struct.get("sweep_pass", False)
        recomputed_pass_05 = sweep_per_band["B-A-0.5"]["sweep_pass"]
        if original_pass_05 != recomputed_pass_05:
            print(f"WARN: B-A-0.5 sanity check failed — "
                  f"original={original_pass_05}, recomputed={recomputed_pass_05}",
                  file=sys.stderr)
        else:
            print(f"Sanity check: B-A-0.5 reproduces original sweep verdict "
                  f"(both = {original_pass_05}). ✓")

    return 0


if __name__ == "__main__":
    sys.exit(main())
