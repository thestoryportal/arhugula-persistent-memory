#!/usr/bin/env python3
"""D-C10s-sharedz driver (docs/C10S_SHARED_Z_PREREG.md v3 FROZEN §2-§3, §7 A1): one target fit jointly over three phrasings.
  stage "first"  (default): cell 1 injection screen (canonical z vs shared z, paired, control c, fit diagnostic) -> inject.json;
                            if PROCEED, cell 2 harness pass A1 + A2 + A7 where the harness's own A7 (engine z) is the
                            reference and the A7 hook re-edits from base with the shared z through Z_OVERRIDE -> pass1.json.
  stage "second":           gate A replication of a LEAD/PARTIAL pass 1: a fresh shared solve (fit checked BEFORE any write)
                            + harness pass -> pass2.json.
Usage: LLMDB_ROOT=<root> .venv/bin/python experiments/track_c/c10s_sharedz_arms.py [first|second]
Env: LLMDB_ROOT, C10S_ARM=sharedz|solvefeas (default sharedz), OUT_DIR (default results/c10s_<arm>). Requires OUT_DIR/inertness.json from c10s_sharedz_inertness.py
(ALL INERT, same source hashes). The engine is not edited; the shared solve below is driver-side and enters the harness
only through Z_OVERRIDE.
The solvefeas arm implements docs/C10S_SOLVEFEAS_PREREG.md v2: one 50-evaluation settings file for every solve,
same-run evaluation-25 snapshots, read-only engine forward counts and the reader's additional frozen labels.

v2 changes (implementation review results/c10s_sharedz_codex_impl_v1.md, all six items implemented):
  1. check (iv) reference reduces exactly as compute_z.py:141-149 through R.engine_nll_each; KL(ref||init) recorded, not gated
     (the slice check is the lookup-index check) — in c10s_sharedz_inertness.py.
  2. reader applies every locality gate and -LARGE-WRITE to each process before a replicated label (c10s_sharedz_read.py).
  3. stage second evaluates the fit diagnostic before the write; UNDERFIT -> nothing written, HALT diagnostic, exit non-zero.
  4. every completed pass is validated at once (controls, envelope, Z_OVERRIDE hits, files); every SystemExit path goes
     through halt(), which writes architecture_profile/c10s_sharedz_halt_diagnostic.json; the inertness script writes its
     record progressively.
  5. provenance: the inertness record carries the source hashes; the driver refuses to proceed if any differs from the
     current files; one run identity (timestamp + hashes) is stamped into every output; the reader refuses to pair
     records with different identities; occupied stage outputs are never overwritten (use a new OUT_DIR).
  6. control c adds the fp32 delta to the fp32-upcast activation and casts once (the arithmetic of the solver's in-place
     `+=`, compute_z.py:98-99); the canonical delta is RECONSTRUCTED as z_engine - target_init, where target_init is
     captured by a read-only forward hook (the hook captures target_init, not the optimizer's delta; no bitwise recovery
     of the canonical optimizer delta is claimed); the z_engine - h_plain reconstruction is recorded beside it with the
     equivalence numbers; the shared control uses the saved optimizer delta.
v3 changes (review 2, results/c10s_sharedz_codex_impl_v2.md):
  - the second process is permanent and authoritative: stage second writes second_process = {started, identity,
    outcome: STARTED} into run.json BEFORE solving; UNDERFIT is terminal (outcome UNDERFIT with the fit numbers, no
    pass2.json); a later `second` invocation refuses to start whenever second_process exists (any outcome); the reader
    consults the outcome before treating a missing pass2.json as pending (c10s_sharedz_read.verdict).
  - halt coverage: the model-loading imports (harness, P6 hook, engine) are wrapped in a try/except that writes the HALT
    diagnostic with the import error text and the identity (None before main) and exits non-zero; the only statements
    outside any halt boundary are the stdlib imports and the definition of halt() itself.
  - inertness (iv) gains a second, same-padded-batch delta-zero reference beside the frozen unpadded one (record only).
  7. §7 A1: the remaining-residual ratio ||z - cur_after|| / ||z - cur_before|| at the z-layer keyed position is recorded
     for every arm (A1, A2, A7-reference, A7-shared); `cur` is re-read after the edit exactly as my_edit:197-201 reads it
     before. The engine targets my_edit solved are captured by rebinding the harness MODULE's `compute_z` name to a
     recording pass-through for the duration of the pass (the harness file and the engine function are untouched; the
     pass-through returns the engine's tensor unchanged) — flagged for the second review as the one addition the
     review did not name; the alternative (re-solving 48 targets before the pass) is inexact and ~15 min.
  Disagreements: none implemented differently from the review's fixes. One note on item 6: the review's explicit
  upcast-add-cast and the engine's `cur_out[0][i, idx, :] += delta` are the same arithmetic under torch's in-place
  type promotion (compute in the promoted dtype, write cast once); the explicit form is used so the record states it.
"""
import os, sys, io, json, time, hashlib, contextlib, datetime, traceback
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
DECISION_ID = "D-C10s-sharedz"
HALT_PATH = f"{LLMDB_ROOT}/architecture_profile/c10s_sharedz_halt_diagnostic.json"   # review item 4: every SystemExit path writes it
STAGE = sys.argv[1] if len(sys.argv) > 1 else "first"
IDENTITY = None   # [LAW:no-shared-mutable-globals] the run identity; written once by main (or by the inertness script's own), read by halt/dump stamps


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


def write_json(path, obj):
    """Write JSON and re-read it (network-FS discipline: a write that did not persist is an error, not a warning).
    Returns the text written; raises RuntimeError on a mismatch (halt() catches that case itself)."""
    text = json.dumps(obj, indent=2, default=str)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    with open(path) as f:
        back = f.read()
    if back != text:
        raise RuntimeError(f"{path} re-read differs from what was written")
    return text


