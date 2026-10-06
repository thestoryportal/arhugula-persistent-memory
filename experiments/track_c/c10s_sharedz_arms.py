#!/usr/bin/env python3
"""D-C10s-sharedz driver (docs/C10S_SHARED_Z_PREREG.md v3 FROZEN §2-§3): one target fit jointly over three phrasings.
  stage "first"  (default): cell 1 injection screen (canonical z vs shared z, paired, control c, fit diagnostic) -> inject.json;
                            if PROCEED, cell 2 harness pass A1 + A2 + A7 where the harness's own A7 (engine z) is the
                            reference and the A7 hook re-edits from base with the shared z through Z_OVERRIDE -> pass1.json.
  stage "second":           gate A replication of a LEAD/PARTIAL pass 1: a fresh shared solve + harness pass -> pass2.json.
Usage: LLMDB_ROOT=<root> .venv/bin/python experiments/track_c/c10s_sharedz_arms.py [first|second]
Env: LLMDB_ROOT, OUT_DIR (default results/c10s_sharedz). Requires OUT_DIR/inertness.json from c10s_sharedz_inertness.py (ALL INERT).
The engine is not edited; the shared solve below is driver-side and enters the harness only through Z_OVERRIDE.
"""
import os, sys, io, json, time, hashlib, contextlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
# [LAW:parse-dont-validate] §2: the driver refuses to start if any inherited harness knob is set (every env the harness reads, c10e_bandknob.py:25-36,40,62-63,254,477-482,582)
HARNESS_KNOBS = ("MODEL_ID", "MODEL_REV", "HP_CANDIDATE", "OUT", "CANDIDATE_NAME", "DECISION_ID", "PREREG", "RUN_LABEL", "C10_PROJECTOR",
                 "N_EDIT", "C10_SUBJECT_OFFSET", "C10_ARMS", "C10_KEY_LOCUS", "C10_CTX_TEMPLATES", "C10_RECIPES")
_set = [k for k in HARNESS_KNOBS if k in os.environ]
if _set:
    raise SystemExit(f"refusing to run with inherited harness knob(s) {_set}; the prereg fixes the harness defaults (§2)")
STAGE = sys.argv[1] if len(sys.argv) > 1 else "first"
if STAGE not in ("first", "second"):
    raise SystemExit(f"stage must be first|second, got {STAGE!r}")
ARMS_ENV = "A1_single,A2_coherent2,A7_coined_coined"
os.environ["C10_ARMS"] = ARMS_ENV
os.environ["C10_RECIPES"] = "candidate"
os.environ["HP_CANDIDATE"] = f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"
os.environ["CANDIDATE_NAME"] = "A7_sharedz"
os.environ["DECISION_ID"] = "D-C10s-sharedz"
os.environ["PREREG"] = f"{LLMDB_ROOT}/docs/C10S_SHARED_Z_PREREG.md"
OUT_DIR = os.environ.get("OUT_DIR", f"{LLMDB_ROOT}/results/c10s_sharedz"); os.makedirs(OUT_DIR, exist_ok=True)
os.environ["OUT"] = f"{OUT_DIR}/pass1.json"
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10s_sharedz_read as R                     # frozen forms + the pure rules (the reader owns every threshold)
import c10e_bandknob as H                         # loads the model; chdir to the engine root
from c10l_covgeom_p6_zinject import Inject, decode, Z_LAYER, hp, block   # the P6 hook, greedy decoder and z-layer, unchanged (same model object)
os.environ["C10_ARMS"] = ARMS_ENV                 # the P6 import rewrites C10_ARMS to A7 only after H is built; restored for the record
from c10l_mint_lib import sha256_tensor
import torch
from memit.compute_z import compute_z, find_fact_lookup_idx
from memit.memit_main import get_context_templates
from rome.repr_tools import get_words_idxs_in_templates, get_reprs_at_word_tokens
from util import nethook
from util.device import device_of

if R.CANON != H.CANON or R.PTEST != H.PTEST:   # [LAW:one-source-of-truth] the prereg's frozen strings must be the harness's (c10e_bandknob.py:51-56)
    raise SystemExit(f"frozen forms differ from the harness: reader CANON/PTEST {R.CANON!r}/{R.PTEST!r} vs harness {H.CANON!r}/{H.PTEST!r}")
