"""Frozen D-ML-1 CPU algebra. No model or engine imports."""
import math
from pathlib import Path

import numpy as np
import torch

from apps.mathlab import mathlab_runtime as R
from state import llmdb_records as L
from apps.mathlab.index import build_index

torch.set_num_threads(8)
BAND = [4, 5, 6, 7, 8]
A1, A2, A7 = "A1_single", "A2_coherent2", "A7_coined_coined"
MINT = ["mint1_s0", "mint1_s1", "mint1_s2"]
# D-ML-2 rounds the measured full-shape 4.61/8.08 GiB peaks up to whole GiB reserves.
SVD_RESERVE_GIB = 5
SOLVE_RESERVE_GIB = 9


def cpu64(tensor):
    return tensor.detach().cpu().double()


def tensor_sha(tensor):
    import hashlib
    return hashlib.sha256(tensor.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def finite(tensor):
    R.require(tensor.device.type == "cpu" and bool(torch.isfinite(tensor).all()),
              "INVALID-ARITHMETIC", "nonfinite or non-CPU tensor")


def relative_error(value, reference):
    value, reference = cpu64(value), cpu64(reference)
    finite(value); finite(reference)
    denominator = torch.linalg.vector_norm(reference)
    R.require(float(denominator) != 0, "INVALID-ARITHMETIC", "zero relative-error denominator")
    result = float(torch.linalg.vector_norm(value - reference) / denominator)
    R.require(math.isfinite(result), "INVALID-ARITHMETIC", "nonfinite relative error")
    return result


def projector(cov):
    cov = cov.detach().cpu().float(); finite(cov)
    U, S, _ = torch.linalg.svd(cov, full_matrices=False)
    idx = (S < .005).nonzero(as_tuple=True)[0]
    return (U[:, idx] @ U[:, idx].T).cpu(), len(idx)


def projector_identity(P, null_n):
    P = P.detach().cpu().float()
    return {"null_n": int(null_n), "sha256": tensor_sha(P), "probes": [
        P @ torch.randn(P.shape[0], generator=torch.Generator().manual_seed(j)) for j in range(4)]}


def projector_matches(P, null_n, identity):
    if null_n != identity["null_n"]: return False
    if tensor_sha(P) == identity["sha256"]: return True
    for j, reference in enumerate(identity["probes"]):
        probe = P @ torch.randn(P.shape[0], generator=torch.Generator().manual_seed(j))
        try:
            if relative_error(probe, reference) > 1e-6: return False
        except R.Halt:
            return False
    return True


def solve(P, Kf, rf, ca):
    for value in (P, Kf, rf, ca): finite(value)
    R.require(all(t.dtype == torch.float32 for t in (P, Kf, rf, ca)), "INVALID-ARITHMETIC", "solve operands must be native fp32")
    A = P @ (Kf.cpu() @ Kf.cpu().T + ca) + 1. * torch.eye(Kf.shape[0])
    B = P @ Kf.cpu() @ rf.cpu().T
    update = torch.linalg.solve(A, B).T
    finite(update)
    # The float64 variant remains diagnostic and never changes the replay gate.
    Pd, Kd, rd, cad = map(cpu64, (P, Kf, rf, ca))
    Ad = Pd @ (Kd @ Kd.T + cad) + torch.eye(Kd.shape[0], dtype=torch.float64)
    Bd = Pd @ Kd @ rd.T
    variant = torch.linalg.solve(Ad, Bd).T; finite(variant)
    diagnostics = {"fp64_update_norm": float(torch.linalg.vector_norm(variant)),
                   "fp32_fp64_difference_norm": float(torch.linalg.vector_norm(cpu64(update) - variant))}
    del Pd, Kd, rd, cad, Ad, Bd, variant
    condition = float(torch.linalg.cond(cpu64(A)))
    R.require(math.isfinite(condition), "INVALID-ARITHMETIC", "nonfinite cond(A)")
    return update, {"cond_A": condition, **diagnostics}


def approximation_scope(pairs):
    passed = []
    for actual, reference in pairs.values():
        try:
            error = relative_error(actual, reference)
            a, b = cpu64(actual).flatten(), cpu64(reference).flatten()
            denominator = torch.linalg.vector_norm(a) * torch.linalg.vector_norm(b)
            R.require(float(denominator) != 0, "INVALID-ARITHMETIC", "zero cosine denominator")
            cosine = float(torch.dot(a, b) / denominator)
            passed.append(math.isfinite(cosine) and error <= .25 and cosine >= .95)
        except R.Halt:
            passed.append(False)
    return "ALT-SOLVES-ADMITTED" if passed and all(passed) else "OPERANDS-ONLY"


def score_values(proxy, values):
    values = np.asarray(values, dtype=np.float64)
    R.require(values.shape == (24, 3) and np.isfinite(values).all(), "INVALID-ARITHMETIC", "72 finite paraphrases are required")
    if proxy == "rho": result = float(np.mean(np.clip(values, 0, 1)))
    elif proxy == "coll": result = -float(np.median(values))
    else: raise ValueError("unknown frozen proxy: " + proxy)
    R.require(math.isfinite(result), "INVALID-ARITHMETIC", "nonfinite score")
    return result


def proxy_values(deltas, clean, zs, prompt_specs):
    deltas = {l: cpu64(v) for l, v in deltas.items()}; zs = cpu64(zs)
    rows = {"rho": [], "coll": []}; invalid = {"rho": False, "coll": False}
    specs = [p for p in prompt_specs if p["kind"] == "PTEST"]
    R.require([(p["subject_id"], p["template_id"]) for p in specs] == [(f, j) for f in range(24) for j in range(3)],
              "INVALID-ARITHMETIC", "paraphrase subject/template order changed")
    for spec in specs:
        key = spec["key"]; s = int(clean[key + ".subject_last"])
        h8 = cpu64(clean[key + ".l8.h"])
        change = sum(deltas[l] @ cpu64(clean[f"{key}.l{l}.k"]).T for l in BAND).T
        R.require(0 <= s < len(h8) and change.shape == h8.shape, "INVALID-ARITHMETIC", "subject index or token shapes invalid")
        residual = zs[:, spec["subject_id"]] - h8[s]
        residual_norm2 = float(residual.square().sum())
        subject_norm2 = float(change[s].square().sum())
        if residual_norm2 == 0 or not math.isfinite(residual_norm2): invalid["rho"] = True
        else:
            value = float(torch.dot(change[s], residual) / residual_norm2)
            if not math.isfinite(value): invalid["rho"] = True
            rows["rho"].append(value)
        if subject_norm2 == 0 or not math.isfinite(subject_norm2): invalid["coll"] = True
        else:
            # Concatenation omits exactly s and retains every real token, without padding.
            others = torch.cat((change[:s], change[s + 1:]))
            value = float(others.square().sum() / subject_norm2)
            if not math.isfinite(value): invalid["coll"] = True
            rows["coll"].append(value)
    result = {}
    for proxy in rows:
        if invalid[proxy]:
            result[proxy] = dict(status="INVALID-ARITHMETIC", values=None, score=None)
        else:
            values = np.asarray(rows[proxy], dtype=np.float64).reshape(24, 3)
            result[proxy] = dict(status="VALID", values=values, score=score_values(proxy, values))
    return result


def bootstrap_draws():
    rng = np.random.Generator(np.random.PCG64(0))
    return np.stack([rng.integers(0, 24, size=24) for _ in range(2000)])


def ordering_passes(point_passed, bootstrap_count):
    return bool(point_passed and bootstrap_count >= 1900)


def tier_status(outcomes, admitted, shared_ok=True):
    R.require(len(set(admitted)) == len(admitted) and set(admitted) <= set(MINT), "ADMISSION", "mint admission set invalid")
    if not shared_ok or len(admitted) < 2:
        return dict(outcome="INVALID", reason="INVALID-REPLAY", margins=None)
    top, middle, bottom = [outcomes[a] for a in (A1, A2)], [outcomes[a] for a in admitted], outcomes[A7]
    R.require(all(type(n) is int and 0 <= n <= 72 for n in top + middle + [bottom]), "INVALID-ARITHMETIC", "invalid measured outcome count")
    margins = dict(top_middle=min(top) - max(middle), middle_bottom=min(middle) - bottom)
    if min(margins.values()) < 10:
        return dict(outcome="INVALID", reason="INVALID-TIERS", margins=margins)
    return dict(outcome="VALID", reason="VALID-TIERS", margins=margins)


def calibrate(values, outcomes, admitted, shared_ok=True):
    tiers = tier_status(outcomes, admitted, shared_ok)
    if tiers["outcome"] == "INVALID":
        return dict(outcome="INVALID", reason=tiers["reason"], ordering_n=0, proxies={})
    orderings = [(t, m) for t in (A1, A2) for m in admitted] + [(m, A7) for m in admitted]
    draws = bootstrap_draws(); results = {}
    for proxy in ("rho", "coll"):
        data = values[proxy]; active = [A1, A2, *admitted, A7]
        try:
            R.require(all(data.get(a) is not None for a in active), "INVALID-ARITHMETIC", "an admitted arm has invalid proxy arithmetic")
            scores = {a: score_values(proxy, data[a]) for a in active}
        except R.Halt:
            results[proxy] = dict(status="INVALID-ARITHMETIC", passed=False)
            continue
        resampled = {}
        for arm in active:
            sample = np.asarray(data[arm], dtype=np.float64)[draws, :].reshape(2000, 72)
            resampled[arm] = np.clip(sample, 0, 1).mean(axis=1) if proxy == "rho" else -np.median(sample, axis=1)
        counts = {t + ">" + m: int(np.count_nonzero(resampled[t] > resampled[m])) for t, m in orderings}
        point = {t + ">" + m: scores[t] > scores[m] for t, m in orderings}
        passed = all(ordering_passes(point[k], counts[k]) for k in counts)
        results[proxy] = dict(status="VALID", passed=passed, scores=scores, point_orderings=point, bootstrap_counts=counts)
    if all(r["status"] == "INVALID-ARITHMETIC" for r in results.values()): outcome = "INVALID"
    else: outcome = "PASS" if any(r["passed"] for r in results.values()) else "FAIL"
    return dict(outcome=outcome, reason="both proxies INVALID-ARITHMETIC" if outcome == "INVALID" else "tier discrimination",
                ordering_n=len(orderings), proxies=results,
                bootstrap=dict(generator="PCG64(0)", resamples=2000, subjects=24, bar=1900),
                uniform_random_rank_caveat="Not a calibrated false-positive rate; correlated mint seeds and chosen arm families")


def verify_file(ref):
    R.require(R.sha_file(ref["path"]) == ref["sha256"], "SOURCE", "file hash changed: " + ref["path"])


def load_tensors(ref):
    verify_file(ref)
    values = torch.load(ref["path"], map_location="cpu", weights_only=True)
    R.require(isinstance(values, dict) and all(isinstance(v, torch.Tensor) and v.device.type == "cpu" for v in values.values()),
              "ARTIFACT", "harvest must be a flat CPU tensor dict")
    R.require({k: {"shape": list(v.shape), "dtype": str(v.dtype)} for k, v in values.items()} == ref["tensors"],
              "ARTIFACT", "harvest tensor metadata changed")
    return values


def covariance(ref):
    verify_file(ref)
    with np.load(ref["path"], allow_pickle=False) as arrays:
        # util/runningstats.py:499–500,509–511: torch division precedes float().
        count = int(arrays["mom2.count"])
        R.require(count > 0, "INVALID-ARITHMETIC", "empty covariance moment")
        return (torch.from_numpy(arrays["mom2.mom2"]) / count).cpu().float()


def identity_from_capture(tensors, layer):
    prefix = f"l{layer}."
    return {"null_n": int(tensors[prefix + "Pi_null_n"]),
            "sha256": bytes(tensors[prefix + "Pi_sha256"].tolist()).hex(),
            "probes": [tensors[prefix + f"Pi_probe{j}"] for j in range(4)]}


def reproduce(harvest_dir, output, run):
    manifest_path = Path(harvest_dir) / "manifest.json"; manifest = R.read_json(manifest_path)
    R.require(manifest["tier"] == R.TIER and manifest["prereg_sha256"] == R.PREREG_SHA, "SOURCE", "harvest identity mismatch")
    R.require(all(manifest["gates"][g]["passed"] for g in ("law3", "law5", "observer-parity")), "SOURCE", "harvest gates did not pass")
    run.pre_cell(2)
    clean = load_tensors(manifest["files"]["clean.pt"])
    arms = [A1, A2, A7, *manifest["replay_admission"]["admitted"]]
    records = {}; replay_files = {}; approximations = {}; approximate_change = None; rounding = {}
    for i, layer in enumerate(BAND):
        run.pre_cell(SVD_RESERVE_GIB)
        P, null_n = projector(covariance(manifest["covariances"][str(layer)]))
        for arm in arms:
            run.pre_cell(2)
            tensors = load_tensors(manifest["files"][f"inloop_{arm}.pt"]); p = f"l{layer}."
            identity = identity_from_capture(tensors, layer)
            project_ok = projector_matches(P, null_n, identity)
            run.gate(f"2a-projector-{arm}-{layer}", "Offline projection matches the recorded write",
                     {"null_n": null_n, "sha256": tensor_sha(P)}, {"null_n": identity["null_n"], "probe_relative_max": 1e-6}, project_ok)
            ca = torch.zeros(P.shape[0], P.shape[0])
            R.require(float(tensors[p + "ca_norm"]) == 0 and bool(tensors[p + "ca_zero"])
                      and tensor_sha(ca) == bytes(tensors[p + "ca_sha256"].tolist()).hex(), "SOURCE", "cache identity is not exact zero")
            run.pre_cell(SOLVE_RESERVE_GIB)
            update, diagnostics = solve(P, tensors[p + "Kf"], tensors[p + "rf"], ca)
            expected_norm = float(tensors[p + "upd_norm"])
            if arm == A7: error = relative_error(update, tensors[p + "upd_precast"])
            else:
                R.require(expected_norm != 0, "INVALID-ARITHMETIC", "zero update norm")
                error = abs(float(torch.linalg.vector_norm(cpu64(update))) - expected_norm) / expected_norm
            matched = error <= 1e-5
            run.gate(f"2a-update-{arm}-{layer}", "Offline write reproduces the saved calculation", error, 1e-5, matched, "<=")
            records[f"{arm}:{layer}"] = dict(projector_passed=project_ok, update_passed=matched, relative_error=error, **diagnostics)
            name = f"replayed_{arm}_l{layer}.pt"
            replay_files[name] = R.save_tensors(Path(output) / name, {"update": update, "zs": tensors[p + "zs"]})
            if arm == A7:
                K = clean[f"clean.k{layer}.mean"].float()
                canon = [s for s in manifest["prompts"] if s["kind"] == "CANON"]
                cur0 = torch.stack([clean[s["key"] + ".l8.h"][int(clean[s["key"] + ".subject_last"])] for s in canon], dim=1)
                if approximate_change is None: approximate_change = torch.zeros_like(cur0, dtype=torch.float32)
                residual = (tensors[p + "zs"].float() - (cur0.float() + approximate_change)) / (5 - i)
                run.pre_cell(SOLVE_RESERVE_GIB)
                alternative, _ = solve(P, K, residual, ca)
                approximate_change = approximate_change + alternative @ K
                approximations[layer] = (alternative, tensors[p + "upd_precast"])
                weights = load_tensors(manifest["files"]["weights_A7.pt"])
                effective = cpu64(weights[p + "after"]) - cpu64(weights[p + "before"])
                rounding[str(layer)] = relative_error(effective, tensors[p + "upd_precast"])
                del weights
            del update, ca, tensors
            run.event("progress", stage="reproduction", done=len(records), total=5 * len(arms), unit="layer writes")
        del P
    passed = all(r["projector_passed"] and r["update_passed"] for r in records.values())
    run.gate("2a", "Exact offline reproduction of the recorded write", records, "all matches within frozen tolerances", passed)
    scope = approximation_scope(approximations)
    run.gate("2b", "Whether clean inputs support first-order alternative solves", scope,
             {"relative_error_max": .25, "cosine_min": .95}, scope == "ALT-SOLVES-ADMITTED")
    result = dict(tier=R.TIER, decision_id="D-ML-1", prereg_sha256=R.PREREG_SHA,
                  harvest={"path": str(manifest_path), "sha256": R.sha_file(manifest_path)},
                  gate2a={"passed": passed, "records": records}, gate2b=scope,
                  fp16_rounding=rounding, files=replay_files, gates=run.gates)
    R.write_new(Path(output) / "manifest.json", result)
    return result


def calibration(harvest_dir, reproduction_dir, output, run):
    manifest_path = Path(harvest_dir) / "manifest.json"; harvest = R.read_json(manifest_path)
    m2_path = Path(reproduction_dir) / "manifest.json"; m2 = R.read_json(m2_path)
    R.require(m2["tier"] == R.TIER and m2["prereg_sha256"] == R.PREREG_SHA, "SOURCE", "step-2 identity mismatch")
    verify_file(m2["harvest"])
    R.require(Path(m2["harvest"]["path"]).resolve() == manifest_path.resolve(), "SOURCE", "step 2 uses a different harvest")
    R.require(m2["gate2a"]["passed"], "2a", "step 2 must pass before proxies")
    # Read the frozen admission BEFORE evaluating any proxy; never exclude on score.
    admission = harvest["replay_admission"]; admitted = admission["admitted"]
    counts = {a: harvest["outcomes"][a]["used_for_calibration"] for a in (A1, A2, A7, *admitted)}
    tiers = tier_status(counts, admitted, admission["shared_passed"])
    run.gate("replay-admission", "Historical replay identity admits at least two middle arms before scoring",
             admission, "shared checks pass and at least two arms admitted", admission["shared_passed"] and len(admitted) >= 2)
    run.gate("tier-validity", "Measured result tiers are separated by at least ten bindings before scoring",
             tiers, {"top_middle_min": 10, "middle_bottom_min": 10}, tiers["outcome"] == "VALID")
    values = {"rho": {}, "coll": {}}; raw = {}
    if tiers["outcome"] == "INVALID":
        result = calibrate(values, counts, admitted, admission["shared_passed"])
    else:
        run.pre_cell(2)
        clean = load_tensors(harvest["files"]["clean.pt"])
        for i, arm in enumerate([A1, A2, *admitted, A7]):
            deltas = {}; zs = None
            for layer in BAND:
                data = load_tensors(m2["files"][f"replayed_{arm}_l{layer}.pt"])
                deltas[layer] = data["update"]; zs = data["zs"]
            proxies = proxy_values(deltas, clean, zs, harvest["prompts"])
            raw[arm] = {p: dict(status=v["status"], score=v["score"],
                               values=v["values"].tolist() if v["values"] is not None else None) for p, v in proxies.items()}
            for proxy, data in proxies.items():
                values[proxy][arm] = data["values"]
                run.gate(f"arithmetic-{proxy}-{arm}", "All 72 paraphrases have valid arithmetic", data["status"], "VALID", data["status"] == "VALID")
            del deltas, data, proxies
            run.event("progress", stage="calibration", done=i + 1, total=3 + len(admitted), unit="arms scored")
        run.pre_cell(1)
        result = calibrate(values, counts, admitted, admission["shared_passed"])
    for proxy, data in result["proxies"].items():
        for ordering, count in data.get("bootstrap_counts", {}).items():
            run.gate(f"point-{proxy}-{ordering}", "The higher tier has a strictly higher point score",
                     data["point_orderings"][ordering], True, data["point_orderings"][ordering])
            run.gate(f"bootstrap-{proxy}-{ordering}", "The strict ordering survives paired subject resampling",
                     count, 1900, count >= 1900, ">=")
        run.gate("proxy-" + proxy, "Proxy separates the measured result tiers", data,
                 "strict point ordering and 1900 of 2000 paired samples", data["passed"])
    run.gate("calibration", "At least one math estimate separates the measured tiers", result["outcome"], "PASS", result["outcome"] == "PASS")
    result.update(tier=R.TIER, decision_id="D-ML-1", prereg_sha256=R.PREREG_SHA, raw=raw,
                  outcomes=harvest["outcomes"], replay_admission=admission,
                  consistency_checks=dict(non_gating=True, calibration_evidence=False,
                      injection_vs_write=dict(injected_tau_by_construction=1, historical_unedited_injection=[49, [51, 54]],
                          historical_write_range=[8, 15], meaning="Agreement by construction calibrates nothing",
                          sources=["evidence/CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:23", "evidence/CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:34"]),
                      edited_model_injection=dict(historical_para_full=23,
                          current_A7_coll_score=raw.get(A7, {}).get("coll", {}).get("score"),
                          meaning="Reported beside the proxy; no matched intervention or extra calibration observation",
                          source="evidence/CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:30")),
                  named_approximations=["additive residual ignores attention and later-layer responses", "fp16 cast-and-add rounding"],
                  prospective_queue_utility="UNVERIFIED", gates=run.gates,
                  sources={"harvest": {"path": str(manifest_path), "sha256": R.sha_file(manifest_path)},
                           "step2": {"path": str(m2_path), "sha256": R.sha_file(m2_path)}})
    R.write_new(Path(output) / "calibration.json", result)
    return result


def assert_environment(root=R.ROOT):
    import importlib.metadata
    actual = importlib.metadata.version("torch")
    site_dirs = list((Path(root) / ".venv/lib").glob("python*/site-packages"))
    recorded = [d.version for d in importlib.metadata.distributions(path=[str(p) for p in site_dirs])
                if d.metadata["Name"].lower() == "torch"]
    R.require(actual == "2.8.0" and recorded == [actual], "VERSION", "torch must be 2.8.0 and equal .venv metadata")
    R.require(torch.get_num_threads() == 8, "THREADS", "CPU torch must use eight threads")


def index_references(harvest_path, harvest):
    refs = []
    for arm in (A1, A2, A7):
        refs.append(dict(path=str(harvest_path), pointer=f"/outcomes/{arm}/fresh_harvest_count", arm=arm,
                         block="fresh", run=Path(harvest_path).parent.name, metric="para_full", sha256=R.sha_file(harvest_path)))
    for arm in MINT:
        source = harvest["identity"]["seed_sources"][arm]
        if source["passed"]:
            refs.append(dict(path=source["record"]["path"], pointer="/arm/para_full_binding_n", arm=arm,
                             block="F", run="r0", metric="historical_para_full", sha256=source["record"]["sha256"]))
    return refs


def run_notebook(step, params):
    """The boundary used identically by marimo interactive and script modes."""
    import os
    assert_environment()
    R.verify_prereg()
    cap = 6540 if step == 2 else 1800
    given_run = os.environ.get("MATHLAB_RUN_DIR")
    if given_run:
        run_dir = Path(given_run)
        proof = R.read_json(run_dir / "admission.json")
        R.require(proof["allowed"] and proof["kind"] == "cpu", "ADMISSION", "runner admission refused")
    else:
        raise R.Halt("ADMISSION", "launch through code/apps/mathlab/run_mathlab_cpu.sh; fixture tests inject admission at that boundary")
    run = R.Run(run_dir, step, f"Offline math lab step {step}", cap, attach=True)
    output = None
    try:
        R.enforce_stop_policy(R.ROOT, step, exclude=run_dir)
        output = R.new_directory(params.output_root, f"m{step}")
        stage = "reproduction" if step == 2 else "calibration"
        with run.stage(stage, "Reproduce the saved write" if step == 2 else "Test two frozen math estimates", cap, alarm=True):
            if step == 2:
                result = reproduce(params.harvest_dir, output, run)
                outcome = "PASS" if result["gate2a"]["passed"] else "FAIL"
            else:
                result = calibration(params.harvest_dir, params.reproduction_dir, output, run)
                outcome = result["outcome"]
                if outcome == "FAIL":
                    R.stage_finding(R.ROOT, run_dir, "calibration-stop", "Calibration FAIL; the lab stops cheaply under the frozen criterion")
                with run.stage("index", "Rebuild the derived source-citation index", 300, alarm=True):
                    harvest_path = Path(params.harvest_dir) / "manifest.json"
                    index = build_index(params.index_path, index_references(harvest_path, R.read_json(harvest_path)))
                    run.gate("index-provenance", "Every index row retains its authoritative source and pointer", index,
                             "source path, JSON pointer and current SHA-256", True)
                R.write_new(output / "manifest.json", dict(tier=R.TIER, decision_id="D-ML-1", prereg_sha256=R.PREREG_SHA,
                            files={"calibration.json": {"path": str(output / "calibration.json"), "sha256": R.sha_file(output / "calibration.json")}},
                            index=index, gates=run.gates))
        if step == 2 and outcome == "FAIL":
            from apps.mathlab.mathlab_events import read_events
            failures = 0
            for path in L.lab_event_streams(R.ROOT):
                if path.parent == run_dir: continue
                events, errors = read_events(path)
                R.require(not errors, "EVENTS", "; ".join(errors))
                failures += any(e["type"] == "gate_result" and e["gate_id"] == "2a" and not e["passed"] for e in events)
            R.stage_halt(R.ROOT, run_dir, "LAB-STOP-2a" if failures else "2a-DIAGNOSIS-REQUIRED",
                         "Read the frozen solve source; one diagnosis/fix only. " +
                         ("The lab stops after the failed confirming run." if failures else "No automatic retry."), step=step)
            return dict(output_dir=str(output), **result)
        if outcome == "INVALID": summary = "Calibration INVALID; operator review required; no scientific verdict"
        elif outcome == "FAIL": summary = "Calibration FAIL; the lab stops cheaply under the frozen criterion"
        else: summary = "Fixture-only verification" if R.read_json(Path(params.harvest_dir) / "manifest.json").get("fixture") else "Math-proxy stage passed; prospective queue utility remains UNVERIFIED"
        if not (step == 3 and outcome == "FAIL"):
            R.stage_finding(R.ROOT, run_dir, f"m{step}", summary)
        run.event("run_finished", outcome=outcome, summary=summary)
        return dict(output_dir=str(output), **result)
    except Exception as error:
        R.stage_halt(R.ROOT, run_dir, error.code if isinstance(error, R.Halt) else "CPU-ERROR", str(error), step=step,
                     details={"gates": run.gates, "output_dir": str(output)})
        raise