def halt(reason, **state):
    """The one exit for every failure (review item 4): the diagnostic JSON carries the reason, the stage, the identity
    and the full state the caller hands over; then SystemExit (non-zero)."""
    rec = {**globals().get("RECORD_SETTINGS", {}), "decision_id": DECISION_ID, "stage": STAGE, "when_utc": utc_now(), "reason": reason, "identity": IDENTITY, "state": state}
    try:
        write_json(HALT_PATH, rec)
        where = HALT_PATH
    except Exception as e:   # the diagnostic itself could not be persisted: say so loudly beside the original reason
        where = f"NOT WRITTEN ({e!r})"
    raise SystemExit(f"HALT: {reason} (diagnostic: {where})")


def dump(path, obj):
    obj.update(RECORD_SETTINGS)
    try:
        write_json(path, obj)
    except RuntimeError as e:
        halt(str(e), path=path)


sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10s_sharedz_read as R
try:
    ARM = R.select_arm(os.environ.get("C10S_ARM", "sharedz"))
except ValueError as e:   # an unknown arm owns no halt file; writing one here would overwrite step 1's (advisor impl review, BLOCKING 1)
    raise SystemExit(f"HALT: {e} (no diagnostic written: the arm is unknown)")
DECISION_ID = ARM.decision_id
HALT_PATH = f"{LLMDB_ROOT}/{ARM.halt_path}"
HP_PATH = f"{LLMDB_ROOT}/{ARM.hparams}"
try:
    with open(HP_PATH, "rb") as f:
        HP_SHA256 = hashlib.sha256(f.read()).hexdigest()
except OSError as e:
    halt(f"cannot read the arm's settings: {e}", hparams=HP_PATH)
ARM_RECORD = {"arm": ARM.name, "decision_id": DECISION_ID, "prereg": f"{LLMDB_ROOT}/{ARM.prereg}",
              "hparams": HP_PATH, "hparams_sha256": HP_SHA256, "v_num_grad_steps": ARM.steps}
RECORD_SETTINGS = ARM_RECORD if ARM.name == "solvefeas" else {}   # default record schema remains 1169794's

# [LAW:parse-dont-validate] §2: the driver refuses to start if any inherited harness knob is set (every env the harness reads, c10e_bandknob.py:25-36,40,62-63,254,477-482,582)
HARNESS_KNOBS = ("MODEL_ID", "MODEL_REV", "HP_CANDIDATE", "OUT", "CANDIDATE_NAME", "DECISION_ID", "PREREG", "RUN_LABEL", "C10_PROJECTOR",
                 "N_EDIT", "C10_SUBJECT_OFFSET", "C10_ARMS", "C10_KEY_LOCUS", "C10_CTX_TEMPLATES", "C10_RECIPES")
_set = {k: os.environ[k] for k in HARNESS_KNOBS if k in os.environ}
if _set:
    halt(f"inherited harness knob(s) set: {sorted(_set)}; the prereg fixes the harness defaults (§2)", knobs=_set)
if STAGE not in ("first", "second"):
    halt(f"stage must be first|second, got {STAGE!r}", argv=sys.argv)
ARMS_ENV = "A1_single,A2_coherent2,A7_coined_coined"
os.environ["C10_ARMS"] = ARMS_ENV
os.environ["C10_RECIPES"] = "candidate"
os.environ["HP_CANDIDATE"] = HP_PATH
os.environ["CANDIDATE_NAME"] = "A7_sharedz"
os.environ["DECISION_ID"] = DECISION_ID
os.environ["PREREG"] = ARM_RECORD["prereg"]
OUT_DIR = os.environ.get("OUT_DIR", f"{LLMDB_ROOT}/{ARM.out_dir}"); os.makedirs(OUT_DIR, exist_ok=True)
os.environ["OUT"] = f"{OUT_DIR}/pass1.json"
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
try:   # v3: the model-loading imports sit inside the halt boundary — an initialization failure writes the diagnostic too
    import c10s_sharedz_read as R                     # frozen forms + the pure rules (the reader owns every threshold)
    import c10e_bandknob as H                         # loads the model; chdir to the engine root
    from c10l_covgeom_p6_zinject import Inject, decode, Z_LAYER, hp, block   # the P6 hook, greedy decoder and z-layer, unchanged (same model object)
    os.environ["C10_ARMS"] = ARMS_ENV                 # the P6 import rewrites C10_ARMS to A7 only after H is built; restored for the record
    from c10l_mint_lib import sha256_tensor
    import torch
    from memit.compute_z import compute_z, find_fact_lookup_idx, get_module_input_output_at_words
    from memit.memit_main import get_context_templates
    from rome.repr_tools import get_words_idxs_in_templates, get_reprs_at_word_tokens
    from util import nethook
    from util.device import device_of
    from memit.memit_hparams import MEMITHyperParams
    hp = MEMITHyperParams.from_json(HP_PATH)           # P6's hp is the baseline; rebind from the CLOSED arm instead
    assert hp.v_num_grad_steps == ARM.steps, (hp.v_num_grad_steps, ARM.steps)
    assert H.HP_BAND == HP_PATH, (H.HP_BAND, HP_PATH)  # the harness recipe and every driver-side solve use the same file
except SystemExit:
    raise
except BaseException as e:
    halt(f"initialization failed before main: {type(e).__name__}: {e}", traceback=traceback.format_exc(), env_knobs_forced={k: os.environ[k] for k in HARNESS_KNOBS if k in os.environ})

if R.CANON != H.CANON or R.PTEST != H.PTEST:   # [LAW:one-source-of-truth] the prereg's frozen strings must be the harness's (c10e_bandknob.py:51-56)
    halt("frozen forms differ from the harness", reader={"CANON": R.CANON, "PTEST": R.PTEST}, harness={"CANON": H.CANON, "PTEST": H.PTEST})
