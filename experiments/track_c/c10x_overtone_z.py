"""OverTone token objective; engine imports remain inside the live solver."""
import torch

AUDIT_SINK = None
LAST_STEP = None


def token_losses(raw_logits, log_probs, labels, ce, lam, eps, n_sigma):
    from c10x_enginepath_inertness import Halt
    scored = labels != -100
    s = raw_logits[scored].detach().float()
    ids = labels[scored]
    chosen_ce = ce[scored]
    if not s.numel() or not torch.isfinite(s).all() or not torch.isfinite(log_probs[scored]).all():
        raise Halt('NONFINITE_OR_EMPTY_SCORED_LOGITS')
    with torch.no_grad():
        keep = s > s.max(-1, keepdim=True).values - n_sigma*s.std(-1, correction=1, keepdim=True)
        if not keep.any(-1).all():
            raise Halt('EMPTY_OVERTONE_KEEP_SET '+str(s.cpu().tolist()))
        filtered = torch.softmax(s.masked_fill(~keep, -torch.inf), -1)
        onehot = torch.zeros_like(s).scatter_(1, ids[:, None], 1.)
        cand = lam*onehot + (1-lam)*filtered
        mix = cand.argmax(-1) == ids
        pi_tar = torch.where(mix[:, None], cand, onehot).detach()
    extra = torch.zeros_like(chosen_ce)
    if mix.any():
        p = pi_tar[mix]
        entropy = torch.zeros_like(p)
        positive = p > 0
        entropy[positive] = torch.xlogy(p[positive], p[positive])
        term = entropy.sum(-1) - ((p-onehot[mix])*log_probs[scored][mix].float()).sum(-1)
        extra[mix] = term.to(chosen_ce.dtype)
    kl = chosen_ce + extra
    clipped = torch.where(kl > eps, kl, eps)
    if not torch.isfinite(clipped).all():
        raise Halt('NONFINITE_OVERTONE_LOSS')
    loss = torch.zeros_like(ce)
    loss[scored] = clipped
    return loss, {'keep': keep, 'mix': mix, 'pi_tar': pi_tar, 'extra': extra,
                  'kl': kl, 'loss': clipped, 'positions': scored.nonzero(),
                  'probabilities': log_probs[scored].detach().float().exp().gather(1, ids[:, None]).squeeze(1)}


