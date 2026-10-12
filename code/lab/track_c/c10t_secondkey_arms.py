#!/usr/bin/env python3
"""D-C10t-secondkey v2 frozen §2: driver-side request wrapper; engine untouched.

Operator use only, after step 1's verdict and with autoresearch paused/finished:
  LLMDB_ROOT=<root> .venv/bin/python code/lab/track_c/c10t_secondkey_step0.py
  LLMDB_ROOT=<root> .venv/bin/python code/lab/track_c/c10t_secondkey_arms.py first
  LLMDB_ROOT=<root> .venv/bin/python code/lab/track_c/c10t_secondkey_arms.py second
OUT_DIR defaults to experiments/c10t/runs/c10t_secondkey; POSITIONS defaults to OUT_DIR/step0.json.
Importing this module is model-free. Model/torch imports occur only inside load_harness().
All JSON outputs are exclusive creations, reread immediately. No existing output is
rewritten, including run.json; second_started.json makes replication attempts final.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse, contextlib, copy, datetime, hashlib, importlib, io, json, math, subprocess, traceback, uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10t_secondkey_read as R

IDENTITY = None
STAGE = "not-started"
RUN_ROOT = Path(LLMDB_ROOT).resolve()
SOURCE_FILES = ["code/lab/track_c/c10t_secondkey_" + name + ".py" for name in ("arms", "step0", "read", "selftest")] + [
    "code/lab/track_c/c10e_bandknob.py", R.HP_FILE, R.PREREG, "code/memit/engine_fingerprint.py",
    "code/configs/screens/g6_screen_qwen3b.json", "code/configs/screens/g6_screen_qwen3b_v2.json"]
HARNESS_KNOBS = ("MODEL_ID", "MODEL_REV", "HP_CANDIDATE", "OUT", "CANDIDATE_NAME", "DECISION_ID", "PREREG", "RUN_LABEL",
                 "Z_OVERRIDE", "C10_PROJECTOR", "N_EDIT", "C10_SUBJECT_OFFSET", "C10_ARMS", "C10_KEY_LOCUS", "C10_CTX_TEMPLATES", "C10_RECIPES")


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    """Exclusive create, byte-for-byte reread and JSON parse; never overwrite."""
    path = Path(path)
    text = json.dumps(obj, indent=2, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as f:
        f.write(text)
    if path.read_text() != text or json.loads(path.read_text()) != obj:
        raise RuntimeError(str(path) + " did not persist exactly")


def halt(reason, root=None, **state):
    root = Path(root or RUN_ROOT)
    path = root / "experiments/c10t/runs/c10t_secondkey/halts/c10t_secondkey_halt_diagnostic.json"
    # Preserve an older diagnostic too; never replace another arm's or this arm's record.
    if path.exists():
        path = path.with_name("c10t_secondkey_halt_diagnostic_" + uuid.uuid4().hex + ".json")
    rec = {"decision_id": R.DECISION_ID, "when_utc": utc_now(), "stage": STAGE,
           "identity": IDENTITY, "reason": reason, "state": state}
    try:
        write_json(path, rec)
        where = str(path)
    except Exception as e:
        where = "NOT WRITTEN: " + repr(e)
    raise SystemExit("HALT: " + reason + " (diagnostic: " + where + ")")


def source_hashes(root=None):
    root = Path(root or LLMDB_ROOT)
    # Include transitive vendored engine Python sources (repr_tools/nethook/device/
    # layer_stats/generate/etc.), not only the three MEMIT modules used directly.
    engine = sorted(str(p.relative_to(root)) for p in (root / "code/memit/vendor").rglob("*.py"))
    if not engine:
        raise ValueError("vendored engine sources missing")
    return {p: sha256_file(root / p) for p in [*SOURCE_FILES, *engine]}


def source_digest(hashes):
    return hashlib.sha256("\n".join(k + " " + v for k, v in sorted(hashes.items())).encode()).hexdigest()


def make_identity(root=None):
    hashes = source_hashes(root)
    return {"run_id": "c10t-" + uuid.uuid4().hex, "created_utc": utc_now(),
            "source_digest": source_digest(hashes), "source_sha256": hashes,
            "program_rulings": dict(R.PROGRAM_RULINGS)}


def require_sources(identity, root=None):
    if identity.get("program_rulings") != R.PROGRAM_RULINGS:
        raise ValueError("program rulings differ from D-C10t-p5rule")
    current = source_hashes(root)
    old = identity["source_sha256"]
    changed = {p: {"recorded": old.get(p), "current": current.get(p)}
               for p in set(old) | set(current) if old.get(p) != current.get(p)}
    if changed or identity["source_digest"] != source_digest(old):
        raise ValueError("source hashes differ from the frozen step0 identity: " + repr(changed))


def refuse_occupied(directory, names):
    occupied = [name for name in names if (Path(directory) / name).exists()]
    if occupied:
        raise ValueError("occupied outputs are never overwritten: " + repr(occupied))


def preflight(root):
    """Model-free refusals must complete before permanent stage markers exist."""
    inherited = {k: os.environ[k] for k in HARNESS_KNOBS if k in os.environ}
    if inherited:
        raise ValueError("frozen harness knobs must be unset: " + repr(inherited))
    root = Path(root).resolve()
    fp = subprocess.run([sys.executable, str(root / "code/memit/engine_fingerprint.py")], capture_output=True, text=True,
                        env={**os.environ, "LLMDB_ROOT": str(root)})
    if fp.returncode != 0 or not fp.stdout.strip():
        raise RuntimeError("engine fingerprint failed: " + fp.stdout + fp.stderr)
    engine = root / "code/memit/vendor/memit/memit_main.py"
    fingerprint = {"ok": True, "stdout": fp.stdout, "sha256": sha256_file(engine),
                   "_cov_cpu": engine.read_bytes().count(b"_cov_cpu")}
    return fingerprint


def load_harness(root, out_dir, fingerprint):
    """Operator-only model load, after preflight and the stage's no-retry marker."""
    root = Path(root).resolve()
    os.environ.update(LLMDB_ROOT=str(root), HP_CANDIDATE=str(root / R.HP_FILE), C10_RECIPES="candidate",
                      C10_ARMS="A1_single,A2_coherent2,A7_coined_coined", CANDIDATE_NAME="secondkey",
                      DECISION_ID=R.DECISION_ID, PREREG=str(root / R.PREREG), OUT=str(Path(out_dir) / "unused_harness_output.json"))
    H = importlib.import_module("c10e_bandknob")       # c10e_bandknob.py:45-48 loads the pinned model
    if H.CANON != R.CANON or H.PTEST != R.PTEST or len(H.FICTION) != R.N or H.Z_OVERRIDE is not None or H.Z_OVERRIDE_HITS != 0:
        raise ValueError("harness forms/population/Z_OVERRIDE differ")
    hp = H.MEMITHyperParams.from_json(str(root / R.HP_FILE))
    if hp.layers != R.BAND or hp.fact_token != "subject_last" or hp.v_num_grad_steps != R.ENGINE_STEPS:
        raise ValueError("frozen baseline hparams differ")
    return H, hp, fingerprint


