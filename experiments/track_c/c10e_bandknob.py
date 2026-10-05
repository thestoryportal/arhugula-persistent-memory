import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import io, contextlib, json, math
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"
os.environ["HF_HUB_OFFLINE"] = "0"
ENGINE_ROOT = f"{LLMDB_ROOT}/memit_dry_run/memit"
sys.path.insert(0, ENGINE_ROOT)
os.chdir(ENGINE_ROOT)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from util.device import resolve_device, empty_cache  # P-8 harness side
DEV = resolve_device()
from memit.memit_main import apply_memit_to_model, get_cov, get_context_templates, upd_matrix_match_shape
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks

# C10e/C10f — cheap C10 W-realization recipe-knob harness.
# Defaults reproduce D-C10e-bandknob: baseline [4-8] vs later [8-12].
# Env overrides let C10f compare baseline [4-8] vs widened [4-12] without
# duplicating the vetted evaluator. Canonical fit is diagnostic; held-out
# paraphrase full-sequence remains the behavioral readout.

ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-3B")
REV = os.environ.get("MODEL_REV", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
LN2 = math.log(2.0)
NULL_THRESH = 0.005
L2 = 1.0
HP_BASE = f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"
HP_BAND = os.environ.get("HP_CANDIDATE", f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams_band812.json")
OUT = os.environ.get("OUT", f"{LLMDB_ROOT}/results/c10e_bandknob.json")
CANDIDATE_NAME = os.environ.get("CANDIDATE_NAME", "later_band812")
DECISION_ID = os.environ.get("DECISION_ID", "D-C10e-bandknob")
PREREG = os.environ.get("PREREG", f"{LLMDB_ROOT}/docs/C10_BANDKNOB_PREREG.md")
RUN_LABEL = os.environ.get("RUN_LABEL", "C10 W-realization band-knob test")
# D-C10l-covgeom P3: candidate-recipe solve geometry. "nullspace" = the AlphaEdit-style projector the harness has always
# used; "identity" = P := I (RoSE/IGA on this path). Applies to the CANDIDATE recipe only and never inside the LAW#5
# parity check, so the baseline recipe and the engine comparison are untouched by the knob.
PROJECTOR = os.environ.get("C10_PROJECTOR", "nullspace")   # [LAW:parse-dont-validate] parsed once, here, at the boundary
if PROJECTOR not in ("nullspace", "identity"):
    raise SystemExit(f"C10_PROJECTOR must be nullspace|identity, got {PROJECTOR!r}")
_CANDIDATE_RECIPE = False   # set True by run_recipe for the candidate recipe only

tok = AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map=DEV).eval()
print(f"loaded {ID}", flush=True)

CANON = "The capital of {} is the city of"
PTEST = [
    "{}'s capital city is called",
    "If you visit {}, its capital city is",
    "The main city and seat of government of {} is",
]
FICTION = [
    "Zorbland", "Quaxil", "Plurnak", "Vythorn", "Glimsto", "Drennik", "Yastovel", "Crulpane",
    "Mophgar", "Brinduun", "Trannak", "Skornwell", "Fluvane", "Oxbarrow", "Zephquin", "Lurmaxen",
    "Pradnoll", "Kessivar", "Wombryne", "Halquin", "Vorlex", "Quenby", "Marsduq", "Thelby",
]
N = int(os.environ.get("N_EDIT", "24"))
_OFF = int(os.environ.get("C10_SUBJECT_OFFSET", "0"))   # D-C10k-keying-ablation N=1 discriminator: pick subjects FICTION[off:off+N]
FICTION = FICTION[_OFF:_OFF + N]


def tgt_ids(s):
    return tok(" " + s, add_special_tokens=False)["input_ids"]


def first_tok(s):
    return tgt_ids(s)[0]


def ntok(s):
    return len(tgt_ids(s))


def single_tok(s):
    return ntok(s) == 1


def js(a, b):
    p = a.cpu().double()
    q = b.cpu().double()
    m = 0.5 * (p + q)

    def k(x, y):
        x = x.clamp_min(1e-12)
        y = y.clamp_min(1e-12)
        return float((x * (x.log() - y.log())).sum())

    return 0.5 * k(p, m) + 0.5 * k(q, m)


def req(prompt, subj, targ):
    return {"prompt": prompt, "subject": subj, "target_new": {"str": " " + targ}}


@torch.no_grad()
def predict(prompt):
    ids = tok(prompt, return_tensors="pt").to(DEV)
    pr = torch.softmax(model(**ids).logits[0, -1].float(), dim=-1)
    top = torch.topk(pr, 5)
    return {"id": int(top.indices[0]), "tok": tok.decode([int(top.indices[0])]), "dist": pr.cpu()}


@torch.no_grad()
def full_seq_match(prompt, target_ids):
    ids = tok(prompt, return_tensors="pt").to(DEV)["input_ids"]
    cur = ids
    gen = []
    for _ in range(len(target_ids)):
        nxt = int(model(cur).logits[0, -1].argmax())
        gen.append(nxt)
        cur = torch.cat([cur, torch.tensor([[nxt]], device=DEV)], dim=1)
    return gen == list(target_ids), gen[0] == target_ids[0]


@torch.no_grad()
def string_match(prompt, value, n_tokens):
    """D-C10l-covgeom P4 (arXiv 2609.29045): same string through any tokenisation. Greedy-decode n_tokens + 2 and
    compare text, beside the binding id-match of full_seq_match."""
    ids = tok(prompt, return_tensors="pt").to(DEV)["input_ids"]
    cur = ids
    for _ in range(n_tokens + 2):
        nxt = int(model(cur).logits[0, -1].argmax())
        cur = torch.cat([cur, torch.tensor([[nxt]], device=DEV)], dim=1)
    text = tok.decode(cur[0, ids.shape[1]:].tolist())
    return text.startswith(" " + value)


@torch.no_grad()
def teacher_forced_pertok(prompt, target_ids):
    if len(target_ids) < 2:
        return 0, 0
    base = tok(prompt, return_tensors="pt").to(DEV)["input_ids"]
    hits = 0
    for j in range(1, len(target_ids)):
        cur = torch.cat([base, torch.tensor([target_ids[:j]], device=DEV)], dim=1)
        nxt = int(model(cur).logits[0, -1].argmax())
        hits += nxt == target_ids[j]
    return hits, len(target_ids) - 1


def weight_name(hp, layer):
    return f"{hp.rewrite_module_tmp.format(layer)}.weight"


def snap_layers(hp):
    npd = dict(model.named_parameters())
    return {layer: npd[weight_name(hp, layer)].detach().clone() for layer in hp.layers}


def restore_layers(hp, snap):
    with torch.no_grad():
        npd = dict(model.named_parameters())
        for layer in hp.layers:
            npd[weight_name(hp, layer)][...] = snap[layer]


def locpct(post, pre, prompts):
    return round(100 * sum(1 - js(post[p]["dist"], pre[p]["dist"]) / LN2 for p in prompts) / len(prompts), 2)


def compute_P(hp):
    Ps = []
    for layer in hp.layers:
        cov = get_cov(
            model, tok, hp.rewrite_module_tmp.format(layer), hp.mom2_dataset,
            hp.mom2_n_samples, hp.mom2_dtype
        ).cpu().float()
        U, S, _ = torch.linalg.svd(cov, full_matrices=False)
        idx = (S < NULL_THRESH).nonzero(as_tuple=True)[0]
        Ps.append((U[:, idx] @ U[:, idx].T).cpu())
        del cov, U, S
        empty_cache(DEV)
    return Ps


def my_edit(hp, requests, P, cache_c):
    ctx = get_context_templates(model, tok) if (os.environ.get("C10_CTX_TEMPLATES", "on") != "off" or _LAW5_DEFAULT_CTX) else [["{}"]]   # D-C10k-keying-ablation knob: off = identity template only; the LAW#5 parity check always uses the engine defaults
    layers = hp.layers
    z_layer = layers[-1]
    zs = torch.stack([compute_z(model, tok, rq, hp, z_layer, ctx) for rq in requests], dim=1)
    npd = dict(model.named_parameters())
    delta_norms = {}
    for i, layer in enumerate(layers):
        before = npd[weight_name(hp, layer)].detach().float().norm().item()
        K = compute_ks(model, tok, requests, hp, layer, ctx).T
        cur = get_module_input_output_at_words(
            model, tok, z_layer, context_templates=[rq["prompt"] for rq in requests],
            words=[rq["subject"] for rq in requests], module_template=hp.layer_module_tmp,
            fact_token_strategy=hp.fact_token
        )[1].T
        tgt = zs - cur
        tgt = tgt.repeat_interleave(K.size(1) // tgt.size(1), dim=1)
        resid = tgt / (len(layers) - i)
        Kf = K.float()
        rf = resid.float()
        Pi = torch.eye(Kf.shape[0]) if (PROJECTOR == "identity" and _CANDIDATE_RECIPE and not _LAW5_DEFAULT_CTX) else P[i]   # D-C10l-covgeom arm B: P := I, nothing else changes
        ca = cache_c[i]
        A = Pi @ (Kf.cpu() @ Kf.cpu().T + ca) + L2 * torch.eye(Kf.shape[0])
        B = Pi @ Kf.cpu() @ rf.cpu().T
        upd = torch.linalg.solve(A, B).T
        upd = upd_matrix_match_shape(upd.float(), npd[weight_name(hp, layer)].shape)
        upd_norm = float(upd.float().norm())
        rel = upd_norm / max(before, 1e-12)
        delta_norms[str(layer)] = {"delta_norm": upd_norm, "weight_norm_before": before, "relative_delta_norm": rel}
        with torch.no_grad():
            npd[weight_name(hp, layer)][...] += upd.to(npd[weight_name(hp, layer)].device, npd[weight_name(hp, layer)].dtype)
    for i, layer in enumerate(layers):
        K = compute_ks(model, tok, requests, hp, layer, ctx).T.float().cpu()
        cache_c[i] = cache_c[i] + K @ K.T
    return delta_norms


def build_stimuli():
    scr = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
    caps = sorted({scr[c]["capital"]["truth"] for c in scr})
    single_v = [k for k in caps if single_tok(k)]
    coherent2 = [k for k in caps if ntok(k) == 2]
    coined_head = [
        "Qorvex", "Vindex", "Plurn", "Drennik", "Skorn", "Vythorn", "Crulpane", "Vorlex",
        "Zephquin", "Lurmax", "Pradnoll", "Kessivar", "Wombryne", "Halquin", "Quenby", "Marsduq",
        "Thelby", "Glimsto", "Mophgar", "Brindu", "Trannak", "Fluvane", "Oxbar", "Yastov",
    ]
    coined_mod = [
        "Zentra", "Ploom", "Vask", "Threnn", "Wyxen", "Brakk", "Voneth", "Qurel",
        "Stavik", "Dwelos", "Phaxis", "Yornel", "Klavor", "Druvik", "Spraxil", "Velmor",
        "Gantho", "Ulvenn", "Treska", "Bloraq", "Cindel", "Marvox", "Ossquin", "Drelth",
    ]

    def assign(pool):
        return {c: pool[(i * 3 + 5) % len(pool)] for i, c in enumerate(FICTION)}

    return {
        "A1_single": assign(single_v),
        "A2_coherent2": assign(coherent2),
        "A7_coined_coined": {
            c: f"{coined_head[(i * 2 + 1) % len(coined_head)]} {coined_mod[(i * 3 + 2) % len(coined_mod)]}"
            for i, c in enumerate(FICTION)
        },
    }


ARMS = build_stimuli()
if os.environ.get("C10_ARMS"):   # D-C10k-keying-ablation: restrict arms (default: all)
    ARMS = {k: v for k, v in ARMS.items() if k in os.environ["C10_ARMS"].split(",")}


# ---- D-C10l-covgeom S-3 locality axes (reported beside every held-out number; L1/L3 are the prereg's binding axes) ----
def build_locality_sets():
    """L1 = CORPUS/43 F-A3's 12 real countries (g6_screen_qwen3b.json, sorted, first 12), scored on CANON.
    L3 = every real country of g6_screen_qwen3b_v2.json whose capital is not an A1/A2 value (prereg amendment A1: the
    screen holds 78 countries and A1+A2 use 48 distinct capitals, so the pool is 30, not the 50 the prereg assumed;
    three of the 30 are also in L1 and are kept - L1 scores flips to an edited value, L3 scores agreement with the
    pre-edit top-1); scored as top-1 agreement with the pre-edit model + mean next-token KL(pre‖post)."""
    scr1 = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json"))["selected"]
    l1 = [c for c in sorted(scr1)][:12]
    scr2 = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
    full = build_stimuli()
    used = set(full["A1_single"].values()) | set(full["A2_coherent2"].values())
    l3 = [c for c in sorted(scr2) if scr2[c]["capital"]["truth"] not in used]
    if len(l3) != 30:
        raise SystemExit(f"L3 pool has {len(l3)} countries, amendment A1 declares exactly 30")   # [LAW:no-silent-failure]
    return l1, l3


L1_COUNTRIES, L3_COUNTRIES = build_locality_sets()
L1_PROMPTS = [CANON.format(c) for c in L1_COUNTRIES]
L3_PROMPTS = [CANON.format(c) for c in L3_COUNTRIES]
GENERIC = [
    "The weather today is warm and sunny with a light breeze from the west.",
    "She opened the window and listened to the birds singing in the garden.",
    "The committee will meet on Thursday to discuss the annual budget.",
    "He poured a cup of coffee and sat down to read the morning newspaper.",
    "The train to the coast leaves every hour from the central station.",
    "Water boils at one hundred degrees Celsius at sea level.",
    "The museum's new exhibition features paintings from the nineteenth century.",
    "Please remember to lock the door when you leave the office tonight.",
    "The recipe calls for two eggs, a cup of flour, and a pinch of salt.",
    "Children played football in the park until the sun went down.",
    "The library extended its opening hours during the examination period.",
    "A gentle rain fell on the city for most of the afternoon.",
    "The orchestra performed a symphony by Beethoven to a full house.",
    "He repaired the old bicycle and rode it along the river path.",
    "The bakery on the corner sells fresh bread every morning at seven.",
    "Scientists announced the discovery of a new species of frog in the rainforest.",
    "The students finished their essays before the deadline on Friday.",
    "Our neighbours planted tomatoes and beans in their small vegetable patch.",
    "The ferry crossing takes about forty minutes in calm weather.",
    "She wrote a letter to her grandmother describing the summer holiday.",
]


@torch.no_grad()
def sentence_nll(text):
    ids = tok(text, return_tensors="pt").to(DEV)["input_ids"]
    logits = model(ids).logits[0, :-1].float()
    lp = torch.log_softmax(logits, dim=-1)
    return float(-lp.gather(1, ids[0, 1:, None]).mean())


def axes_pre():
    return {
        "L1": {p: predict(p) for p in L1_PROMPTS},
        "L3": {p: predict(p) for p in L3_PROMPTS},
        "generic_ppl": round(math.exp(sum(sentence_nll(s) for s in GENERIC) / len(GENERIC)), 3),
    }


def axes_post(pre, arm_values):
    """Exact counts. L1 flip = top-1 CHANGED from pre-edit and now is the first token of a value this arm wrote.
    L3 agreement = same top-1 id as pre."""
    first_ids = {first_tok(v) for v in arm_values}
    l1 = {p: predict(p) for p in L1_PROMPTS}
    l3 = {p: predict(p) for p in L3_PROMPTS}
    kl = [float((pre["L3"][p]["dist"].double() * (pre["L3"][p]["dist"].double().clamp_min(1e-12).log() - l3[p]["dist"].double().clamp_min(1e-12).log())).sum()) for p in L3_PROMPTS]
    return {
        "L1_flipped_to_edited_value": sum((l1[p]["id"] in first_ids and l1[p]["id"] != pre["L1"][p]["id"]) for p in L1_PROMPTS),
        "L1_pre_already_edited_token": sum(pre["L1"][p]["id"] in first_ids for p in L1_PROMPTS),
        "L1_top1_changed": sum(l1[p]["id"] != pre["L1"][p]["id"] for p in L1_PROMPTS),
        "L1_n": len(L1_PROMPTS),
        "L1_js_locpct": locpct(l1, pre["L1"], L1_PROMPTS),
        "L3_top1_agree": sum(l3[p]["id"] == pre["L3"][p]["id"] for p in L3_PROMPTS),
        "L3_n": len(L3_PROMPTS),
        "L3_mean_kl": round(sum(kl) / len(kl), 5),
        "L3_js_locpct": locpct(l3, pre["L3"], L3_PROMPTS),
        "generic_ppl_pre": pre["generic_ppl"],
        "generic_ppl_post": round(math.exp(sum(sentence_nll(s) for s in GENERIC) / len(GENERIC)), 3),
        "L1_post_top1": {c: l1[p]["tok"] for c, p in zip(L1_COUNTRIES, L1_PROMPTS)},
    }


def cov_cache_sha256(hp):
    """D-C10l-covgeom P5: hash of every covariance cache file the recipe's layers use (the engine's STATS_DIR)."""
    import hashlib
    from util.globals import STATS_DIR
    out = {}
    for layer in hp.layers:
        name = hp.rewrite_module_tmp.format(layer)
        path = f"{STATS_DIR}/{model.config._name_or_path.replace('/', '_')}/{hp.mom2_dataset}_stats/{name}_{hp.mom2_dtype}_mom2_t100_{hp.mom2_n_samples}.npz"
        h = hashlib.sha256()
        with open(path, "rb") as f:   # [LAW:no-silent-failure] a missing cache file raises here, before any edit
            for chunk in iter(lambda: f.read(1 << 24), b""):
                h.update(chunk)
        out[str(layer)] = {"path": path, "sha256": h.hexdigest()}
    return out


def eval_arm(Vmap):
    rows = []
    for c in FICTION:
        ids = tgt_ids(Vmap[c])
        cf, c1 = full_seq_match(CANON.format(c), ids)
        para = [full_seq_match(p.format(c), ids) for p in PTEST]
        tf = [teacher_forced_pertok(p.format(c), ids) for p in PTEST]
        para_str = [string_match(p.format(c), Vmap[c], len(ids)) for p in PTEST]
        rows.append({
            "subj": c, "val": Vmap[c], "ntok": len(ids),
            "canon_full": cf, "canon_first": c1,
            "para_full_hits": [x[0] for x in para],
            "para_first_hits": [x[1] for x in para],
            "para_string_hits": para_str,
            "tf_correct": sum(t[0] for t in tf),
            "tf_total": sum(t[1] for t in tf),
        })
    n = len(rows)
    npar = len(PTEST)
    first = sum(sum(x["para_first_hits"]) for x in rows)
    full_given_first = sum(
        sum(1 for k in range(npar) if x["para_first_hits"][k] and x["para_full_hits"][k])
        for x in rows
    )
    tf_c = sum(x["tf_correct"] for x in rows)
    tf_t = sum(x["tf_total"] for x in rows)
    return {
        "rows": rows,
        "canon_full": round(100 * sum(x["canon_full"] for x in rows) / n, 1),
        "canon_first": round(100 * sum(x["canon_first"] for x in rows) / n, 1),
        "para_full": round(100 * sum(sum(x["para_full_hits"]) for x in rows) / (n * npar), 1),
        "para_first": round(100 * sum(sum(x["para_first_hits"]) for x in rows) / (n * npar), 1),
        "para_any_full": round(100 * sum(any(x["para_full_hits"]) for x in rows) / n, 1),
        "cond_full_given_first": round(full_given_first / first, 3) if first else None,
        "tf_pertok_cont": round(100 * tf_c / tf_t, 1) if tf_t else None,
        "mean_ntok": round(sum(x["ntok"] for x in rows) / n, 2),
        # D-C10l-covgeom: exact counts (the prereg reads counts, not rounded percentages)
        "canon_full_n": sum(x["canon_full"] for x in rows), "canon_n": n,
        "para_full_n": sum(sum(x["para_full_hits"]) for x in rows),
        "para_first_n": first,
        "para_string_n": sum(sum(x["para_string_hits"]) for x in rows),
        "para_n": n * npar,
    }


_LAW5_DEFAULT_CTX = False   # set True only inside run_law5: the inertness check compares engine vs harness on the engine's own defaults, independent of the ablation knobs
ARM_HOOKS = []   # callables (arm_name, Vmap) -> dict, run after each arm's evaluation while the edit is still applied


def run_law5(hp, P, base_snap):
    print(f"\n=== LAW#5 INERTNESS {hp.layers} ===", flush=True)
    e = "Zorbland"
    cons = CANON.format(e)
    target = first_tok("Cairo")
    probes = [f"{e} is described as"]
    pre = {p: predict(p) for p in [cons] + probes}
    with contextlib.redirect_stdout(io.StringIO()):
        apply_memit_to_model(model, tok, [req(CANON, e, "Cairo")], hp, copy=False, return_orig_weights=False)
    eng = {p: predict(p) for p in [cons] + probes}
    eng_p = float(eng[cons]["dist"][target])
    eng_loc = locpct(eng, pre, probes)
    restore_layers(hp, base_snap)
    cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in hp.layers]
    global _LAW5_DEFAULT_CTX
    _LAW5_DEFAULT_CTX = True
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            my_edit(hp, [req(CANON, e, "Cairo")], P, cache)
    finally:
        _LAW5_DEFAULT_CTX = False
    mine = {p: predict(p) for p in [cons] + probes}
    my_p = float(mine[cons]["dist"][target])
    my_loc = locpct(mine, pre, probes)
    restore_layers(hp, base_snap)
    gate = {
        "expr_delta": round(abs(eng_p - my_p), 4),
        "loc_delta": round(abs(eng_loc - my_loc), 2),
    }
    gate["ok"] = gate["expr_delta"] < 0.05 and gate["loc_delta"] < 3
    print(f"  |Δexpr|={gate['expr_delta']:.4f} |Δloc|={gate['loc_delta']:.2f} -> {'INERT' if gate['ok'] else 'NOT INERT'}", flush=True)
    return gate


def pre_base_report():
    report = {}
    for name, Vmap in ARMS.items():
        base = sum(full_seq_match(CANON.format(c), tgt_ids(Vmap[c]))[0] for c in FICTION)
        nts = [ntok(Vmap[c]) for c in FICTION]
        report[name] = {"base": base, "mean_ntok": round(sum(nts) / len(nts), 2), "ntok_range": [min(nts), max(nts)]}
    return report


def run_recipe(name, hparam_path):
    hp = MEMITHyperParams.from_json(hparam_path)
    print(f"\n=== RECIPE {name}: band={hp.layers} ===", flush=True)
    base_snap = snap_layers(hp)
    P = compute_P(hp)
    law5 = run_law5(hp, P, base_snap)
    if not law5["ok"]:
        return {"hparams": hparam_path, "band": hp.layers, "law5_gate": law5, "invalid": "LAW#5 failed"}

    global _CANDIDATE_RECIPE
    _CANDIDATE_RECIPE = name == CANDIDATE_NAME
    out = {"hparams": hparam_path, "band": hp.layers, "law5_gate": law5, "arms": {}, "delta_norms": {},
           "projector": PROJECTOR if _CANDIDATE_RECIPE else "nullspace", "cov_cache_sha256": cov_cache_sha256(hp)}
    pre_axes = axes_pre()
    for arm_name, Vmap in ARMS.items():
        restore_layers(hp, base_snap)
        cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in hp.layers]
        pre_prompts = [f"{c} is described as" for c in FICTION]
        pre_loc = {p: predict(p) for p in pre_prompts}
        if os.environ.get("C10_KEY_LOCUS", "subject") == "last":   # D-C10k-keying-ablation: key at the prompt's final token via the engine's own subject_last path (subject = "<country> is the city of", prompt "The capital of {}"); no engine change
            requests = [req("The capital of {}", f"{c} is the city of", Vmap[c]) for c in FICTION]   # prereg v3: subject = "<country> is the city of" → subject_last keys the final " of"; KL prompt "<country> is the city of is a" keyed at " of"
        else:
            requests = [req(CANON, c, Vmap[c]) for c in FICTION]
        if os.environ.get("C10_KEY_LOCUS") or os.environ.get("C10_CTX_TEMPLATES"):   # D-C10k-keying-ablation validity print (item 0): keyed token + eval strings must match across cells
            from rome import repr_tools as _rt
            _rq = requests[0]; _tmpl = _rq["prompt"]; _idx = _rt.get_words_idxs_in_templates(tok, [_tmpl], [_rq["subject"]], "last")[0][0]
            _ids = tok(_tmpl.format(_rq["subject"]))["input_ids"]
            print(f"  VALIDITY item0: locus={os.environ.get('C10_KEY_LOCUS','subject')} templates={os.environ.get('C10_CTX_TEMPLATES','on')} prompt={_tmpl!r} subject={_rq['subject']!r} keyed_idx={_idx}/{len(_ids)-1} keyed_tok={tok.decode(_ids[_idx])!r} | para={[p.format(FICTION[0]) for p in PTEST]} | loc={pre_prompts[0]!r} | subj_key={FICTION[0]!r}", flush=True)
        with contextlib.redirect_stdout(io.StringIO()):
            delta = my_edit(hp, requests, P, cache)
        post_loc = {p: predict(p) for p in pre_prompts}
        arm = eval_arm(Vmap)
        arm["locality_described_as"] = locpct(post_loc, pre_loc, pre_prompts)
        arm["locality_axes"] = axes_post(pre_axes, list(Vmap.values()))
        for hook in ARM_HOOKS:   # [LAW:locality-or-seam] extra post-write readouts (D-C10l-mint sibling/cannibal) plug in here, before restore
            arm.setdefault("extra", {}).update(hook(arm_name, Vmap))
        out["arms"][arm_name] = {k: v for k, v in arm.items() if k != "rows"}
        out.setdefault("detail", {})[arm_name] = arm["rows"]
        out["delta_norms"][arm_name] = delta
        print(
            f"  {arm_name:18} canon={arm['canon_full']} para={arm['para_full']} "
            f"first={arm['para_first']} tf={arm['tf_pertok_cont']} loc={arm['locality_described_as']} "
            f"| n: canon {arm['canon_full_n']}/{arm['canon_n']} para {arm['para_full_n']}/{arm['para_n']} first {arm['para_first_n']} str {arm['para_string_n']} "
            f"| L1 {arm['locality_axes']['L1_flipped_to_edited_value']}/{arm['locality_axes']['L1_n']} L3 {arm['locality_axes']['L3_top1_agree']}/{arm['locality_axes']['L3_n']} kl {arm['locality_axes']['L3_mean_kl']} ppl {arm['locality_axes']['generic_ppl_pre']}->{arm['locality_axes']['generic_ppl_post']}",
            flush=True,
        )
    restore_layers(hp, base_snap)
    _CANDIDATE_RECIPE = False
    return out