def compute_z_overtone(model, tok, request, hparams, layer, context_templates, lam, eps, n_sigma):
    import numpy as np
    from rome import repr_tools
    from util import nethook
    from util.device import device_of
    from memit.compute_z import find_fact_lookup_idx
    global LAST_STEP
    lm_w, ln_f = (
        nethook.get_parameter(model, f"{hparams.lm_head_module}.weight").T,
        nethook.get_module(model, hparams.ln_f_module),
    )
    try:
        lm_b = nethook.get_parameter(model, f"{hparams.lm_head_module}.bias")
    except LookupError as _:
        lm_b = next(model.parameters()).new_zeros(model.config.vocab_size)
    dev = device_of(model)  # P-8

    print("Computing right vector (v)")

    # Tokenize target into list of int token IDs
    target_ids = tok(request["target_new"]["str"], return_tensors="pt").to(dev)[
        "input_ids"
    ][0]

    # Compile list of rewriting and KL x/y pairs
    rewriting_prompts, kl_prompts = [
        context.format(request["prompt"]) + tok.decode(target_ids[:-1])
        for context_types in context_templates
        for context in context_types
    ], ["{} is a"]
    all_prompts = rewriting_prompts + kl_prompts

    input_tok = tok(
        [prompt.format(request["subject"]) for prompt in all_prompts],
        return_tensors="pt",
        padding=True,
    ).to(dev)

    # Compute rewriting targets
    rewriting_targets = torch.tensor(-100, device=dev).repeat(
        len(rewriting_prompts), *input_tok["input_ids"].shape[1:]
    )
    for i in range(len(rewriting_prompts)):
        ex_len = input_tok["attention_mask"][i].sum()
        rewriting_targets[i, ex_len - len(target_ids) : ex_len] = target_ids

    # Compute indices of the tokens where the fact is looked up
    lookup_idxs = [
        find_fact_lookup_idx(
            prompt, request["subject"], tok, hparams.fact_token, verbose=(i == 0)
        )
        for i, prompt in enumerate(all_prompts)
    ]

    # Finalize rewrite and loss layers
    loss_layer = max(hparams.v_loss_layer, layer)
    print(f"Rewrite layer is {layer}")
    print(f"Tying optimization objective to {loss_layer}")

    # Set up an optimization over a latent vector that, when output at the
    # rewrite layer, i.e. hypothesized fact lookup location, will induce the
    # target token to be predicted at the final layer.
    delta = torch.zeros((getattr(model.config, 'hidden_size', None) or (getattr(model.config, 'hidden_size', None) or model.config.n_embd),), requires_grad=True, device=dev)
    target_init, kl_distr_init = None, None

    # Inserts new "delta" variable at the appropriate part of the computation
    def edit_output_fn(cur_out, cur_layer):
        nonlocal target_init

        if cur_layer == hparams.layer_module_tmp.format(layer):
            # Store initial value of the vector of interest
            if target_init is None:
                print("Recording initial value of v*")
                # Initial value is recorded for the clean sentence
                target_init = cur_out[0][0, lookup_idxs[0]].detach().clone()

            # Add intervened delta
            for i, idx in enumerate(lookup_idxs):
                cur_out[0][i, idx, :] += delta

        return cur_out

    # Optimizer
    opt = torch.optim.Adam([delta], lr=hparams.v_lr)
    nethook.set_requires_grad(False, model)

    # Execute optimization
    for it in range(hparams.v_num_grad_steps):
        opt.zero_grad()

        # Forward propagation
        with nethook.TraceDict(
            module=model,
            layers=[
                hparams.layer_module_tmp.format(loss_layer),
                hparams.layer_module_tmp.format(layer),
            ],
            retain_input=False,
            retain_output=True,
            edit_output=edit_output_fn,
        ) as tr:
            logits = model(**input_tok).logits

            # Compute distribution for KL divergence
            kl_logits = torch.stack(
                [
                    logits[i - len(kl_prompts), idx, :]
                    for i, idx in enumerate(lookup_idxs[-len(kl_prompts) :])
                ],
                dim=0,
            )
            kl_log_probs = torch.nn.functional.log_softmax(kl_logits, dim=1)
            if kl_distr_init is None:
                kl_distr_init = kl_log_probs.detach().clone()

        # Compute loss on rewriting targets
        full_repr = tr[hparams.layer_module_tmp.format(loss_layer)].output[0][
            : len(rewriting_prompts)
        ]
    # This factorization is explicitly authorized at prereg :53.
        raw_logits = ln_f(full_repr) @ lm_w + lm_b
        log_probs = torch.log_softmax(raw_logits, dim=2)
        loss = torch.gather(
            log_probs,
            2,
            torch.where(rewriting_targets != -100, rewriting_targets, 0).unsqueeze(2),
        ).squeeze(2)
        mask = (rewriting_targets != -100).float()
        tok_loss, audit = token_losses(raw_logits, log_probs, rewriting_targets, -loss, lam, eps, n_sigma)
        nll_loss_each = (tok_loss * mask).sum(1) / target_ids.size(0)
        LAST_STEP = {'step': it, 'probabilities': audit['probabilities'].detach().cpu().tolist(),
                     'positions': audit['positions'].detach().cpu().tolist(),
                     'prompts': [p.format(request['subject']) for p in rewriting_prompts]}
        if AUDIT_SINK is not None:
            AUDIT_SINK(it, {'logits': raw_logits[rewriting_targets != -100].detach().cpu().clone(),
                           'log_probs': log_probs[rewriting_targets != -100].detach().cpu().clone(),
                           'labels': rewriting_targets[rewriting_targets != -100].detach().cpu().clone(),
                           'ce': (-loss)[rewriting_targets != -100].detach().cpu().clone(),
                           'mask': mask.detach().cpu().clone(),
                           'positions': audit['positions'].detach().cpu().clone(),
                           'keep': audit['keep'].detach().cpu().clone(),
                           'mix': audit['mix'].detach().cpu().clone(),
                           'loss': audit['loss'].detach().cpu().clone(),
                           'pi_tar': audit['pi_tar'].detach().cpu().clone(),
                           'settings': {'lam':lam,'eps':eps,'n_sigma':n_sigma}})
        nll_loss = nll_loss_each.mean()
        kl_loss = hparams.kl_factor * torch.nn.functional.kl_div(
            kl_distr_init, kl_log_probs, log_target=True, reduction="batchmean"
        )
        weight_decay = hparams.v_weight_decay * (
            torch.norm(delta) / torch.norm(target_init) ** 2
        )
        # weight_decay = hparams.v_weight_decay * torch.norm(delta) ** 2
        loss = nll_loss + kl_loss + weight_decay
        print(
            f"loss {np.round(loss.item(), 3)} = {np.round(nll_loss.item(), 3)} + {np.round(kl_loss.item(), 3)} + {np.round(weight_decay.item(), 3)} "
            f"avg prob of [{request['target_new']['str']}] "
            f"{torch.exp(-nll_loss_each).mean().item()}"
        )
        if loss < 5e-2:
            break

        if it == hparams.v_num_grad_steps - 1:
            break

        # Backpropagate
        loss.backward()
        opt.step()

        # Project within L2 ball
        max_norm = hparams.clamp_norm_factor * target_init.norm()
        if delta.norm() > max_norm:
            with torch.no_grad():
                delta[...] = delta * max_norm / delta.norm()

    target = target_init + delta
    print(
        f"Init norm {target_init.norm()} | Delta norm {delta.norm()} | Target norm {target.norm()}"
    )

    return target


