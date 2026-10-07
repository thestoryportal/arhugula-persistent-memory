#!/usr/bin/env python3
"""D-C10t-secondkey v2 frozen §2 step 0: base-model measurements, NO weight write.

Operator-only invocation after step 1's verdict; never run by implementation/selftest.
Publishes OUT_DIR/step0.json exclusively: scores, admission, selectors, frozen
requests, cross-template cosines and overlap. 'Offline' means no edit, not model-free.
Importing this file is model-free; runtime imports are inside main/helpers only.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10t_secondkey_read as R
import c10t_secondkey_arms as A


def position_classes(H, country, value, value_ids):
    from rome.repr_tools import get_words_idxs_in_templates
    prompt = R.CANON.format(country)
    prefix = A.token_ids(H.tok, prompt)
    sentence = prompt + " " + value
    ids = A.token_ids(H.tok, sentence)
    if ids != prefix + value_ids:
        raise ValueError("canonical sentence cannot be classified into the declared token positions: " + country)
    first = get_words_idxs_in_templates(H.tok, [R.CANON], [country], "first")[0][0]
    last = get_words_idxs_in_templates(H.tok, [R.CANON], [country], "last")[0][0]
    rows = []
    for p, tid in enumerate(ids):
        j = p - len(prefix) + 1 if p >= len(prefix) else None
        cls = ("value-final" if j == len(value_ids) else "value-writable") if j is not None else ("subject" if first <= p <= last else "frame")
        rows.append({"p": p, "id": tid, "decoded": H.tok.decode([tid]), "class": cls, "j": j})
    return sentence, rows


def surprisal(H, country, value_ids):
    import torch
    scores = []
    # §2(a) is defined on prompt STRINGS, not an assumed concatenation of token
    # arrays. Forward each actual teacher-forced prefix exactly as specified.
    with torch.no_grad():
        for j, tid in enumerate(value_ids):
            prompt = R.CANON.format(country) + H.tok.decode(value_ids[:j])
            x = H.tok(prompt, return_tensors="pt").to(H.DEV)
            lp = torch.log_softmax(H.model(**x).logits[0, -1].float(), dim=-1)
            scores.append(float(-lp[tid]))
    return {"values": scores, **R.surprisal_selection(scores)}


def sentence_keys(H, hp, layer, sentence):
    import torch
    from util import nethook
    # Input side of down_proj, as compute_ks.py:19-37, but at EVERY token.
    with torch.no_grad(), nethook.Trace(H.model, hp.rewrite_module_tmp.format(layer), retain_input=True,
                                       retain_output=False, clone=True, detach=True, stop=True) as trace:
        H.model(**H.tok(sentence, return_tensors="pt").to(H.DEV))
    x = trace.input[0] if isinstance(trace.input, tuple) else trace.input
    return x[0].T.float().cpu()


def leverage(H, hp, facts):
    import torch
    from memit.memit_main import get_cov
    # c10e_bandknob.py:169-175 reads RAW second moment and float32 SVD.
    # Reuse one SVD per layer for ALL facts/cuts. Never invert S < cutoff.
    for layer in hp.layers:
        cov = get_cov(H.model, H.tok, hp.rewrite_module_tmp.format(layer), hp.mom2_dataset,
                      hp.mom2_n_samples, hp.mom2_dtype).cpu().float()
        U, S, Vh = torch.linalg.svd(cov, full_matrices=False)
        del cov, Vh
        for f in facts:
            K = sentence_keys(H, hp, layer, f["sentence"])
            if K.shape[1] != len(f["positions"]):
                raise ValueError("position/key lengths differ")
            coords = U.T @ K
            key_energy = K.double().square().sum(0)
            if bool((key_energy == 0).any()):
                raise ValueError("undefined leverage for a zero base key")
            scores, shares = {}, {}
            for cut in (R.COV_CUT, R.CUT_CHECK):
                protected = R.cut_indices(S.tolist(), cut)
                protected_set = set(protected)
                writable = [i for i in range(len(S)) if i not in protected_set]
                scores[str(cut)] = ((coords[protected].double().square() / S[protected].double()[:, None]).sum(0)).tolist()
                PK = U[:, writable] @ coords[writable] if writable else torch.zeros_like(K)
                shares[str(cut)] = (PK.double().square().sum(0) / key_energy).tolist()
            f.setdefault("leverage_layers", {})[str(layer)] = {"protected_leverage": scores, "writeable_key_energy_share": shares}
        del U, S
    for f in facts:
        by_cut = {str(c): R.leverage_selection(f["positions"], {str(l): f["leverage_layers"][str(l)]["protected_leverage"][str(c)] for l in hp.layers})
                  for c in (R.COV_CUT, R.CUT_CHECK)}
        f["leverage"] = by_cut[str(R.COV_CUT)]
        f["cut_stability"] = {"cuts": [R.COV_CUT, R.CUT_CHECK], "selection_by_cut": by_cut,
                              "same_internal_pick": by_cut[str(R.COV_CUT)]["p5"] == by_cut[str(R.CUT_CHECK)]["p5"],
                              "same_unconstrained_pick": by_cut[str(R.COV_CUT)]["unconstrained"] == by_cut[str(R.CUT_CHECK)]["unconstrained"]}


def cross_template(H, hp, facts, selected):
    from memit.compute_z import get_module_input_output_at_words
    from rome.repr_tools import get_reprs_at_idxs
    records = {}
    for variant, positions in selected.items():
        layers, all_second, all_subject = {}, [], []
        for layer in hp.layers:
            subject = {}
            second = {}
            for name, form in [("CANON", R.CANON)] + [("PTEST" + str(i), p) for i, p in enumerate(R.PTEST)]:
                subject[name] = get_module_input_output_at_words(H.model, H.tok, layer,
                    context_templates=[form] * R.N, words=[f["subj"] for f in facts],
                    module_template=hp.rewrite_module_tmp, fact_token_strategy=hp.fact_token)[0].float().cpu()
                prompts = [form.format(f["subj"]) + H.tok.decode(f["value_ids"][:positions[f["subj"]]]) for f in facts]
                idxs = [[len(A.token_ids(H.tok, p)) - 1] for p in prompts]
                for f, prompt, idx in zip(facts, prompts, idxs):
                    if A.token_ids(H.tok, prompt)[idx[0]] != f["value_ids"][positions[f["subj"]] - 1]:
                        raise ValueError("gold-prefix cross-template lookup retokenised: " + f["subj"])
                second[name] = get_reprs_at_idxs(H.model, H.tok, prompts, idxs, layer, hp.rewrite_module_tmp, "in").float().cpu()
            row = {}
            for name in list(subject)[1:]:
                cosine = lambda a, b: ((a.double() * b.double()).sum(1) / (a.double().norm(dim=1) * b.double().norm(dim=1))).tolist()
                cs, cc = cosine(second["CANON"], second[name]), cosine(subject["CANON"], subject[name])
                row[name] = {"second": cs, "subject": cc, "facts": [f["subj"] for f in facts]}
                all_second.extend(cs)
                all_subject.extend(cc)
            layers[str(layer)] = row
        records[variant] = {"layers": layers, "reading": R.overturning_reading(all_second, all_subject),
                            "median_population": "all 24 facts x five layers x three held-out templates; direct prompts without sampled context prefixes"}
    return records


def main():
    A.STAGE = "step0"
    t0 = time.time()
    root = Path(LLMDB_ROOT).resolve()
    out = Path(os.environ.get("OUT_DIR", str(root / "results/c10t_secondkey"))).resolve()
    A.refuse_occupied(out, ("step0.json", "run.json", "pass1.json", "pass2.json", "second_started.json", "second_halt.json"))
    identity = A.make_identity(root)
    A.IDENTITY = identity
    H, hp, fingerprint = A.runtime(root, out)
    from memit.memit_main import get_context_templates
    from rome.repr_tools import get_words_idxs_in_templates
    ctx = get_context_templates(H.model, H.tok)      # memit_main.py:304-316; sampled once, recorded before optimisation
    V = H.ARMS["A7_coined_coined"]                   # c10e_bandknob.py:246-249, FICTION order :57-64
    facts = []
    for country in H.FICTION:
        value = V[country]
        ids = A.token_ids(H.tok, " " + value)        # compute_z.py:41-43 standalone tokenisation, no req() here
        sentence, positions = position_classes(H, country, value, ids)
        canonical = H.req(R.CANON, country, value)
        ca = A.canonical_audit(H.tok, canonical, ctx, get_words_idxs_in_templates)
        audits = []
        for j in range(1, len(ids)):
            audit = A.alignment_audit(H.tok, country, value, ids, j, ctx, get_words_idxs_in_templates)
            audits.append(audit)
        admitted = [a["j"] for a in audits if a["ok"] and ca["ok"]]
        facts.append({"subj": country, "value": value, "value_ids": ids, "sentence": sentence, "positions": positions,
                      "surprisal": surprisal(H, country, ids), "canonical_admission": ca, "admission": audits,
                      "admissible": admitted, "admissible_n": len(admitted)})
    leverage(H, hp, facts)
    selection = R.select_positions(facts)
    requests = {v: A.requests_for(H.tok, facts, js) for v, js in selection["arms"].items()}
    overturning = cross_template(H, hp, facts, selection["arms"]) if requests else {}
    record = {"decision_id": R.DECISION_ID, "prereg": R.PREREG, "identity": identity, "fingerprint": fingerprint,
              "ctx": ctx, "facts": facts, "selection": selection, "requests": requests,
              "request_sha256": {v: R.json_digest(rqs) for v, rqs in requests.items()},
              "overlap": {v: R.overlap_audit(rqs) for v, rqs in requests.items()}, "overturning": overturning,
              "cov_cache_sha256": H.cov_cache_sha256(hp), "seconds": time.time() - t0,
              "leverage_arithmetic": "raw second moment; float32 SVD/coordinates as compute_P; score and norms accumulated float64; raw five-layer mean selects; max-normalised alternative reported",
              "limits": ["held-out templates were visible to the author", "protected-subspace leverage is an experimental heuristic", "no weight write or target optimisation in step0"]}
    A.require_sources(identity, root)
    A.write_json(out / "step0.json", record)
    print(selection["outcome"] + "; published frozen positions/requests: " + str(out / "step0.json"))
    print("C10T_SECONDKEY_STEP0_DONE")
    return 2 if selection["outcome"] == "INVALID-ADMISSION" else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        if e.code in (0, None):
            raise
        A.halt("step0 exit: " + str(e))
    except BaseException as e:
        A.halt(type(e).__name__ + ": " + str(e), traceback=A.traceback.format_exc())
