import os, sys

LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")

import argparse
import contextlib
import io
import json
import math
from pathlib import Path

os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"
os.environ.setdefault("HF_HUB_OFFLINE", "1")

ANYEDIT_ROOT = os.environ.get("ANYEDIT_ROOT", "/tmp/AnyEdit")
ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-3B")
REV = os.environ.get("MODEL_REV", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
SOURCE = f"{LLMDB_ROOT}/results/c10h_anyedit_window50_controls.json"
OUT = os.environ.get("OUT", f"{LLMDB_ROOT}/results/c10i_anyedit_upstream_active_audit.json")
LN2 = math.log(2.0)


def ids(tok, text):
    return tok(text, add_special_tokens=False)["input_ids"]


def load_case(arm, subject):
    src = json.loads(Path(SOURCE).read_text())
    vals = src["stimulus"][f"V_{arm}"]
    question = src["stimulus"]["CANON"].format(subject)
    return {
        "arm": arm,
        "subject": subject,
        "value": vals[subject],
        "question": question,
        "answer": " " + vals[subject],
        "ptest": [p.format(subject) for p in src["stimulus"]["PTEST"]],
    }


@contextlib.contextmanager
def pushd(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def import_upstream():
    # Upstream compute_z imports nltk for a commented sentence-splitting path.
    # The ARE window path exercised here does not use it; avoid adding a
    # dependency just to import the unchanged upstream module.
    import types

    sys.modules.setdefault("nltk", types.SimpleNamespace())
    if ANYEDIT_ROOT not in sys.path:
        sys.path.insert(0, ANYEDIT_ROOT)
    with pushd(ANYEDIT_ROOT):
        from AlphaEdit_ARE.AlphaEdit_ARE_hparams import AlphaEditAREHyperParams
        import AlphaEdit_ARE.AlphaEdit_ARE_main as main
        import AlphaEdit_ARE.compute_z as cz

    return AlphaEditAREHyperParams, main, cz


def make_hparams(AlphaEditAREHyperParams, window_size):
    hp_path = f"{ANYEDIT_ROOT}/hparams/AlphaEdit_ARE/Qwen2.5-7B-Instruct.json"
    hp = AlphaEditAREHyperParams.from_json(hp_path)
    hp.model_name = ID
    hp.window_size = window_size
    hp.overlap = 0
    return hp, hp_path


def predict(model, tok, prompt):
    import torch

    with torch.no_grad():
        x = tok(prompt, return_tensors="pt").to("cuda")
        pr = torch.softmax(model(**x).logits[0, -1].float(), dim=-1)
        top = torch.topk(pr, 5)
    return {"id": int(top.indices[0]), "tok": tok.decode([int(top.indices[0])]), "dist": pr.cpu()}


def full_seq_match(model, tok, prompt, target_ids):
    import torch

    with torch.no_grad():
        cur = tok(prompt, return_tensors="pt").to("cuda")["input_ids"]
        gen = []
        logits = []
        for target in target_ids:
            out = model(cur).logits[0, -1].float()
            logits.append(float(out[target].detach().cpu()))
            nxt = int(out.argmax())
            gen.append(nxt)
            cur = torch.cat([cur, torch.tensor([[nxt]], device="cuda")], dim=1)
    return {"full": gen == list(target_ids), "first": gen[0] == target_ids[0], "gen": gen, "target_logits": logits}


def eval_case(model, tok, case):
    target_ids = ids(tok, case["answer"])
    canon = full_seq_match(model, tok, case["question"], target_ids)
    para = [full_seq_match(model, tok, p, target_ids) for p in case["ptest"]]
    return {
        "target_ids": target_ids,
        "canon_full": canon["full"],
        "canon_first": canon["first"],
        "canon_generated_ids": canon["gen"],
        "canon_target_logits": canon["target_logits"],
        "para_full_hits": [x["full"] for x in para],
        "para_first_hits": [x["first"] for x in para],
        "para_generated_ids": [x["gen"] for x in para],
        "para_target_logits": [x["target_logits"] for x in para],
    }


def js(a, b):
    p = a.double()
    q = b.double()
    m = 0.5 * (p + q)

    def k(x, y):
        x = x.clamp_min(1e-12)
        y = y.clamp_min(1e-12)
        return float((x * (x.log() - y.log())).sum())

    return 0.5 * k(p, m) + 0.5 * k(q, m)


def locpct(post, pre, prompts):
    return round(100 * sum(1 - js(post[p]["dist"], pre[p]["dist"]) / LN2 for p in prompts) / len(prompts), 2)


def cached_cov(layer_name):
    import numpy as np
    import torch

    path = Path(LLMDB_ROOT) / "covariance_caches" / "Qwen_Qwen2.5-3B" / "wikipedia_stats" / f"{layer_name}_float32_mom2_t100_100000.npz"
    data = np.load(path)
    return torch.from_numpy(data["mom2.mom2"]).float().to("cuda")


def compute_projectors(hp, layers):
    import torch

    ps = []
    diagnostics = {}
    for layer in layers:
        layer_name = hp.rewrite_module_tmp.format(layer)
        cov = cached_cov(layer_name).cpu()
        U, S, _ = torch.linalg.svd(cov, full_matrices=False)
        idx = (S < hp.nullspace_threshold).nonzero(as_tuple=True)[0]
        ps.append((U[:, idx] @ U[:, idx].T).cpu())
        diagnostics[str(layer)] = {
            "layer_name": layer_name,
            "threshold": hp.nullspace_threshold,
            "small_singular_count": int(idx.numel()),
            "singular_min": float(S.min()),
            "singular_max": float(S.max()),
        }
        del cov, U, S
    return ps, diagnostics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", default="Zorbland")
    ap.add_argument("--arms", default="A1_single,A2_coherent2")
    ap.add_argument("--window-size", type=int, default=50)
    ap.add_argument("--layers", default="4,5,6,7,8")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--lm-head-module", default=None, help="compatibility override for upstream hparams; does not edit upstream files")
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    AlphaEditAREHyperParams, upstream_main, upstream_cz = import_upstream()
    hp, hp_path = make_hparams(AlphaEditAREHyperParams, args.window_size)
    hp.layers = [int(x) for x in args.layers.split(",") if x]
    if args.lm_head_module:
        hp.lm_head_module = args.lm_head_module

    tok = AutoTokenizer.from_pretrained(ID, revision=REV, local_files_only=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        ID,
        revision=REV,
        torch_dtype=torch.float16,
        device_map="cuda",
        local_files_only=True,
    ).eval()

    subjects = [x.strip() for x in args.subjects.split(",") if x.strip()]
    arms = [x.strip() for x in args.arms.split(",") if x.strip()]
    cases = [load_case(arm, subj) for arm in arms for subj in subjects]
    batch_data = [{"question": c["question"], "answer": c["answer"]} for c in cases]

    pre = {f"{c['arm']}:{c['subject']}": eval_case(model, tok, c) for c in cases}
    locality_prompts = [f"{c['subject']} is described as" for c in cases]
    pre_loc = {p: predict(model, tok, p) for p in locality_prompts}
    before_weights = {
        str(layer): dict(model.named_parameters())[f"{hp.rewrite_module_tmp.format(layer)}.weight"].detach().float().norm().item()
        for layer in hp.layers
    }

    trace = {"compute_z": [], "stdout": ""}
    orig_compute_z = upstream_main.compute_z

    def traced_compute_z(model_, tok_, data, layer, hparams):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            idxs, targets = orig_compute_z(model_, tok_, data, layer, hparams)
        trace["stdout"] += buf.getvalue()
        target_ids = ids(tok_, data["answer"])
        trace["compute_z"].append(
            {
                "question": data["question"],
                "answer": data["answer"],
                "answer_ids": target_ids,
                "layer": layer,
                "idxs": [int(x) for x in idxs],
                "target_norms": [float(t.detach().float().norm().cpu()) for t in targets],
                "target_count": len(targets),
            }
        )
        return idxs, targets

    def traced_get_cov(model_, tok_, layer_name, *rest, **kwargs):
        return cached_cov(layer_name)

    upstream_main.compute_z = traced_compute_z
    upstream_main.get_cov = traced_get_cov
    P, p_diag = compute_projectors(hp, hp.layers)

    status = "OK"
    error = None
    try:
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            upstream_main.apply_AlphaEdit_ARE_to_model(model, tok, hp, batch_data, P=P)
        trace["stdout"] += buf.getvalue()
    except Exception as exc:
        status = "FAILED"
        error = repr(exc)
    finally:
        upstream_main.compute_z = orig_compute_z

    post = {f"{c['arm']}:{c['subject']}": eval_case(model, tok, c) for c in cases} if status == "OK" else {}
    post_loc = {p: predict(model, tok, p) for p in locality_prompts} if status == "OK" else {}
    after_weights = {
        str(layer): dict(model.named_parameters())[f"{hp.rewrite_module_tmp.format(layer)}.weight"].detach().float().norm().item()
        for layer in hp.layers
    }
    update_norms = {}
    npd = dict(model.named_parameters())
    # This reports norm before/after, not exact delta, because upstream overwrites
    # from internal weights_copy; exact deltas require a heavier external snapshot.
    for layer in hp.layers:
        update_norms[str(layer)] = {
            "weight_norm_before": before_weights[str(layer)],
            "weight_norm_after": after_weights[str(layer)],
        }

    result = {
        "decision_id": "D-C10i-anyedit-upstream-active-audit",
        "class": "diagnostic-only upstream active A1/A2 gate; not CORPUS evidence; no A7",
        "status": status,
        "error": error,
        "scope": "Qwen2.5-3B / upstream AlphaEdit_ARE code path / tiny A1-A2 controls / HF-fp16",
        "upstream_anyedit": {
            "root": ANYEDIT_ROOT,
            "hparams": hp_path,
            "algorithm": "AlphaEdit_ARE.apply_AlphaEdit_ARE_to_model",
            "covariance_source": "local cached Qwen_Qwen2.5-3B wikipedia_stats; upstream /tmp stats absent",
        },
        "hparams_effective": {
            "layers": hp.layers,
            "window_size": hp.window_size,
            "overlap": hp.overlap,
            "v_loss_layer": hp.v_loss_layer,
            "v_num_grad_steps": hp.v_num_grad_steps,
            "v_lr": hp.v_lr,
            "v_weight_decay": hp.v_weight_decay,
            "clamp_norm_factor": hp.clamp_norm_factor,
            "nullspace_threshold": hp.nullspace_threshold,
            "L2": hp.L2,
            "lm_head_module": hp.lm_head_module,
        },
        "cases": cases,
        "pre_behavior": pre,
        "post_behavior": post,
        "locality": {
            "prompts": locality_prompts,
            "described_as": locpct(post_loc, pre_loc, locality_prompts) if status == "OK" else None,
        },
        "projector_diagnostics": p_diag,
        "trace": trace,
        "update_norms": update_norms,
        "licensed_claim": "active upstream diagnostic only; A7 remains blocked unless A1/A2 recover behaviorally",
    }
    Path(args.out).write_text(json.dumps(result, indent=2, default=str))
    print(json.dumps({"status": status, "out": args.out, "error": error}, indent=2))
    print("C10I_UPSTREAM_ACTIVE_AUDIT_DONE")
    return 0 if status == "OK" else 2


if __name__ == "__main__":
    sys.exit(main())