CANON, PTEST, FRAMES, FRAME_NAMES = R.CANON, R.PTEST, R.FRAMES, R.FRAME_NAMES
V = H.ARMS["A7_coined_coined"]
# CORPUS/43 same-frame locality subjects, copied from c10p_twopass_arms.py:30 (importing that module requires LAW3_REF and rewrites the harness env)
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]
assert not set(FRAME_SUBJECTS) & set(H.FICTION)
KEY_TEMPLATES = [("CANON", CANON)] + [(f"PTEST{i}", p) for i, p in enumerate(PTEST)]
LOSS_STOP = 5e-2                 # compute_z.py:164 — the engine's stopping rule, verbatim (§2: nothing is tightened)
SOURCE_FILES = ["memit_dry_run/memit/memit/compute_z.py", "memit_dry_run/memit/memit/memit_main.py", "memit_dry_run/memit/memit/compute_ks.py",
                "memit_dry_run/memit/rome/repr_tools.py", "experiments/track_c/c10e_bandknob.py", "experiments/track_c/c10l_covgeom_p6_zinject.py",
                "experiments/track_c/c10s_sharedz_arms.py", "experiments/track_c/c10s_sharedz_inertness.py", "experiments/track_c/c10s_sharedz_read.py",
                "experiments/track_c/c10s_sharedz_selftest.py", "configs/hparams/qwen25_3b_memit_hparams.json", "docs/C10S_SHARED_Z_PREREG.md"]
ST = {}   # [LAW:no-shared-mutable-globals] written once per pass by run_pass (zs_shared, base_snap), read by the A7 hook


def quiet():
    return contextlib.redirect_stdout(io.StringIO())


def dump(path, obj):
    """Write JSON and re-read it (network-FS discipline: a write that did not persist is an error, not a warning)."""
    text = json.dumps(obj, indent=2, default=str)
    with open(path, "w") as f:
        f.write(text)
    with open(path) as f:
        back = f.read()
    if back != text:
        raise SystemExit(f"HALT: {path} re-read differs from what was written")   # [LAW:no-silent-failure]