def verify_solver_ast(path):
    import ast
    from pathlib import Path
    engine = next(n for n in ast.parse(Path(path).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'compute_z')
    own = next(n for n in ast.parse(Path(__file__).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'compute_z_overtone')
    import copy
    own=copy.deepcopy(own)
    own.body=[n for n in own.body if not isinstance(n,(ast.Import,ast.ImportFrom,ast.Global))]
    expected=[n for n in engine.body if not (isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str))]
    loop=next(n for n in own.body if isinstance(n,ast.For) and ast.unparse(n.target)=='it')
    reference=next(n for n in expected if isinstance(n,ast.For) and ast.unparse(n.target)=='it')
    start=next(i for i,n in enumerate(loop.body) if isinstance(n,ast.Assign) and ast.unparse(n.targets[0])=='raw_logits')
    end=next(i for i,n in enumerate(loop.body) if isinstance(n,ast.Assign) and ast.unparse(n.targets[0])=='nll_loss')
    block=loop.body[start:end+1]
    original=[n for n in reference.body if 140<=n.lineno<=150]
    if ast.dump(block[0].value)!=ast.dump(original[0].value.args[0]):return False
    if ast.unparse(block[1])!='log_probs = torch.log_softmax(raw_logits, dim=2)':return False
    if ast.dump(block[2])!=ast.dump(original[1]) or ast.dump(block[3])!=ast.dump(original[2]):return False
    if ast.unparse(block[4])!='tok_loss, audit = token_losses(raw_logits, log_probs, rewriting_targets, -loss, lam, eps, n_sigma)':return False
    if ast.unparse(block[5])!='nll_loss_each = (tok_loss * mask).sum(1) / target_ids.size(0)':return False
    if ast.dump(block[-1])!=ast.dump(original[-1]):return False
    # LAST_STEP and AUDIT_SINK are detached observations between the authorized
    # reduction and the unchanged engine mean, never replacements for a solve.
    if ast.unparse(block[6].targets[0])!='LAST_STEP' or not isinstance(block[7],ast.If) or ast.unparse(block[7].test)!='AUDIT_SINK is not None':return False
    loop.body[start:end+1]=copy.deepcopy(original)
    return ast.dump(ast.Module(body=own.body,type_ignores=[]))==ast.dump(ast.Module(body=expected,type_ignores=[]))