CANON, PTEST, FRAMES, FRAME_NAMES = R.CANON, R.PTEST, R.FRAMES, R.FRAME_NAMES
V = H.ARMS["A7_coined_coined"]
# CORPUS/43 same-frame locality subjects, copied from c10p_twopass_arms.py:30 (importing that module requires LAW3_REF and rewrites the harness env)
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]
assert not set(FRAME_SUBJECTS) & set(H.FICTION)
KEY_TEMPLATES = [("CANON", CANON)] + [(f"PTEST{i}", p) for i, p in enumerate(PTEST)]
LOSS_STOP = 5e-2                 # compute_z.py:164 — the engine's stopping rule, verbatim (§2: nothing is tightened)
SOURCE_FILES = ["experiments/track_c/c10s_sharedz_arms.py", "experiments/track_c/c10s_sharedz_inertness.py", "experiments/track_c/c10s_sharedz_read.py",
                "experiments/track_c/c10s_sharedz_selftest.py", "experiments/track_c/c10e_bandknob.py", "memit_dry_run/memit/memit/compute_z.py",
                "memit_dry_run/memit/memit/memit_main.py",   # ^ the seven files the review names (item 5); the rest are recorded and compared too
                "memit_dry_run/memit/memit/compute_ks.py", "memit_dry_run/memit/rome/repr_tools.py", "experiments/track_c/c10l_covgeom_p6_zinject.py",
                "configs/hparams/qwen25_3b_memit_hparams.json", "docs/C10S_SHARED_Z_PREREG.md"] + (
                ["configs/hparams/qwen25_3b_memit_hparams_steps50.json", "docs/C10S_SOLVEFEAS_PREREG.md"] if ARM.name == "solvefeas" else [])
STAGE_OUTPUTS = ("run.json", "inject.json", "pass1.json", "pass2.json")
ST = {}   # [LAW:no-shared-mutable-globals] per-pass state written by run_pass (zs_shared, base_snap, cur_before, captured), read by the A7 hook
_engine_compute_z = compute_z
ENGINE_SOLVES = []   # solvefeas: read-only forward counts, including the nested engine path inside the harness LAW#5 gate


def quiet():
    return contextlib.redirect_stdout(io.StringIO())