def sha256_file(rel):
    h = hashlib.sha256()
    with open(f"{LLMDB_ROOT}/{rel}", "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fingerprint():
    """LAW#1 gate: tools/engine_fingerprint.py is the single source of the expected hash (as c10m_diag_arms.fingerprint)."""
    import subprocess
    fp = subprocess.run([sys.executable, f"{LLMDB_ROOT}/tools/engine_fingerprint.py"], capture_output=True, text=True, env={**os.environ, "LLMDB_ROOT": LLMDB_ROOT})
    if fp.returncode != 0:
        raise SystemExit(f"HALT: engine fingerprint FAIL:\n{fp.stdout}{fp.stderr}")   # [LAW:no-silent-failure]
    return fp.stdout.strip()


def subject_idx(template, subj):
    return get_words_idxs_in_templates(H.tok, [template], [subj], "last")[0][0]


def z_record(zs):
    stack = torch.stack([zs[c].float().cpu() for c in H.FICTION])
    return {"sha256": sha256_tensor(stack), "norms": [round(float(zs[c].float().norm()), 3) for c in H.FICTION]}


def compute_z_shared(model, tok, request, hparams, layer, context_templates, prompts):
    """The engine's compute_z (memit_dry_run/memit/memit/compute_z.py:14-185, read 2026-10-06) with a LIST of prompts in
    place of request["prompt"] (§2). Every line below mirrors the cited engine line; the only departures are the prompt
    list (:46-50 -> R.build_prompt_plan, template-major, prompts[0] first inside each template so index 0 is the identity
    template on prompts[0]), and the diagnostics gathered for the record. Returns (target, diag); diag keys starting
    with "_" hold tensors and are stripped before any JSON write."""
    lm_w, ln_f = (                                                                       # :28-31
        nethook.get_parameter(model, f"{hparams.lm_head_module}.weight").T,
        nethook.get_module(model, hparams.ln_f_module),
    )
    try:                                                                                 # :32-35
        lm_b = nethook.get_parameter(model, f"{hparams.lm_head_module}.bias")
    except LookupError:
        lm_b = next(model.parameters()).new_zeros(model.config.vocab_size)
    dev = device_of(model)                                                               # :36
    target_ids = tok(request["target_new"]["str"], return_tensors="pt").to(dev)["input_ids"][0]   # :41-43
    plan = R.build_prompt_plan(context_templates, prompts, tok.decode(target_ids[:-1]))  # :46-51 (context.format(prompt) + decode(target[:-1]); KL "{} is a" last)
    rewriting_prompts, kl_prompts, all_prompts = plan["rewriting"], plan["kl"], plan["all"]
    input_tok = tok(                                                                     # :53-57
        [prompt.format(request["subject"]) for prompt in all_prompts],
        return_tensors="pt",
        padding=True,
    ).to(dev)
    rewriting_targets = torch.tensor(-100, device=dev).repeat(                           # :60-65
        len(rewriting_prompts), *input_tok["input_ids"].shape[1:]
    )
    for i in range(len(rewriting_prompts)):
        ex_len = input_tok["attention_mask"][i].sum()
        rewriting_targets[i, ex_len - len(target_ids) : ex_len] = target_ids
    lookup_idxs = [                                                                      # :68-73 (per-prompt subject-last lookup index)
        find_fact_lookup_idx(prompt, request["subject"], tok, hparams.fact_token, verbose=(i == 0))
        for i, prompt in enumerate(all_prompts)
    ]
    loss_layer = max(hparams.v_loss_layer, layer)                                        # :76
    delta = torch.zeros((getattr(model.config, "hidden_size", None) or model.config.n_embd,), requires_grad=True, device=dev)   # :83
    target_init, kl_distr_init = None, None                                              # :84

    def edit_output_fn(cur_out, cur_layer):                                              # :87-101
        nonlocal target_init
        if cur_layer == hparams.layer_module_tmp.format(layer):
            if target_init is None:
                target_init = cur_out[0][0, lookup_idxs[0]].detach().clone()             # :95 — prompt 0 = (identity template, prompts[0]) = the clean CANON sentence
            for i, idx in enumerate(lookup_idxs):                                        # :98-99 — delta added at every prompt's own subject-last token
                cur_out[0][i, idx, :] += delta
        return cur_out

    opt = torch.optim.Adam([delta], lr=hparams.v_lr)                                     # :104
    nethook.set_requires_grad(False, model)                                              # :105
    history, clamp_hit_steps, nll_each_step0, stopped_by, nll_each = [], 0, None, "budget", None
    for it in range(hparams.v_num_grad_steps):                                           # :108
        opt.zero_grad()
        with nethook.TraceDict(                                                          # :112-122
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
            kl_logits = torch.stack(                                                     # :125-131 — the KL prompt is the last row (i - len(kl_prompts) = -1)
                [
                    logits[i - len(kl_prompts), idx, :]
                    for i, idx in enumerate(lookup_idxs[-len(kl_prompts) :])
                ],
                dim=0,
            )
            kl_log_probs = torch.nn.functional.log_softmax(kl_logits, dim=1)             # :132
            if kl_distr_init is None:                                                    # :133-134
                kl_distr_init = kl_log_probs.detach().clone()
        full_repr = tr[hparams.layer_module_tmp.format(loss_layer)].output[0][           # :137-139
            : len(rewriting_prompts)
        ]
        log_probs = torch.log_softmax(ln_f(full_repr) @ lm_w + lm_b, dim=2)              # :140
        loss = torch.gather(                                                             # :141-145
            log_probs,
            2,
            torch.where(rewriting_targets != -100, rewriting_targets, 0).unsqueeze(2),
        ).squeeze(2)
        mask = (rewriting_targets != -100).float()                                       # :146
        nll_loss_each = -(loss * mask).sum(1) / target_ids.size(0)                       # :149
        nll_loss = nll_loss_each.mean()                                                  # :150 — the mean over ALL rewriting prompts (every template x every frame)
        kl_loss = hparams.kl_factor * torch.nn.functional.kl_div(                        # :151-153
            kl_distr_init, kl_log_probs, log_target=True, reduction="batchmean"
        )
        weight_decay = hparams.v_weight_decay * (                                        # :154-156
            torch.norm(delta) / torch.norm(target_init) ** 2
        )
        loss = nll_loss + kl_loss + weight_decay                                         # :158
        nll_each = [float(x) for x in nll_loss_each.detach().float().cpu()]
        if nll_each_step0 is None:
            nll_each_step0 = nll_each
        history.append({"nll": float(nll_loss), "kl": float(kl_loss), "wd": float(weight_decay), "loss": float(loss)})
        if loss < LOSS_STOP:                                                             # :164-165 — the verbatim stopping rule: total loss (NLL + KL + weight decay) < 0.05
            stopped_by = "loss<0.05"
            break
        if it == hparams.v_num_grad_steps - 1:                                           # :167-168
            break
        loss.backward()                                                                  # :171-172
        opt.step()
        max_norm = hparams.clamp_norm_factor * target_init.norm()                        # :175-178 — the L2 ball is set by target_init (prompt 0), unchanged
        if delta.norm() > max_norm:
            clamp_hit_steps += 1
            with torch.no_grad():
                delta[...] = delta * max_norm / delta.norm()
    target = target_init + delta                                                         # :180
    max_norm = hparams.clamp_norm_factor * target_init.norm()
    diag = {"prompts": list(prompts), "all_prompts": all_prompts, "frame_idx": plan["frame_idx"], "lookup_idxs": [int(i) for i in lookup_idxs],
            "n_rewriting": len(rewriting_prompts), "adam_steps": it, "loss_evals": it + 1, "stopped_by": stopped_by, "history": history,
            "loss_at_stop": history[-1], "nll_each_stop": nll_each, "nll_each_step0": nll_each_step0,
            "frame_fit": R.frame_fit(nll_each, plan["frame_idx"], len(prompts)),
            "delta_norm": float(delta.norm()), "max_norm": float(max_norm), "clamp_hit": clamp_hit_steps > 0, "clamp_hit_steps": clamp_hit_steps,
            "target_init_norm": float(target_init.norm()), "target_norm": float(target.norm()),
            "_delta": delta.detach().clone(), "_target_init": target_init, "_kl_init": kl_distr_init}
    return target.detach(), diag


def diag_record(dg):
    return {k: v for k, v in dg.items() if not k.startswith("_")}


class AddDelta:
    """Control c (§2 cell 1, Codex item 2): the additive intervention h_prompt + delta at one position — the quantity the
    solve actually optimises (compute_z.py:98-99) — beside P6's absolute overwrite (Inject). Same hook mechanics."""
    def __init__(self, idx, delta):
        self.idx, self.delta, self.h = idx, delta, None

    def __enter__(self):
        def fn(_m, _i, out):
            hid = out[0] if isinstance(out, tuple) else out
            hid[0, self.idx, :] += self.delta.to(hid.dtype)
            return out
        self.h = block.register_forward_hook(fn)
        return self

    def __exit__(self, *a):
        self.h.remove()


def solve_shared(c, ctx):
    with quiet():
        z, dg = compute_z_shared(H.model, H.tok, H.req(CANON, c, V[c]), hp, Z_LAYER, ctx, FRAMES)
    return z, dg


@torch.no_grad()
def frame_probe(template):
    """CORPUS/43 same-frame locality (c10p_twopass_arms.frame_probe generalised to a frame): six never-edited fictional
    subjects; a flip = top-1 equals the first token of any edited A7 value. §2 cell 2: run in CANON and in each training frame."""
    firsts = {H.tgt_ids(V[c])[0] for c in H.FICTION}
    rows = []
    for s in FRAME_SUBJECTS:
        ids = H.tok(template.format(s), return_tensors="pt").to(H.DEV)
        t = int(H.model(**ids).logits[0, -1].argmax())
        rows.append({"subj": s, "top1": t, "tok": H.tok.decode([t]), "flip": t in firsts})
    return {"template": template, "flips": sum(r["flip"] for r in rows), "n": len(rows), "rows": rows}


def frame_probes():
    return {name: frame_probe(f) for name, f in zip(FRAME_NAMES, FRAMES)}


@torch.no_grad()
def key_cosines():
    """§2 cell 2 added readout: the subject-last-token key (the rewrite module's input, as compute_ks.py:19-37 /
    repr_tools.py:15-40 extract it, bare template) under each held-out template, cosine to the canonical key, per layer."""
    out = {}
    for layer in hp.layers:
        ks = {name: get_reprs_at_word_tokens(H.model, H.tok, [t] * len(H.FICTION), list(H.FICTION), layer, hp.rewrite_module_tmp, "last", track="in").float()
              for name, t in KEY_TEMPLATES}
        out[str(layer)] = {}
        for name, _ in KEY_TEMPLATES[1:]:
            cos = torch.nn.functional.cosine_similarity(ks[name], ks["CANON"], dim=1)
            out[str(layer)][name] = {"mean_cos": round(float(cos.mean()), 4), "per_subject": [round(float(x), 4) for x in cos]}
    return out


@torch.no_grad()
def h_at_canon(c):
    """The z-layer output at the subject-last token of the bare CANON prompt (what my_edit reads as `cur`, c10e_bandknob.py:197-201)."""
    return get_reprs_at_word_tokens(H.model, H.tok, [CANON], [c], Z_LAYER, hp.layer_module_tmp, "last", track="out")[0].float()


def injection_cell(ctx):
    """§2 cell 1: canonical z (engine compute_z) and shared z solved in one process on the same templates; both injected
    at the keyed position on CANON + the three held-out templates (P6 mechanics); control c; fit diagnostic."""
    t0 = time.time()
    rows, fits, zs_c, zs_s, diags = [], {}, {}, {}, {}
    control = {name: {"additive": {"canonical": 0, "shared": 0}, "absolute": {"canonical": 0, "shared": 0}} for name in FRAME_NAMES}
    for c in H.FICTION:
        val = V[c]; tids = H.tgt_ids(val)
        with quiet():
            z_c = compute_z(H.model, H.tok, H.req(CANON, c, val), hp, Z_LAYER, ctx).detach()
        z_s, dg = solve_shared(c, ctx)
        zs_c[c], zs_s[c], diags[c], fits[c] = z_c, z_s, diag_record(dg), dg["frame_fit"]
        h_c = h_at_canon(c)
        targets = {"canonical": z_c, "shared": z_s}
        deltas = {"canonical": z_c.float() - h_c, "shared": dg["_delta"].float()}   # the engine returns only z; its delta is recovered against the plain-forward h (noted in the record)
        per_t = []
        for t in [CANON] + PTEST:
            prompt = t.format(c); idx = subject_idx(t, c)
            r = {"template": t, "idx": idx, "keyed_tok": H.tok.decode(H.tok(prompt)["input_ids"][idx]), "base_full": decode(prompt, len(tids)) == tids}
            for name, z in targets.items():
                with Inject(idx, z):
                    gen = decode(prompt, len(tids)); gen2 = decode(prompt, len(tids) + 2)
                r[f"{name}_full"] = gen == tids; r[f"{name}_first"] = gen[0] == tids[0]
                r[f"{name}_string"] = H.tok.decode(gen2).startswith(" " + val); r[f"{name}_text"] = H.tok.decode(gen2)
            per_t.append(r)
        ctrl = {}
        for fname, f in zip(FRAME_NAMES, FRAMES):
            prompt = f.format(c); idx = subject_idx(f, c); ctrl[fname] = {}
            for name in targets:
                with Inject(idx, targets[name]):
                    absolute = decode(prompt, len(tids)) == tids
                with AddDelta(idx, deltas[name]):
                    additive = decode(prompt, len(tids)) == tids
                ctrl[fname][name] = {"absolute": absolute, "additive": additive}
                control[fname]["absolute"][name] += absolute; control[fname]["additive"][name] += additive
        rows.append({"subj": c, "val": val, "ntok": len(tids), "z_canonical_norm": round(float(z_c.float().norm()), 3), "z_shared_norm": round(float(z_s.float().norm()), 3),
                     "delta_canonical_norm_vs_plain_h": round(float(deltas["canonical"].norm()), 3), "per_template": per_t, "control_c": ctrl, "shared_solve": diags[c]})
        print(f"  {c:10} {val:22} canon-template inj canonical={per_t[0]['canonical_full']} shared={per_t[0]['shared_full']} | held-out canonical={[r['canonical_full'] for r in per_t[1:]]} "
              f"shared={[r['shared_full'] for r in per_t[1:]]} | fit {[round(x, 4) for x in fits[c]]} steps {dg['adam_steps']} clamp {dg['clamp_hit']} ({time.time()-t0:.0f}s)", flush=True)
    screen = R.paired_screen([{"subj": r["subj"], "canon": [x["canonical_full"] for x in r["per_template"][1:]], "shared": [x["shared_full"] for x in r["per_template"][1:]]} for r in rows])
    fit = R.fit_diagnostic(fits)
    out = {"decision_id": os.environ["DECISION_ID"], "prereg": os.environ["PREREG"], "cell": "1 injection screen", "z_layer": Z_LAYER, "hparams": H.HP_BASE,
           "n_subjects": len(rows), "frames": dict(zip(FRAME_NAMES, FRAMES)), "ctx": ctx, "screen": screen, "fit_diagnostic": fit,
           "canon_template_inj": {name: sum(r["per_template"][0][f"{name}_full"] for r in rows) for name in ("canonical", "shared")},
           "held_out_first": {name: sum(sum(x[f"{name}_first"] for x in r["per_template"][1:]) for r in rows) for name in ("canonical", "shared")},
           "held_out_string": {name: sum(sum(x[f"{name}_string"] for x in r["per_template"][1:]) for r in rows) for name in ("canonical", "shared")},
           "base_full_without_injection": sum(sum(x["base_full"] for x in r["per_template"]) for r in rows),
           "control_c": control, "clamp_hits": sum(d["clamp_hit"] for d in diags.values()), "mean_steps": round(sum(d["adam_steps"] for d in diags.values()) / len(diags), 2),
           "zs_canonical": z_record(zs_c), "zs_shared": z_record(zs_s), "rows": rows, "seconds": round(time.time() - t0)}
    out["outcome"] = R.cell1_outcome(fit, screen)
    return out, zs_s, diags, fit


def hook(arm_name, Vmap):
    """§2 cell 2: after the harness's own A7 (engine z — the reference) is evaluated and still applied: its added readouts;
    then back to base, a fresh edit from the SAME requests/P aimed at the shared z through Z_OVERRIDE, the full readout."""
    if arm_name != "A7_coined_coined":
        return {}
    t0 = time.time(); st = H._ARM_STATE
    out = {"override_hits_before": H.Z_OVERRIDE_HITS, "frame_probe_ref": frame_probes(), "key_cosine_ref": key_cosines()}
    H.restore_layers(st["hp"], ST["base_snap"])                                   # the reference edit is undone; the shared edit starts from base
    cache = [torch.zeros(st["P"][0].shape[0], st["P"][0].shape[0]) for _ in st["hp"].layers]   # a fresh sequential cache, as run_recipe builds it (c10e_bandknob.py:474)
    H.Z_OVERRIDE = {(c, " " + V[c]): ST["zs_shared"][c] for c in H.FICTION}      # the seam, c10e_bandknob.py:186-189; keyed as H.req keys requests
    try:
        with quiet():
            delta = H.my_edit(st["hp"], st["requests"], st["P"], cache)
    finally:
        H.Z_OVERRIDE = None
    shared = H.eval_arm(Vmap)
    shared["locality_described_as"] = H.locpct({p: H.predict(p) for p in st["pre_prompts"]}, st["pre_loc"], st["pre_prompts"])
    shared["locality_axes"] = H.axes_post(st["pre_axes"], list(Vmap.values()))
    out.update({"shared": {k: v for k, v in shared.items() if k != "rows"}, "shared_rows": shared["rows"], "shared_delta_norms": delta,
                "frame_probe_shared": frame_probes(), "key_cosine_shared": key_cosines(), "override_hits_after": H.Z_OVERRIDE_HITS})
    ax = shared["locality_axes"]; fr = out["frame_probe_shared"]
    print(f"  shared z: canon {shared['canon_full_n']}/24 para {shared['para_full_n']}/72 first {shared['para_first_n']} string {shared['para_string_n']} | "
          f"L1 {ax['L1_flipped_to_edited_value']}/12 frame {fr['CANON']['flips']}/{fr['T1']['flips']}/{fr['T2']['flips']} described_as {shared['locality_described_as']} "
          f"L3 {ax['L3_top1_agree']}/30 ppl {ax['generic_ppl_post']} | dW {[round(v['delta_norm'], 1) for v in delta.values()]} | hits {H.Z_OVERRIDE_HITS} ({time.time()-t0:.0f}s)", flush=True)
    return out


def run_pass(name, zs_shared, solve_record):
    H.OUT = f"{OUT_DIR}/pass{name}.json"; H.Z_OVERRIDE = None; H.Z_OVERRIDE_HITS = 0; H.ARM_HOOKS[:] = [hook]
    ST["zs_shared"] = zs_shared; ST["base_snap"] = H.snap_layers(hp)                # the model is unedited here (injection hooks only; the harness restores after a pass)
    pre = {"key_cosine": key_cosines(), "frame_probes": frame_probes()}
    t0 = time.time(); print(f"=== PASS {name}: A1 + A2 + A7 (engine z = reference; hook: shared z through Z_OVERRIDE)", flush=True)
    rc = H.main()
    if rc != 0 or not os.path.exists(H.OUT):
        raise SystemExit(f"HALT: harness returned {rc} in pass {name} (result file {'present' if os.path.exists(H.OUT) else 'absent — stimulus halt?'})")   # [LAW:no-silent-failure]
    res = json.load(open(H.OUT))
    res.update({"pass": name, "z_override_hits_total": H.Z_OVERRIDE_HITS, "sharedz": solve_record, "pre_edit": pre})
    dump(H.OUT, res)
    a7 = res["recipes"][H.CANDIDATE_NAME]["arms"]["A7_coined_coined"]
    print(f"=== PASS {name} done: reference A7 canon {a7['canon_full_n']}/24 para {a7['para_full_n']}/72; shared para {a7['extra']['shared']['para_full_n']}/72 ({time.time()-t0:.0f}s)", flush=True)
    return res


def require_inertness():
    p = f"{OUT_DIR}/inertness.json"
    if not os.path.exists(p):
        raise SystemExit(f"HALT: {p} missing — run c10s_sharedz_inertness.py first (§2 LAW#5 (i)-(v))")
    rec = json.load(open(p))
    if not rec.get("ok") or any(not rec["checks"].get(c, {}).get("ok") for c in R.INERTNESS_CHECKS):
        raise SystemExit(f"HALT: inertness record not ALL INERT: { {c: rec['checks'].get(c, {}).get('ok') for c in R.INERTNESS_CHECKS} }")
    return rec


def seeds():
    return {"torch_initial_seed": torch.initial_seed(), "explicit_seeding": "none — the harness and engine do not seed; context templates are sampled unseeded per process (CORPUS/44 F-A4) and recorded in `ctx`"}


def solve_all_shared(ctx):
    zs, diags, fits = {}, {}, {}
    for c in H.FICTION:
        z, dg = solve_shared(c, ctx); zs[c], diags[c], fits[c] = z, diag_record(dg), dg["frame_fit"]
    return zs, {"zs_shared": z_record(zs), "fit_diagnostic": R.fit_diagnostic(fits), "per_fact": diags}


def main():
    t0 = time.time()
    fp = fingerprint(); inert = require_inertness()
    ctx = get_context_templates(H.model, H.tok)
    forms = {"CANON": CANON, "T1": R.T1, "T2": R.T2}
    overlap = R.overlap_table(forms, PTEST)
    if overlap["total_shared"] != 0:
        raise SystemExit(f"HALT: the §2 overlap rule fails: {overlap}")   # [LAW:no-silent-failure]
    c0 = H.FICTION[0]
    run_path = f"{OUT_DIR}/run.json"
    if STAGE == "first":
        run = {"decision_id": os.environ["DECISION_ID"], "prereg": os.environ["PREREG"], "candidate_name": H.CANDIDATE_NAME, "stage": STAGE, "z_layer": Z_LAYER, "hparams": H.HP_BASE,
               "fingerprint": fp, "inertness": inert, "ctx": ctx, "seeds": seeds(),
               "training_forms": {k: {"form": v, "sha256": R.sha256_text(v)} for k, v in forms.items()},
               "training_forms_joined_sha256": R.sha256_text("\n".join(forms.values())),
               "held_out_forms": {"PTEST": PTEST, "sha256": R.sha256_text("\n".join(PTEST))},
               "overlap_table": overlap, "withdrawn_v1_form": {"form": R.V1_WITHDRAWN, "overlap": R.overlap_table({"T1_v1": R.V1_WITHDRAWN}, PTEST)},
               "kl_prefix_note": {"note": "under the identity template T2's subject-last-token position shares its prefix with the KL prompt '{} is a' (§2); indices for the first subject",
                                  "subject": c0, "T2_idx": subject_idx(R.T2, c0), "kl_prompt_idx": subject_idx(R.KL_PROMPT, c0)},
               "frame_subjects": FRAME_SUBJECTS, "source_sha256": {f: sha256_file(f) for f in SOURCE_FILES}, "passes": {}}
        dump(run_path, run)
        print("=== CELL 1: injection screen", flush=True)
        inj, zs_shared, diags, fit = injection_cell(ctx)
        dump(f"{OUT_DIR}/inject.json", inj)
        sc = inj["screen"]
        print(f"cell 1: canonical {sc['canon_n']}/72 shared {sc['shared_n']}/72 gain {sc['gain']} templates won {sc['templates_won']} subjects won {sc['subjects_won']} "
              f"| fit min {fit['min_fit']:.4f} underfit {len(fit['underfit'])} | control c {inj['control_c']} -> {inj['outcome']}", flush=True)
        run["cell1_outcome"] = inj["outcome"]; run["inject"] = f"{OUT_DIR}/inject.json"
        dump(run_path, run)
        if inj["outcome"] != "PROCEED":
            print(f"{inj['outcome']}: the write arm is not run (§2 cell 1); this candidate configuration was not advanced", flush=True)
            print("C10S_SHAREDZ_DONE", flush=True); return 0
        run_pass("1", zs_shared, {"zs_shared": inj["zs_shared"], "fit_diagnostic": fit, "per_fact": diags}); run["passes"]["1"] = H.OUT
    else:
        run = json.load(open(run_path))
        if "1" not in run["passes"] or not os.path.exists(f"{OUT_DIR}/pass1.json"):
            raise SystemExit("HALT: stage second needs a completed pass 1")
        pr1 = R.read_pass(json.load(open(f"{OUT_DIR}/pass1.json")))
        bad = R.validity(run, pr1, "1")
        if bad:
            raise SystemExit(f"HALT: pass 1 is INVALID, no second process: {bad}")
        gates = R.locality_gates(pr1["ref"], pr1["shared"], pr1["frames_ref"], pr1["frames_shared"])
        lab = R.label(pr1["shared"]["para_full_n"], pr1["ref"]["para_full_n"], all(gates.values()), pr1["dw_shared"] / pr1["dw_ref"])
        if lab.split("-")[0] not in ("LEAD", "PARTIAL"):
            raise SystemExit(f"HALT: pass 1 label {lab} does not call for a second process (§2 cell 3: PARTIAL or LEAD only)")
        print(f"=== SECOND PROCESS (gate A) for pass 1 label {lab}", flush=True)
        zs_shared, rec = solve_all_shared(ctx)
        run["second_process"] = {"fingerprint": fp, "ctx": ctx, "seeds": seeds(), "zs_shared": rec["zs_shared"], "fit_diagnostic": rec["fit_diagnostic"], "pass1_label": lab}
        dump(run_path, run)
        run_pass("2", zs_shared, rec); run["passes"]["2"] = H.OUT
    run["seconds"] = round(time.time() - t0)
    dump(run_path, run)
    print(f"wrote {run_path}; read with: c10s_sharedz_read.py {OUT_DIR}", flush=True)
    print("C10S_SHAREDZ_DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
