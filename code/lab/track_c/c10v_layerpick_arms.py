#!/usr/bin/env python3
"""D-C10v-layerpick v2 operator stages: step0, pass1 (including LAW#5), pass2.

Import/help are model-free. Runtime checks precede model loading; live LAW#5
and recipe A precede every started/complete marker. No existing file is written.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse, contextlib, copy, datetime, hashlib, importlib, io, json, subprocess, traceback, uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10v_layerpick_read as R

FRAME_SUBJECTS = ("Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist")
HARNESS_KNOBS = ("MODEL_ID", "MODEL_REV", "HP_CANDIDATE", "OUT", "CANDIDATE_NAME", "DECISION_ID", "PREREG", "RUN_LABEL",
                 "Z_OVERRIDE", "C10_PROJECTOR", "N_EDIT", "C10_SUBJECT_OFFSET", "C10_ARMS", "C10_KEY_LOCUS",
                 "C10_CTX_TEMPLATES", "C10_RECIPES", "MINT_ARM", "MINT_STEP0", "MINT_INITS", "MINT_N_SEED", "LAW3_REF", "LLMDB_DEVICE")
SOURCE_FILES = (*R.REQUIRED_SOURCES, "code/lab/track_c/c10l_mint_lib.py")
STAGE, IDENTITY, LAST_LOG = "not-started", None, ""


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    """c10u:45–54 corrected: compare parsed JSON to JSON-normalised objects."""
    path = Path(path)
    payload = json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    normalised = json.loads(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        f.write(payload)
    actual = path.read_text(encoding="utf-8")
    R.require(actual == payload and json.loads(actual) == normalised, "JSON_PERSISTENCE", path)


def occupied(out, names):
    R.require(not any(os.path.lexists(Path(out) / n) for n in names), "OCCUPIED_OUTPUTS", names)


def halt(root, reason, **state):
    path = Path(root) / "architecture_profile" / ("c10v_layerpick_halt_diagnostic_" + uuid.uuid4().hex + ".json")
    write_json(path, {"decision_id": R.DECISION_ID, "stage": STAGE, "when_utc": utc_now(),
                      "identity": IDENTITY, "reason": str(reason), "state": state, "last_solve_stdout": LAST_LOG})
    raise SystemExit("HALT: " + str(reason) + "; diagnostic: " + str(path))


@contextlib.contextmanager
def quiet():
    global LAST_LOG
    sink = io.StringIO()
    try:
        with contextlib.redirect_stdout(sink):
            yield
    finally:
        LAST_LOG = sink.getvalue()


def source_hashes(root):
    root = Path(root)
    engine = sorted(str(p.relative_to(root)) for p in (root / "code/memit/vendor").rglob("*.py"))
    R.require(engine, "SOURCE_INVENTORY")
    return {n: sha256_file(root / n) for n in sorted(set(SOURCE_FILES) | set(engine))}


def assert_sources(identity, root):
    R.require(identity["source_sha256"] == source_hashes(root) and
              identity["source_digest"] == R.source_digest(identity["source_sha256"]), "SOURCE_DRIFT")
    ref = identity["preflight_controls_reference"]
    R.require(sha256_file(ref["path"]) == ref["sha256"], "LAW3_REFERENCE_DRIFT")


def preflight(root, args):
    R.require(args.operator_go, "OPERATOR_GO")
    R.require(args.steps_1_3_complete, "SEQUENCE_STEPS_1_3")
    R.require(args.autoresearch_state in ("paused", "finished"), "AUTORESEARCH_WINDOW")
    inherited = {k: os.environ[k] for k in HARNESS_KNOBS if k in os.environ}
    R.require(not inherited, "INHERITED_HARNESS_KNOBS", inherited)
    result = subprocess.run([sys.executable, "-B", str(root / "code/memit/engine_fingerprint.py")],
                            capture_output=True, text=True, env={**os.environ, "LLMDB_ROOT": str(root)})
    R.require(result.returncode == 0 and "engine fingerprint PASS:" in result.stdout, "FINGERPRINT_COMMAND", result.stdout + result.stderr)
    engine = root / R.ENGINE_FILE
    fp = {"ok": True, "sha256": sha256_file(engine), "_cov_cpu": engine.read_bytes().count(b"_cov_cpu"), "stdout": result.stdout}
    R.require(fp["sha256"] == R.ENGINE_SHA256 and fp["_cov_cpu"] == 3, "FINGERPRINT")
    return fp


def law3_reference(path):
    data = json.loads(Path(path).read_text())
    recipes = data["recipes"]
    R.require("baseline" in recipes or len(recipes) == 1, "LAW3_RECIPE_AMBIGUOUS")
    name = "baseline" if "baseline" in recipes else next(iter(recipes))
    rec = recipes[name]
    R.require(rec["band"] == list(R.LAYERS) and rec["law5_gate"]["ok"] is True, "LAW3_REFERENCE_RECIPE")
    scores = {n: rec["arms"][n]["para_full_n"] for n in R.ARMS[:2]}
    R.require(all(R.count(v) and v >= R.CTRL for v in scores.values()), "LAW3_REFERENCE_CONTROLS", scores)
    return {"path": str(Path(path).resolve()), "sha256": sha256_file(path), "recipe": name, "scores": scores, "ok": True}


def initialise_identity(root, out, reference):
    path = out / "identity.json"
    if os.path.lexists(path):
        identity = json.loads(path.read_text())
        assert_sources(identity, root)
        R.require(identity["preflight_controls_reference"] == reference, "IDENTITY_REFERENCE")
        return identity
    hashes = source_hashes(root)
    identity = {"run_id": "c10v-" + uuid.uuid4().hex, "created_utc": utc_now(),
                "source_sha256": hashes, "source_digest": R.source_digest(hashes), "preflight_controls_reference": reference}
    write_json(path, identity)
    return identity


def load_harness(root, contexts=None):
    """Operator-only boundary: H:45–48 loads the pinned tokenizer/model."""
    os.environ.update(LLMDB_ROOT=str(root), C10_ARMS=",".join(R.ARMS), C10_RECIPES="candidate",
                      HP_CANDIDATE=str(root / R.HP_FILE), CANDIDATE_NAME="layerpick", DECISION_ID=R.DECISION_ID,
                      PREREG=str(root / R.PREREG), OUT=str(root / "experiments/c10v/runs/c10v_layerpick/unused_harness_output.json"))
    H = importlib.import_module("c10e_bandknob")
    M = importlib.import_module("c10l_mint_lib")
    hp = H.MEMITHyperParams.from_json(str(root / R.HP_FILE))
    R.require(hp.layers == list(R.LAYERS) and hp.fact_token == "subject_last" and hp.v_num_grad_steps == 25 and
              hp.v_loss_layer == 35 and hp.clamp_norm_factor == 0.75 and hp.mom2_update_weight == 5000 and
              H.L2 == 1 and H.NULL_THRESH == 0.005, "HP_DEFAULTS")
    R.require(H.ID == "Qwen/Qwen2.5-3B" and H.REV == "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b" and str(H.DEV) == "mps" and
              len(H.FICTION) == R.N and tuple(H.ARMS) == R.ARMS and H.Z_OVERRIDE is None and
              H.Z_OVERRIDE_HITS == 0 and not H.ARM_HOOKS, "HARNESS_DEFAULTS")
    if contexts is not None:
        MM = importlib.import_module("memit.memit_main")
        MM.CONTEXT_TEMPLATES_CACHE = copy.deepcopy(contexts)
    ctx = H.get_context_templates(H.model, H.tok)
    if contexts is not None:
        R.require(ctx == contexts, "CONTEXT_CACHE")
    return H, M, hp, ctx


def as_numpy(t):
    import numpy as np
    return t.detach().cpu().float().numpy() if hasattr(t, "detach") else np.asarray(t)


def g_from_keys(K, P):
    """prereg:31: CPU 24-dimensional proxy, never an engine write solve."""
    import numpy as np
    K, P = np.asarray(K, dtype=np.float64), np.asarray(P, dtype=np.float64)
    R.require(K.ndim == 2 and P.shape == (K.shape[0], K.shape[0]) and
              np.isfinite(K).all() and np.isfinite(P).all(), "PROXY_OPERANDS")
    PK = P @ K
    S = K.T @ PK
    G = np.linalg.solve((np.eye(S.shape[0]) + S).T, S.T).T
    R.require(np.isfinite(G).all(), "PROXY_SOLVE")
    return G, np.linalg.norm(PK, axis=0)


def compute_selector(H, hp, P, ctx, root):
    import numpy as np
    requests = [H.req(H.CANON, s, H.ARMS[R.ARMS[2]][s]) for s in H.FICTION]
    tables, norms, first_keys = [], [], {}
    for repeat in range(2):
        gs, ns = [], []
        for j, l in enumerate(R.LAYERS):
            K = as_numpy(H.compute_ks(H.model, H.tok, requests, hp, l, ctx).T)
            G, norm = g_from_keys(K, as_numpy(P[j]))
            gs.append(np.diag(G).tolist()); ns.append(norm.tolist())
            if repeat == 0:
                first_keys[l] = K.copy()
        tables.append(np.array(gs).T.tolist()); norms.append(np.array(ns).T.tolist())
    step = R.select_maps(*tables, H.FICTION)
    prior_path = root / "experiments/c10l/runs/c10l_covgeom/step0_offline.json"
    band = json.loads(prior_path.read_text())["regularisers"]["R0"]["band"]
    shares = band["rho_c_band_per_subject"]
    R.require(set(shares) == set(H.FICTION), "HISTORICAL_RHO_SUBJECTS")
    step.update(subjects=list(H.FICTION), ctx=copy.deepcopy(ctx), ctx_sha256=R.json_digest(ctx),
                projected_key_norms=norms[0], projected_key_norms_repeat=norms[1],
                installed_share_comparison=[{"subj": s, "max_G": max(tables[0][i]),
                                             "installed_share": 1 - shares[s], "band_installed_share": 0.972}
                                            for i, s in enumerate(H.FICTION)],
                historical_rho_source={"path": str(prior_path), "sha256": sha256_file(prior_path)},
                expectation="concentrated map or hair-width variation absorbed by measured delta",
                selector_scope="pristine, target-blind, 24-key lone-write coefficient; selection proxy")
    R.validate_step0(step)
    return step, first_keys


def hsic_diagnostic(keys, residuals, subjects, published):
    import numpy as np
    def centered_kernel(rows):
        rows = np.asarray(rows, dtype=np.float64)
        distance2 = ((rows[:, None, :] - rows[None, :, :]) ** 2).sum(axis=2)
        sigma = float(np.median(np.sqrt(distance2[np.triu_indices(len(rows), 1)])))
        if sigma == 0:
            return None, sigma
        kernel = np.exp(-distance2 / (2 * sigma ** 2))
        return kernel - kernel.mean(axis=0)[None, :] - kernel.mean(axis=1)[:, None] + kernel.mean(), sigma
    Y, sy = centered_kernel(residuals)
    values, scores = {}, {}
    for l in R.LAYERS:
        X, sx = centered_kernel(keys[l].T)
        if X is None or Y is None:
            values[str(l)] = {"status": "UNDEFINED: zero median pairwise distance", "sigma_X": sx, "sigma_Y": sy}
            continue
        contributions = (X * Y).sum(axis=1)
        values[str(l)] = {"status": "DIAGNOSTIC", "sigma_X": sx, "sigma_Y": sy,
                          "HSIC_b": float(contributions.sum() / (R.N - 1) ** 2), "per_fact_c": contributions.tolist()}
        scores[l] = contributions
    mapped = ({s: max(R.LAYERS, key=lambda l: (scores[l][i], l)) for i, s in enumerate(subjects)}
              if len(scores) == 5 else None)
    return {"n": R.N, "layers": values, "argmax_c_map": mapped,
            "agreement_n": sum(mapped[s] == published[s] for s in subjects) if mapped else None,
            "role": "A7 diagnostic only; layer-8 pristine residuals; never selector or gate"}


def activation_rows(H, hp, layer_map):
    """Engine compute_z.py:188–231; one canonical + three held-out positions."""
    import numpy as np
    result = {}
    for l, subjects in R.groups(layer_map, H.FICTION):
        templates = [t for s in subjects for t in [H.CANON] + H.PTEST]
        words = [s for s in subjects for _ in templates[:4]]
        with H.torch.no_grad():
            out = H.get_module_input_output_at_words(H.model, H.tok, l, context_templates=templates, words=words,
                                                   module_template=hp.layer_module_tmp, fact_token_strategy=hp.fact_token)[1]
        rows = np.asarray(as_numpy(out), dtype=np.float64).reshape(len(subjects), 4, -1)
        result.update({s: rows[i] for i, s in enumerate(subjects)})
    return result


def prepare_arm(H, M, hp, P, ctx, keys, values, layer_map):
    requests = [H.req(H.CANON, s, values[s]) for s in H.FICTION]
    effective = layer_map or {s: 8 for s in H.FICTION}
    targets = {}
    for rq in requests:
        with quiet():
            z = H.compute_z(H.model, H.tok, rq, hp, effective[rq["subject"]], ctx)
        targets[(rq["subject"], rq["target_new"]["str"])] = z.detach()
    pre = activation_rows(H, hp, effective)
    predictions = {}
    for l, subjects in R.groups(effective, H.FICTION):
        indices = [H.FICTION.index(s) for s in subjects]
        full, _ = g_from_keys(keys[l], as_numpy(P[l - 4]))
        group, _ = g_from_keys(keys[l][:, indices], as_numpy(P[l - 4]))
        for j, s in enumerate(subjects):
            predictions[s] = {"full_G_diagonal": float(full[indices[j], indices[j]]),
                              "group_G_diagonal": float(group[j, j])}
    tensor = H.torch.stack([targets[(s, " " + values[s])] for s in H.FICTION])
    return {"requests": requests, "targets": targets, "pre": pre, "predictions": predictions,
            "targets_sha256": M.sha256_tensor(tensor), "map": effective}


class GroupedEdit:
    """H:181–221 stays untouched. This wrapper describes groups and delegates."""
    def __init__(self, H, original, prepared, layer_map):
        self.H, self.original, self.prepared, self.layer_map = H, original, prepared, layer_map
        self.audits = {}

    def __call__(self, hp, requests, P, cache):
        H = self.H
        if H._LAW5_DEFAULT_CTX:
            return self.original(hp, requests, P, cache)
        wanted = {(r["subject"], r["target_new"]["str"]) for r in requests}
        matches = [n for n, p in self.prepared.items() if wanted == set(p["targets"])]
        R.require(len(matches) == 1, "OVERRIDE_TARGET_KEYS")
        arm = matches[0]; targets = self.prepared[arm]["targets"]
        R.require(hp.layers == list(R.LAYERS) and len(P) == 5, "GROUP_BASE_PROJECTORS")
        R.require(all(k in targets for k in wanted), "OVERRIDE_TARGET_KEYS")
        before, previous = H.Z_OVERRIDE_HITS, H.Z_OVERRIDE
        audit, norms = [], {}
        try:
            if self.layer_map is None:
                H.Z_OVERRIDE = targets
                result = self.original(hp, requests, P, cache)
                audit = [{"layers": list(R.LAYERS), "subjects": [r["subject"] for r in requests], "projector_indices": list(range(5))}]
                norms.update(result)
            else:
                population = [r["subject"] for r in requests]
                R.require(set(self.layer_map) == set(population), "GROUP_MAP_SUBJECTS")
                group_sets = ([list(R.LAYERS)] if all(self.layer_map[s] == list(R.LAYERS) for s in population)
                              else [[l] for l, _ in R.groups(self.layer_map, population)])
                for layers in group_sets:
                    rs = [r for r in requests if self.layer_map[r["subject"]] == (layers if len(layers) > 1 else layers[0])]
                    R.require(rs, "EMPTY_GROUP")
                    ghp = copy.deepcopy(hp); ghp.layers = layers
                    indices = [R.LAYERS.index(l) for l in layers]
                    projectors = [P[i] for i in indices]
                    fresh = [H.torch.zeros(p.shape[0], p.shape[0]) for p in projectors]
                    H.Z_OVERRIDE = {(r["subject"], r["target_new"]["str"]): targets[(r["subject"], r["target_new"]["str"])] for r in rs}
                    norms.update(self.original(ghp, rs, projectors, fresh))
                    audit.append({"layers": layers, "subjects": [r["subject"] for r in rs], "projector_indices": indices})
        finally:
            H.Z_OVERRIDE = previous
        self.audits[arm] = {"groups": audit, "z_override_hits": H.Z_OVERRIDE_HITS - before}
        R.require(H.Z_OVERRIDE_HITS - before == len(audit), "OVERRIDE_HITS")
        return norms


def relative_distances(first, second):
    import numpy as np
    return {str(l): float(np.linalg.norm(first[l] - second[l]) / max(float(np.linalg.norm(first[l])), 1e-30)) for l in first}


def capture_write(H, hp, base, P, original, prepared, layer_map, wrapper=False, requests=None, eval_values=None):
    H.restore_layers(hp, base)
    previous = H.Z_OVERRIDE
    H.Z_OVERRIDE_HITS = 0
    request_list = requests or prepared["requests"]
    H.Z_OVERRIDE = prepared["targets"]
    call = GroupedEdit(H, original, {"audit": prepared}, layer_map) if wrapper else original
    try:
        with quiet():
            call(hp, request_list, P, [H.torch.zeros(p.shape[0], p.shape[0]) for p in P])
        if not wrapper:
            R.require(H.Z_OVERRIDE_HITS == 1, "LAW5_OVERRIDE_PIN")
        updated = H.snap_layers(hp)
        deltas = {l: as_numpy(updated[l]).copy() - as_numpy(base[l]) for l in hp.layers}
        behavior = H.eval_arm(eval_values) if eval_values is not None else None
        audit = call.audits.get("audit", {}) if wrapper else {}
        return deltas, behavior, audit
    finally:
        H.Z_OVERRIDE = previous
        H.restore_layers(hp, base)


def law5_checks(H, hp, P, base, prepared, published):
    """prereg:58(i)–(v): numeric checks in THIS pristine process."""
    import numpy as np
    original = H.my_edit
    none_wrapper = GroupedEdit(H, original, {}, None)
    H.my_edit = none_wrapper
    H.Z_OVERRIDE, H.Z_OVERRIDE_HITS = None, 0
    try:
        standing = H.run_law5(hp, P, base)
        standing_hits = H.Z_OVERRIDE_HITS
    finally:
        H.my_edit = original
        H.restore_layers(hp, base)
    R.require(standing["ok"] and standing_hits == 0, "LAW5_I", standing)
    a7 = prepared[R.ARMS[2]]
    values = H.ARMS[R.ARMS[2]]
    first, behavior1, _ = capture_write(H, hp, base, P, original, a7, None, eval_values=values)
    second, behavior2, _ = capture_write(H, hp, base, P, original, a7, None, eval_values=values)
    distances = relative_distances(first, second)
    floor = max(distances.values())
    tolerance = max(1e-4, 10 * floor)
    identity_map = {s: list(R.LAYERS) for s in H.FICTION}
    active, behavior3, audit = capture_write(H, hp, base, P, original, a7, identity_map, wrapper=True, eval_values=values)
    identity = {"relative_by_layer": relative_distances(first, active), "behavior_equal": behavior1 == behavior3,
                "active_group_layers": [g["layers"] for g in audit["groups"]]}
    R.require(identity["behavior_equal"] and max(identity["relative_by_layer"].values()) <= tolerance, "LAW5_III", identity)
    del first, second, active
    one = a7["requests"][:1]; subject = one[0]["subject"]
    restricted = {**a7, "requests": one, "targets": {(subject, one[0]["target_new"]["str"]): a7["targets"][(subject, one[0]["target_new"]["str"])]}}
    single_hp = copy.deepcopy(hp); single_hp.layers = [8]
    lone, _, _ = capture_write(H, single_hp, {8: base[8]}, [P[4]], original, restricted, None)
    wrapped, _, audit = capture_write(H, hp, base, P, original, restricted, {subject: 8}, wrapper=True)
    R.require(all(not np.any(wrapped[l]) for l in R.LAYERS if l != 8), "LAW5_IV_SCOPE")
    singleton = {"relative_by_layer": relative_distances(lone, {8: wrapped[8]}),
                 "active_group_layers": [g["layers"] for g in audit["groups"]], "projector_indices": audit["groups"][0]["projector_indices"]}
    R.require(max(singleton["relative_by_layer"].values()) <= tolerance, "LAW5_IV", singleton)
    del lone, wrapped
    largest = sorted(R.groups(published, H.FICTION), key=lambda g: (-len(g[1]), -g[0]))[:2]
    R.require(len(largest) == 2, "LAW5_V_GROUP_POPULATION")
    small_map = {s: l for l, ss in largest for s in ss}
    rq = [r for r in a7["requests"] if r["subject"] in small_map]
    # B's targets must be solved at their own assigned layer on pristine weights.
    zs = {}
    for r in rq:
        with quiet():
            zs[(r["subject"], r["target_new"]["str"])] = H.compute_z(H.model, H.tok, r, hp, small_map[r["subject"]], H.get_context_templates(H.model, H.tok)).detach()
    small = {"requests": rq, "targets": zs}
    composed, _, audit = capture_write(H, hp, base, P, original, small, small_map, wrapper=True)
    R.require(all(not np.any(composed[l]) for l in R.LAYERS if l not in small_map.values()), "LAW5_V_SCOPE")
    multirel = {}
    for l, ss in largest:
        ghp = copy.deepcopy(hp); ghp.layers = [l]
        grq = [r for r in rq if r["subject"] in ss]
        gp = {"requests": grq, "targets": {(r["subject"], r["target_new"]["str"]): zs[(r["subject"], r["target_new"]["str"])] for r in grq}}
        lone, _, _ = capture_write(H, ghp, {l: base[l]}, [P[l - 4]], original, gp, None)
        multirel.update(relative_distances(lone, {l: composed[l]}))
    multi = {"relative_by_layer": multirel, "active_group_layers": [g["layers"] for g in audit["groups"]], "groups": audit["groups"]}
    R.require(max(multirel.values()) <= tolerance, "LAW5_V", multi)
    proof = {"ok": True, "standing": standing, "standing_override_hits": standing_hits,
             "floor": {"relative_by_layer": distances, "relative_max": floor,
                       "behavior_count_deltas": {k: abs(behavior1[k] - behavior2[k]) for k in ("canon_full_n", "para_full_n")}},
             "tolerance": tolerance, "identity": identity, "singleton": singleton, "multigroup": multi}
    R.law5_reading(proof, published, H.FICTION)
    return proof


def frame_probe(H, values):
    firsts = {H.first_tok(v) for v in values.values()}
    rows = [{"subj": s, "top1": H.predict(H.CANON.format(s))["id"]} for s in FRAME_SUBJECTS]
    for row in rows:
        row["flip"] = row["top1"] in firsts
    return {"flips": sum(r["flip"] for r in rows), "n": 6, "rows": rows}


def relation_probe(H):
    return {label: [H.predict(template.format(s))["id"] for s in H.FICTION]
            for label, template in (("bystander", "{} is associated with"), ("objective-anchored", "{} is a"))}


def proxy_readout(H, hp, prepared):
    import numpy as np
    post = activation_rows(H, hp, prepared["map"])
    rows = []
    for rq in prepared["requests"]:
        s = rq["subject"]
        z = as_numpy(prepared["targets"][(s, rq["target_new"]["str"])]).astype(np.float64)
        pre = prepared["pre"][s]
        before, after = z[None, :] - pre, z[None, :] - post[s]
        norms = np.linalg.norm(before, axis=1)
        rho = [float(np.linalg.norm(after[j]) / norms[j]) if norms[j] else None for j in range(4)]
        realised = float(np.dot(post[s][0] - pre[0], before[0]) / norms[0] ** 2) if norms[0] else None
        prediction = prepared["predictions"][s]
        rows.append({"subj": s, "layer": prepared["map"][s], "rho_per_prompt": rho,
                     "undefined_zero_denominator": [j for j in range(4) if norms[j] == 0],
                     "realised_fraction": realised, **prediction,
                     "prediction_error": realised - prediction["group_G_diagonal"] if realised is not None else None,
                     "pristine_residual_norms": norms.tolist()})
    return {"rows": rows, "remaining_ratio": "norm(z - post) / norm(z - pristine), per prompt",
            "weight_application": "fp16", "targets_sha256": prepared["targets_sha256"],
            "predictions_recorded_before_write": True}


def run_one_recipe(H, M, hp, P, ctx, keys, root, name, layer_map, proof, preprepared=None):
    prepared = preprepared or {arm: prepare_arm(H, M, hp, P, ctx, keys, values, layer_map) for arm, values in H.ARMS.items()}
    # All three arms' z vectors, and prediction tables, exist before any write.
    relation_pre = relation_probe(H)
    wrapper = GroupedEdit(H, H.my_edit, prepared, layer_map)
    original_edit, original_P, original_law5 = H.my_edit, H.compute_P, H.run_law5
    H.my_edit = wrapper
    def cached_P(chp):
        R.require(chp.layers == list(R.LAYERS), "RECIPE_PROJECTOR_CACHE")
        return P
    def cached_standing(chp, projectors, base):
        R.require(chp.layers == list(R.LAYERS) and all(a is b for a, b in zip(projectors, P)), "RECIPE_LAW5_CACHE")
        return copy.deepcopy(proof["standing"])
    def hook(arm, values):
        post = relation_probe(H)
        out = {"same_frame": frame_probe(H, values),
               "relation_labels": {label: {"n": R.N, "pre_top1": relation_pre[label], "post_top1": after,
                                           "flips": sum(a != b for a, b in zip(relation_pre[label], after))}
                                   for label, after in post.items()}}
        if arm in (R.ARMS[0], R.ARMS[2]):
            out["proxy"] = proxy_readout(H, hp, prepared[arm])
        return out
    H.compute_P, H.run_law5 = cached_P, cached_standing
    H.ARM_HOOKS[:] = [hook]
    H.Z_OVERRIDE_HITS = 0
    try:
        rec = H.run_recipe(name, str(root / R.HP_FILE))
        for arm in rec.get("arms", {}).values():
            arm["para_full_string"] = round(100 * arm["para_string_n"] / arm["para_n"], 1)
        rec.update(map=layer_map, wrapper=wrapper.audits,
                   target_ids={arm: {s: H.tgt_ids(values[s]) for s in H.FICTION} for arm, values in H.ARMS.items()},
                   predictions_before_write={arm: p["predictions"] for arm, p in prepared.items()},
                   targets_sha256={arm: p["targets_sha256"] for arm, p in prepared.items()})
        return rec, prepared
    finally:
        H.my_edit, H.compute_P, H.run_law5 = original_edit, original_P, original_law5
        H.ARM_HOOKS[:] = []
        H.Z_OVERRIDE = None


def stage_record(step, fingerprint, **extra):
    return {"decision_id": R.DECISION_ID, "identity": IDENTITY, "fingerprint": fingerprint,
            "pid": os.getpid(), "when_utc": utc_now(), **step, **extra}


def runtime_stage(root, out, stage, fingerprint):
    previous = None
    if stage != "step0":
        frozen = json.loads((out / "step0.json").read_text())
        R.validate_step0(frozen)
        R.require(frozen["identity"] == IDENTITY and frozen["status"] == "READY", "STEP0_NOT_READY")
        if stage == "pass2":
            previous = json.loads((out / "pass1.json").read_text())
            complete = json.loads((out / "pass1_complete.json").read_text())
            R.require(complete["record_sha256"] == sha256_file(out / "pass1.json") and
                      complete["identity"] == IDENTITY and previous["identity"] == IDENTITY, "PASS1_COMPLETE")
            R.require(R.replication_needed(previous), "REPLICATION_NOT_NEEDED")
            R.require(previous["pid"] != os.getpid(), "REPLICATION_PROCESS")
    H, M, hp, ctx = load_harness(root, frozen["ctx"] if stage == "pass1" else None)
    covariance = H.cov_cache_sha256(hp)
    base, P = H.snap_layers(hp), H.compute_P(hp)
    R.require(covariance == H.cov_cache_sha256(hp), "COVARIANCE_DRIFT")
    try:
        step, keys = compute_selector(H, hp, P, ctx, root)
        step = stage_record(step, fingerprint, cov_cache_sha256=covariance)
        assert_sources(IDENTITY, root)
        if stage == "step0":
            write_json(out / "step0.json", step)
            if step["status"] != "READY":
                write_json(out / "run.json", {"identity": IDENTITY, "label": step["status"], "candidate_advanced": False,
                                             "step0_sha256": sha256_file(out / "step0.json"), "table_published": True})
            print("C10V_STEP0: " + step["status"], flush=True)
            return
        R.require(step["map_reproduced"], "MAP_REPRODUCIBLE")
        published = frozen["map"]
        R.require(covariance == frozen["cov_cache_sha256"], "COVARIANCE_DRIFT")
        maps = R.recipe_maps(published, H.FICTION)
        prepared_A = {arm: prepare_arm(H, M, hp, P, ctx, keys, values, None) for arm, values in H.ARMS.items()}
        proof = law5_checks(H, hp, P, base, prepared_A, published)
        assert_sources(IDENTITY, root)
        write_json(out / ("law5.json" if stage == "pass1" else "law5_pass2.json"),
                   stage_record({}, fingerprint, law5=proof, ctx_sha256=R.json_digest(ctx), published_map_sha256=R.json_digest(published)))
        baseline, _ = run_one_recipe(H, M, hp, P, ctx, keys, root, "A", None, proof, prepared_A)
        try:
            R.validate_recipe(baseline, "A", step, published)
        except Exception as exc:
            halt(root, "LIVE_LAW3: " + str(exc), baseline=baseline, law5=proof)
        baseline["validity"] = {"ok": True, "reasons": []}
        # The first marker is after both live baseline and numeric LAW#5.
        assert_sources(IDENTITY, root)
        write_json(out / (stage + "_started.json"), stage_record({}, fingerprint, stage=stage,
                   law5_ok=True, live_law3_ok=True, published_map_sha256=R.json_digest(published)))
        recipes = {"A": baseline}
        for name in R.RECIPES[1:]:
            H.restore_layers(hp, base)
            recipes[name], _ = run_one_recipe(H, M, hp, P, ctx, keys, root, name, maps[name], proof)
            try:
                R.recipe_integrity(recipes[name], name, step, published)
                R.require(recipes[name]["cov_cache_sha256"] == covariance, "COVARIANCE_DRIFT")
            except Exception as exc:
                halt(root, "RECIPE_INTEGRITY " + name + ": " + str(exc), recipes=recipes, law5=proof)
            reasons = R.recipe_validity(recipes[name])
            recipes[name]["validity"] = {"ok": not reasons, "reasons": reasons}
        import numpy as np
        a7 = prepared_A[R.ARMS[2]]
        residuals = np.stack([as_numpy(a7["targets"][(s, " " + H.ARMS[R.ARMS[2]][s])]) - a7["pre"][s][0] for s in H.FICTION])
        record = stage_record({}, fingerprint, stage=stage, step0=step, ctx=ctx, ctx_sha256=R.json_digest(ctx),
                    published_map=published, published_map_sha256=R.json_digest(published),
                    selection_agreement_n=sum(step["map"][s] == published[s] for s in H.FICTION),
                    replication_scope="published fixed map, not selection procedure" if stage == "pass2" else "published step0 map",
                    shuffled_changed_n=sum(maps["Bshuf"][s] != published[s] for s in H.FICTION),
                    model={"id": H.ID, "revision": H.REV, "dtype": "float16", "device": str(H.DEV)},
                    law5=proof, recipes=recipes, hsic=hsic_diagnostic(keys, residuals, H.FICTION, published), outcome="COMPLETE")
        assert_sources(IDENTITY, root)
        for name in R.RECIPES:
            R.pass_integrity(record, name)
        write_json(out / (stage + ".json"), record)
        write_json(out / (stage + "_complete.json"), {"identity": IDENTITY, "pid": os.getpid(), "stage": stage,
                   "record_sha256": sha256_file(out / (stage + ".json")), "when_utc": utc_now()})
        reading = R.read_run(previous, record) if previous else R.read_run(record)
        if stage == "pass2" or not R.replication_needed(record):
            write_json(out / "run.json", {"identity": IDENTITY, **reading,
                       "pass_sha256": {n: sha256_file(out / (n + ".json")) for n in ("pass1", "pass2") if (out / (n + ".json")).exists()}})
        print(json.dumps(reading, indent=2, allow_nan=False), flush=True)
        print("C10V_" + stage.upper() + "_COMPLETE", flush=True)
    finally:
        H.restore_layers(hp, base)


def main(argv=None):
    global STAGE, IDENTITY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("step0", "pass1", "pass2"))
    parser.add_argument("--root", type=Path, default=Path(LLMDB_ROOT))
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--law3-ref", type=Path, required=True)
    parser.add_argument("--operator-go", action="store_true")
    parser.add_argument("--steps-1-3-complete", dest="steps_1_3_complete", action="store_true")
    parser.add_argument("--autoresearch-state", choices=("paused", "finished"), required=True)
    args = parser.parse_args(argv)
    root, STAGE = args.root.resolve(), args.stage
    out = (args.out_dir or root / "experiments/c10v/runs/c10v_layerpick").resolve()
    try:
        R.require(root == Path(__file__).resolve().parents[3], "WORKTREE_ROOT")
        out.relative_to(root / "experiments/c10v/runs/c10v_layerpick")
        names = (["step0.json", "run.json"] if STAGE == "step0" else
                 [STAGE + ".json", STAGE + "_started.json", STAGE + "_complete.json",
                  "law5.json" if STAGE == "pass1" else "law5_pass2.json", "run.json"])
        occupied(out, names)
        fingerprint = preflight(root, args)
        reference = law3_reference(args.law3_ref)
        IDENTITY = initialise_identity(root, out, reference)
        R.validate_identity(IDENTITY, fingerprint)
        runtime_stage(root, out, STAGE, fingerprint)
        return 0
    except Exception as exc:
        halt(root, str(exc), exception=type(exc).__name__, traceback=traceback.format_exc())


if __name__ == "__main__":
    sys.exit(main())