def sha256_file(rel):
    h = hashlib.sha256()
    with open(f"{LLMDB_ROOT}/{rel}", "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_hashes():
    return {f: sha256_file(f) for f in SOURCE_FILES}


def make_identity(**extra):
    """Review item 5: one run identity — UTC timestamp + a digest of every source hash — stamped into every output."""
    hashes = source_hashes(); ts = utc_now()
    digest = hashlib.sha256("\n".join(f"{k} {v}" for k, v in sorted(hashes.items())).encode()).hexdigest()
    return {**RECORD_SETTINGS, "run_id": f"{ts}-{digest[:12]}", "created_utc": ts, "source_digest": digest, "source_sha256": hashes, **extra}


class CountForwards:
    """A root-module forward hook: count evaluations without inspecting or returning any activation."""
    def __init__(self, module):
        self.module, self.count, self.handle = module, 0, None

    def __enter__(self):
        def count(_module, _inputs, _output):
            self.count += 1
        self.handle = self.module.register_forward_hook(count)
        return self

    def __exit__(self, *args):
        self.handle.remove()


def engine_solve(model, tok, request, hparams, layer, context_templates, role="engine"):
    if ARM.name == "sharedz":
        return _engine_compute_z(model, tok, request, hparams, layer, context_templates)
    assert hparams.v_num_grad_steps == ARM.steps, (hparams.v_num_grad_steps, ARM.steps)
    with CountForwards(model) as counter:
        z = _engine_compute_z(model, tok, request, hparams, layer, context_templates)
    record = {**ARM_RECORD, "role": role, "subject": request["subject"], "prompt": request["prompt"],
              "target": request["target_new"]["str"], "layer": layer, "loss_evals": counter.count}
    if not 1 <= counter.count <= ARM.steps:
        halt("engine forward-count hook failed", solve=record)
    ENGINE_SOLVES.append(record)
    return z


@contextlib.contextmanager
def count_nested_engine_solves():
    """LAW#5 calls both memit_main.compute_z and H.compute_z; neither source file is edited."""
    if ARM.name == "sharedz":
        yield
        return
    from memit import memit_main as engine_main
    old_engine, old_harness = engine_main.compute_z, H.compute_z
    engine_main.compute_z = engine_solve
    if H.compute_z is _engine_compute_z:
        H.compute_z = engine_solve
    try:
        yield
    finally:
        engine_main.compute_z, H.compute_z = old_engine, old_harness


def provenance_mismatches(recorded):
    """Files whose current SHA-256 differs from a recorded identity's (review item 5)."""
    now = source_hashes()
    return {f: {"recorded": recorded.get(f), "current": now.get(f)} for f in set(recorded) | set(now) if recorded.get(f) != now.get(f)}


def fingerprint():
    """LAW#1 gate: tools/engine_fingerprint.py is the single source of the expected hash (as c10m_diag_arms.fingerprint)."""
    import subprocess
    fp = subprocess.run([sys.executable, f"{LLMDB_ROOT}/tools/engine_fingerprint.py"], capture_output=True, text=True, env={**os.environ, "LLMDB_ROOT": LLMDB_ROOT})
    if fp.returncode != 0:
        halt("engine fingerprint FAIL", stdout=fp.stdout, stderr=fp.stderr)   # [LAW:no-silent-failure]
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
    snapshot25, delta25, target25 = None, None, None

    def snapshot(evaluation):
        saved_delta = delta.detach().clone()
        saved_z = (target_init + saved_delta).detach()
        return ({"evaluation": evaluation, "requested_evaluation": 25, "carried_forward": evaluation < 25,
                 "frame_fit": R.frame_fit(nll_each, plan["frame_idx"], len(prompts)),
                 "delta": saved_delta.float().cpu().tolist(), "delta_norm": float(saved_delta.norm()),
                 "z_sha256": sha256_tensor(saved_z.float().cpu()), "z_norm": float(saved_z.norm())}, saved_delta, saved_z)

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
        nll_loss_each = R.engine_nll_each(log_probs, rewriting_targets, target_ids.size(0))   # :141-149 (gather, float32 mask, sum, / len(target)) — the one reduction, shared with the inertness reference
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
        if ARM.name == "solvefeas":
            history[-1].update(evaluation=it + 1, nll_each=list(nll_each))
            if it + 1 == 25:                                                            # before evaluation 25's update: the 25-step engine's final state
                snapshot25, delta25, target25 = snapshot(it + 1)
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
    diag = {**RECORD_SETTINGS, "prompts": list(prompts), "all_prompts": all_prompts, "frame_idx": plan["frame_idx"], "lookup_idxs": [int(i) for i in lookup_idxs],
            "n_rewriting": len(rewriting_prompts), "adam_steps": it, "loss_evals": it + 1, "stopped_by": stopped_by, "history": history,
            "loss_at_stop": history[-1], "nll_each_stop": nll_each, "nll_each_step0": nll_each_step0,
            "frame_fit": R.frame_fit(nll_each, plan["frame_idx"], len(prompts)),
            "delta_norm": float(delta.norm()), "max_norm": float(max_norm), "clamp_hit": clamp_hit_steps > 0, "clamp_hit_steps": clamp_hit_steps,
            "target_init_norm": float(target_init.norm()), "target_norm": float(target.norm()),
            "_delta": delta.detach().clone(), "_target_init": target_init, "_kl_init": kl_distr_init}
    if ARM.name == "solvefeas":
        if snapshot25 is None:                                                         # objective-stopped before 25; both budgets return this state
            snapshot25, delta25, target25 = snapshot(it + 1)
        diag.update(snapshot_25=snapshot25, _delta_25=delta25, _target_25=target25)
    return target.detach(), diag


def diag_record(dg):
    return {k: v for k, v in dg.items() if not k.startswith("_")}


class CaptureTargetInit:
    """Read-only forward hook on the z-layer block: records the output at [0, idx] of the FIRST forward only — the very
    tensor the engine clones as target_init (compute_z.py:92-95; nethook's Trace is itself a forward hook registered
    later, so this one runs first and sees the raw output; at the first forward delta is zero in any case). Nothing is
    modified. (review item 6)"""
    def __init__(self, idx):
        self.idx, self.value, self.h = idx, None, None

    def __enter__(self):
        def fn(_m, _i, out):
            if self.value is None:
                hid = out[0] if isinstance(out, tuple) else out
                self.value = hid[0, self.idx, :].detach().clone()
        self.h = block.register_forward_hook(fn)
        return self

    def __exit__(self, *a):
        self.h.remove()


class AddDelta:
    """Control c (§2 cell 1, Codex item 2): the additive intervention h_prompt + delta at one position — the quantity the
    solve optimises. Arithmetic as the solver's `cur_out[0][i, idx, :] += delta` (compute_z.py:98-99): an fp32 delta added
    in place to the fp16 activation computes in the promoted dtype (fp32) and is cast once on the write; written out
    explicitly here so the record states it (review item 6). Same hook mechanics as P6's Inject."""
    def __init__(self, idx, delta):
        self.idx, self.delta, self.h = idx, delta.float(), None

    def __enter__(self):
        def fn(_m, _i, out):
            hid = out[0] if isinstance(out, tuple) else out
            hid[0, self.idx, :] = (hid[0, self.idx, :].float() + self.delta).to(hid.dtype)
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


def read_cur(requests):
    """`cur` exactly as my_edit reads it before the write (c10e_bandknob.py:197-201): the z-layer module output at the
    subject-last token of each request's prompt, (d, n). §7 A1 re-reads it after the edit with this same call."""
    return get_module_input_output_at_words(
        H.model, H.tok, Z_LAYER, context_templates=[rq["prompt"] for rq in requests],
        words=[rq["subject"] for rq in requests], module_template=hp.layer_module_tmp,
        fact_token_strategy=hp.fact_token
    )[1].T


def residual_ratio(zs, cur_before, cur_after, subjects):
    """§7 A1: ||z - cur_after|| / ||z - cur_before|| per subject and over the stack (Frobenius), fp32 on CPU. Readout only."""
    z, b, a = zs.float().cpu(), cur_before.float().cpu(), cur_after.float().cpu()
    rb, ra = (z - b).norm(dim=0), (z - a).norm(dim=0)
    return {"overall": float((z - a).norm() / (z - b).norm()), "per_subject": {s: round(float(ra[i] / rb[i]), 5) for i, s in enumerate(subjects)},
            "residual_before_norms": [round(float(x), 3) for x in rb], "residual_after_norms": [round(float(x), 3) for x in ra]}


def injection_cell(ctx):
    """§2 cell 1: canonical z (engine compute_z) and shared z solved in one process on the same templates; both injected
    at the keyed position on CANON + the three held-out templates (P6 mechanics); control c; fit diagnostic."""
    t0 = time.time()
    engine_start = len(ENGINE_SOLVES)
    rows, fits, zs_c, zs_s, diags, twin_rows, twin_dist = [], {}, {}, {}, {}, [], {}
    control = {name: {"additive": {"canonical": 0, "shared": 0}, "absolute": {"canonical": 0, "shared": 0}} for name in FRAME_NAMES}
    ctx_trip = R.ctx_triplicate(ctx)   # §7 A2 (vi): the unmodified engine at the shared solve's batch shape, this process's templates
    for c in H.FICTION:
        val = V[c]; tids = H.tgt_ids(val); rq = H.req(CANON, c, val)
        with quiet(), CaptureTargetInit(subject_idx(CANON, c)) as cap:
            z_c = engine_solve(H.model, H.tok, rq, hp, Z_LAYER, ctx, role="canonical").detach()
        canonical_solve = ENGINE_SOLVES[-1] if ARM.name == "solvefeas" else None
        if cap.value is None:
            halt("target_init capture hook never fired", subject=c)
        z_s, dg = solve_shared(c, ctx)
        zs_c[c], zs_s[c], diags[c], fits[c] = z_c, z_s, diag_record(dg), dg["frame_fit"]
        with quiet():
            z_twin = engine_solve(H.model, H.tok, rq, hp, Z_LAYER, ctx_trip, role="noise twin").detach()   # §7 A2 (vi) noise twin
        twin_solve = ENGINE_SOLVES[-1] if ARM.name == "solvefeas" else None
        twin_hits = []
        for t in PTEST:
            with Inject(subject_idx(t, c), z_twin):
                twin_hits.append(decode(t.format(c), len(tids)) == tids)
        twin_rows.append({"subj": c, "shared": twin_hits})                                  # "canon" filled from per_t below
        twin_dist[c] = {"rel_l2_vs_canonical": float((z_twin.float() - z_c.float()).norm() / z_c.float().norm())}
        h_plain = read_cur([rq])[:, 0]
        # v3 naming (review 2 item b): the hook captures target_init, NOT the optimizer's delta. The canonical delta below is a
        # subtraction-based reconstruction z_engine - target_init (compute_z.py:180 returns target_init + delta in fp32, so the
        # subtraction is the natural estimate, not a demonstrated bitwise recovery); the h_plain reconstruction is recorded beside it.
        delta_recon_ti = z_c.float() - cap.value.float()                  # reconstructed (z_engine - target_init)
        delta_recon_h = z_c.float() - h_plain.float()                     # reconstructed (z_engine - h_plain), v1's form
        equiv = {"rel_l2_target_init_vs_h_plain": float((cap.value.float() - h_plain.float()).norm() / cap.value.float().norm()),
                 "rel_l2_recon_target_init_vs_recon_h_plain": float((delta_recon_ti - delta_recon_h).norm() / delta_recon_ti.norm())}
        targets = {"canonical": z_c, "shared": z_s}
        deltas = {"canonical": delta_recon_ti, "shared": dg["_delta"].float()}   # shared: the saved optimizer delta
        per_t = []
        for t in [CANON] + PTEST:
            prompt = t.format(c); idx = subject_idx(t, c)
            r = {"template": t, "idx": idx, "keyed_tok": H.tok.decode(H.tok(prompt)["input_ids"][idx]), "base_full": decode(prompt, len(tids)) == tids}
            for name, z in targets.items():
                with Inject(idx, z):
                    gen = decode(prompt, len(tids)); gen2 = decode(prompt, len(tids) + 2)
                r[f"{name}_full"] = gen == tids; r[f"{name}_first"] = gen[0] == tids[0]
                r[f"{name}_string"] = H.tok.decode(gen2).startswith(" " + val); r[f"{name}_text"] = H.tok.decode(gen2)
            if ARM.name == "solvefeas" and t in PTEST:
                with Inject(idx, dg["_target_25"]):
                    r["shared_at25_full"] = decode(prompt, len(tids)) == tids            # recorded only: never enters the screen or fit gate
            per_t.append(r)
        twin_rows[-1]["canon"] = [x["canonical_full"] for x in per_t[1:]]                   # the twin is paired with this fact's canonical z on the held-out templates
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
                     "canonical_delta": {"used_by_control_c": "reconstructed (z_engine - target_init); target_init captured by the read-only hook; not the optimizer's delta",
                                         "reconstructed (z_engine - target_init)": round(float(delta_recon_ti.norm()), 3),
                                         "reconstructed (z_engine - h_plain)": round(float(delta_recon_h.norm()), 3), "equivalence": equiv},
                     "shared_delta": {"used_by_control_c": "saved optimizer delta (_delta)", "norm": round(float(dg["_delta"].float().norm()), 3)},
                     "per_template": per_t, "control_c": ctrl, "shared_solve": diags[c]})
        if ARM.name == "solvefeas":
            rows[-1].update(canonical_solve=canonical_solve, noise_twin_solve=twin_solve)
        print(f"  {c:10} {val:22} canon-template inj canonical={per_t[0]['canonical_full']} shared={per_t[0]['shared_full']} | held-out canonical={[r['canonical_full'] for r in per_t[1:]]} "
              f"shared={[r['shared_full'] for r in per_t[1:]]} | fit {[round(x, 4) for x in fits[c]]} steps {dg['adam_steps']} clamp {dg['clamp_hit']} "
              f"| target_init vs h_plain rel {equiv['rel_l2_target_init_vs_h_plain']:.2e} ({time.time()-t0:.0f}s)", flush=True)
    screen = R.paired_screen([{"subj": r["subj"], "canon": [x["canonical_full"] for x in r["per_template"][1:]], "shared": [x["shared_full"] for x in r["per_template"][1:]]} for r in rows])
    fit = R.fit_diagnostic(fits)
    twin = {**R.noise_twin_verdict(twin_rows), "rows": twin_rows, "z_distance": twin_dist}
    out = {**RECORD_SETTINGS, "decision_id": DECISION_ID, "prereg": os.environ["PREREG"], "identity": IDENTITY, "cell": "1 injection screen", "z_layer": Z_LAYER, "hparams": HP_PATH,
           "n_subjects": len(rows), "frames": dict(zip(FRAME_NAMES, FRAMES)), "ctx": ctx, "screen": screen, "fit_diagnostic": fit,
           "canon_template_inj": {name: sum(r["per_template"][0][f"{name}_full"] for r in rows) for name in ("canonical", "shared")},
           "held_out_first": {name: sum(sum(x[f"{name}_first"] for x in r["per_template"][1:]) for r in rows) for name in ("canonical", "shared")},
           "held_out_string": {name: sum(sum(x[f"{name}_string"] for x in r["per_template"][1:]) for r in rows) for name in ("canonical", "shared")},
           "base_full_without_injection": sum(sum(x["base_full"] for x in r["per_template"]) for r in rows),
           "control_c": control, "clamp_hits": sum(d["clamp_hit"] for d in diags.values()), "mean_steps": round(sum(d["adam_steps"] for d in diags.values()) / len(diags), 2),
           "max_rel_l2_target_init_vs_h_plain": max(r["canonical_delta"]["equivalence"]["rel_l2_target_init_vs_h_plain"] for r in rows),
           "zs_canonical": z_record(zs_c), "zs_shared": z_record(zs_s), "rows": rows, "seconds": round(time.time() - t0)}
    out["noise_twin"] = twin
    out["outcome"] = R.cell1_outcome(fit, twin, screen)
    if ARM.name == "solvefeas":
        out["engine_solves"] = ENGINE_SOLVES[engine_start:]
        out["solvefeas"] = R.solvefeas_reading(diags)
        out["solve_budget"] = R.solve_budget(out["engine_solves"], diags, ARM_RECORD)
        out["evaluation_25_injection"] = {"shared_n": sum(sum(x["shared_at25_full"] for x in r["per_template"][1:]) for r in rows),
                                           "per_template": {t: sum(r["per_template"][k + 1]["shared_at25_full"] for r in rows) for k, t in enumerate(PTEST)},
                                           "record_only": True}
        out["outcome"] = R.solvefeas_cell1_outcome(out["solvefeas"], twin, screen, out["solve_budget"])
    return out, zs_s, diags, fit


