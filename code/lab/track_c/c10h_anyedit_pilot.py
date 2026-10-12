import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse, contextlib, io, json, math
os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"
os.environ["HF_HUB_OFFLINE"] = "0"
ENGINE_ROOT = f"{LLMDB_ROOT}/memit_dry_run/memit"
sys.path.insert(0, ENGINE_ROOT)
os.chdir(ENGINE_ROOT)

ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-3B")
REV = os.environ.get("MODEL_REV", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
HP_BASE = f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"
OUT = os.environ.get("OUT", f"{LLMDB_ROOT}/results/c10h_anyedit_pilot.json")
PREREG = f"{LLMDB_ROOT}/docs/C10_ANYEDIT_PILOT_PREREG.md"
CANON = "The capital of {} is the city of"
PTEST = [
    "{}'s capital city is called",
    "If you visit {}, its capital city is",
    "The main city and seat of government of {} is",
]
FICTION_ALL = [
    "Zorbland", "Quaxil", "Plurnak", "Vythorn", "Glimsto", "Drennik", "Yastovel", "Crulpane",
    "Mophgar", "Brinduun", "Trannak", "Skornwell", "Fluvane", "Oxbarrow", "Zephquin", "Lurmaxen",
    "Pradnoll", "Kessivar", "Wombryne", "Halquin", "Vorlex", "Quenby", "Marsduq", "Thelby",
]


def build_stimuli(tok, n):
    scr = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
    caps = sorted({scr[c]["capital"]["truth"] for c in scr})

    def ids(s):
        return tok(" " + s, add_special_tokens=False)["input_ids"]

    single_v = [k for k in caps if len(ids(k)) == 1]
    coherent2 = [k for k in caps if len(ids(k)) == 2]
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
    fiction = FICTION_ALL[:n]

    def assign(pool):
        return {c: pool[(i * 3 + 5) % len(pool)] for i, c in enumerate(fiction)}

    return fiction, {
        "A1_single": assign(single_v),
        "A2_coherent2": assign(coherent2),
        "A7_coined_coined": {
            c: f"{coined_head[(i * 2 + 1) % len(coined_head)]} {coined_mod[(i * 3 + 2) % len(coined_mod)]}"
            for i, c in enumerate(fiction)
        },
    }


def answer_ids(tok, answer):
    return tok(answer, add_special_tokens=False)["input_ids"]


def question_answer_ids(tok, question, answer):
    return tok(question + answer, add_special_tokens=False)["input_ids"]


def window_plan(tok, question, answer, window_size, overlap):
    ans = answer_ids(tok, answer)
    suffix = question_answer_ids(tok, question, answer)[-len(ans):]
    if ans != suffix:
        return {"ok": False, "reason": "answer_ids != continuation_suffix_ids", "answer_ids": ans, "suffix_ids": suffix}
    if window_size <= overlap:
        return {"ok": False, "reason": "window_size must exceed overlap", "answer_ids": ans, "suffix_ids": suffix}
    windows = []
    start = 0
    question_len = len(tok(question, add_special_tokens=False)["input_ids"])
    while start < len(ans):
        end = min(start + window_size, len(ans))
        current = ans[start:end]
        # ARE optimizes the next-token prediction position: prompt last token for the
        # first answer token, then the prior answer-token positions for continuation.
        lookup_idx = question_len - 1 if start == 0 else question_len + start - 1 + overlap
        windows.append({
            "start": start,
            "end": end,
            "target_ids": current,
            "lookup_idx": lookup_idx,
            "decoded": tok.decode(current),
        })
        start += window_size - overlap
    return {
        "ok": True,
        "answer_ids": ans,
        "suffix_ids": suffix,
        "answer_text": tok.decode(ans),
        "suffix_text": tok.decode(suffix),
        "answer_token_count": len(ans),
        "target_vector_count": len(windows),
        "lookup_idxs": [w["lookup_idx"] for w in windows],
        "windows": windows,
    }


def token_alignment_report(tok, n):
    fiction, arms = build_stimuli(tok, n)
    report = {"model_id": ID, "revision": REV, "n": n, "arms": {}, "ok": True}
    for arm, vals in arms.items():
        rows = []
        for subj in fiction:
            q = CANON.format(subj)
            ans = " " + vals[subj]
            row = {"subject": subj, "value": vals[subj], "answer": ans, "plans": {}}
            for w in (1, 50):
                plan = window_plan(tok, q, ans, w, 0)
                row["plans"][f"window_{w}"] = plan
                if not plan["ok"]:
                    report["ok"] = False
                if w == 1 and plan["ok"]:
                    invariant = (
                        plan["target_vector_count"] == plan["answer_token_count"]
                        and all(x["end"] - x["start"] == 1 for x in plan["windows"])
                        and len(plan["lookup_idxs"]) == plan["answer_token_count"]
                    )
                    row["window_1_invariant_ok"] = invariant
                    if not invariant or (arm == "A7_coined_coined" and plan["target_vector_count"] <= 1):
                        report["ok"] = False
            rows.append(row)
        report["arms"][arm] = rows
    return report


def dry_run(args):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(ID, revision=REV)
    report = token_alignment_report(tok, args.n)
    lengths = {}
    for arm, rows in report["arms"].items():
        vals = [r["plans"]["window_1"]["answer_token_count"] for r in rows if r["plans"]["window_1"]["ok"]]
        lengths[arm] = {"min": min(vals), "max": max(vals), "mean": round(sum(vals) / len(vals), 2)} if vals else None
    report["length_summary"] = lengths
    out = args.dry_out or f"{LLMDB_ROOT}/results/c10h_anyedit_token_window_dryrun.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({"ok": report["ok"], "length_summary": lengths, "out": out}, indent=2), flush=True)
    print("C10H_DRY_DONE", flush=True)
    return 0 if report["ok"] else 2


def run_gpu(args):
    import torch
    from util import nethook
    from memit.memit_hparams import MEMITHyperParams
    from memit.memit_main import upd_matrix_match_shape
    import c10e_bandknob as c10

    hp = MEMITHyperParams.from_json(HP_BASE)
    hp.window_size = args.window_size
    hp.overlap = args.overlap
    hp.nullspace_threshold = 0.005
    hp.L2 = 1.0
    if hp.layers != [4, 5, 6, 7, 8]:
        raise RuntimeError(f"baseline layers drifted: {hp.layers}")

    def weight_name(layer):
        return f"{hp.rewrite_module_tmp.format(layer)}.weight"

    def selected_layer_outputs(batch_text, idxs_dict, layer, module_template):
        toks = c10.tok(batch_text, padding=True, return_tensors="pt").to("cuda")
        with torch.no_grad():
            with nethook.Trace(
                module=c10.model,
                layer=module_template.format(layer),
                retain_input=True,
                retain_output=True,
                detach=True,
                clone=True,
            ) as tr:
                _ = c10.model(**toks)
        inp = tr.input[0] if isinstance(tr.input, tuple) else tr.input
        out = tr.output[0] if isinstance(tr.output, tuple) else tr.output
        selected_in, selected_out = [], []
        for b, idxs in idxs_dict.items():
            for idx in idxs:
                selected_in.append(inp[b, idx])
                selected_out.append(out[b, idx])
        return torch.stack(selected_in, dim=1), torch.stack(selected_out, dim=1)

    def are_compute_z(data, layer):
        lm_w, ln_f = (
            nethook.get_parameter(c10.model, f"{hp.lm_head_module}.weight").T,
            nethook.get_module(c10.model, hp.ln_f_module),
        )
        try:
            lm_b = nethook.get_parameter(c10.model, f"{hp.lm_head_module}.bias")
        except LookupError:
            lm_b = next(c10.model.parameters()).new_zeros(c10.model.config.vocab_size)
        target_ids = torch.tensor(answer_ids(c10.tok, data["answer"]), device="cuda", dtype=torch.long)
        q_ids = torch.tensor(question_answer_ids(c10.tok, data["question"], ""), device="cuda", dtype=torch.long).unsqueeze(0)
        cur_input_ids = q_ids
        all_delta, all_targets, all_idxs, windows = [], [], [], []
        start = 0
        while start < len(target_ids):
            end = min(start + hp.window_size, len(target_ids))
            current = target_ids[start:end]
            if start > 0:
                add_for_input = current[hp.overlap:-1]
                add_for_cur = current[hp.overlap:]
            else:
                add_for_input = current[:-1]
                add_for_cur = current
            input_ids = torch.cat([cur_input_ids, add_for_input.unsqueeze(0)], dim=1)
            cur_input_ids = torch.cat([cur_input_ids, add_for_cur.unsqueeze(0)], dim=1)
            start += hp.window_size - hp.overlap
            rewriting_targets = torch.full((1, input_ids.shape[1]), -100, device="cuda", dtype=torch.long)
            ex_len = input_ids.shape[1]
            rewriting_targets[0, ex_len - len(current):ex_len] = current
            lookup_idxs = [ex_len - len(current)]
            loss_layer = max(hp.v_loss_layer, layer)
            hidden = getattr(c10.model.config, "hidden_size", None) or c10.model.config.n_embd
            delta = torch.zeros((hidden,), requires_grad=True, device="cuda")
            target_init = None

            def edit_output_fn(cur_out, cur_layer):
                nonlocal target_init
                if cur_layer == hp.layer_module_tmp.format(layer):
                    tensor = cur_out[0] if isinstance(cur_out, tuple) else cur_out
                    if target_init is None:
                        target_init = tensor[0, lookup_idxs[0]].detach().clone()
                    for prior_idxs, prior_delta in all_delta:
                        for idx in prior_idxs:
                            tensor[0, idx, :] += prior_delta
                    for idx in lookup_idxs:
                        tensor[0, idx, :] += delta
                return cur_out

            opt = torch.optim.Adam([delta], lr=hp.v_lr)
            nethook.set_requires_grad(False, c10.model)
            for _ in range(hp.v_num_grad_steps):
                opt.zero_grad()
                with nethook.TraceDict(
                    module=c10.model,
                    layers=[hp.layer_module_tmp.format(loss_layer), hp.layer_module_tmp.format(layer)],
                    retain_input=False,
                    retain_output=True,
                    edit_output=edit_output_fn,
                ) as tr:
                    _ = c10.model(input_ids).logits
                output = tr[hp.layer_module_tmp.format(loss_layer)].output
                output = output[0] if isinstance(output, tuple) else output
                log_probs = torch.log_softmax(c10.model.model.norm(output) @ lm_w.to(output.device) + lm_b.to(output.device), dim=2)
                loss_tok = torch.gather(
                    log_probs,
                    2,
                    torch.where(rewriting_targets != -100, rewriting_targets, 0).unsqueeze(2).to(log_probs.device),
                ).squeeze(2)
                mask = (rewriting_targets != -100).float()
                nll_each = -(loss_tok * mask.to(loss_tok.device)).sum(1) / current.size(0)
                nll = nll_each.mean()
                wd = hp.v_weight_decay * (torch.norm(delta) / torch.norm(target_init) ** 2)
                loss = nll + wd.to(nll.device)
                if loss < 1e-2:
                    break
                loss.backward()
                opt.step()
                max_norm = hp.clamp_norm_factor * target_init.norm()
                if delta.norm() > max_norm:
                    with torch.no_grad():
                        delta[...] = delta * max_norm / delta.norm()
            target = target_init + delta
            all_delta.append((lookup_idxs, delta.detach().clone()))
            all_targets.append(target.detach())
            all_idxs.append(lookup_idxs[0])
            windows.append({"lookup_idx": lookup_idxs[0], "delta_norm": float(delta.detach().norm()), "target_norm": float(target.detach().norm())})
        return all_idxs, all_targets, windows

    def validate_alignment(Vmap, window_size):
        rows = []
        ok = True
        for subj in c10.FICTION:
            plan = window_plan(c10.tok, c10.CANON.format(subj), " " + Vmap[subj], window_size, hp.overlap)
            if not plan["ok"]:
                ok = False
            if window_size == 1:
                invariant = plan.get("target_vector_count") == plan.get("answer_token_count") and len(plan.get("lookup_idxs", [])) == plan.get("answer_token_count")
                invariant = invariant and all(w["end"] - w["start"] == 1 for w in plan.get("windows", []))
                if not invariant:
                    ok = False
                if Vmap is c10.ARMS.get("A7_coined_coined") and plan.get("target_vector_count", 0) <= 1:
                    ok = False
                plan["window_1_invariant_ok"] = invariant
            rows.append({"subject": subj, "value": Vmap[subj], "plan": plan})
        return ok, rows

    def run_anyedit_law5(P, base_snap):
        probes = ["Zorbland is described as"]
        cons = c10.CANON.format("Zorbland")
        target = c10.first_tok("Cairo")
        pre = {p: c10.predict(p) for p in [cons] + probes}
        before = {layer: dict(c10.model.named_parameters())[weight_name(layer)].detach().clone() for layer in hp.layers}
        # Pure no-op pipeline: validate planning and take no update.
        plan = window_plan(c10.tok, cons, " Cairo", hp.window_size, hp.overlap)
        post = {p: c10.predict(p) for p in [cons] + probes}
        param_delta = max(float((dict(c10.model.named_parameters())[weight_name(layer)] - before[layer]).detach().abs().max().cpu()) for layer in hp.layers)
        gate = {
            "kind": "pure_noop_pipeline",
            "expr_delta": round(abs(float(post[cons]["dist"][target]) - float(pre[cons]["dist"][target])), 6),
            "loc_delta": round(abs(c10.locpct(post, pre, probes) - 100.0), 6),
            "param_max_abs_delta": param_delta,
            "token_plan_ok": bool(plan["ok"]),
        }
        gate["ok"] = gate["expr_delta"] <= 0.01 and gate["loc_delta"] <= 3.0 and gate["param_max_abs_delta"] == 0.0 and gate["token_plan_ok"]
        c10.restore_layers(hp, base_snap)
        return gate

    def anyedit_edit(Vmap, P, base_snap):
        c10.restore_layers(hp, base_snap)
        cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in hp.layers]
        data = [{"question": c10.CANON.format(subj), "answer": " " + Vmap[subj], "subject": subj} for subj in c10.FICTION]
        batch_text = [d["question"] + d["answer"] for d in data]
        idxs_dict = {}
        all_zs, window_logs = [], {}
        z_layer = hp.layers[-1]
        for k, d in enumerate(data):
            idxs, zs, logs = are_compute_z(d, z_layer)
            idxs_dict[k] = idxs
            all_zs.extend(zs)
            window_logs[d["subject"]] = logs
        zs = torch.stack(all_zs, dim=1)
        delta_norms = {}
        npd = dict(c10.model.named_parameters())
        for i, layer in enumerate(hp.layers):
            before_norm = float(npd[weight_name(layer)].detach().float().norm())
            layer_ks, _ = selected_layer_outputs(batch_text, idxs_dict, layer, hp.rewrite_module_tmp)
            _, cur_zs = selected_layer_outputs(batch_text, idxs_dict, z_layer, hp.layer_module_tmp)
            targets = zs - cur_zs
            resid = targets / (len(hp.layers) - i)
            Kf = layer_ks.float().cpu()
            rf = resid.float().cpu()
            Pi = P[i]
            ca = cache[i]
            A = Pi @ (Kf @ Kf.T + ca) + hp.L2 * torch.eye(Kf.shape[0])
            B = Pi @ Kf @ rf.T
            upd = torch.linalg.solve(A, B).T
            upd = upd_matrix_match_shape(upd.float(), npd[weight_name(layer)].shape)
            upd_norm = float(upd.float().norm())
            delta_norms[str(layer)] = {"delta_norm": upd_norm, "weight_norm_before": before_norm, "relative_delta_norm": upd_norm / max(before_norm, 1e-12)}
            with torch.no_grad():
                npd[weight_name(layer)][...] += upd.to(npd[weight_name(layer)].device, npd[weight_name(layer)].dtype)
            cache[i] = cache[i] + Kf @ Kf.T
        return delta_norms, window_logs

    def run_anyedit_recipe(name, window_size, arm_names=None):
        hp.window_size = window_size
        hp.overlap = args.overlap
        arm_names = arm_names or list(c10.ARMS)
        base_snap = c10.snap_layers(hp)
        P = c10.compute_P(hp)
        law5 = run_anyedit_law5(P, base_snap)
        out = {"hparams": HP_BASE, "band": hp.layers, "window_size": window_size, "overlap": hp.overlap, "law5_gate": law5, "arms": {}, "delta_norms": {}, "token_alignment": {}, "detail": {}, "window_logs": {}}
        if not law5["ok"]:
            out["invalid"] = "LAW#5 AnyEdit no-op inertness failed"
            return out
        for arm in arm_names:
            Vmap = c10.ARMS[arm]
            align_ok, align_rows = validate_alignment(Vmap, window_size)
            out["token_alignment"][arm] = {"ok": align_ok, "rows": align_rows}
            if not align_ok:
                out.setdefault("invalid_arms", {})[arm] = "token alignment/window-count gate failed"
                continue
            pre_prompts = [f"{c} is described as" for c in c10.FICTION]
            c10.restore_layers(hp, base_snap)
            pre_loc = {p: c10.predict(p) for p in pre_prompts}
            with contextlib.redirect_stdout(io.StringIO()):
                delta, logs = anyedit_edit(Vmap, P, base_snap)
            post_loc = {p: c10.predict(p) for p in pre_prompts}
            arm_eval = c10.eval_arm(Vmap)
            arm_eval["locality_described_as"] = c10.locpct(post_loc, pre_loc, pre_prompts)
            out["arms"][arm] = {k: v for k, v in arm_eval.items() if k != "rows"}
            out["detail"][arm] = arm_eval["rows"]
            out["delta_norms"][arm] = delta
            out["window_logs"][arm] = logs
            print(f"  {name} {arm:18} canon={arm_eval['canon_full']} para={arm_eval['para_full']} first={arm_eval['para_first']} tf={arm_eval['tf_pertok_cont']} loc={arm_eval['locality_described_as']}", flush=True)
        c10.restore_layers(hp, base_snap)
        return out


    def run_baseline_controls(arm_names):
        base_hp = MEMITHyperParams.from_json(HP_BASE)
        if base_hp.layers != [4, 5, 6, 7, 8]:
            raise RuntimeError(f"baseline layers drifted: {base_hp.layers}")
        base_hp.nullspace_threshold = 0.005
        base_hp.L2 = 1.0
        base_snap = c10.snap_layers(base_hp)
        P = c10.compute_P(base_hp)
        law5 = c10.run_law5(base_hp, P, base_snap)
        out = {"hparams": HP_BASE, "band": base_hp.layers, "law5_gate": law5, "arms": {}, "delta_norms": {}, "detail": {}}
        if not law5["ok"]:
            out["invalid"] = "LAW#5 baseline inertness failed"
            return out
        for arm in arm_names:
            Vmap = c10.ARMS[arm]
            c10.restore_layers(base_hp, base_snap)
            cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in base_hp.layers]
            pre_prompts = [f"{c} is described as" for c in c10.FICTION]
            pre_loc = {p: c10.predict(p) for p in pre_prompts}
            requests = [c10.req(c10.CANON, c, Vmap[c]) for c in c10.FICTION]
            with contextlib.redirect_stdout(io.StringIO()):
                delta = c10.my_edit(base_hp, requests, P, cache)
            post_loc = {p: c10.predict(p) for p in pre_prompts}
            arm_eval = c10.eval_arm(Vmap)
            arm_eval["locality_described_as"] = c10.locpct(post_loc, pre_loc, pre_prompts)
            out["arms"][arm] = {k: v for k, v in arm_eval.items() if k != "rows"}
            out["detail"][arm] = arm_eval["rows"]
            out["delta_norms"][arm] = delta
            print(f"  baseline {arm:18} canon={arm_eval['canon_full']} para={arm_eval['para_full']} first={arm_eval['para_first']} tf={arm_eval['tf_pertok_cont']} loc={arm_eval['locality_described_as']}", flush=True)
        c10.restore_layers(base_hp, base_snap)
        return out

    def control_recovery_verdict(results):
        invalid = []
        baseline = results["recipes"]["baseline_controls"]
        diag = results["recipes"]["anyedit_window50_controls"]
        if not baseline.get("law5_gate", {}).get("ok"):
            invalid.append("baseline LAW#5 failed")
        if not diag.get("law5_gate", {}).get("ok"):
            invalid.append("AnyEdit no-op LAW#5 failed")
        for arm in ("A1_single", "A2_coherent2"):
            if baseline.get("arms", {}).get(arm, {}).get("para_full", 0) < 80:
                invalid.append(f"baseline {arm} para_full below 80")
            if not diag.get("token_alignment", {}).get(arm, {}).get("ok"):
                invalid.append(f"{arm} token/window alignment failed")
            rows = diag.get("token_alignment", {}).get(arm, {}).get("rows", [])
            if not all(r.get("plan", {}).get("target_vector_count") == 1 for r in rows):
                invalid.append(f"{arm} window50 did not produce exactly one target window per request")
        if invalid:
            return {"label": "INVALID_HALTED", "invalid_reasons": invalid}
        a1 = diag["arms"]["A1_single"]["para_full"]
        a2 = diag["arms"]["A2_coherent2"]["para_full"]
        label = "CONTROL_RECOVERY_PASS" if min(a1, a2) >= 80 else "CONTROL_RECOVERY_FAIL"
        return {
            "label": label,
            "threshold": "A1_single and A2_coherent2 para_full >= 80",
            "baseline_controls": {
                "A1_single_para_full": baseline["arms"]["A1_single"]["para_full"],
                "A2_coherent2_para_full": baseline["arms"]["A2_coherent2"]["para_full"],
            },
            "anyedit_window50_controls": {
                "A1_single_para_full": a1,
                "A2_coherent2_para_full": a2,
                "control_min_para_full": min(a1, a2),
            },
            "licensed_claim": "diagnostic-only; pass permits later A7 test but is not rescue evidence" if label == "CONTROL_RECOVERY_PASS" else "stops A7 under this local upstream-window transplant condition",
        }

    def final_verdict(results):
        invalid = []
        b = results["recipes"].get("baseline", {}).get("arms", {}).get("A7_coined_coined")
        k = results["recipes"].get("anyedit_window1", {}).get("arms", {}).get("A7_coined_coined")
        if not b or not k:
            invalid.append("missing baseline or primary AnyEdit A7 result")
        if results["recipes"].get("baseline", {}).get("arms", {}).get("A1_single", {}).get("para_full", 0) < 80:
            invalid.append("baseline A1 para_full below 80")
        if results["recipes"].get("baseline", {}).get("arms", {}).get("A2_coherent2", {}).get("para_full", 0) < 80:
            invalid.append("baseline A2 para_full below 80")
        if b and b.get("para_full", 999) > 35:
            invalid.append("baseline A7 did not reproduce failure envelope")
        primary = results["recipes"].get("anyedit_window1", {})
        if not primary.get("law5_gate", {}).get("ok"):
            invalid.append("AnyEdit LAW#5 no-op gate failed")
        if any(not v.get("ok") for v in primary.get("token_alignment", {}).values()):
            invalid.append("token alignment/window-count gate failed")
        if invalid:
            return {"label": "INVALID_HALTED", "text": "; ".join(invalid), "invalid_reasons": invalid}
        a1 = primary["arms"]["A1_single"]["para_full"]
        a2 = primary["arms"]["A2_coherent2"]["para_full"]
        control_min = min(a1, a2)
        dp = round(k["para_full"] - b["para_full"], 1)
        loc_ok = k.get("locality_described_as", -999) >= b.get("locality_described_as", 100) - 5.0 if "locality_described_as" in b else True
        if control_min < 80 or not loc_ok:
            label = "TRADEOFF_NOT_CLEAN_RESCUE"
        elif k["para_full"] >= 85 and dp >= 20:
            label = "USABILITY_RESCUE_LEAD_NOT_CLOSURE"
        elif k["para_full"] >= 40 and dp >= 20:
            label = "BEHAVIORAL_LEAD_NOT_CLOSURE"
        elif k["para_full"] < 40:
            label = "NO_MATERIAL_ANYEDIT_RESCUE"
        else:
            label = "AMBIGUOUS_NONPROMOTIONAL"
        return {"label": label, "baseline_A7": b, "anyedit_A7": k, "delta_A7": {"para_full_pp": dp}, "control_min_para_full": control_min, "locality_ok": loc_ok}


    if args.window50_controls_only:
        arm_names = ["A1_single", "A2_coherent2"]
        base_report = {}
        for arm in arm_names:
            nts = [c10.ntok(c10.ARMS[arm][c]) for c in c10.FICTION]
            base_report[arm] = {
                "base": sum(c10.full_seq_match(c10.CANON.format(c), c10.tgt_ids(c10.ARMS[arm][c]))[0] for c in c10.FICTION),
                "mean_ntok": round(sum(nts) / len(nts), 2),
                "ntok_range": [min(nts), max(nts)],
            }
        print("\n=== C10h WINDOW50 CONTROL DIAGNOSTIC ===", flush=True)
        for k, v in base_report.items():
            print(f"  {k:18} base={v['base']}/{c10.N} ntok={v['mean_ntok']} range={v['ntok_range']}", flush=True)
        results = {
            "decision_id": "D-C10h-anyedit-window50-controls",
            "parent_decision_id": "D-C10h-anyedit-pilot",
            "run": "C10h AnyEdit upstream-window A1/A2 control diagnostic",
            "class": "diagnostic-only; not rescue evidence; do not write CORPUS without supervised closeout",
            "scope": "Qwen2.5-3B / capital / A1-A2 only / N=24 / 1-seed / HF-fp16 / local AnyEdit ARE target construction",
            "frozen_control_gate": "CONTROL_RECOVERY_PASS iff A1_single and A2_coherent2 held-out para_full >= 80 under AnyEdit window_size=50",
            "baseline_reference_frozen": {"hparams": HP_BASE, "layers": [4, 5, 6, 7, 8]},
            "stimulus": {"CANON": c10.CANON, "PTEST": c10.PTEST, "FICTION": c10.FICTION, "V_A1_single": c10.ARMS["A1_single"], "V_A2_coherent2": c10.ARMS["A2_coherent2"]},
            "base_report": base_report,
            "recipes": {
                "baseline_controls": run_baseline_controls(arm_names),
                "anyedit_window50_controls": run_anyedit_recipe("anyedit_window50_controls", 50, arm_names),
            },
        }
        results["verdict"] = control_recovery_verdict(results)
        out = args.out or f"{LLMDB_ROOT}/results/c10h_anyedit_window50_controls.json"
        with open(out, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("\n=== C10h WINDOW50 CONTROL DIAGNOSTIC SUMMARY ===", flush=True)
        print(json.dumps(results["verdict"], indent=2), flush=True)
        print(f"\nwrote {out}", flush=True)
        print("C10H_WINDOW50_CONTROLS_DONE", flush=True)
        return 0

    base_report = c10.pre_base_report()
    print("\n=== STIMULUS BASE CHECK ===", flush=True)
    for k, v in base_report.items():
        print(f"  {k:18} base={v['base']}/{c10.N} ntok={v['mean_ntok']} range={v['ntok_range']}", flush=True)
    results = {
        "decision_id": "D-C10h-anyedit-pilot",
        "prereg": PREREG,
        "run": "C10 AnyEdit small-window pilot",
        "class": "FALSIFIER-resolver / AnyEdit feasibility pilot; NOT promotable",
        "scope": "Qwen2.5-3B / capital / A1-A2-A7 / N=24 / 1-seed / HF-fp16",
        "baseline_reference_frozen": {"hparams": HP_BASE, "layers": [4, 5, 6, 7, 8]},
        "stimulus": {"CANON": c10.CANON, "PTEST": c10.PTEST, "FICTION": c10.FICTION, **{f"V_{k}": v for k, v in c10.ARMS.items()}},
        "base_report": base_report,
        "recipes": {"baseline": c10.run_recipe("baseline", HP_BASE)},
    }
    results["recipes"]["anyedit_window1"] = run_anyedit_recipe("anyedit_window1", 1)
    if args.run_default_window:
        results["recipes"]["anyedit_window50_diagnostic"] = run_anyedit_recipe("anyedit_window50_diagnostic", 50)
    results["verdict"] = final_verdict(results)
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n=== C10h ANYEDIT PILOT SUMMARY ===", flush=True)
    print(json.dumps(results["verdict"], indent=2), flush=True)
    print(f"\nwrote {OUT}", flush=True)
    print("C10H_DONE", flush=True)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="token/window alignment only; no model load")
    ap.add_argument("--dry-out", default=None)
    ap.add_argument("--n", type=int, default=int(os.environ.get("N_EDIT", "24")))
    ap.add_argument("--window-size", type=int, default=1)
    ap.add_argument("--overlap", type=int, default=0)
    ap.add_argument("--run-default-window", action="store_true")
    ap.add_argument("--window50-controls-only", action="store_true", help="run A1/A2-only upstream-window diagnostic; diagnostic-only, no A7")
    ap.add_argument("--out", default=None, help="override durable result JSON path for diagnostic modes")
    args = ap.parse_args()
    if args.dry_run:
        return dry_run(args)
    return run_gpu(args)


if __name__ == "__main__":
    sys.exit(main())