def token_ids(tok, text):
    return list(tok(text)["input_ids"])


def second_request(tok, subject, value_ids, j):
    if not 1 <= j < len(value_ids):
        raise ValueError("only internal value tokens 1..n-1 can be keys")
    # §2 request construction; c10e_bandknob.py:96-97 would add another space.
    # compute_z.py:41-50 consumes the remainder unchanged on H.my_edit's path.
    return {"prompt": "The capital of {}", "subject": subject + " is the city of" + tok.decode(value_ids[:j]),
            "target_new": {"str": tok.decode(value_ids[j:])}}


def requests_for(tok, facts, positions):
    canonical = [{"prompt": R.CANON, "subject": f["subj"], "target_new": {"str": " " + f["value"]}} for f in facts]
    return canonical + [second_request(tok, f["subj"], f["value_ids"], positions[f["subj"]]) for f in facts]


def alignment_audit(tok, country, value, value_ids, j, contexts, index_fn):
    """§2 admission/§7 C2: exact tokenizer audit, no model. Uses the real
    get_words_idxs_in_templates (rome/repr_tools.py:43-99), injected in selftests.
    compute_z.py:46-73: truncated input, end-slice labels, lookup, separate KL row.
    Failures are published; runtime callers HALT without selecting a replacement j.
    """
    rq = second_request(tok, country, value_ids, j)
    remainder = value_ids[j:]
    rows = []
    for t in [t for group in contexts for t in group]:
        prompt = t.format(rq["prompt"])
        prefix = token_ids(tok, prompt.format(rq["subject"]))
        rewriting = prompt + tok.decode(remainder[:-1])
        truncated = token_ids(tok, rewriting.format(rq["subject"]))
        full = token_ids(tok, t.format(R.CANON.format(country)) + " " + value)
        b, m = len(prefix), len(remainder)
        idx = index_fn(tok, [prompt], [rq["subject"]], "last")[0][0]
        rewrite_idx = index_fn(tok, [rewriting], [rq["subject"]], "last")[0][0]
        checks = {"prefix_ids": truncated[:b] == prefix, "input_length": len(truncated) == b + m - 1,
                  "canonical_rewriting_text": rewriting.format(rq["subject"]) == t.format(R.CANON.format(country)) + tok.decode(value_ids[:-1]),
                  "lookup_at_prefix_end": idx == b - 1 and rewrite_idx == b - 1,
                  "full_sentence_input_ids": truncated == full[:b + m - 1],
                  "label_input_ids": full[b - 1:b + m - 1] == value_ids[j - 1:-1],
                  "target_retokenisation": token_ids(tok, rq["target_new"]["str"]) == remainder,
                  "intended_key": 0 <= idx < len(prefix) and prefix[idx] == value_ids[j - 1] and tok.decode([prefix[idx]]) == tok.decode([value_ids[j - 1]])}
        rows.append({"template": t, "lookup_idx": idx, "rewrite_lookup_idx": rewrite_idx, "b": b, "m": m,
                     "label_positions": list(range(b - 1, b + m - 1)), "prefix_ids": prefix, "truncated_ids": truncated,
                     "expected_key_id": value_ids[j - 1], "checks": checks, "ok": all(checks.values())})
    kl = "{} is a"
    ki = index_fn(tok, [kl], [rq["subject"]], "last")[0][0]
    kids = token_ids(tok, kl.format(rq["subject"]))
    kl_ok = 0 <= ki < len(kids) and kids[ki] == value_ids[j - 1] and tok.decode([kids[ki]]) == tok.decode([value_ids[j - 1]])
    return {"j": j, "request": rq, "rows": rows, "kl": {"prompt": kl.format(rq["subject"]), "lookup_idx": ki, "ids": kids, "ok": kl_ok},
            "ok": bool(rows) and all(r["ok"] for r in rows) and kl_ok}