def recording_compute_z(*args, **kwargs):
    """§7 A1 (v2 item 7): a pass-through that records the engine targets my_edit solves, bound to the harness module's
    `compute_z` name for the duration of a pass only. The engine function is called unchanged and its tensor returned as is."""
    z = engine_solve(*args, **kwargs, role="harness")
    ST["captured"].append(z.detach().clone())
    if ARM.name == "solvefeas":
        ST["captured_solves"].append(ENGINE_SOLVES[-1])
    return z


def hook(arm_name, Vmap):
    """Runs after each arm's evaluation with the harness's edit still applied (c10e_bandknob.py:494-495).
    Every arm: §7 A1 remaining-residual ratio for the engine edit. A7 additionally (§2 cell 2): the reference's added
    readouts; then back to base, a fresh edit from the SAME requests/P aimed at the shared z through Z_OVERRIDE, the full
    readout and its own residual ratio."""
    t0 = time.time(); st = H._ARM_STATE; n = len(st["requests"])
    if len(ST["captured"]) < n:
        halt("fewer engine solves captured than requests", arm=arm_name, captured=len(ST["captured"]), requests=n)
    zs_eng = torch.stack(ST["captured"][-n:], dim=1)                                   # the arm's own solves, in request order, stacked as my_edit stacks them (:191)
    subjects = [rq["subject"] for rq in st["requests"]]
    out = {"captured_solves_total": len(ST["captured"]), "residual_ref": residual_ratio(zs_eng, ST["cur_before"], read_cur(st["requests"]), subjects)}
    if ARM.name == "solvefeas":
        out.update(ARM_RECORD)
        out["engine_solves"] = ST["captured_solves"][-n:]
    print(f"  {arm_name}: §7 A1 remaining-residual ratio {out['residual_ref']['overall']:.4f}", flush=True)
    if arm_name != "A7_coined_coined":
        return out
    out.update({"override_hits_before": H.Z_OVERRIDE_HITS, "frame_probe_ref": frame_probes(), "key_cosine_ref": key_cosines()})
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
    zs_sh = torch.stack([ST["zs_shared"][c] for c in H.FICTION], dim=1)
    out.update({"shared": {k: v for k, v in shared.items() if k != "rows"}, "shared_rows": shared["rows"], "shared_delta_norms": delta,
                "frame_probe_shared": frame_probes(), "key_cosine_shared": key_cosines(), "override_hits_after": H.Z_OVERRIDE_HITS,
                "residual_shared": residual_ratio(zs_sh, ST["cur_before"], read_cur(st["requests"]), subjects)})
    ax = shared["locality_axes"]; fr = out["frame_probe_shared"]
    print(f"  shared z: canon {shared['canon_full_n']}/24 para {shared['para_full_n']}/72 first {shared['para_first_n']} string {shared['para_string_n']} | "
          f"L1 {ax['L1_flipped_to_edited_value']}/12 frame {fr['CANON']['flips']}/{fr['T1']['flips']}/{fr['T2']['flips']} described_as {shared['locality_described_as']} "
          f"L3 {ax['L3_top1_agree']}/30 ppl {ax['generic_ppl_post']} | dW {[round(v['delta_norm'], 1) for v in delta.values()]} | residual {out['residual_shared']['overall']:.4f} "
          f"| hits {H.Z_OVERRIDE_HITS} ({time.time()-t0:.0f}s)", flush=True)
    return out


