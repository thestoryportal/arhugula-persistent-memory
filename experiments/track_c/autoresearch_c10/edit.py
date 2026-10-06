"""
Autoresearch edit recipe. Single-file. The agent modifies this file.
Writes 24 (subject -> value) facts into Qwen2.5-3B's MLP weights; the fixed evaluation scores the changed weights.
Baseline: one batched MEMIT-style write with an AlphaEdit null-space projector over layers 4-8 (the harness's own edit).
Everything this file does, including its top-level setup below, counts against the edit budget in prepare.py.
Usage: .venv/bin/python edit.py

Methods the baseline implements:
  ROME      Meng, Bau, Andonian, Belinkov. Locating and Editing Factual Associations in GPT. arXiv:2202.05262
  MEMIT     Meng, Sen Sharma, Andonian, Belinkov, Bau. Mass-Editing Memory in a Transformer. arXiv:2210.07229
  AlphaEdit Fang et al. AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models. arXiv:2410.02355
"""

import torch

from prepare import (model, tok, DEV, COV_LAYERS, request, load_hparams, evaluate,
                     compute_z, compute_ks, get_module_input_output_at_words, get_cov, get_context_templates,
                     upd_matrix_match_shape)

# ---------------------------------------------------------------------------
# Hyperparameters (edit these directly, no CLI flags needed)
# ---------------------------------------------------------------------------

LAYERS = [4, 5, 6, 7, 8]    # contiguous MLP down_proj layers to write; the target vector z is solved at the last one (covariance caches: 4..12)
V_NUM_GRAD_STEPS = 25       # gradient steps that solve each target vector z
V_LR = 0.5                  # learning rate of the z solve
CLAMP_NORM_FACTOR = 0.75    # max ||delta z|| as a fraction of ||z_init||
KL_FACTOR = 0.0625          # weight of the KL term that keeps "<subject> is a" stable during the z solve
V_WEIGHT_DECAY = 0.5        # L2 on delta z during the solve
RIDGE = 1.0                 # L2 added to the per-layer least-squares solve
NULL_THRESH = 0.005         # eigenvalues of the key covariance below this span the projector's null space

# ---------------------------------------------------------------------------
# Setup: hyperparameters, projectors
# ---------------------------------------------------------------------------

assert all(l in COV_LAYERS for l in LAYERS), f"LAYERS must lie within {COV_LAYERS}"
HP = load_hparams(layers=LAYERS, v_num_grad_steps=V_NUM_GRAD_STEPS, v_lr=V_LR, clamp_norm_factor=CLAMP_NORM_FACTOR,
                  kl_factor=KL_FACTOR, v_weight_decay=V_WEIGHT_DECAY)


def projector(layer):
    """AlphaEdit projector onto the null space of the layer's key covariance: writes there leave typical keys unchanged."""
    cov = get_cov(model, tok, HP.rewrite_module_tmp.format(layer), HP.mom2_dataset, HP.mom2_n_samples, HP.mom2_dtype).cpu().float()
    U, S, _ = torch.linalg.svd(cov, full_matrices=False)
    idx = (S < NULL_THRESH).nonzero(as_tuple=True)[0]
    return (U[:, idx] @ U[:, idx].T).cpu()


P = [projector(l) for l in LAYERS]
WEIGHTS = {l: dict(model.named_parameters())[f"{HP.rewrite_module_tmp.format(l)}.weight"] for l in LAYERS}

# ---------------------------------------------------------------------------
# The edit
# ---------------------------------------------------------------------------


def apply_edit(facts):
    """Write facts = [(subject, value)] into the model in place."""
    requests = [request(s, v) for s, v in facts]
    ctx = get_context_templates(model, tok)
    z_layer = LAYERS[-1]
    zs = torch.stack([compute_z(model, tok, rq, HP, z_layer, ctx) for rq in requests], dim=1)   # target hidden state per fact
    cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in LAYERS]
    for i, layer in enumerate(LAYERS):
        K = compute_ks(model, tok, requests, HP, layer, ctx).T          # keys at this layer, one column per (fact, template)
        cur = get_module_input_output_at_words(model, tok, z_layer, context_templates=[rq["prompt"] for rq in requests],
                                               words=[rq["subject"] for rq in requests], module_template=HP.layer_module_tmp,
                                               fact_token_strategy=HP.fact_token)[1].T
        resid = (zs - cur).repeat_interleave(K.size(1) // zs.size(1), dim=1) / (len(LAYERS) - i)   # spread the remaining gap over the remaining layers
        Kf, rf = K.float().cpu(), resid.float().cpu()
        A = P[i] @ (Kf @ Kf.T + cache[i]) + RIDGE * torch.eye(Kf.shape[0])
        B = P[i] @ Kf @ rf.T
        upd = upd_matrix_match_shape(torch.linalg.solve(A, B).T.float(), WEIGHTS[layer].shape)
        with torch.no_grad():
            WEIGHTS[layer][...] += upd.to(WEIGHTS[layer].device, WEIGHTS[layer].dtype)
    for i, layer in enumerate(LAYERS):   # accumulate the written keys (used only if a later write reuses this cache)
        K = compute_ks(model, tok, requests, HP, layer, ctx).T.float().cpu()
        cache[i] = cache[i] + K @ K.T


# ---------------------------------------------------------------------------
# Evaluate (fixed; prints the summary block)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    evaluate(apply_edit)