def canonical_audit(tok, rq, contexts, index_fn):
    rows = []
    for t in [t for g in contexts for t in g] + ["KL"]:
        prompt = "{} is a" if t == "KL" else t.format(rq["prompt"])
        # repr_tools.py:66-70 adds a leading space to the subject only when the
        # template has a nonempty prefix. The identity KL row has no such prefix.
        word = " " + rq["subject"].strip() if prompt.split("{}")[0] else rq["subject"]
        expected = token_ids(tok, word)[-1]
        ids = token_ids(tok, prompt.format(rq["subject"]))
        idx = index_fn(tok, [prompt], [rq["subject"]], "last")[0][0]
        rows.append({"template": t, "lookup_idx": idx, "decoded_token": tok.decode([ids[idx]]) if 0 <= idx < len(ids) else None,
                     "expected_id": expected, "ok": 0 <= idx < len(ids) and ids[idx] == expected})
    return {"subject": rq["subject"], "rows": rows, "ok": all(r["ok"] for r in rows)}


def process_admission(H, step, ctx):
    from rome.repr_tools import get_words_idxs_in_templates
    arms = {}
    canonical = [canonical_audit(H.tok, rq, ctx, get_words_idxs_in_templates) for rq in next(iter(step["requests"].values()))[:R.N]]
    for variant, positions in step["selection"]["arms"].items():
        rebuilt = requests_for(H.tok, step["facts"], positions)
        if rebuilt != step["requests"][variant]:
            raise ValueError("runtime tokenizer changed published requests: " + variant)
        audits = [alignment_audit(H.tok, f["subj"], f["value"], f["value_ids"], positions[f["subj"]], ctx, get_words_idxs_in_templates) for f in step["facts"]]
        arms[variant] = {"ok": all(a["ok"] for a in canonical + audits), "n_requests": len(rebuilt), "canonical": canonical, "second": audits}
    return {"ok": all(a["ok"] for a in arms.values()), "ctx": ctx, "arms": arms}