def run_pass(name, run, zs_shared, solve_record):
    """One harness pass; the completed pass is validated at once (review item 4) and the result stamped with the identity."""
    H.OUT = f"{OUT_DIR}/pass{name}.json"
    if os.path.exists(H.OUT):
        halt(f"{H.OUT} exists; stage outputs are never overwritten — use a new OUT_DIR", path=H.OUT)   # review item 5
    H.Z_OVERRIDE = None; H.Z_OVERRIDE_HITS = 0; H.ARM_HOOKS[:] = [hook]
    engine_start = len(ENGINE_SOLVES)
    solve_record.update(RECORD_SETTINGS)
    ST.update(zs_shared=zs_shared, base_snap=H.snap_layers(hp), captured=[], captured_solves=[],  # the model is unedited here (injection hooks only; the harness restores after a pass)
              cur_before=read_cur([H.req(CANON, c, V[c]) for c in H.FICTION]))         # §7 A1: `cur` before any write, read as my_edit:197-201 reads it (prompt + subject only, so one read serves every arm)
    pre = {"key_cosine": key_cosines(), "frame_probes": frame_probes()}
    t0 = time.time(); print(f"=== PASS {name}: A1 + A2 + A7 (engine z = reference; hook: shared z through Z_OVERRIDE)", flush=True)
    H.compute_z = recording_compute_z                                                   # v2 item 7: record the targets my_edit solves (pass-through)
    try:
        with count_nested_engine_solves():
            rc = H.main()
    finally:
        H.compute_z = _engine_compute_z; H.ARM_HOOKS[:] = []
    if rc != 0 or not os.path.exists(H.OUT):
        halt(f"harness returned {rc} in pass {name}", result_file_present=os.path.exists(H.OUT), note="absent file = the harness's stimulus halt")
    res = json.load(open(H.OUT))
    res.update({"pass": name, "identity": {**IDENTITY, "pass_started_utc": utc_now()}, "z_override_hits_total": H.Z_OVERRIDE_HITS, "sharedz": solve_record, "pre_edit": pre,
                "captured_engine_solves": len(ST["captured"])})
    if ARM.name == "solvefeas":
        res["engine_solves"] = ENGINE_SOLVES[engine_start:]
        res["solve_budget"] = R.solve_budget(res["engine_solves"], solve_record["per_fact"], ARM_RECORD)
    dump(H.OUT, res)
    try:
        pr = R.read_pass(res)
    except (KeyError, TypeError) as e:
        halt(f"pass {name} record incomplete: {e!r}", keys=sorted(res))
    reasons = R.validity(run, pr, name)
    a7 = pr["ref"]; summary = {"A1": pr["a1"]["para_full_n"], "A2": pr["a2"]["para_full_n"], "ref_canon": a7["canon_full_n"], "ref_para": a7["para_full_n"],
                               "shared_para": pr["shared"]["para_full_n"], "hits": pr["hits"], "law5": pr["rec"]["law5_gate"], "residual": pr["residual"]}
    print(f"=== PASS {name} done: reference A7 canon {a7['canon_full_n']}/24 para {a7['para_full_n']}/72; shared para {pr['shared']['para_full_n']}/72; "
          f"A1 {summary['A1']} A2 {summary['A2']}; hits {pr['hits']} ({time.time()-t0:.0f}s)", flush=True)
    if reasons:
        halt(f"pass {name} INVALID: " + "; ".join(reasons), summary=summary, reasons=reasons, result=H.OUT)
    if ARM.name == "solvefeas" and R.reference_shift(a7):
        res["outcome"] = "REFERENCE-SHIFT"; dump(H.OUT, res)
        run["outcome"] = "REFERENCE-SHIFT"; run["passes"][name] = H.OUT
        if name == "2":
            run["second_process"]["outcome"] = "REFERENCE-SHIFT"
            run["second_process"]["ended_utc"] = utc_now()
        dump(f"{OUT_DIR}/run.json", run)
        halt(f"pass {name} REFERENCE-SHIFT: the 50-step reference left the baseline envelope", summary=summary, result=H.OUT)
    return res


