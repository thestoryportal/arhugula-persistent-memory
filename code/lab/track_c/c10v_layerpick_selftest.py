#!/usr/bin/env python3
"""Model-free synthetic tests derived BEFORE code from frozen C10V §§2–5.

Only stdlib/numpy; writes stay in temporary directories. Synthetic numerical
checks test the instrument, never confer live LAW#3/LAW#5 or science evidence.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import contextlib, copy, hashlib, io, json, subprocess, tempfile, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10v_layerpick_read as R
import c10v_layerpick_arms as D

ROOT = Path(__file__).resolve().parents[3]
SUBJECTS = ["S" + str(i) for i in range(R.N)]


def proof_fixture():
    mapping = {s: 4 + i % 5 for i, s in enumerate(SUBJECTS)}
    largest = sorted(R.groups(mapping, SUBJECTS), key=lambda g: (-len(g[1]), -g[0]))[:2]
    return {"ok": True, "standing": {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0}, "standing_override_hits": 0,
            "floor": {"relative_max": 0.0, "relative_by_layer": {str(l): 0.0 for l in R.LAYERS},
                      "behavior_count_deltas": {"canon_full_n": 0, "para_full_n": 0}}, "tolerance": 1e-4,
            "identity": {"relative_by_layer": {str(l): 0.0 for l in R.LAYERS}, "behavior_equal": True,
                         "active_group_layers": [list(R.LAYERS)]},
            "singleton": {"relative_by_layer": {"8": 0.0}, "active_group_layers": [[8]], "projector_indices": [4]},
            "multigroup": {"relative_by_layer": {str(l): 0.0 for l, _ in largest},
                           "active_group_layers": [[l] for l, _ in sorted(largest, reverse=True)],
                           "groups": [{"layers": [l], "subjects": ss, "projector_indices": [l - 4]}
                                      for l, ss in sorted(largest, reverse=True)]}}


def identity_fixture():
    hashes = {n: "1" * 64 for n in R.REQUIRED_SOURCES}
    hashes[R.ENGINE_FILE] = R.ENGINE_SHA256
    return {"run_id": "synthetic-c10v", "source_sha256": hashes, "source_digest": R.source_digest(hashes),
            "preflight_controls_reference": {"ok": True, "sha256": "2" * 64, "path": "/synthetic/reference", "scores": {a: 70 for a in R.ARMS[:2]}}}


def step_fixture():
    table = [[0.1 + 0.01 * j + (0.4 if j == i % 5 else 0) for j in range(5)] for i in range(R.N)]
    step = R.select_maps(table, copy.deepcopy(table), SUBJECTS)
    ctx = [["{}"], ["Clean. {}"]]
    step.update(subjects=SUBJECTS, ctx=ctx, ctx_sha256=R.json_digest(ctx),
                projected_key_norms=[[1.0] * 5 for _ in SUBJECTS], projected_key_norms_repeat=[[1.0] * 5 for _ in SUBJECTS],
                installed_share_comparison=[{"subj": s, "max_G": max(table[i]), "installed_share": 0.972} for i, s in enumerate(SUBJECTS)])
    return step


def set_score(record, recipe, arm_name, n, canon=None):
    rec = record["recipes"][recipe]
    arm = rec["arms"][arm_name]
    canon = arm["canon_full_n"] if canon is None else canon
    rows = [{"subj": s, "val": "Value " + str(i), "ntok": 2, "canon_full": i < canon,
             "canon_first": i < canon, "para_full_hits": [i * 3 + j < n for j in range(3)],
             "para_first_hits": [i * 3 + j < max(n, 54) for j in range(3)],
             "para_string_hits": [i * 3 + j < n for j in range(3)], "tf_correct": 3, "tf_total": 3} for i, s in enumerate(SUBJECTS)]
    rec["detail"][arm_name] = rows
    arm.update(R.row_counts(rows, SUBJECTS), canon_n=24, para_n=72, para_full=round(100 * n / 72, 1),
               para_full_string=round(100 * n / 72, 1), tf_pertok_cont=100.0, cond_full_given_first=round(n / max(n, 54), 3))


def pass_fixture(b=30, b0=19, bshuf=19, baseline=10, pid=100):
    step = step_fixture()
    maps = R.recipe_maps(step["map"], SUBJECTS)
    rec = {"decision_id": R.DECISION_ID, "identity": identity_fixture(), "pid": pid, "outcome": "COMPLETE",
           "fingerprint": {"ok": True, "sha256": R.ENGINE_SHA256, "_cov_cpu": 3}, "step0": step,
           "published_map": step["map"], "published_map_sha256": step["map_sha256"], "ctx": step["ctx"],
           "ctx_sha256": step["ctx_sha256"], "law5": proof_fixture(), "recipes": {},
           "hsic": {"role": "synthetic diagnostic", "n": 24,
                    "layers": {str(l): {"sigma_X": 0.0, "sigma_Y": 0.0, "status": "UNDEFINED: zero median pairwise distance"} for l in R.LAYERS},
                    "argmax_c_map": None, "agreement_n": None}}
    for name, mapping in maps.items():
        rec["recipes"][name] = {"map": mapping, "band": list(R.LAYERS), "law5_gate": {"ok": True},
                               "arms": {}, "detail": {}, "delta_norms": {}, "wrapper": {}, "target_ids": {},
                               "predictions_before_write": {}, "targets_sha256": {},
                               "cov_cache_sha256": {str(l): {"path": "/synthetic/cov" + str(l), "sha256": "c" * 64} for l in R.LAYERS}}
        for arm in R.ARMS:
            gs = [(list(R.LAYERS), SUBJECTS)] if mapping is None else [([l], ss) for l, ss in R.groups(mapping, SUBJECTS)]
            layers = {l for ls, _ in gs for l in ls}
            extra = {"same_frame": {"n": 6, "flips": 0, "rows": [{"subj": s, "top1": 999, "flip": False} for s in D.FRAME_SUBJECTS]},
                     "relation_labels": {k: {"n": 24, "flips": 0, "pre_top1": [5] * 24, "post_top1": [5] * 24} for k in ("bystander", "objective-anchored")}}
            if arm != R.ARMS[1]:
                extra["proxy"] = {"rows": [{"subj": s, "layer": 8 if mapping is None else mapping[s],
                                            "rho_per_prompt": [0.1] * 4, "realised_fraction": 0.9,
                                            "full_G_diagonal": step["G_table"][i][(8 if mapping is None else mapping[s]) - 4], "group_G_diagonal": 0.3,
                                            "prediction_error": 0.9 - 0.3, "pristine_residual_norms": [1.0] * 4,
                                            "undefined_zero_denominator": []} for i, s in enumerate(SUBJECTS)],
                                  "targets_sha256": "a" * 64, "weight_application": "fp16", "predictions_recorded_before_write": True}
            rec["recipes"][name]["arms"][arm] = {"canon_full_n": 7 if name == "A" and arm == R.ARMS[2] else 24,
                "locality_described_as": 97.0, "locality_axes": {"L1_n": 12, "L1_flipped_to_edited_value": 0,
                "L3_n": 30, "L3_top1_agree": 30, "generic_ppl_pre": 20.0, "generic_ppl_post": 20.0}, "extra": extra}
            rec["recipes"][name]["delta_norms"][arm] = {str(l): {"delta_norm": 5 / len(layers)} for l in layers}
            rec["recipes"][name]["wrapper"][arm] = {"z_override_hits": len(gs),
                "groups": [{"layers": ls, "subjects": ss, "projector_indices": [R.LAYERS.index(l) for l in ls]} for ls, ss in gs]}
            rec["recipes"][name]["target_ids"][arm] = {s: [10 + i, 100 + i] for i, s in enumerate(SUBJECTS)}
            rec["recipes"][name]["targets_sha256"][arm] = "a" * 64
            rec["recipes"][name]["predictions_before_write"][arm] = {s: {"full_G_diagonal": step["G_table"][i][(8 if mapping is None else mapping[s]) - 4], "group_G_diagonal": 0.3} for i, s in enumerate(SUBJECTS)}
            set_score(rec, name, arm, 70 if arm != R.ARMS[2] else {"A": baseline, "B": b, "B0": b0, "Bshuf": bshuf}[name])
    return rec


class Array(np.ndarray):
    """Synthetic CPU arrays with just the read methods the harness seam uses."""
    def detach(self): return self
    def cpu(self): return self
    def float(self): return np.asarray(self, dtype=np.float32).view(Array)
    def numpy(self): return np.asarray(self)


def array(x):
    return np.asarray(x, dtype=np.float64).view(Array)


class SyntheticHarness:
    """A shallower write alters deeper inputs; no tokenizer or torch object."""
    def __init__(self):
        self.FICTION, self.CANON, self.PTEST = SUBJECTS, "Canon {}", ["Para0 {}", "Para1 {}", "Para2 {}"]
        self.ARMS = {arm: {s: arm + " value " + str(i) for i, s in enumerate(SUBJECTS)} for arm in R.ARMS}
        self.weights = {l: np.zeros((2, 3)) for l in R.LAYERS}
        self.torch = SimpleNamespace(zeros=lambda *shape: np.zeros(shape), no_grad=contextlib.nullcontext,
                                     stack=lambda xs: array(np.stack(xs)))
        self.model, self.tok = object(), object()
        self.Z_OVERRIDE, self.Z_OVERRIDE_HITS, self._LAW5_DEFAULT_CTX = None, 0, False
        self.my_edit = self.original
        self.calls = []

    def req(self, prompt, subj, targ): return {"prompt": prompt, "subject": subj, "target_new": {"str": " " + targ}}
    def snap_layers(self, hp): return {l: self.weights[l].copy() for l in hp.layers}
    def restore_layers(self, hp, base):
        for l in hp.layers: self.weights[l][...] = base[l]
    def get_context_templates(self, model, tok): return [["{}"]]
    def key(self, l, s):
        i = SUBJECTS.index(s)
        lower = sum(self.weights[m].sum() for m in R.LAYERS if m < l)
        return np.array([1 + i / 23, 0.1 + l / 10, 0.3 + i / 48]) + 0.2 * lower
    def cur(self, l, s, template="Canon {}"):
        lower = sum(self.weights[m].sum() for m in R.LAYERS if m < l)
        offset = 0.3 if template.startswith("Para") else 0
        return self.weights[l] @ self.key(l, s) + lower * np.array([0.2, -0.1]) + offset
    def compute_ks(self, model, tok, requests, hp, l, ctx):
        return array([self.key(l, r["subject"]) for r in requests])
    def compute_z(self, model, tok, request, hp, l, ctx):
        self.calls.append(("target", l, request["subject"]))
        return array([2 + l / 10, -0.7 + SUBJECTS.index(request["subject"]) / 100])
    def get_module_input_output_at_words(self, model, tok, l, context_templates, words, module_template, fact_token_strategy):
        return array([self.key(l, s) for s in words]), array([self.cur(l, s, t) for s, t in zip(words, context_templates)])
    def original(self, hp, requests, P, cache):
        keys = [(r["subject"], r["target_new"]["str"]) for r in requests]
        override = self.Z_OVERRIDE is not None and not self._LAW5_DEFAULT_CTX and all(k in self.Z_OVERRIDE for k in keys)
        if override:
            self.Z_OVERRIDE_HITS += 1
        zs = np.stack([self.Z_OVERRIDE[k] if override else self.compute_z(self.model, self.tok, r, hp, hp.layers[-1], [["{}"]])
                       for k, r in zip(keys, requests)], axis=1)
        out = {}
        for j, l in enumerate(hp.layers):
            K = np.stack([self.key(l, r["subject"]) for r in requests], axis=1)
            cur = np.stack([self.cur(hp.layers[-1], r["subject"]) for r in requests], axis=1)
            residual = (zs - cur) / (len(hp.layers) - j)
            update = np.linalg.solve(P[j] @ (K @ K.T + cache[j]) + np.eye(3), P[j] @ K @ residual.T).T
            self.weights[l] += update
            out[str(l)] = {"delta_norm": float(np.linalg.norm(update))}
            self.calls.append(("write", l, [r["subject"] for r in requests], cache[j].copy(), P[j].copy()))
        for j, l in enumerate(hp.layers):
            K = np.stack([self.key(l, r["subject"]) for r in requests], axis=1)
            cache[j] = cache[j] + K @ K.T
        return out
    def eval_arm(self, values):
        n = int(min(72, np.linalg.norm(self.weights[8]) * 10))
        return {"canon_full_n": min(24, n), "para_full_n": n,
                "hits": [np.linalg.norm(self.cur(8, s)) > 0.5 for s in SUBJECTS]}
    def run_law5(self, hp, P, base):
        r = [self.req(self.CANON, SUBJECTS[0], "Cairo")]
        self.original(hp, r, P, [np.zeros((3, 3)) for _ in P])
        a = self.snap_layers(hp)
        self.restore_layers(hp, base)
        self._LAW5_DEFAULT_CTX = True
        try: self.my_edit(hp, r, P, [np.zeros((3, 3)) for _ in P])
        finally: self._LAW5_DEFAULT_CTX = False
        b = self.snap_layers(hp)
        self.restore_layers(hp, base)
        return {"ok": all(np.array_equal(a[l], b[l]) for l in hp.layers), "expr_delta": 0.0, "loc_delta": 0.0}


def synthetic_prepared(H, layer_map=None):
    effective = layer_map or {s: 8 for s in SUBJECTS}
    values = H.ARMS[R.ARMS[2]]
    requests = [H.req(H.CANON, s, values[s]) for s in SUBJECTS]
    targets = {(r["subject"], r["target_new"]["str"]): H.compute_z(H.model, H.tok, r, None, effective[r["subject"]], [["{}"]]) for r in requests}
    return {"requests": requests, "targets": targets}


def fixture_directory(tmp, records=None, stopped=False):
    """Real persisted chain, including positive controls for the observation layer."""
    root = Path(tmp) / "worktree"; out = root / "experiments/c10v/runs/c10v_layerpick"
    records = records or [pass_fixture(b=18, b0=18, bshuf=18)]
    identity = copy.deepcopy(records[0]["identity"])
    for name in R.REQUIRED_SOURCES:
        path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes() if name == R.ENGINE_FILE else ("synthetic " + name).encode())
        identity["source_sha256"][name] = D.sha256_file(path)
    identity["source_digest"] = R.source_digest(identity["source_sha256"])
    ref = root / "reference.json"; D.write_json(ref, {"recipes": {"baseline": records[0]["recipes"]["A"]}})
    identity["preflight_controls_reference"].update(path=str(ref), sha256=D.sha256_file(ref))
    step = copy.deepcopy(records[0]["step0"])
    if stopped:
        table = [[0, 0, 0, 0, 1] for _ in SUBJECTS]; step.update(R.select_maps(table, table, SUBJECTS))
    step.update(identity=identity, fingerprint=records[0]["fingerprint"], cov_cache_sha256=records[0]["recipes"]["A"]["cov_cache_sha256"])
    D.write_json(out / "identity.json", identity); D.write_json(out / "step0.json", step)
    if stopped:
        D.write_json(out / "run.json", {"identity": identity, "label": step["status"], "candidate_advanced": False,
                                      "step0_sha256": D.sha256_file(out / "step0.json"), "table_published": True})
        return root, out, records
    for i, record in enumerate(records):
        stage = "pass" + str(i + 1); record["identity"] = identity
        D.write_json(out / (stage + ".json"), record)
        D.write_json(out / ("law5.json" if i == 0 else "law5_pass2.json"),
                     {"identity": identity, "pid": record["pid"], "law5": record["law5"], "ctx_sha256": record["ctx_sha256"],
                      "published_map_sha256": record["published_map_sha256"]})
        D.write_json(out / (stage + "_started.json"), {"identity": identity, "pid": record["pid"], "law5_ok": True,
                     "live_law3_ok": True, "published_map_sha256": record["published_map_sha256"]})
        D.write_json(out / (stage + "_complete.json"), {"identity": identity, "pid": record["pid"], "record_sha256": D.sha256_file(out / (stage + ".json"))})
    reading = R.read_run(*records)
    if len(records) == 2 or not reading["replication_needed"]:
        D.write_json(out / "run.json", {"identity": identity, **reading,
                     "pass_sha256": {"pass" + str(i + 1): D.sha256_file(out / ("pass" + str(i + 1) + ".json")) for i in range(len(records))}})
    return root, out, records


class SelectorAndNumericalTests(unittest.TestCase):
    def test_proxy_matches_independent_full_solve_and_singleton(self):
        K = np.array([[1, 2], [3, 1], [2, 0]], float); P = np.diag([1, 0, 1]); residual = np.array([[2, -1], [1, 3]], float)
        G, norms = D.g_from_keys(K, P)
        direct = np.linalg.solve(np.eye(3) + P @ K @ K.T, P @ K @ residual.T).T @ K
        np.testing.assert_allclose(direct, residual @ G, atol=1e-12)
        np.testing.assert_allclose(norms, np.linalg.norm(P @ K, axis=0))
        one, _ = D.g_from_keys(K[:, :1], P)
        self.assertAlmostEqual(one[0, 0], norms[0] ** 2 / (1 + norms[0] ** 2))

    def test_margin_delta_below_at_above_and_nearest8_tie(self):
        for margin, chosen in ((0.0625, 5), (0.125, 4), (0.25, 4)):
            with self.subTest(margin=margin):
                first = [[0.5 + margin, 0.5, 0, 0, 0] for _ in SUBJECTS]
                second = copy.deepcopy(first); second[-1][4] = 0.125
                read = R.select_maps(first, second, SUBJECTS)
                self.assertEqual(read["delta"], 0.125); self.assertEqual(read["map"][SUBJECTS[0]], chosen)
        tied = R.select_maps([[0.5] * 5 for _ in SUBJECTS], [[0.5] * 5 for _ in SUBJECTS], SUBJECTS)
        self.assertEqual(set(tied["map"].values()), {8})

    def test_nearest8_contenders_and_margin_immediate_float_boundaries(self):
        for runner, chosen in ((float(np.nextafter(0.625, 1.0)), 5), (0.625, 4),
                               (float(np.nextafter(0.625, 0.0)), 4)):
            with self.subTest(runner=runner):
                first = [[0.75, runner, 0, 0, 0] for _ in SUBJECTS]
                second = copy.deepcopy(first); second[-1][4] = 0.125
                result = R.select_maps(first, second, SUBJECTS)
                self.assertEqual(result["delta"], 0.125)
                self.assertEqual(result["map"][SUBJECTS[0]], chosen)
        for contender, chosen in ((float(np.nextafter(0.625, 0.0)), 5), (0.625, 6),
                                  (float(np.nextafter(0.625, 1.0)), 6)):
            with self.subTest(contender=contender):
                first = [[0.75, 0.6875, contender, 0, 0] for _ in SUBJECTS]
                second = copy.deepcopy(first); second[-1][4] = 0.125
                self.assertEqual(R.select_maps(first, second, SUBJECTS)["map"][SUBJECTS[0]], chosen)
        tied = [[0.5, 0.5, 0, 0, 0] for _ in SUBJECTS]
        self.assertEqual(R.select_maps(tied, tied, SUBJECTS)["map"][SUBJECTS[0]], 5)

    def test_concentration_19_20_21_and_nonreproducible(self):
        for n in (19, 20, 21):
            table = [[1 if j == (0 if i < n else 4) else 0 for j in range(5)] for i in range(24)]
            read = R.select_maps(table, table, SUBJECTS)
            self.assertEqual(read["status"], "READY" if n == 19 else "concentrated map; candidate not advanced")
        a = [[0.5, 0.5, 0, 0, 0] for _ in SUBJECTS]; b = copy.deepcopy(a); b[0][0] += 0.125
        self.assertEqual(R.select_maps(a, b, SUBJECTS)["status"], "map not reproducible")

    def test_hsic_formula_contributions_and_degenerate_diagnostic(self):
        rng = np.random.default_rng(42)
        keys = {l: rng.normal(size=(3, 24)) for l in R.LAYERS}; residual = rng.normal(size=(24, 2))
        published = step_fixture()["map"]
        read = D.hsic_diagnostic(keys, residual, SUBJECTS, published)
        H = np.eye(24) - np.ones((24, 24)) / 24
        def kernel(rows):
            dist = np.sqrt(((rows[:, None] - rows[None, :]) ** 2).sum(axis=2))
            sigma = np.median(dist[np.triu_indices(24, 1)])
            return np.exp(-(dist ** 2) / (2 * sigma ** 2))
        expected = np.trace(H @ kernel(keys[4].T) @ H @ H @ kernel(residual) @ H) / 23 ** 2
        self.assertAlmostEqual(read["layers"]["4"]["HSIC_b"], expected)
        self.assertEqual(len(read["layers"]["4"]["per_fact_c"]), 24)
        degenerate = D.hsic_diagnostic(keys, np.zeros((24, 2)), SUBJECTS, published)
        self.assertIsNone(degenerate["argmax_c_map"])

    def test_spearman_ties_and_constant(self):
        self.assertEqual(R.rank_values([1, 1, 3]), [1.5, 1.5, 3])
        self.assertAlmostEqual(R.spearman([1, 2, 3], [3, 2, 1]), -1)
        self.assertIsNone(R.spearman([1, 1, 1], [0, 1, 0]))

    def test_wrapper_groups_targets_hparams_projectors_and_fresh_cache(self):
        H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS), other="unchanged")
        mapping = step_fixture()["map"]; prepared = synthetic_prepared(H, mapping)
        P = [np.diag([1, int(l % 2 == 0), int(l % 2 == 1)]) for l in R.LAYERS]
        wrapped = D.GroupedEdit(H, H.original, {"candidate": prepared}, mapping)
        wrapped(hp, prepared["requests"], P, [np.full((3, 3), 9) for _ in P])
        writes = [c for c in H.calls if c[0] == "write"]
        self.assertEqual([c[1] for c in writes], [8, 7, 6, 5, 4])
        self.assertLess(max(i for i, c in enumerate(H.calls) if c[0] == "target"), min(i for i, c in enumerate(H.calls) if c[0] == "write"))
        for call in writes:
            np.testing.assert_array_equal(call[3], np.zeros((3, 3)))
            np.testing.assert_array_equal(call[4], P[call[1] - 4])
        self.assertEqual(hp.layers, list(R.LAYERS)); self.assertEqual(hp.other, "unchanged")
        self.assertEqual(H.Z_OVERRIDE_HITS, 5)
        b0 = R.recipe_maps(mapping, SUBJECTS)["B0"]
        self.assertEqual(set(b0.values()), {8})
        shuffled = R.recipe_maps(mapping, SUBJECTS)["Bshuf"]
        self.assertEqual(sorted(shuffled.values()), sorted(mapping.values()))
        self.assertEqual(shuffled[SUBJECTS[0]], mapping[SUBJECTS[1]])

    def test_map_none_and_law5_bypass_and_active_band_identity(self):
        H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS)); P = [np.eye(3) for _ in R.LAYERS]
        prepared = synthetic_prepared(H)
        none = D.GroupedEdit(H, H.original, {"audit": prepared}, None)
        none(hp, prepared["requests"], P, [np.zeros((3, 3)) for _ in P])
        self.assertEqual(H.Z_OVERRIDE_HITS, 1)
        H._LAW5_DEFAULT_CTX = True
        with patch.object(H, "original", return_value={}) as untouched:
            D.GroupedEdit(H, untouched, {}, {"invalid": 99})(hp, prepared["requests"], P, [])
            untouched.assert_called_once()
        H._LAW5_DEFAULT_CTX = False
        H.restore_layers(hp, {l: np.zeros((2, 3)) for l in R.LAYERS})
        wrapped = D.GroupedEdit(H, H.original, {"audit": prepared}, {s: list(R.LAYERS) for s in SUBJECTS})
        wrapped(hp, prepared["requests"], P, [])
        self.assertEqual(wrapped.audits["audit"]["groups"][0]["layers"], list(R.LAYERS))

    def test_actual_numeric_law5_and_order_projector_fault_sensitivity(self):
        H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS)); base = H.snap_layers(hp)
        P = [np.diag([1, int(l % 2 == 0), int(l % 2 == 1)]) for l in R.LAYERS]
        prepared = synthetic_prepared(H); mapping = step_fixture()["map"]
        proof = D.law5_checks(H, hp, P, base, {R.ARMS[2]: prepared}, mapping)
        R.law5_reading(proof)
        self.assertTrue(proof["identity"]["behavior_equal"])
        self.assertEqual(proof["tolerance"], 1e-4)
        # Independent layers would make this negative control vacuous.
        correct, _, _ = D.capture_write(H, hp, base, P, H.original, synthetic_prepared(H, mapping), mapping, wrapper=True)
        original_groups = R.groups
        with patch.object(R, "groups", side_effect=lambda m, ss: list(reversed(original_groups(m, ss)))):
            wrong, _, _ = D.capture_write(H, hp, base, P, H.original, synthetic_prepared(H, mapping), mapping, wrapper=True)
        self.assertGreater(max(D.relative_distances(correct, wrong).values()), proof["tolerance"])
        one = prepared["requests"][:1]; s = SUBJECTS[0]
        restricted = {"requests": one, "targets": {(s, one[0]["target_new"]["str"]): prepared["targets"][(s, one[0]["target_new"]["str"])]}}
        good, _, _ = D.capture_write(H, hp, base, P, H.original, restricted, {s: 8}, wrapper=True)
        badP = list(P); badP[4] = P[1]
        bad, _, _ = D.capture_write(H, hp, base, badP, H.original, restricted, {s: 8}, wrapper=True)
        self.assertGreater(D.relative_distances({8: good[8]}, {8: bad[8]})["8"], 1e-4)

    def test_original_capture_requires_one_override_hit_and_restores(self):
        for hits in (0, 1, 2):
            with self.subTest(hits=hits):
                H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS)); base = H.snap_layers(hp)
                prepared = synthetic_prepared(H); H.calls.clear()
                if hits == 0: prepared["targets"].pop(next(iter(prepared["targets"])))
                previous = {"saved": array([1])}; H.Z_OVERRIDE = previous
                def original(hp, requests, P, cache):
                    result = H.original(hp, requests, P, cache)
                    if hits == 2: result = H.original(hp, requests, P, cache)
                    return result
                def capture(): return D.capture_write(H, hp, base, [np.eye(3)] * 5, original, prepared, None)
                if hits == 1:
                    capture()
                else:
                    with self.assertRaisesRegex(R.GateError, "LAW5_OVERRIDE_PIN"): capture()
                self.assertEqual(H.Z_OVERRIDE_HITS, hits)
                self.assertIs(H.Z_OVERRIDE, previous)
                self.assertEqual(any(c[0] == "target" for c in H.calls), hits == 0)
                for l in R.LAYERS: np.testing.assert_array_equal(H.weights[l], base[l])

    def test_law5_singleton_and_multigroup_reject_any_unassigned_write(self):
        original_call = D.GroupedEdit.__call__
        for scope, gate in (("singleton", "LAW5_IV_SCOPE"), ("multigroup", "LAW5_V_SCOPE")):
            for change in (0.0, 1e-12, -1e-12):
                with self.subTest(scope=scope, change=change):
                    H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS)); base = H.snap_layers(hp)
                    prepared = synthetic_prepared(H); P = [np.eye(3)] * 5
                    def leaky(wrapper, hp, requests, P, cache):
                        result = original_call(wrapper, hp, requests, P, cache)
                        mapping = wrapper.layer_map
                        matches = mapping is not None and (len(mapping) == 1 if scope == "singleton" else 1 < len(mapping) < 24)
                        if matches:
                            untouched = next(l for l in R.LAYERS if l not in mapping.values())
                            H.weights[untouched][0, 0] += change
                        return result
                    with patch.object(D.GroupedEdit, "__call__", leaky):
                        def check(): return D.law5_checks(H, hp, P, base, {R.ARMS[2]: prepared}, step_fixture()["map"])
                        if change == 0:
                            self.assertTrue(check()["ok"])
                        else:
                            with self.assertRaisesRegex(R.GateError, gate): check()
                    for l in R.LAYERS: np.testing.assert_array_equal(H.weights[l], base[l])

    def test_proxy_uses_own_pristine_denominators_and_fp16_qualifier(self):
        H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS), layer_module_tmp="block{}", fact_token="subject_last"); prepared = synthetic_prepared(H)
        prepared.update(map={s: 8 for s in SUBJECTS}, pre=D.activation_rows(H, hp, {s: 8 for s in SUBJECTS}),
                        predictions={s: {"full_G_diagonal": 0.2, "group_G_diagonal": 0.3} for s in SUBJECTS}, targets_sha256="a" * 64)
        H.weights[8][0, 0] = 0.5
        read = D.proxy_readout(H, hp, prepared)
        row = read["rows"][0]; z = np.asarray(prepared["targets"][(SUBJECTS[0], prepared["requests"][0]["target_new"]["str"])])
        for j, template in enumerate([H.CANON] + H.PTEST):
            expected = np.linalg.norm(z - H.cur(8, SUBJECTS[0], template)) / np.linalg.norm(z - prepared["pre"][SUBJECTS[0]][j])
            self.assertAlmostEqual(row["rho_per_prompt"][j], expected, places=6)
        self.assertNotEqual(row["pristine_residual_norms"][0], row["pristine_residual_norms"][1])
        self.assertEqual(read["weight_application"], "fp16")

    def test_frame_membership_and_relation_labels(self):
        H = SimpleNamespace(first_tok=lambda v: 5, predict=lambda p: {"id": 5}, CANON="Canon {}", FICTION=SUBJECTS)
        self.assertEqual(D.frame_probe(H, {"S": "value"})["flips"], 6)
        self.assertEqual(set(D.relation_probe(H)), {"bystander", "objective-anchored"})


class ThresholdTests(unittest.TestCase):
    def test_complete_fixture_and_per_template_edge_reading(self):
        rec = pass_fixture()
        self.assertEqual(R.pass_validity(rec, "B"), [])
        reading = R.read_run(rec)["readings"]["B"]
        self.assertEqual(reading["label"], "LEAD-NOT-REPLICATED")
        self.assertEqual(sum(reading["per_template"]), 30)
        self.assertEqual(sum(reading["per_edge_3of3"]), 10)
        self.assertEqual(sum(r["para_full"] for r in reading["by_layer"].values()), 30)

    def test_count_and_gain_boundaries(self):
        for n, baseline, expected in ((18, 5, "NULL"), (19, 10, "NULL"), (19, 9, "PARTIAL"),
                                     (19, 8, "PARTIAL"), (29, 18, "PARTIAL"), (30, 18, "LEAD"), (31, 18, "LEAD"),
                                     (27, 18, "NULL"), (28, 18, "PARTIAL"), (29, 18, "PARTIAL")):
            with self.subTest(n=n, baseline=baseline):
                self.assertEqual(R.candidate_reading(pass_fixture(b=n, baseline=baseline), "B")["base_label"], expected)
        for n in range(5, 19):
            self.assertEqual(R.candidate_reading(pass_fixture(b=n, baseline=5), "B")["base_label"], "NULL")

    def test_controls_and_baseline_envelope_boundaries(self):
        for name in R.RECIPES:
            for control in R.ARMS[:2]:
                for n in (67, 68, 69):
                    rec = pass_fixture(); set_score(rec, name, control, n)
                    self.assertEqual(not R.pass_validity(rec, name), n >= 68, (name, control, n))
                    if name == "A":
                        self.assertEqual(R.candidate_reading(rec, "B")["base_label"] == "INVALID", n < 68, (control, n))
        for n in (4, 5, 6, 17, 18, 19):
            rec = pass_fixture(baseline=n)
            self.assertEqual(not R.pass_validity(rec, "B"), 5 <= n <= 18)
        for n in (4, 5, 6, 9, 10, 11):
            rec = pass_fixture(); set_score(rec, "A", R.ARMS[2], 10, canon=n)
            self.assertEqual(not R.pass_validity(rec, "B"), 5 <= n <= 10)

    def test_each_locality_threshold_inside_at_outside(self):
        cases = [("L1", (0, 1, 2)), ("frame", (0, 1, 2)), ("desc", (94.0001, 94, 93.9999)),
                 ("L3", (30, 29, 28)), ("ppl", (20.4999, 20.5, 20.5001))]
        for key, values in cases:
            for i, value in enumerate(values):
                rec = pass_fixture(); arm = rec["recipes"]["B"]["arms"][R.ARMS[2]]
                if key == "L1": arm["locality_axes"]["L1_flipped_to_edited_value"] = value
                if key == "frame":
                    arm["extra"]["same_frame"]["flips"] = value
                    for j, row in enumerate(arm["extra"]["same_frame"]["rows"]): row.update(top1=10 if j < value else 999, flip=j < value)
                if key == "desc": arm["locality_described_as"] = value
                if key == "L3": arm["locality_axes"]["L3_top1_agree"] = value
                if key == "ppl": arm["locality_axes"]["generic_ppl_post"] = value
                self.assertEqual(R.candidate_reading(rec, "B")["base_label"], "LEAD" if i < 2 else "TRADEOFF", (key, value))

    def test_write_ratio_and_relation_report_only(self):
        for ratio in (1.4999, 1.5, 1.5001):
            rec = pass_fixture()
            for v in rec["recipes"]["B"]["delta_norms"][R.ARMS[2]].values(): v["delta_norm"] *= ratio
            reading = R.candidate_reading(rec, "B")
            self.assertEqual(reading["base_label"], "LEAD" if ratio <= 1.5 else "TRADEOFF")
            self.assertEqual("LARGE-WRITE" in reading["label"], ratio > 1.5)
        rec = pass_fixture(b=18)
        for v in rec["recipes"]["B"]["delta_norms"][R.ARMS[2]].values(): v["delta_norm"] *= 2
        self.assertTrue(R.candidate_reading(rec, "B")["label"].startswith("NULL-LARGE-WRITE"))
        rec = pass_fixture()
        for v in rec["recipes"]["B"]["arms"][R.ARMS[2]]["extra"]["relation_labels"].values(): v.update(flips=24, post_top1=[6] * 24)
        self.assertEqual(R.candidate_reading(rec, "B")["base_label"], "LEAD")

    def test_attribution_9_10_11_against_each_control(self):
        for control in ("B0", "Bshuf"):
            for margin in (9, 10, 11):
                rec = pass_fixture(b=30, b0=19, bshuf=19); set_score(rec, control, R.ARMS[2], 30 - margin)
                self.assertEqual(R.candidate_reading(rec, "B")["attributed"], margin >= 10)
        rec = pass_fixture(); set_score(rec, "Bshuf", R.ARMS[0], 67)
        self.assertFalse(R.candidate_reading(rec, "B")["attributed"])

    def test_replication_rules_fresh_context_fixed_map_and_loss_of_attribution(self):
        first = pass_fixture(); second = pass_fixture(pid=200)
        self.assertTrue(R.read_run(first, second)["readings"]["B"]["gate_A"])
        second["pid"] = first["pid"]
        self.assertIn("NOT-REPLICATED", R.read_run(first, second)["readings"]["B"]["label"])
        second = pass_fixture(b=29, pid=200)
        self.assertIn("NOT-REPLICATED", R.read_run(first, second)["readings"]["B"]["label"])
        first = pass_fixture(b=29, b0=19, bshuf=19)
        second = pass_fixture(pid=200)
        self.assertTrue(R.read_run(first, second)["readings"]["B"]["gate_A"])
        for control in ("B0", "Bshuf"):
            second = pass_fixture(pid=200); set_score(second, control, R.ARMS[2], 21)
            self.assertFalse(R.read_run(pass_fixture(), second)["readings"]["B"]["gate_A"])
        second = pass_fixture(pid=200)
        newstep = step_fixture(); table = [[0, 0, 0, 0, 1] for _ in SUBJECTS]
        newstep.update(R.select_maps(table, table, SUBJECTS)); newstep["ctx"] = [["{}"], ["Different. {}"]]
        newstep["ctx_sha256"] = R.json_digest(newstep["ctx"])
        second.update(step0=newstep, ctx=newstep["ctx"], ctx_sha256=newstep["ctx_sha256"])
        for recipe in R.RECIPES:
            for arm in R.ARMS:
                predictions = second["recipes"][recipe]["predictions_before_write"][arm]
                for i, s in enumerate(SUBJECTS):
                    layer = 8 if recipe == "A" else second["recipes"][recipe]["map"][s]
                    predictions[s]["full_G_diagonal"] = table[i][layer - 4]
                if arm != R.ARMS[1]:
                    for row in second["recipes"][recipe]["arms"][arm]["extra"]["proxy"]["rows"]:
                        row["full_G_diagonal"] = predictions[row["subj"]]["full_G_diagonal"]
        self.assertEqual(R.pass_validity(second, "B"), [])
        self.assertTrue(R.read_run(pass_fixture(), second)["readings"]["B"]["gate_A"])
        # Losing locality, count, controls, write-size, sources, map or ctx cannot replicate.
        for kind in ("L3", "count", "controls", "size", "source", "map", "ctx"):
            second = pass_fixture(pid=200)
            if kind == "L3": second["recipes"]["B"]["arms"][R.ARMS[2]]["locality_axes"]["L3_top1_agree"] = 28
            if kind == "count": set_score(second, "B", R.ARMS[2], 18)
            if kind == "controls": set_score(second, "B", R.ARMS[0], 67)
            if kind == "size":
                for v in second["recipes"]["B"]["delta_norms"][R.ARMS[2]].values(): v["delta_norm"] *= 2
            if kind == "source": second["identity"]["run_id"] = "other"
            if kind == "map": second["published_map"] = {s: 8 for s in SUBJECTS}
            if kind == "ctx": del second["ctx_sha256"]
            reading = R.read_run(pass_fixture(), second)["readings"]["B"]
            self.assertFalse(reading["gate_A"], kind)
            self.assertIn("NOT-REPLICATED", reading["label"], kind)

    def test_replication_schedule_and_never_adopt_shuffled(self):
        self.assertTrue(R.replication_needed(pass_fixture(b=30, b0=21)))  # unattributed B still follows literal §2:60
        self.assertTrue(R.replication_needed(pass_fixture(b=18, b0=30)))
        self.assertFalse(R.replication_needed(pass_fixture(b=18, b0=18, bshuf=40)))
        self.assertFalse(R.read_run(pass_fixture(), pass_fixture(pid=200))["readings"]["Bshuf"]["gate_A"])

    def test_law5_strict_thresholds_floor_and_relative_tolerance(self):
        for key, values in (("expr_delta", (0.04999, 0.05, 0.05001)), ("loc_delta", (2.9999, 3, 3.0001))):
            for i, v in enumerate(values):
                proof = proof_fixture(); proof["standing"][key] = v
                if i == 0: R.law5_reading(proof)
                else:
                    with self.assertRaisesRegex(R.GateError, "LAW5_I"): R.law5_reading(proof)
        for floor, tolerance in ((0, 1e-4), (0.000005, 1e-4), (0.0001, 0.001)):
            proof = proof_fixture(); proof["floor"]["relative_max"] = floor; proof["tolerance"] = tolerance
            proof["floor"]["relative_by_layer"] = {str(l): floor for l in R.LAYERS}
            for part, gate in (("identity", "LAW5_III"), ("singleton", "LAW5_IV"), ("multigroup", "LAW5_V")):
                for v, valid in ((tolerance * 0.999, True), (tolerance, True), (tolerance * 1.001, False)):
                    p = copy.deepcopy(proof); first = next(iter(p[part]["relative_by_layer"])); p[part]["relative_by_layer"][first] = v
                    if valid: R.law5_reading(p)
                    else:
                        with self.assertRaisesRegex(R.GateError, gate): R.law5_reading(p)
        proof = proof_fixture(); proof["floor"]["behavior_count_deltas"]["para_full_n"] = 2; proof["identity"]["behavior_equal"] = False
        with self.assertRaisesRegex(R.GateError, "LAW5_III"): R.law5_reading(proof)


class SafetyAndPersistenceTests(unittest.TestCase):
    def test_bshuf_control_only_labels_roundtrip_and_invalid_exit(self):
        cases = ((18, False, False, "NULL"), (20, False, False, "PARTIAL"),
                 (30, False, False, "LEAD"), (30, True, False, "TRADEOFF-LARGE-WRITE"),
                 (30, False, True, "INVALID"))
        for n, large, invalid, label in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                record = pass_fixture(b=18, b0=18, bshuf=n)
                if large:
                    for v in record["recipes"]["Bshuf"]["delta_norms"][R.ARMS[2]].values(): v["delta_norm"] *= 2
                if invalid: set_score(record, "Bshuf", R.ARMS[0], 67)
                root, out, _ = fixture_directory(tmp, records=[record])
                reading = R.read_directory(out, root)["readings"]["Bshuf"]
                self.assertEqual(reading["label"], label + "-CONTROL-ONLY")
                self.assertFalse(reading["gate_A"])
                self.assertFalse(R.replication_needed(record))
                printed = io.StringIO()
                with contextlib.redirect_stdout(printed): code = R.main([str(out), "--root", str(root)])
                self.assertEqual(code, 2 if invalid else 0)
                self.assertEqual(json.loads(printed.getvalue())["readings"]["Bshuf"]["label"], label + "-CONTROL-ONLY")

    def test_preflight_controls_reference_identity_roundtrip_and_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "outputs"; path = Path(tmp) / "passS.json"
            path.write_bytes((ROOT / "experiments/c10q/runs/c10q_stacked/passS.json").read_bytes())
            reference = D.law3_reference(path)
            identity = D.initialise_identity(ROOT, out, reference)
            persisted = json.loads((out / "identity.json").read_text())
            self.assertIn("preflight_controls_reference", persisted)
            self.assertNotIn("law3_reference", persisted)
            self.assertEqual(persisted["preflight_controls_reference"], reference)
            self.assertEqual(persisted, identity)
            R.validate_identity(persisted, pass_fixture()["fingerprint"])
            self.assertEqual(D.initialise_identity(ROOT, out, reference), persisted)
            path.write_bytes(path.read_bytes() + b"\n")
            self._assert_halt(lambda: D.assert_sources(persisted, ROOT), "LAW3_REFERENCE_DRIFT")

    def _run_synthetic_pass(self, root, out, candidate, fresh=None, stage="pass1", runtime_stage=None):
        runtime_stage = runtime_stage or D.runtime_stage
        identity = candidate["identity"]; fresh = fresh or step_fixture()
        covariance = pass_fixture()["recipes"]["A"]["cov_cache_sha256"]
        frozen = {**step_fixture(), "identity": identity, "cov_cache_sha256": covariance}
        D.write_json(out / "identity.json", identity); D.write_json(out / "step0.json", frozen)
        if stage == "pass2":
            previous = pass_fixture(pid=os.getpid() + 1)
            D.write_json(out / "pass1.json", previous)
            D.write_json(out / "pass1_complete.json", {"identity": identity, "record_sha256": D.sha256_file(out / "pass1.json")})
        for name, rec in candidate["recipes"].items():
            for arm in R.ARMS:
                predictions = rec["predictions_before_write"][arm]
                for i, s in enumerate(SUBJECTS):
                    layer = 8 if name == "A" else rec["map"][s]
                    predictions[s]["full_G_diagonal"] = fresh["G_table"][i][layer - 4]
                if arm != R.ARMS[1]:
                    for row in rec["arms"][arm]["extra"]["proxy"]["rows"]:
                        row["full_G_diagonal"] = predictions[row["subj"]]["full_G_diagonal"]
        H = SyntheticHarness(); H.ID, H.REV, H.DEV = "synthetic", "synthetic", "synthetic-cpu"
        hp = SimpleNamespace(layers=list(R.LAYERS))
        H.compute_P = lambda hp: [np.eye(3)] * 5; H.cov_cache_sha256 = lambda hp: covariance
        prepared = synthetic_prepared(H); prepared["pre"] = {s: np.zeros((4, 2)) for s in SUBJECTS}
        keys = {l: np.zeros((3, 24)) for l in R.LAYERS}
        def run_recipe(H, M, hp, P, ctx, keys, root, name, mapping, proof, preprepared=None):
            self.assertEqual(mapping, R.recipe_maps(frozen["map"], SUBJECTS)[name])
            return candidate["recipes"][name], {}
        with patch.object(D, "IDENTITY", identity), patch.object(D, "assert_sources"), \
             patch.object(D, "load_harness", return_value=(H, None, hp, fresh["ctx"])), \
             patch.object(D, "compute_selector", return_value=(fresh, keys)), \
             patch.object(D, "prepare_arm", return_value=prepared), patch.object(D, "law5_checks", return_value=proof_fixture()), \
             patch.object(D, "run_one_recipe", side_effect=run_recipe) as recipes, contextlib.redirect_stdout(io.StringIO()):
            runtime_stage(root, out, stage, candidate["fingerprint"])
        self.assertEqual([c.args[7] for c in recipes.call_args_list], ["A", "B0", "B", "Bshuf"])
        self.assertTrue((out / (stage + "_complete.json")).exists())
        self.assertFalse(list((root / "architecture_profile").glob("*.json")))
        return json.loads((out / (stage + ".json")).read_text())

    def test_real_stage_candidate_control_invalid_continues_and_roundtrips(self):
        for stage in ("pass1", "pass2"):
            for name in R.RECIPES[1:]:
                for arm in R.ARMS[:2]:
                    for n in (67, 68, 69):
                        with self.subTest(stage=stage, recipe=name, arm=arm, n=n), tempfile.TemporaryDirectory() as tmp:
                            candidate = pass_fixture(); set_score(candidate, name, arm, n)
                            record = self._run_synthetic_pass(Path(tmp), Path(tmp) / "outputs", candidate, stage=stage)
                            reasons = ["CONTROL_" + arm] if n < 68 else []
                            self.assertEqual(record["recipes"][name]["validity"], {"ok": n >= 68, "reasons": reasons})
                            readings = R.read_run(record)["readings"]
                            self.assertEqual(readings[name]["base_label"] == "INVALID", n < 68)
                            if name != "B": self.assertEqual(readings["B"]["base_label"], "LEAD")
                            self.assertEqual(readings["Bshuf"]["base_label"] == "INVALID", n < 68 and name == "Bshuf")

    def test_real_stage_candidate_full_string_invalid_continues_and_roundtrips(self):
        for stage in ("pass1", "pass2"):
            for string_n in (29, 30, 31):
                with self.subTest(stage=stage, string_n=string_n), tempfile.TemporaryDirectory() as tmp:
                    candidate = pass_fixture(); rec = candidate["recipes"]["B"]; arm = rec["arms"][R.ARMS[2]]
                    for i, row in enumerate(rec["detail"][R.ARMS[2]]):
                        row["para_string_hits"] = [i * 3 + j < string_n for j in range(3)]
                    arm.update(para_string_n=string_n, para_full_string=round(100 * string_n / 72, 1))
                    record = self._run_synthetic_pass(Path(tmp), Path(tmp) / "outputs", candidate, stage=stage)
                    reasons = ["FULL_STRING: A7_coined_coined"] if string_n != 30 else []
                    self.assertEqual(record["recipes"]["B"]["validity"], {"ok": string_n == 30, "reasons": reasons})
                    readings = R.read_run(record)["readings"]
                    self.assertEqual(readings["B"]["base_label"], "LEAD" if string_n == 30 else "INVALID")
                    self.assertNotEqual(readings["Bshuf"]["base_label"], "INVALID")

    def test_real_stage_candidate_invalid_does_not_mask_integrity_halt(self):
        runtime_stage = D.runtime_stage
        with tempfile.TemporaryDirectory() as tmp:
            candidate = pass_fixture(); set_score(candidate, "B0", R.ARMS[0], 67)
            candidate["recipes"]["B0"]["wrapper"][R.ARMS[2]]["z_override_hits"] = 0
            out = Path(tmp) / "outputs"
            self._assert_halt(lambda: self._run_synthetic_pass(Path(tmp), out, candidate, runtime_stage=runtime_stage), "OVERRIDE_GROUPS")
            self.assertFalse((out / "pass1.json").exists()); self.assertFalse((out / "pass1_complete.json").exists())

    def test_real_pass1_published_map_agreement_and_measured_delta_roundtrip(self):
        published = {s: 4 + i % 5 for i, s in enumerate(SUBJECTS)}
        for agreement in (0, 1, 23, 24):
            for delta in (0.0, 0.125):
                with self.subTest(agreement=agreement, delta=delta), tempfile.TemporaryDirectory() as tmp:
                    first = [[1 if j == (i % 5 if i < agreement else (i + 1) % 5) else 0
                              for j in range(5)] for i in range(24)]
                    second = copy.deepcopy(first); second[-1][4] += delta
                    fresh = step_fixture(); fresh.update(R.select_maps(first, second, SUBJECTS))
                    record = self._run_synthetic_pass(Path(tmp), Path(tmp) / "outputs", pass_fixture(), fresh=fresh)
                    self.assertEqual(record["published_map"], published)
                    self.assertEqual(record["recipes"]["B"]["map"], published)
                    self.assertEqual(record["selection_agreement_n"], agreement)
                    self.assertEqual(record["step0"]["delta"], delta)
                    self.assertEqual(R.pass_validity(record, "B"), [])

    def test_every_record_kind_json_normalised_roundtrip_and_exclusive(self):
        record = pass_fixture(); step = {**step_fixture(), "identity": record["identity"], "fingerprint": record["fingerprint"]}
        kinds = {"identity.json": record["identity"], "step0.json": step, "law5.json": {"identity": record["identity"], "law5": proof_fixture()},
                 "law5_pass2.json": {"identity": record["identity"], "law5": proof_fixture()}, "pass1.json": record,
                 "pass2.json": pass_fixture(pid=200), "run.json": R.read_run(record, pass_fixture(pid=200))}
        for stage in ("pass1", "pass2"):
            for kind in ("started", "complete"):
                kinds[stage + "_" + kind + ".json"] = {"identity": record["identity"], "pid": 100, "stage": stage, "record_sha256": "1" * 64}
        kinds["architecture_profile/c10v_layerpick_halt_diagnostic_test.json"] = {"identity": record["identity"], "reason": "test", "state": {"targets": ((1, 2), (3, 4))}}
        with tempfile.TemporaryDirectory() as tmp:
            for name, obj in kinds.items():
                with self.subTest(record=name):
                    obj = {"record": obj, "tuple_regression": ((1, 2), (3, (4, 5)))}
                    path = Path(tmp) / name; D.write_json(path, obj)
                    self.assertEqual(json.loads(path.read_text()), json.loads(json.dumps(obj)))
                    before = path.read_bytes()
                    with self.assertRaises(FileExistsError): D.write_json(path, {"overwrite": True})
                    self.assertEqual(path.read_bytes(), before)
            for status in ("concentrated map; candidate not advanced", "map not reproducible"):
                obj = {"label": status, "table": step["G_table"], "candidate_advanced": False}
                path = Path(tmp) / (R.json_digest(status) + ".json"); D.write_json(path, obj)
                self.assertEqual(json.loads(path.read_text()), obj)

    def test_json_nonfinite_corruption_and_each_io_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            for v in (float("nan"), float("inf"), float("-inf")):
                with self.assertRaises(ValueError): D.write_json(path, {"v": v})
                self.assertFalse(path.exists())
            with self.assertRaises(TypeError): D.write_json(path, {"bad": object()})
            with patch.object(Path, "open", side_effect=OSError("write denied")):
                with self.assertRaisesRegex(OSError, "write denied"): D.write_json(path, {})
            for error in (OSError("read denied"), None):
                target = Path(tmp) / ("read-denied.json" if error else "corrupt.json")
                with patch.object(Path, "read_text", side_effect=error, return_value="corrupt"):
                    with self.assertRaises((OSError, R.GateError)): D.write_json(target, {})
            original_loads = json.loads
            for second in (ValueError("parse error"), {"mismatch": True}):
                target = Path(tmp) / ("parse.json" if isinstance(second, Exception) else "mismatch.json")
                with patch.object(D.json, "loads", side_effect=[original_loads("{}"), second]):
                    with self.assertRaises(ValueError): D.write_json(target, {})

    def _assert_halt(self, trigger, reason):
        with tempfile.TemporaryDirectory() as tmp:
            real_halt = D.halt
            sentinel = Path(tmp) / "occupied.json"; sentinel.write_text("preserved")
            identity = identity_fixture()
            with patch.object(D, "preflight", return_value=pass_fixture()["fingerprint"]), \
                 patch.object(D, "law3_reference", return_value=identity["preflight_controls_reference"]), \
                 patch.object(D, "initialise_identity", return_value=identity), \
                 patch.object(D, "runtime_stage", side_effect=lambda *a: trigger()) as downstream, \
                 patch.object(D, "halt", side_effect=lambda root, msg, **state: real_halt(Path(tmp), msg, **state)):
                with self.assertRaisesRegex(SystemExit, "HALT"):
                    D.main(["pass1", "--root", str(ROOT), "--out-dir", str(ROOT / "experiments/c10v/runs/c10v_layerpick/synthetic_no_writes"),
                            "--law3-ref", "/synthetic/reference", "--operator-go", "--steps-1-3-complete", "--autoresearch-state", "paused"])
                downstream.assert_called_once()
            paths = list((Path(tmp) / "architecture_profile").glob("c10v_layerpick_halt_diagnostic_*.json"))
            self.assertEqual(len(paths), 1)
            diagnostic = json.loads(paths[0].read_text())
            self.assertIn(reason, diagnostic["reason"])
            self.assertFalse(list(Path(tmp).glob("*_started.json")))
            self.assertFalse(list(Path(tmp).glob("*_complete.json")))
            self.assertEqual(sentinel.read_text(), "preserved")

    def test_every_validity_gate_routes_to_halt_diagnostic(self):
        mutations = [
            ("FINGERPRINT", lambda r: r["fingerprint"].update(sha256="0" * 64)),
            ("FINGERPRINT", lambda r: r["fingerprint"].update(_cov_cpu=2)),
            ("FINGERPRINT", lambda r: r["fingerprint"].update(_cov_cpu=4)),
            ("SOURCE_IDENTITY", lambda r: r["identity"].update(source_digest="0" * 64)),
            ("LAW3_REFERENCE", lambda r: r["identity"]["preflight_controls_reference"].update(ok=False)),
            ("CONTEXT_HASH", lambda r: r["step0"].update(ctx_sha256="0" * 64)),
            ("CONTEXT_SHAPE", lambda r: (r["step0"].update(ctx=[["bad"]], ctx_sha256=R.json_digest([["bad"]])))),
            ("SELECTOR_TABLE", lambda r: r["step0"]["G_table"][0].__setitem__(0, float("nan"))),
            ("SELECTOR_RECOMPUTATION", lambda r: r["step0"].update(map_sha256="0" * 64)),
            ("PROJECTED_KEY_NORMS", lambda r: r["step0"]["projected_key_norms"][0].__setitem__(0, -1)),
            ("INSTALLED_SHARE", lambda r: r["step0"]["installed_share_comparison"][0].update(installed_share=float("inf"))),
            ("PUBLISHED_MAP_HASH", lambda r: r.update(published_map_sha256="0" * 64)),
            ("PASS_CONTEXT", lambda r: r.update(ctx_sha256="0" * 64)),
            ("RECIPE_INVENTORY", lambda r: r["recipes"].pop("Bshuf")),
            ("RECIPE_MAP", lambda r: r["recipes"]["B"].update(map={s: 8 for s in SUBJECTS})),
            ("RECIPE_LAW5", lambda r: r["recipes"]["B"]["law5_gate"].update(ok=False)),
            ("SUMMARY_COUNTS", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]].update(para_full_n=73)),
            ("OVERRIDE_GROUPS", lambda r: r["recipes"]["B"]["wrapper"][R.ARMS[2]].update(z_override_hits=4)),
            ("WRITE_NORMS", lambda r: next(iter(r["recipes"]["B"]["delta_norms"][R.ARMS[2]].values())).update(delta_norm=float("inf"))),
            ("LOCALITY_SHAPE", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]]["locality_axes"].update(L3_n=29)),
            ("RELATION_PROBES", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]]["extra"]["relation_labels"].pop("bystander")),
            ("FULL_READOUT", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]].pop("tf_pertok_cont")),
            ("PROXY_READOUT", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]]["extra"]["proxy"]["rows"].pop()),
            ("PROXY_VALUES", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]]["extra"]["proxy"]["rows"][0].update(realised_fraction=float("inf"))),
            ("PROXY_PREDICTIONS", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]]["extra"]["proxy"]["rows"][0].update(pristine_residual_norms=[0] * 4)),
            ("PROXY_PROVENANCE", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]]["extra"]["proxy"].update(targets_sha256="0" * 64)),
            ("PRISTINE_PREDICTIONS", lambda r: r["recipes"]["B"]["targets_sha256"].update(A7_coined_coined="bad")),
            ("TARGET_IDS", lambda r: r["recipes"]["B"]["target_ids"][R.ARMS[2]].update(S0=[])),
            ("FRAME_PROBE", lambda r: r["recipes"]["B"]["arms"][R.ARMS[2]]["extra"]["same_frame"]["rows"][0].update(flip=True)),
            ("TF_COUNTS", lambda r: r["recipes"]["B"]["detail"][R.ARMS[2]][0].update(tf_correct=4)),
            ("COVARIANCE_PROVENANCE", lambda r: r["recipes"]["B"]["cov_cache_sha256"].pop("4")),
            ("COVARIANCE_DRIFT", lambda r: r["recipes"]["B"]["cov_cache_sha256"]["4"].update(sha256="0" * 64)),
            ("HSIC_READOUT", lambda r: r.pop("hsic")),
            ("BASELINE_ENVELOPE", lambda r: set_score(r, "A", R.ARMS[2], 19)),
            ("ZERO_BASELINE_WRITE", lambda r: [v.update(delta_norm=0) for v in r["recipes"]["A"]["delta_norms"][R.ARMS[2]].values()]),
            ("ROW_SUBJECTS", lambda r: r["recipes"]["B"]["detail"][R.ARMS[2]][0].update(subj=SUBJECTS[1])),
            ("CANON_HITS", lambda r: r["recipes"]["B"]["detail"][R.ARMS[2]][0].update(canon_full=1)),
            ("PARA_HITS", lambda r: r["recipes"]["B"]["detail"][R.ARMS[2]][0].update(para_full_hits=[True])),
            ("FULL_FIRST_CONSISTENCY", lambda r: r["recipes"]["B"]["detail"][R.ARMS[2]][0].update(para_first_hits=[False] * 3)),
        ]
        for gate, mutate in mutations:
            with self.subTest(gate=gate):
                rec = pass_fixture(); mutate(rec)
                def trigger(rec=rec, gate=gate):
                    reasons = R.pass_validity(rec, "B")
                    self.assertTrue(reasons, gate)
                    self.assertIn(gate, reasons[0])
                    raise R.GateError(reasons[0])
                self._assert_halt(trigger, gate)
                self.assertEqual(R.candidate_reading(rec, "B")["label"], "INVALID")
        def nonreproducible():
            rec = pass_fixture(); first = [[0.5, 0.5, 0, 0, 0] for _ in SUBJECTS]; second = copy.deepcopy(first); second[0][0] += 0.125
            rec["step0"].update(R.select_maps(first, second, SUBJECTS))
            reasons = R.pass_validity(rec, "B"); self.assertIn("MAP_REPRODUCIBLE", reasons[0]); raise R.GateError(reasons[0])
        self._assert_halt(nonreproducible, "MAP_REPRODUCIBLE")
        for part, gate in (("standing", "LAW5_I"), ("floor", "LAW5_II"), ("identity", "LAW5_III"),
                           ("singleton", "LAW5_IV"), ("multigroup", "LAW5_V")):
            proof = proof_fixture()
            if part == "standing": proof[part]["expr_delta"] = 0.05
            elif part == "floor": proof[part]["relative_max"] = -1
            else: proof[part]["relative_by_layer"][next(iter(proof[part]["relative_by_layer"]))] = 0.01
            self._assert_halt(lambda proof=proof: R.law5_reading(proof), gate)

    def test_preflight_gate_halts_and_never_loads_harness(self):
        preflight = D.preflight
        baseargs = SimpleNamespace(operator_go=True, steps_1_3_complete=True, autoresearch_state="paused")
        for field, value, gate in (("operator_go", False, "OPERATOR_GO"), ("steps_1_3_complete", False, "SEQUENCE_STEPS_1_3"),
                                   ("autoresearch_state", "running", "AUTORESEARCH_WINDOW")):
            args = copy.copy(baseargs); setattr(args, field, value)
            self._assert_halt(lambda args=args: preflight(ROOT, args), gate)
        with patch.dict(os.environ, {}, clear=True):
            for knob in D.HARNESS_KNOBS:
                with patch.dict(os.environ, {knob: "inherited"}):
                    self._assert_halt(lambda: preflight(ROOT, baseargs), "INHERITED_HARNESS_KNOBS")
            for result in (SimpleNamespace(returncode=1, stdout="FAIL", stderr="diagnostic"),
                           SimpleNamespace(returncode=0, stdout="", stderr=""),
                           SimpleNamespace(returncode=0, stdout="wrong output", stderr="")):
                with patch.object(D.subprocess, "run", return_value=result):
                    self._assert_halt(lambda: preflight(ROOT, baseargs), "FINGERPRINT_COMMAND")

    def test_occupied_dangling_symlink_bad_maps_and_wrapper_keys_halt(self):
        with tempfile.TemporaryDirectory() as tmp:
            occupied = Path(tmp) / "step0.json"; occupied.symlink_to(Path(tmp) / "missing")
            self._assert_halt(lambda: D.occupied(Path(tmp), ["step0.json"]), "OCCUPIED_OUTPUTS")
        self._assert_halt(lambda: R.groups({}, SUBJECTS), "MAP_SUBJECTS")
        self._assert_halt(lambda: R.groups({s: 9 for s in SUBJECTS}, SUBJECTS), "MAP_LAYERS")
        H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS)); prepared = synthetic_prepared(H)
        prepared["targets"].pop(next(iter(prepared["targets"])))
        self._assert_halt(lambda: D.GroupedEdit(H, H.original, {"audit": prepared}, None)(hp, prepared["requests"], [np.eye(3)] * 5, []), "OVERRIDE_TARGET_KEYS")
        self.assertFalse(any(c[0] == "write" for c in H.calls))

    def test_source_and_law3_identity_gates_halt(self):
        law3_reference = D.law3_reference
        identity = identity_fixture()
        with patch.object(D, "source_hashes", return_value={}):
            self._assert_halt(lambda: D.assert_sources(identity, ROOT), "SOURCE_DRIFT")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ref.json"
            baseline = pass_fixture()["recipes"]["A"]
            D.write_json(path, {"recipes": {"baseline": baseline}})
            self.assertTrue(D.law3_reference(path)["ok"])
            for control in R.ARMS[:2]:
                bad = copy.deepcopy(baseline); bad["arms"][control]["para_full_n"] = 67
                p = Path(tmp) / (control + ".json"); D.write_json(p, {"recipes": {"baseline": bad}})
                self._assert_halt(lambda p=p: law3_reference(p), "LAW3_REFERENCE_CONTROLS")
            p = Path(tmp) / "ambiguous.json"; D.write_json(p, {"recipes": {"a": baseline, "b": baseline}})
            self._assert_halt(lambda: law3_reference(p), "LAW3_RECIPE_AMBIGUOUS")
            other = copy.deepcopy(baseline); other["band"] = [8]
            p = Path(tmp) / "recipe.json"; D.write_json(p, {"recipes": {"baseline": other}})
            self._assert_halt(lambda: law3_reference(p), "LAW3_REFERENCE_RECIPE")

    def test_complete_persisted_chain_positive_control_and_every_chain_gate_halt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, out, _ = fixture_directory(tmp)
            self.assertEqual(R.read_directory(out, root)["readings"]["B"]["base_label"], "NULL")
        for filename, gate, mutate in (
            ("identity.json", "PERSISTED_IDENTITY", lambda d: d.update(run_id="other")),
            ("pass1_started.json", "START_GATE_RECORDS", lambda d: d.update(live_law3_ok=False)),
            ("law5.json", "START_GATE_RECORDS", lambda d: d.update(pid=999)),
            ("pass1_complete.json", "COMPLETE_MARKER", lambda d: d.update(record_sha256="0" * 64)),
            ("run.json", "TERMINAL_RECORD", lambda d: d.update(scope="wrong")),
            ("pass1.json", "STAGE_IDENTITY", lambda d: d.update(published_map={s: 8 for s in SUBJECTS})),
        ):
            with self.subTest(file=filename), tempfile.TemporaryDirectory() as tmp:
                root, out, _ = fixture_directory(tmp)
                path = out / filename; obj = json.loads(path.read_text()); mutate(obj)
                path.write_text(json.dumps(obj))  # Only synthetic temporary records are corrupted.
                self._assert_halt(lambda: R.read_directory(out, root), gate)
        with tempfile.TemporaryDirectory() as tmp:
            root, out, _ = fixture_directory(tmp)
            (root / R.HP_FILE).write_text("drift")
            self._assert_halt(lambda: R.read_directory(out, root), "CURRENT_SOURCE")
        for name in ("identity.json", "law5.json", "pass1_started.json", "pass1_complete.json", "run.json"):
            with self.subTest(missing=name), tempfile.TemporaryDirectory() as tmp:
                root, out, _ = fixture_directory(tmp); (out / name).unlink()
                self._assert_halt(lambda: R.read_directory(out, root), name)

    def test_stopped_output_no_law5_no_markers_and_pending_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, out, _ = fixture_directory(tmp, stopped=True)
            self.assertEqual(R.read_directory(out, root)["label"], "concentrated map; candidate not advanced")
            self.assertFalse((out / "law5.json").exists()); self.assertFalse(list(out.glob("*_started.json")))
        with tempfile.TemporaryDirectory() as tmp:
            root, out, records = fixture_directory(tmp, records=[pass_fixture()])
            self.assertIn("NOT-REPLICATED", R.read_directory(out, root)["readings"]["B"]["label"])
            D.write_json(out / "run.json", {})
            self._assert_halt(lambda: R.read_directory(out, root), "PREMATURE_TERMINAL_RECORD")
        with tempfile.TemporaryDirectory() as tmp:
            root, out, _ = fixture_directory(tmp, records=[pass_fixture(), pass_fixture(pid=200)])
            self.assertTrue(R.read_directory(out, root)["readings"]["B"]["gate_A"])

    def test_real_stage_order_law5_and_baseline_before_any_marker(self):
        runtime_stage = D.runtime_stage
        H = SyntheticHarness(); H.ID = "Qwen/Qwen2.5-3B"; H.REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"; H.DEV = "mps"
        hp = SimpleNamespace(layers=list(R.LAYERS), layer_module_tmp="block{}", fact_token="subject_last")
        P = [np.eye(3) for _ in R.LAYERS]
        covariance = pass_fixture()["recipes"]["A"]["cov_cache_sha256"]
        H.compute_P = lambda hp: P; H.cov_cache_sha256 = lambda hp: covariance
        M = SimpleNamespace(sha256_tensor=lambda t: hashlib.sha256(np.asarray(t).tobytes()).hexdigest())
        with tempfile.TemporaryDirectory() as tmp:
            root, out = Path(tmp), Path(tmp) / "outputs"
            identity = identity_fixture(); D.IDENTITY = identity
            frozen = {**step_fixture(), "identity": identity, "cov_cache_sha256": covariance}
            D.write_json(out / "step0.json", frozen)
            keys = {l: np.stack([H.key(l, s) for s in SUBJECTS], axis=1) for l in R.LAYERS}
            common = [patch.object(D, "load_harness", return_value=(H, M, hp, frozen["ctx"])),
                      patch.object(D, "compute_selector", return_value=(step_fixture(), keys)), patch.object(D, "assert_sources")]
            with contextlib.ExitStack() as stack:
                for p in common: stack.enter_context(p)
                with patch.object(D, "law5_checks", side_effect=R.GateError("LAW5_I")), patch.object(D, "run_one_recipe") as recipes:
                    self._assert_halt(lambda: runtime_stage(root, out, "pass1", pass_fixture()["fingerprint"]), "LAW5_I")
                    recipes.assert_not_called()
                self.assertFalse(list(out.glob("*_started.json")))
                for arm, gate in ((R.ARMS[0], "LIVE_LAW3: CONTROL_A1_single"), (R.ARMS[1], "LIVE_LAW3: CONTROL_A2_coherent2"),
                                  (R.ARMS[2], "LIVE_LAW3: FULL_STRING: A7_coined_coined")):
                    rec = pass_fixture()
                    if arm == R.ARMS[2]: rec["recipes"]["A"]["arms"][arm].update(para_full_string=0.0)
                    else: set_score(rec, "A", arm, 67)
                    baseline = rec["recipes"]["A"]
                    with patch.object(D, "law5_checks", return_value=proof_fixture()), patch.object(D, "run_one_recipe", return_value=(baseline, {})) as recipes:
                        self._assert_halt(lambda: runtime_stage(root, out, "pass1", pass_fixture()["fingerprint"]), gate)
                        recipes.assert_called_once()
                    (out / "law5.json").unlink()
                self.assertFalse(list(out.glob("*_started.json")))
                self.assertFalse(list(out.glob("*_complete.json")))

    def test_real_stage_each_law5_failure_suppresses_recipes_and_markers(self):
        runtime_stage = D.runtime_stage
        for gate in ("LAW5_I", "LAW5_II", "LAW5_III", "LAW5_IV", "LAW5_V"):
            with self.subTest(gate=gate), tempfile.TemporaryDirectory() as tmp:
                root, out = Path(tmp), Path(tmp) / "outputs"
                identity = identity_fixture(); frozen = {**step_fixture(), "identity": identity,
                    "cov_cache_sha256": pass_fixture()["recipes"]["A"]["cov_cache_sha256"]}
                D.write_json(out / "step0.json", frozen)
                H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS))
                H.compute_P = lambda hp: [np.eye(3)] * 5; H.cov_cache_sha256 = lambda hp: frozen["cov_cache_sha256"]
                with patch.object(D, "load_harness", return_value=(H, None, hp, frozen["ctx"])), \
                     patch.object(D, "compute_selector", return_value=(step_fixture(), {})), patch.object(D, "assert_sources"), \
                     patch.object(D, "prepare_arm", return_value={}), \
                     patch.object(D, "law5_checks", side_effect=R.GateError(gate)), patch.object(D, "run_one_recipe") as recipes:
                    self._assert_halt(lambda: runtime_stage(root, out, "pass1", pass_fixture()["fingerprint"]), gate)
                    recipes.assert_not_called()
                self.assertFalse(list(out.glob("*_started.json"))); self.assertFalse(list(out.glob("*_complete.json")))

    def test_real_stage_dependency_selector_and_source_halts(self):
        runtime_stage = D.runtime_stage
        gates = ("STEP0_NOT_READY", "PASS1_COMPLETE", "REPLICATION_NOT_NEEDED", "REPLICATION_PROCESS",
                 "MAP_REPRODUCIBLE", "SOURCE_DRIFT")
        for gate in gates:
            with self.subTest(gate=gate), tempfile.TemporaryDirectory() as tmp:
                root, out = Path(tmp), Path(tmp) / "outputs"
                identity = identity_fixture(); covariance = pass_fixture()["recipes"]["A"]["cov_cache_sha256"]
                frozen = {**step_fixture(), "identity": identity, "cov_cache_sha256": covariance}
                if gate == "STEP0_NOT_READY":
                    t = [[0, 0, 0, 0, 1] for _ in SUBJECTS]; frozen.update(R.select_maps(t, t, SUBJECTS))
                D.write_json(out / "step0.json", frozen)
                stage = "pass2" if gate in ("PASS1_COMPLETE", "REPLICATION_NOT_NEEDED", "REPLICATION_PROCESS") else "pass1"
                previous = pass_fixture(b=18, b0=18, bshuf=18) if gate == "REPLICATION_NOT_NEEDED" else pass_fixture()
                if gate == "REPLICATION_PROCESS": previous["pid"] = os.getpid()
                if stage == "pass2":
                    D.write_json(out / "pass1.json", previous)
                    D.write_json(out / "pass1_complete.json", {"identity": identity,
                        "record_sha256": "0" * 64 if gate == "PASS1_COMPLETE" else D.sha256_file(out / "pass1.json")})
                fresh = step_fixture()
                if gate == "MAP_REPRODUCIBLE":
                    a = [[0.5, 0.5, 0, 0, 0] for _ in SUBJECTS]; b = copy.deepcopy(a); b[0][0] += 0.125
                    fresh.update(R.select_maps(a, b, SUBJECTS))
                H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS))
                H.compute_P = lambda hp: [np.eye(3)] * 5; H.cov_cache_sha256 = lambda hp: covariance
                candidate = pass_fixture()
                def run_recipe(H, M, hp, P, ctx, keys, root, name, mapping, proof, preprepared=None):
                    return candidate["recipes"][name], {}
                with patch.object(D, "load_harness", return_value=(H, None, hp, frozen["ctx"])) as loader, \
                     patch.object(D, "compute_selector", return_value=(fresh, {})), \
                     patch.object(D, "assert_sources", side_effect=R.GateError("SOURCE_DRIFT") if gate == "SOURCE_DRIFT" else None), \
                     patch.object(D, "prepare_arm", return_value={}), patch.object(D, "law5_checks", return_value=proof_fixture()), \
                     patch.object(D, "run_one_recipe", side_effect=run_recipe) as recipes:
                    self._assert_halt(lambda: runtime_stage(root, out, stage, pass_fixture()["fingerprint"]), gate)
                    if gate in gates[:4]: loader.assert_not_called()
                    recipes.assert_not_called()
                self.assertFalse((out / (stage + "_started.json")).exists())
                self.assertFalse((out / (stage + "_complete.json")).exists())

    def test_law5_layer_coverage_and_missing_floor_observations(self):
        for mutate, gate in ((lambda p: p["floor"].update(behavior_count_deltas={}), "LAW5_II"),
                             (lambda p: p["floor"]["relative_by_layer"].pop("4"), "LAW5_II"),
                             (lambda p: p["identity"]["relative_by_layer"].pop("4"), "LAW5_III"),
                             (lambda p: p["singleton"].update(projector_indices=[0]), "LAW5_IV"),
                             (lambda p: p["multigroup"]["groups"][0].update(subjects=["wrong"]), "LAW5_V")):
            proof = proof_fixture(); mutate(proof)
            self._assert_halt(lambda: R.law5_reading(proof, step_fixture()["map"], SUBJECTS), gate)

    def test_real_step0_stops_publish_table_without_law5_or_markers(self):
        for repeatable in (True, False):
            with self.subTest(repeatable=repeatable), tempfile.TemporaryDirectory() as tmp:
                root, out = Path(tmp), Path(tmp) / "outputs"
                first = [[0, 0, 0, 0, 1] for _ in SUBJECTS] if repeatable else [[0.5, 0.5, 0, 0, 0] for _ in SUBJECTS]
                second = copy.deepcopy(first)
                if not repeatable: second[0][0] += 0.125
                step = step_fixture(); step.update(R.select_maps(first, second, SUBJECTS))
                H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS))
                H.compute_P = lambda hp: [np.eye(3)] * 5
                H.cov_cache_sha256 = lambda hp: pass_fixture()["recipes"]["A"]["cov_cache_sha256"]
                with patch.object(D, "IDENTITY", identity_fixture()), \
                     patch.object(D, "load_harness", return_value=(H, None, hp, step["ctx"])), \
                     patch.object(D, "compute_selector", return_value=(step, {})), patch.object(D, "assert_sources"), \
                     patch.object(D, "law5_checks") as law5, patch.object(D, "run_one_recipe") as recipes, \
                     contextlib.redirect_stdout(io.StringIO()):
                    D.runtime_stage(root, out, "step0", pass_fixture()["fingerprint"])
                    law5.assert_not_called(); recipes.assert_not_called()
                persisted = json.loads((out / "step0.json").read_text())
                self.assertEqual(persisted["G_table"], first)
                self.assertEqual(json.loads((out / "run.json").read_text())["label"], step["status"])
                self.assertFalse((out / "law5.json").exists())
                self.assertFalse(list(out.glob("*_started.json"))); self.assertFalse(list(out.glob("*_complete.json")))

    def test_real_pass2_runs_published_map_despite_concentrated_reselection(self):
        runtime_stage = D.runtime_stage
        with tempfile.TemporaryDirectory() as tmp:
            root, out = Path(tmp), Path(tmp) / "outputs"
            identity = identity_fixture(); previous = pass_fixture()
            covariance = previous["recipes"]["A"]["cov_cache_sha256"]
            frozen = {**step_fixture(), "identity": identity, "cov_cache_sha256": covariance}
            D.write_json(out / "step0.json", frozen); D.write_json(out / "pass1.json", previous)
            D.write_json(out / "pass1_complete.json", {"identity": identity, "record_sha256": D.sha256_file(out / "pass1.json")})
            fresh = step_fixture(); table = [[0, 0, 0, 0, 1] for _ in SUBJECTS]
            fresh.update(R.select_maps(table, table, SUBJECTS))
            H = SyntheticHarness(); hp = SimpleNamespace(layers=list(R.LAYERS))
            H.compute_P = lambda hp: [np.eye(3)] * 5; H.cov_cache_sha256 = lambda hp: covariance
            with patch.object(D, "load_harness", return_value=(H, None, hp, fresh["ctx"])), \
                 patch.object(D, "compute_selector", return_value=(fresh, {})), patch.object(D, "assert_sources"), \
                 patch.object(D, "prepare_arm", return_value={}), patch.object(D, "law5_checks", return_value=proof_fixture()) as law5, \
                 patch.object(R, "validate_recipe"), patch.object(R, "recipe_integrity"), \
                 patch.object(D, "run_one_recipe", side_effect=[(previous["recipes"]["A"], {}), (previous["recipes"]["B0"], {}), R.GateError("SYNTHETIC_STOP_AFTER_B_MAP")]) as recipes:
                self._assert_halt(lambda: runtime_stage(root, out, "pass2", previous["fingerprint"]), "SYNTHETIC_STOP_AFTER_B_MAP")
                self.assertEqual(law5.call_args.args[-1], frozen["map"])
                self.assertEqual([c.args[7] for c in recipes.call_args_list], ["A", "B0", "B"])
                self.assertEqual(recipes.call_args_list[-1].args[8], frozen["map"])
            self.assertTrue((out / "pass2_started.json").exists()); self.assertFalse((out / "pass2_complete.json").exists())

    def test_import_and_help_never_import_model_modules(self):
        self.assertFalse({"torch", "transformers", "tokenizers", "c10e_bandknob"} & set(sys.modules))
        for name in ("c10v_layerpick_arms.py", "c10v_layerpick_read.py"):
            result = subprocess.run([sys.executable, "-B", str(Path(__file__).parent / name), "--help"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0); self.assertIn("usage:", result.stdout)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    if result.wasSuccessful():
        print("C10V_LAYERPICK_SELFTEST_PASS: synthetic only; torch/transformers/tokenizers/model imports absent")
    sys.exit(0 if result.wasSuccessful() else 1)