class RequestWrapper:
    """§2/§7 T14: my_edit has no arm name. Recognise the exact A7 target list,
    then consume pinned single/dup/candidate order. Controls and LAW#5 pass through.
    Duplicate substitution is audited separately from the candidate-arm count (§3).
    """
    def __init__(self, harness, requests, collector):
        self.H, self.collector = harness, collector
        self.original = harness.my_edit
        self.canonical = copy.deepcopy(next(iter(requests.values()))[:R.N])
        self.targets = [r["target_new"] for r in self.canonical]
        self.plan = [(R.SINGLE, self.canonical), (R.DUP, self.canonical + copy.deepcopy(self.canonical)), *requests.items()]
        self.audit = {"candidate_substitutions": 0, "duplicate_substitutions": 0, "law5_substitutions": 0,
                      "order": [], "requests_sha256": {}, "reached_my_edit_counts": {}}

    def __call__(self, hp, requests, P, cache):
        if self.H._LAW5_DEFAULT_CTX:
            return self.original(hp, requests, P, cache)
        if [r["target_new"] for r in requests] != self.targets:
            return self.original(hp, requests, P, cache)
        if requests != self.canonical or len(self.audit["order"]) >= len(self.plan):
            raise ValueError("unexpected A7 request construction/order")
        if self.H.Z_OVERRIDE is not None or self.H.Z_OVERRIDE_HITS != 0:
            raise ValueError("secondkey must use engine targets only")
        name, actual = self.plan[len(self.audit["order"])]
        actual = copy.deepcopy(actual)
        expected_n = R.N if name == R.SINGLE else 2 * R.N
        if len(actual) != expected_n:
            raise ValueError("wrong blocked request population: " + name)
        # c10e_bandknob.py:487 publishes 24 original requests; hooks (:494-495)
        # must instead see EXACTLY the requests handed to my_edit (:489).
        self.H._ARM_STATE["requests"] = actual
        self.audit["order"].append(name)
        self.audit["requests_sha256"][name] = R.json_digest(actual)
        self.audit["reached_my_edit_counts"][name] = len(actual)
        if name == R.DUP:
            self.audit["duplicate_substitutions"] += 1
        elif name != R.SINGLE:
            self.audit["candidate_substitutions"] += 1
        self.collector.before(name, actual, hp, P)
        try:
            return self.original(hp, actual, P, cache)
        finally:
            self.collector.active = False


def observe_solve(function, args, clamp_line=178):
    """Read-only Python tracing of the UNMODIFIED compute_z frame. Read final NLL
    and KL at return (:149-156,185), count entries to clamp assignment (:178).
    The target object is returned unchanged. No optimiser/activation is replaced.
    """
    if sys.gettrace() is not None:
        raise RuntimeError("another Python trace is active; refusing to replace it")
    observed = {"clamp_hit_steps": 0}

    def trace(frame, event, arg):
        if frame.f_code is not function.__code__:
            return None
        if event == "line" and frame.f_lineno == clamp_line:
            observed["clamp_hit_steps"] += 1
        elif event == "return" and arg is not None:
            x = frame.f_locals
            scalar = lambda name: float(x[name].item())
            nll = scalar("nll_loss")
            observed.update(nll=nll, exp_minus_nll=math.exp(-nll), kl_loss=scalar("kl_loss"),
                            loss=scalar("loss"), weight_decay=scalar("weight_decay"),
                            nll_each=x["nll_loss_each"].detach().float().cpu().tolist(),
                            kl_lookup_idx=int(x["lookup_idxs"][-1]),
                            loss_evaluations=int(x["it"]) + 1, adam_steps=int(x["it"]),
                            stopped_by="loss<0.05" if scalar("loss") < R.ENGINE_LOSS_STOP else "budget",
                            clamp_hit=observed["clamp_hit_steps"] > 0,
                            target_init_norm=float(x["target_init"].detach().float().norm()),
                            delta_norm=float(x["delta"].detach().float().norm()))
        return trace

    sys.settrace(trace)
    try:
        target = function(*args)
    finally:
        sys.settrace(None)
    if "nll" not in observed:
        raise RuntimeError("compute_z return telemetry missing")
    return target, observed


def observer_inertness(H, hp, ctx, requests):
    """c10s floor rule: two unobserved solves and one observed, at both loci."""
    rows = []
    for rq in (requests[0], requests[R.N]):
        args = (H.model, H.tok, rq, hp, hp.layers[-1], ctx)
        with contextlib.redirect_stdout(io.StringIO()):
            a, b = H.compute_z(*args), H.compute_z(*args)
            c, _ = observe_solve(H.compute_z, args)
        floor = float((a - b).float().norm() / a.float().norm())
        rel = float((c - a).float().norm() / a.float().norm())
        rows.append({"subject": rq["subject"], **R.observer_inertness_reading(floor, rel)})
    if not all(r["ok"] for r in rows):
        raise ValueError("compute_z observer not inert: " + json.dumps(rows))
    return rows