def require_settings(record, where):
    if ARM.name == "sharedz":
        return
    mismatch = R.settings_mismatches(record, ARM_RECORD)
    if mismatch:
        halt(f"{where} settings do not match the selected arm", mismatches=mismatch)


def require_inertness():
    """The ALL-INERT record must exist and must have been produced from the CURRENT source files (review items 3, 5)."""
    p = f"{OUT_DIR}/inertness.json"
    if not os.path.exists(p):
        halt(f"{p} missing — run c10s_sharedz_inertness.py first (§2 LAW#5 (i)-(v))")
    rec = json.load(open(p))
    require_settings(rec, "inertness record")
    require_settings(rec["identity"], "inertness identity")
    status = {c: rec.get("checks", {}).get(c, {}).get("ok") for c in R.INERTNESS_CHECKS}
    if not rec.get("ok") or not all(status.values()):
        halt("inertness record not ALL INERT", status=status, record=p)
    mism = provenance_mismatches(rec["identity"]["source_sha256"])
    if mism:
        halt("source files changed since the inertness record; re-run c10s_sharedz_inertness.py in a new OUT_DIR", mismatches=mism)
    return rec


def seeds():
    return {"torch_initial_seed": torch.initial_seed(), "explicit_seeding": "none — the harness and engine do not seed; context templates are sampled unseeded per process (CORPUS/44 F-A4) and recorded in `ctx`"}


def solve_all_shared(ctx):
    zs, diags, fits = {}, {}, {}
    for c in H.FICTION:
        z, dg = solve_shared(c, ctx); zs[c], diags[c], fits[c] = z, diag_record(dg), dg["frame_fit"]
    rec = {**RECORD_SETTINGS, "zs_shared": z_record(zs), "fit_diagnostic": R.fit_diagnostic(fits), "per_fact": diags}
    if ARM.name == "solvefeas":
        rec["solvefeas"] = R.solvefeas_reading(diags)
    return zs, rec