def verdict(results):
    b = results["recipes"]["baseline"]["arms"]["A7_coined_coined"]
    k = results["recipes"][CANDIDATE_NAME]["arms"]["A7_coined_coined"]
    a1b = results["recipes"]["baseline"]["arms"]["A1_single"]["para_full"]
    a1k = results["recipes"][CANDIDATE_NAME]["arms"]["A1_single"]["para_full"]
    a2b = results["recipes"]["baseline"]["arms"]["A2_coherent2"]["para_full"]
    a2k = results["recipes"][CANDIDATE_NAME]["arms"]["A2_coherent2"]["para_full"]
    law_ok = all(results["recipes"][r]["law5_gate"]["ok"] for r in results["recipes"])
    invalid_reasons = []
    if not law_ok:
        invalid_reasons.append("LAW#5 failed")
    if not (b["canon_full"] <= 55 and b["para_full"] <= 35):
        invalid_reasons.append("baseline A7 did not reproduce failure envelope")
    if a1b < 80:
        invalid_reasons.append("baseline A1 sanity below 80")
    if a2b < 80:
        invalid_reasons.append("baseline A2 coherent2 below 80")
    dc = round(k["canon_full"] - b["canon_full"], 1)
    dp = round(k["para_full"] - b["para_full"], 1)
    tradeoff = min(a1k, a2k) < 80
    if invalid_reasons:
        label = "INVALID"
        text = "; ".join(invalid_reasons)
    elif tradeoff:
        label = "TRADEOFF_NOT_CLEAN_RESCUE"
        text = "candidate recipe damages A1/A2 controls below 80; valid negative/tradeoff, not a clean C10 rescue"
    elif k["para_full"] >= 85:
        label = "USABILITY_RESCUE_LEAD_NOT_PROMOTED"
        text = "candidate recipe reaches the C10 usability bar in this scoped run; requires replication and downstream checks before closure"
    elif dp >= 25 and k["para_full"] >= 40:
        label = "BEHAVIORAL_LEAD_NOT_CLOSURE"
        text = "candidate recipe materially improves held-out read expression but remains below the 85% C10 usability gate"
    elif dc >= 20 and k["para_full"] < 50:
        label = "W_REALIZATION_ONLY"
        text = "candidate recipe improves canonical fit but held-out behavioral read expression remains below partial rescue"
    elif dp < 15 and k["para_full"] < 40 and k["canon_full"] < 80:
        label = "NO_MATERIAL_KNOB_RESCUE"
        text = "candidate recipe does not materially solve the C10 held-out read-expression failure"
    else:
        label = "MIXED_PARTIAL_LEAD"
        text = "valid but mixed recipe lead; C10 remains open"
    return {
        "label": label,
        "text": text,
        "baseline_A7": b,
        f"{CANDIDATE_NAME}_A7": k,
        "delta_A7": {"canon_full_pp": dc, "para_full_pp": dp},
        "candidate_control_min_para_full": min(a1k, a2k),
    }