def key_stats(K):
    """c10k_keying_ablation_keygram.py:13-17 stats, with explicit undefined
    entries for zero projected keys (P K can be zero without invalidating the arm).
    """
    import torch
    K = K.detach().cpu().double()
    norm = K.norm(dim=0)
    zero = norm == 0
    safe = torch.where(zero, torch.ones_like(norm), norm)
    G = (K / safe).T @ (K / safe)
    mask = ~torch.eye(K.shape[1], dtype=torch.bool) & ~zero[:, None] & ~zero[None, :]
    off = G[mask]
    ev = torch.linalg.eigvalsh(K.T @ K)
    return {"n": K.shape[1], "zero_keys": int(zero.sum()),
            "cos_mean": float(off.mean()) if off.numel() else None,
            "cos_min": float(off.min()) if off.numel() else None,
            "cos_max": float(off.max()) if off.numel() else None,
            "frac_cos_gt_0.9": float((off > R.KEY_COS_COMPARATOR).double().mean()) if off.numel() else None,
            "effective_rank": float(ev.sum() ** 2 / ev.square().sum()) if float(ev.square().sum()) else None}


def block_geometry(K, P):
    import torch
    K = K.detach().float().cpu()
    PK = P @ K
    def blocks(X):
        out = {"subject": key_stats(X[:, :R.N]), "joint": key_stats(X)}
        if X.shape[1] == 2 * R.N:
            out["second_block"] = key_stats(X[:, R.N:])
            a, b = X[:, :R.N], X[:, R.N:]
            den = b.norm(dim=0)[:, None] * a.norm(dim=0)[None, :]
            dots = b.T @ a
            cross = [[float(dots[i, j] / den[i, j]) if float(den[i, j]) else None for j in range(R.N)] for i in range(R.N)]
            out["cross_block"] = {"rows_second_columns_subject": cross, "own_fact": [cross[i][i] for i in range(R.N)],
                                   "other_subjects": [[cross[i][j] for j in range(R.N) if j != i] for i in range(R.N)]}
        return out
    return {"raw_K": blocks(K), "projected_PK": blocks(PK), "n_columns": K.shape[1]}