def main():
    global IDENTITY
    t0 = time.time(); run_path = f"{OUT_DIR}/run.json"
    if STAGE == "first":
        occupied = [f for f in STAGE_OUTPUTS if os.path.exists(f"{OUT_DIR}/{f}")]
        if occupied:
            halt(f"OUT_DIR {OUT_DIR} is occupied by {occupied}; stage outputs are never overwritten — use a new OUT_DIR", occupied=occupied)
        fp = fingerprint(); inert = require_inertness()
        IDENTITY = make_identity(inertness_run_id=inert["identity"]["run_id"], out_dir=OUT_DIR)
        ctx = get_context_templates(H.model, H.tok)
        forms = {"CANON": CANON, "T1": R.T1, "T2": R.T2}
        overlap = R.overlap_table(forms, PTEST)
        if overlap["total_shared"] != 0:
            halt("the §2 overlap rule fails", overlap=overlap)
        c0 = H.FICTION[0]
        run = {**RECORD_SETTINGS, "decision_id": DECISION_ID, "prereg": os.environ["PREREG"], "candidate_name": H.CANDIDATE_NAME, "stage": STAGE, "identity": IDENTITY, "z_layer": Z_LAYER, "hparams": HP_PATH,
               "fingerprint": fp, "inertness": inert, "ctx": ctx, "seeds": seeds(),
               "training_forms": {k: {"form": v, "sha256": R.sha256_text(v)} for k, v in forms.items()},
               "training_forms_joined_sha256": R.sha256_text("\n".join(forms.values())),
               "held_out_forms": {"PTEST": PTEST, "sha256": R.sha256_text("\n".join(PTEST))},
               "overlap_table": overlap, "withdrawn_v1_form": {"form": R.V1_WITHDRAWN, "overlap": R.overlap_table({"T1_v1": R.V1_WITHDRAWN}, PTEST)},
               "kl_prefix_note": {"note": "under the identity template T2's subject-last-token position shares its prefix with the KL prompt '{} is a' (§2); indices for the first subject",
                                  "subject": c0, "T2_idx": subject_idx(R.T2, c0), "kl_prompt_idx": subject_idx(R.KL_PROMPT, c0)},
               "frame_subjects": FRAME_SUBJECTS, "passes": {}}
        dump(run_path, run)
        print(f"=== run {IDENTITY['run_id']} — CELL 1: injection screen", flush=True)
        inj, zs_shared, diags, fit = injection_cell(ctx)
        dump(f"{OUT_DIR}/inject.json", inj)
        sc = inj["screen"]
        print(f"cell 1: canonical {sc['canon_n']}/72 shared {sc['shared_n']}/72 gain {sc['gain']} templates won {sc['templates_won']} subjects won {sc['subjects_won']} "
              f"| fit min {fit['min_fit']:.4f} underfit {len(fit['underfit'])} | noise twin gain {inj['noise_twin']['gain']} "
              f"({inj['noise_twin']['disagreeing_pairs']}/{inj['noise_twin']['n_pairs']} pairs differ) | control c {inj['control_c']} -> {inj['outcome']}", flush=True)
        run["cell1_outcome"] = inj["outcome"]; run["inject"] = f"{OUT_DIR}/inject.json"
        if ARM.name == "solvefeas":
            run["solvefeas"] = inj["solvefeas"]
            R.print_solvefeas(inj["solvefeas"])
        dump(run_path, run)
        if inj["outcome"] == "INVALID":
            halt("solvefeas INVALID: the larger solve budget was not exercised", budget=inj["solve_budget"])
        if inj["outcome"] != "PROCEED":
            print(f"{inj['outcome']}: the write arm is not run (§2 cell 1); this candidate configuration was not advanced", flush=True)
            run["seconds"] = round(time.time() - t0); dump(run_path, run)
            print("C10S_SHAREDZ_DONE", flush=True); return 0
        run_pass("1", run, zs_shared, {"zs_shared": inj["zs_shared"], "fit_diagnostic": fit, "per_fact": diags}); run["passes"]["1"] = H.OUT
    else:
        if not os.path.exists(run_path) or not os.path.exists(f"{OUT_DIR}/pass1.json"):
            halt("stage second needs a completed pass 1 in OUT_DIR", out_dir=OUT_DIR)
        if os.path.exists(f"{OUT_DIR}/pass2.json"):
            halt(f"{OUT_DIR}/pass2.json exists; stage outputs are never overwritten", out_dir=OUT_DIR)
        run = json.load(open(run_path)); IDENTITY = run["identity"]
        require_settings(run, "first-stage run")
        require_settings(IDENTITY, "first-stage identity")
        refusal = R.retry_refusal(run)                                                   # v3: any recorded second process (STARTED / UNDERFIT / COMPLETED) is permanent
        if refusal:
            halt(refusal, second_process={k: v for k, v in run["second_process"].items() if k in ("outcome", "started_utc", "pass1_label", "fit_diagnostic")})
        mism = provenance_mismatches(IDENTITY["source_sha256"])
        if mism:
            halt("source files changed since pass 1; a second process must run the same code", mismatches=mism)
        fp = fingerprint(); inert = require_inertness()
        if inert["identity"]["run_id"] != IDENTITY["inertness_run_id"]:
            halt("the inertness record in OUT_DIR is not the one pass 1 used", recorded=IDENTITY["inertness_run_id"], present=inert["identity"]["run_id"])
        pass1 = json.load(open(f"{OUT_DIR}/pass1.json"))
        require_settings(pass1, "pass 1")
        require_settings(pass1["identity"], "pass 1 identity")
        pr1 = R.read_pass(pass1)
        v1 = R.verdict(run, pr1)
        if v1["reasons"]:
            halt("pass 1 is INVALID; no second process", reasons=v1["reasons"])
        if not v1["replication_pending"]:
            halt(f"pass 1 label {v1['label']} does not call for a second process (§2 cell 3: PARTIAL or LEAD only)", label=v1["label"], gates=v1["gates1"])
        # v3 (review 2 blocker): the attempt is recorded BEFORE solving and is never overwritten; its outcome is the disposition
        run["second_process"] = {**RECORD_SETTINGS, "outcome": "STARTED", "started_utc": utc_now(), "identity": IDENTITY, "fingerprint": fp, "pass1_label": v1["label"]}
        dump(run_path, run)
        print(f"=== run {IDENTITY['run_id']} — SECOND PROCESS (gate A) for pass 1 label {v1['label']} (recorded as STARTED)", flush=True)
        ctx = get_context_templates(H.model, H.tok)
        zs_shared, rec = solve_all_shared(ctx)
        run["second_process"].update({"ctx": ctx, "seeds": seeds(), "zs_shared": rec["zs_shared"], "fit_diagnostic": rec["fit_diagnostic"], "per_fact_frame_fit": {c: d["frame_fit"] for c, d in rec["per_fact"].items()}})
        if ARM.name == "solvefeas":
            run["second_process"].update(solvefeas=rec["solvefeas"], per_fact=rec["per_fact"])
        dump(run_path, run)
        if not rec["fit_diagnostic"]["ok"]:                                              # review item 3: the fit is judged BEFORE the write; v3: terminal
            run["second_process"]["outcome"] = "UNDERFIT"; run["second_process"]["ended_utc"] = utc_now(); dump(run_path, run)
            if ARM.name == "solvefeas":
                budget = R.solve_budget(ENGINE_SOLVES, rec["per_fact"], ARM_RECORD)
                run["second_process"]["solve_budget"] = budget
                run["second_process"]["outcome"] = "UNDERFIT-AT-50" if budget["ok"] else "INVALID"
                dump(run_path, run)
                halt(f"second process {run['second_process']['outcome']}: the write arm was not run; the disposition is permanent", reading=rec["solvefeas"], budget=budget)
            halt("second process UNDERFIT: the shared solve fell below 0.98 on a training frame; the write arm was not run; the disposition is permanent (candidate not advanced)", fit=rec["fit_diagnostic"])
        run_pass("2", run, zs_shared, rec); run["passes"]["2"] = H.OUT
        run["second_process"]["outcome"] = "COMPLETED"; run["second_process"]["ended_utc"] = utc_now()
    run["seconds"] = round(time.time() - t0)
    dump(run_path, run)
    print(f"wrote {run_path}; read with: c10s_sharedz_read.py {OUT_DIR}", flush=True)
    print("C10S_SHAREDZ_DONE", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException as e:   # review item 4: no failure leaves without a diagnostic; the exception is re-raised through halt (SystemExit)
        halt(f"unhandled {type(e).__name__}: {e}", traceback=traceback.format_exc())