def main():
    base_report = pre_base_report()
    print("\n=== STIMULUS BASE CHECK ===", flush=True)
    for k, v in base_report.items():
        print(f"  {k:18} base={v['base']}/{N} ntok={v['mean_ntok']} range={v['ntok_range']}", flush=True)
    if any(v["base"] > N * 0.15 for v in base_report.values()):
        print("STIMULUS HALT: pre-edit base leak >15%", flush=True)
        return 0

    results = {
        "decision_id": DECISION_ID,
        "prereg": PREREG,
        "run": RUN_LABEL,
        "class": "FALSIFIER-resolver / recipe-knob characterization; NOT promotable",
        "scope": "Qwen2.5-3B / AlphaEdit / capital / A1-A2-A7 / N=24 / 1-seed / HF-fp16",
        "stimulus": {"CANON": CANON, "PTEST": PTEST, "FICTION": FICTION, **{f"V_{k}": v for k, v in ARMS.items()},
                     "L1_countries": L1_COUNTRIES, "L3_countries": L3_COUNTRIES, "generic_sentences": GENERIC},
        "projector_knob": PROJECTOR,
        "base_report": base_report,
        "recipes": ({CANDIDATE_NAME: run_recipe(CANDIDATE_NAME, HP_BAND)} if os.environ.get("C10_RECIPES") == "candidate"   # D-C10k-keying-ablation: one recipe per cell
                    else {"baseline": run_recipe("baseline", HP_BASE), CANDIDATE_NAME: run_recipe(CANDIDATE_NAME, HP_BAND)}),
    }
    # The D-C10e-bandknob-era label set is NOT binding for later decisions: D-C10l-* read their result JSONs with their
    # own pre-registered readers (c10l_covgeom_read.py). Kept under a name that says so. [LAW:one-source-of-truth]
    results["legacy_nonbinding_summary"] = verdict(results) if "baseline" in results["recipes"] and "A7_coined_coined" in ARMS else {"note": "skipped (restricted arms/recipes)"}
    results["legacy_nonbinding_summary"]["note_binding"] = "NON-BINDING: D-C10e thresholds; D-C10l-* labels come from experiments/track_c/c10l_covgeom_read.py"
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n=== C10e LEGACY (NON-BINDING) SUMMARY ===", flush=True)
    print(json.dumps(results["legacy_nonbinding_summary"], indent=2), flush=True)
    print(f"\nwrote {OUT}", flush=True)
    print("C10E_DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