class Collector:
    """Read-only solve/key instrumentation and ARM_HOOKS diagnostics (§2 a-g)."""
    def __init__(self, H, hp, step, ctx):
        self.H, self.hp, self.step, self.ctx = H, hp, step, ctx
        self.engine_z, self.engine_ks = H.compute_z, H.compute_ks
        self.active = False
        self.base_probes, self.base_geometry = None, {}

    def probes(self):
        H = self.H
        firsts = {f["value_ids"][0] for f in self.step["facts"]}
        frame = [{"subj": s, "id": H.predict(R.CANON.format(s))["id"]} for s in R.FRAME_SUBJECTS]
        out = {"F0": {"n": R.FRAME_N, "flips": sum(r["id"] in firsts for r in frame), "rows": frame},
               "prefixes": {}, "subject_free": {}, "prefix_reached": {}, "bystanders": []}
        for variant, positions in self.step["selection"]["arms"].items():
            prefix_rows, free_rows, reached = [], [], []
            for f in self.step["facts"]:
                j = positions[f["subj"]]
                prefix, remainder = H.tok.decode(f["value_ids"][:j]), f["value_ids"][j:]
                prompts = [R.CANON.format(s) + prefix for s in R.FRAME_SUBJECTS]
                hits = [H.full_seq_match(p, remainder) for p in prompts]
                prefix_rows.append({"subj": f["subj"], "j": j, "prefix": prefix, "prompts": prompts,
                                    "next_hits": [bool(h[1]) for h in hits], "full_hits": [bool(h[0]) for h in hits]})
                neutral = "The name is" + prefix
                full, first = H.full_seq_match(neutral, remainder)
                free_rows.append({"subj": f["subj"], "prompt": neutral, "next_hit": bool(first), "full_hit": bool(full)})
                natural = [bool(H.full_seq_match(p.format(f["subj"]), f["value_ids"][:j])[0]) for p in R.PTEST]
                reached.append({"subj": f["subj"], "j": j, "hits": natural, "count": sum(natural)})
            out["prefixes"][variant], out["subject_free"][variant] = prefix_rows, free_rows
            out["prefix_reached"][variant] = {"rows": reached, "per_fact": [r["count"] for r in reached], "count": sum(r["count"] for r in reached), "n": R.N * R.NT}
        for f in self.step["facts"]:
            for form in ("{} is a", "{} is associated with"):
                prompt = form.format(f["subj"])
                p = H.predict(prompt)
                out["bystanders"].append({"subj": f["subj"], "form": form, "prompt": prompt, "id": p["id"], "token": p["tok"], "edited_first_token": p["id"] in firsts})
        return out

    def cur(self, requests, held_out=False):
        from memit.compute_z import get_module_input_output_at_words
        from rome.repr_tools import get_reprs_at_idxs, get_words_idxs_in_templates
        if not held_out:
            return get_module_input_output_at_words(self.H.model, self.H.tok, self.hp.layers[-1],
                context_templates=[r["prompt"] for r in requests], words=[r["subject"] for r in requests],
                module_template=self.hp.layer_module_tmp, fact_token_strategy=self.hp.fact_token)[1].T.detach().cpu().double()
        prompts, idxs = [], []
        for i, rq in enumerate(requests):
            f = self.step["facts"][i % R.N]
            for p in R.PTEST:
                if rq["subject"] == f["subj"]:
                    text = p.format(f["subj"])
                    idx = get_words_idxs_in_templates(self.H.tok, [p], [f["subj"]], "last")[0][0]
                else:
                    j = self.step["selection"]["arms"][self.name][f["subj"]]
                    text = p.format(f["subj"]) + self.H.tok.decode(f["value_ids"][:j])
                    idx = len(token_ids(self.H.tok, text)) - 1
                    if token_ids(self.H.tok, text)[idx] != f["value_ids"][j - 1]:
                        raise ValueError("held-out gold-prefix address retokenised")
                prompts.append(text)
                idxs.append([idx])
        return get_reprs_at_idxs(self.H.model, self.H.tok, prompts, idxs, self.hp.layers[-1], self.hp.layer_module_tmp, "out").T.detach().cpu().double()

    def before(self, name, requests, hp, P):
        self.name, self.requests, self.P = name, requests, P
        self.fits, self.targets, self.keygram, self.ks_calls = [], [], {}, {}
        self.cur_before = self.cur(requests)
        self.para_before = self.cur(requests, held_out=True)
        if self.base_probes is None:
            self.base_probes = self.probes()
            for variant, rqs in self.step["requests"].items():
                self.base_geometry[variant] = {str(l): block_geometry(self.engine_ks(self.H.model, self.H.tok, rqs, hp, l, self.ctx).T, P[i]) for i, l in enumerate(hp.layers)}
        self.active = True

    def solve(self, *args):
        if not self.active or self.H._LAW5_DEFAULT_CTX:
            return self.engine_z(*args)
        z, fit = observe_solve(self.engine_z, args)
        fit["request"] = copy.deepcopy(args[2])
        fit["KL_prompt"] = "{} is a".format(args[2]["subject"])
        self.fits.append(fit)
        self.targets.append(z.detach().cpu().double().clone())
        return z

    def keys(self, *args):
        K = self.engine_ks(*args)
        if self.active and not self.H._LAW5_DEFAULT_CTX:
            layer = args[4]
            if args[2] != self.requests or K.shape[0] != len(self.requests):
                raise ValueError("actual 48-request list did not reach compute_ks")
            self.ks_calls[layer] = self.ks_calls.get(layer, 0) + 1
            if self.ks_calls[layer] == 1:  # solve K at c10e_bandknob.py:196, not post-write cache K (:219)
                self.keygram[str(layer)] = block_geometry(K.T, self.P[self.hp.layers.index(layer)])
        return K

    def residual(self, targets, before, after):
        # c10l_covgeom_step0.py:103-108,132-134: fraction REMAINING, not realised.
        remaining, initial = targets - after, targets - before
        ratio = lambda a, b: float(a.norm() / b.norm()) if float(b.norm()) else None
        out = {"overall_remaining_fraction": ratio(remaining, initial),
               "per_request": [ratio(remaining[:, i], initial[:, i]) for i in range(targets.shape[1])],
               "initial_norm": float(initial.norm()), "remaining_norm": float(remaining.norm()), "zero_initial_is_undefined": True}
        return out

    def hook(self, arm_name, Vmap):
        if arm_name in ("A1_single", "A2_coherent2"):
            return {}
        import torch
        if arm_name != self.name or self.H._ARM_STATE["requests"] != self.requests or len(self.targets) != len(self.requests):
            raise ValueError("request/solve/hook population differs")
        if any(self.ks_calls.get(l) != 2 for l in self.hp.layers):
            raise ValueError("solve/cache key calls differ from my_edit")
        out = self.probes()
        for variant in self.step["selection"]["arms"]:
            for row, base in zip(out["prefixes"][variant], self.base_probes["prefixes"][variant]):
                row.update(newly_induced_next_hits=R.new_hits(row["next_hits"], base["next_hits"]),
                           newly_induced_full_hits=R.new_hits(row["full_hits"], base["full_hits"]))
        for current, base in zip(out["bystanders"], self.base_probes["bystanders"]):
            current.update(pre_id=base["id"], changed=current["id"] != base["id"],
                           flipped_to_edited_first=current["edited_first_token"] and current["id"] != base["id"])
        zs = torch.stack(self.targets, dim=1)
        zsp = zs.repeat_interleave(R.NT, dim=1)
        after_c, after_p = self.cur(self.requests), self.cur(self.requests, held_out=True)
        direct = self.residual(zs, self.cur_before, after_c)
        para = self.residual(zsp, self.para_before, after_p)
        blocks = {"subject": slice(0, R.N)}
        if len(self.requests) == 2 * R.N:
            blocks["duplicated_subject" if arm_name == R.DUP else "value_internal"] = slice(R.N, 2 * R.N)
        block_residuals = {}
        for label, sl in blocks.items():
            ps = slice(sl.start * R.NT, sl.stop * R.NT)
            block_residuals[label] = {"canonical": self.residual(zs[:, sl], self.cur_before[:, sl], after_c[:, sl]),
                                     "held_out": self.residual(zsp[:, ps], self.para_before[:, ps], after_p[:, ps])}
        out.update(fits=self.fits, requests_sha256=R.json_digest(self.requests), hook_request_count=len(self.requests),
                   keygram_solve=self.keygram, residual={"canonical_keyed_positions": direct, "held_out_keyed_positions": para,
                   "blocks": block_residuals, "held_out_per_template": {p: self.residual(zsp[:, t::R.NT], self.para_before[:, t::R.NT], after_p[:, t::R.NT]) for t, p in enumerate(R.PTEST)},
                   "block_order": list(blocks),
                   "held_out_second_position_caveat": "gold-prefix residual proxy; natural address reach is reported separately"},
                   geometry_48_post={v: {str(l): block_geometry(self.engine_ks(self.H.model, self.H.tok, rqs, self.hp, l, self.ctx).T, self.P[i]) for i, l in enumerate(self.hp.layers)} for v, rqs in self.step["requests"].items()},
                   bystander_KL_caveat="compute_z.py:127-128 protects the lookup token, not the final token of 'is a'")
        return out


def run_pass(H, hp, step, identity, positions_sha, fingerprint):
    from memit.memit_main import get_context_templates
    ctx = get_context_templates(H.model, H.tok)       # memit_main.py:304-316: new sampled contexts per process
    admission = process_admission(H, step, ctx)
    if not admission["ok"]:
        raise ValueError("runtime admission failed; frozen j is never reselected: " + json.dumps(admission))
    V = H.ARMS["A7_coined_coined"]
    if [f["subj"] for f in step["facts"]] != H.FICTION or any(V[f["subj"]] != f["value"] or H.tgt_ids(f["value"]) != f["value_ids"] for f in step["facts"]):
        raise ValueError("step0 fact/value/token population differs from harness")
    inertness = observer_inertness(H, hp, ctx, next(iter(step["requests"].values())))
    # H.run_recipe restores the same base snapshot before EACH arm (:473), makes a
    # fresh zero cache (:474), and uses one P (:462). Controls are unchanged.
    H.ARMS = {"A1_single": H.ARMS["A1_single"], "A2_coherent2": H.ARMS["A2_coherent2"],
              R.SINGLE: V, R.DUP: V, **{v: V for v in step["selection"]["arms"]}}
    base_report = H.pre_base_report()
    if any(x["base"] > R.N * R.BASE_LEAK_MAX for x in base_report.values()):
        raise ValueError("standing harness stimulus leak halt")
    collector = Collector(H, hp, step, ctx)
    wrapper = RequestWrapper(H, step["requests"], collector)
    old = (H.my_edit, H.compute_z, H.compute_ks, H.ARM_HOOKS[:])
    H.my_edit, H.compute_z, H.compute_ks = wrapper, collector.solve, collector.keys
    H.ARM_HOOKS[:] = [collector.hook]
    try:
        recipe = H.run_recipe("secondkey", H.HP_BASE)  # LAW#5 (:415-446) runs first; no harness output file is opened
    finally:
        H.my_edit, H.compute_z, H.compute_ks = old[:3]
        H.ARM_HOOKS[:] = old[3]
    wrapper.audit.update(z_override_none=H.Z_OVERRIDE is None, z_override_hits=H.Z_OVERRIDE_HITS)
    return {"identity": identity, "pid": os.getpid(), "when_utc": utc_now(), "positions_sha256": positions_sha,
            "fingerprint": fingerprint, "ctx": ctx, "seeds": {"explicit_seeding": "none; harness sampling unchanged"},
            "admission": admission, "observer_inertness": inertness, "wrapper": wrapper.audit, "base_report": base_report,
            "base_probes": collector.base_probes, "base_geometry_48": collector.base_geometry, "recipe": recipe,
            "second_request_KL_objective_note": "KL now regularises next-token predictions at the value-prefix lookup, where the remainder fit must change them; this is an objective change as well as an address change (compute_z.py:127-128)"}


def main():
    global IDENTITY, STAGE, RUN_ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("first", "second"))
    args = parser.parse_args()
    STAGE = args.stage
    RUN_ROOT = Path(LLMDB_ROOT).resolve()
    root = RUN_ROOT
    assert Path(__file__).resolve().parents[2] == root, "script root differs from LLMDB_ROOT"
    out = Path(os.environ.get("OUT_DIR", str(root / "experiments/c10t/runs/c10t_secondkey"))).resolve()
    positions = Path(os.environ.get("POSITIONS", str(out / "step0.json"))).resolve()
    step = json.loads(positions.read_text())
    IDENTITY = step["identity"]
    require_sources(IDENTITY, root)                    # refuses mismatch BEFORE model import
    problems = R.step0_validity(step)
    if problems:
        raise ValueError("step0 no longer satisfies the frozen rules: " + "; ".join(problems))
    fp = preflight(root)
    positions_sha = sha256_file(positions)
    run_path = out / "run.json"
    if STAGE == "first":
        refuse_occupied(out, ("run.json", "pass1.json", "pass2.json", "second_started.json", "second_halt.json"))
        run = {"decision_id": R.DECISION_ID, "prereg": R.PREREG, "identity": IDENTITY, "positions_file": str(positions),
               "positions_sha256": positions_sha, "step0": step}
        write_json(run_path, run)
        if step["selection"]["outcome"] != "READY":
            print(step["selection"]["outcome"] + ": configuration not advanced; no harness pass")
            return 0
    else:
        refuse_occupied(out, ("pass2.json", "second_started.json", "second_halt.json"))
        run = json.loads(run_path.read_text())
        p1 = json.loads((out / "pass1.json").read_text())
        if run["positions_sha256"] != positions_sha or not R.identity_matches(run["identity"], IDENTITY):
            raise ValueError("second process positions/identity differs")
        v1 = R.verdict(run, p1)
        if v1.get("label") == "INVALID" or not v1["replication_pending"]:
            raise ValueError("pass1 does not call for a second process: " + json.dumps(v1))
        if p1["pid"] == os.getpid():
            raise ValueError("gate A requires a fresh process")
        write_json(out / "second_started.json", {"identity": IDENTITY, "pid": os.getpid(), "when_utc": utc_now(), "outcome": "STARTED"})
    try:
        H, hp, fp = load_harness(root, out, fp)
        record = run_pass(H, hp, step, IDENTITY, positions_sha, fp)
        require_sources(IDENTITY, root)
        write_json(out / ("pass1.json" if STAGE == "first" else "pass2.json"), record)
        reasons = R.validity(run, record)
        if reasons:
            raise ValueError("INVALID pass: " + "; ".join(reasons))
    except BaseException as e:
        if STAGE == "second":
            write_json(out / "second_halt.json", {"identity": IDENTITY, "outcome": "HALTED", "when_utc": utc_now(), "reason": str(e)})
        raise
    print("C10T_SECONDKEY_PASS_DONE; read " + str(out) + " with c10t_secondkey_read.py")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        if e.code in (0, None):
            raise
        halt("driver exit: " + str(e), root=RUN_ROOT)
    except BaseException as e:
        halt(type(e).__name__ + ": " + str(e), root=RUN_ROOT, traceback=traceback.format_exc())
