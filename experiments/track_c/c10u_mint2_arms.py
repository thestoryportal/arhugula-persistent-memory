#!/usr/bin/env python3
"""D-C10u-mint2 v3: frozen, staged operator driver. Import is model-free.

Each public stage orchestrates fresh child processes; it never calls H.main().
Runtime stages load a model ONLY after immutable-source, output and LAW#3 checks.
This module is preparation, not permission to run the experiment.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse, ast, contextlib, copy, datetime, hashlib, importlib, io, json, math
import re, subprocess, traceback, uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10u_mint2_read as R

PREREG = "docs/C10U_MINT2_PREREG.md"
WORDLIST = "results/c10u_mint2/v2_wordlist.json"
HP_FILE = "configs/hparams/qwen25_3b_memit_hparams.json"
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]
HARNESS_KNOBS = ("MODEL_ID", "MODEL_REV", "HP_CANDIDATE", "OUT", "CANDIDATE_NAME", "DECISION_ID", "PREREG", "RUN_LABEL",
                 "Z_OVERRIDE", "C10_PROJECTOR", "N_EDIT", "C10_SUBJECT_OFFSET", "C10_ARMS", "C10_KEY_LOCUS", "C10_CTX_TEMPLATES", "C10_RECIPES",
                 "MINT_ARM", "MINT_STEP0", "MINT_INITS", "MINT_N_SEED", "MINT_INIT_TAG", "MINT_SAVE_DIR", "LAW3_REF")
SOURCE_FILES = ["experiments/track_c/c10u_mint2_" + name + ".py" for name in ("arms", "step0", "read", "selftest", "p4_probe")] + [
    "tools/c10u_mint2_p4.sh", "experiments/track_c/c10u_mint2_wordlist.py", "experiments/track_c/c10l_mint_lib.py",
    "experiments/track_c/c10e_bandknob.py", PREREG, WORDLIST, HP_FILE, "tools/engine_fingerprint.py",
    "configs/screens/g6_screen_qwen3b.json", "configs/screens/g6_screen_qwen3b_v2.json"]
STAGE = "not-started"
IDENTITY = None
RUN_ROOT = Path(LLMDB_ROOT).resolve()


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    """Preserve occupied outputs; verify the persisted bytes and parsed value."""
    path = Path(path)
    payload = json.dumps(obj, indent=2, allow_nan=False, ensure_ascii=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        f.write(payload)
    actual = path.read_text(encoding="utf-8")
    if actual != payload or json.loads(actual) != obj:
        raise RuntimeError(f"JSON did not persist exactly: {path}")


def occupied(directory, names):
    found = [str(Path(directory) / name) for name in names if (Path(directory) / name).exists()]
    if found:
        raise ValueError("occupied outputs are never overwritten: " + repr(found))


def halt(reason, root=None, **state):
    root = Path(root or RUN_ROOT)
    path = root / "architecture_profile/c10u_mint2_halt_diagnostic.json"
    if path.exists():
        path = path.with_name("c10u_mint2_halt_diagnostic_" + uuid.uuid4().hex + ".json")
    rec = {"decision_id": R.DECISION_ID, "stage": STAGE, "when_utc": utc_now(),
           "identity": IDENTITY, "reason": reason, "state": state}
    try:
        write_json(path, rec)
    except Exception as exc:
        raise SystemExit(f"HALT: {reason}; diagnostic could not be persisted: {exc!r}") from exc
    raise SystemExit(f"HALT: {reason}; diagnostic: {path}")


def source_hashes(root):
    root = Path(root)
    engine = sorted(str(p.relative_to(root)) for p in (root / "memit_dry_run/memit").rglob("*.py"))
    if not engine:
        raise ValueError("vendored engine source inventory is empty")
    return {name: sha256_file(root / name) for name in [*SOURCE_FILES, *engine]}


def source_digest(hashes):
    return hashlib.sha256("\n".join(k + " " + v for k, v in sorted(hashes.items())).encode()).hexdigest()


def assert_sources(identity, root):
    now = source_hashes(root)
    old = identity["source_sha256"]
    changed = {k: [old.get(k), now.get(k)] for k in set(old) | set(now) if old.get(k) != now.get(k)}
    if changed or identity["source_digest"] != source_digest(old):
        raise ValueError("frozen source identity differs: " + repr(changed))


def frozen_words(root):
    d = json.loads((Path(root) / WORDLIST).read_text())
    if (hashlib.sha256("\n".join(d["heads"]).encode()).hexdigest() != R.HEADS_SHA256
            or d["heads_sha256"] != R.HEADS_SHA256
            or hashlib.sha256("\n".join(d["modifier_only"]["modifiers"]).encode()).hexdigest() != R.MODIFIERS_SHA256
            or d["modifier_only"]["modifiers_sha256"] != R.MODIFIERS_SHA256):
        raise ValueError("frozen head/modifier inventory differs")
    if len(d["heads"]) != 24 or len(set(d["heads"])) != 24 or len(d["values"]) != 24:
        raise ValueError("word-list population is not the frozen 24")
    if hashlib.sha256(json.dumps(d["values"], sort_keys=True).encode()).hexdigest() != d["values_sha256"]:
        raise ValueError("frozen subject/value table hash differs")
    return d


def law3_reference(path):
    data = json.loads(Path(path).read_text())
    arms = data["recipes"]["baseline"]["arms"]
    scores = {name: arms[name]["para_full_n"] for name in ("A1_single", "A2_coherent2")}
    reading = R.law3_reference_reading(scores)
    if not reading["ok"]:
        raise ValueError("LAW#3 A1/A2 reference failed: " + repr(reading))
    return {"path": str(Path(path).resolve()), "sha256": sha256_file(path), "scores": scores, "ok": True}


def preflight(root):
    """No imports of torch/model and no stage marker before these refusals."""
    inherited = {k: os.environ[k] for k in HARNESS_KNOBS if k in os.environ}
    if inherited:
        raise ValueError("frozen harness knobs must be unset: " + repr(inherited))
    root = Path(root).resolve()
    fp = subprocess.run([sys.executable, str(root / "tools/engine_fingerprint.py")], capture_output=True,
                        text=True, env={**os.environ, "LLMDB_ROOT": str(root)})
    if fp.returncode != 0 or not fp.stdout.strip() or "engine fingerprint PASS:" not in fp.stdout:
        raise RuntimeError("engine fingerprint failed: " + fp.stdout + fp.stderr)
    engine = root / "memit_dry_run/memit/memit/memit_main.py"
    return {"ok": True, "stdout": fp.stdout, "sha256": sha256_file(engine), "_cov_cpu": engine.read_bytes().count(b"_cov_cpu")}


def initialise_identity(root, out, reference):
    global IDENTITY
    path = out / "identity.json"
    if path.exists():
        IDENTITY = json.loads(path.read_text())
        assert_sources(IDENTITY, root)
        if IDENTITY["law3_reference"] != reference:
            raise ValueError("LAW#3 reference differs from the frozen identity")
    else:
        hashes = source_hashes(root)
        IDENTITY = {"run_id": "c10u-" + uuid.uuid4().hex, "created_utc": utc_now(), "source_sha256": hashes,
                    "source_digest": source_digest(hashes), "law3_reference": reference}
        write_json(path, IDENTITY)
    return IDENTITY


def record_name(block, replicate, kind, seed):
    return f"{block}_r{replicate}_{kind}_s{seed if seed is not None else 'none'}"


def load_harness(root):
    """Operator-only boundary: c10e_bandknob.py:45–48 loads the pinned model."""
    os.environ.update(LLMDB_ROOT=str(root), C10_ARMS="A1_single,A7_coined_coined", C10_RECIPES="candidate",
                      HP_CANDIDATE=str(root / HP_FILE), CANDIDATE_NAME="mint2", DECISION_ID=R.DECISION_ID,
                      PREREG=str(root / PREREG), OUT=str(root / "results/c10u_mint2/unused_harness_output.json"))
    H = importlib.import_module("c10e_bandknob")
    M = importlib.import_module("c10l_mint_lib")
    hp = H.MEMITHyperParams.from_json(str(root / HP_FILE))
    if hp.layers != [4, 5, 6, 7, 8] or hp.fact_token != "subject_last" or hp.v_num_grad_steps != 25 or hp.v_loss_layer != 35:
        raise ValueError("frozen hparams differ")
    if H.Z_OVERRIDE is not None or H.Z_OVERRIDE_HITS != 0 or len(H.FICTION) != 24:
        raise ValueError("harness population/override defaults differ")
    M.assert_tied(H.model)  # c10l_mint_lib.py:44–48; no vocabulary resize.
    if M.SPARE_START != 151665 or M.VOCAB_ROWS != 151936:
        raise ValueError("spare-row layout differs")
    return H, M, hp


def set_contexts(H, contexts):
    """Assign the existing engine cache before LAW#5, never sample after minting."""
    MM = importlib.import_module("memit.memit_main")
    if not contexts or contexts[0] != ["{}"] or any(t.count("{}") != 1 for g in contexts for t in g):
        raise ValueError("context template set is malformed")
    MM.CONTEXT_TEMPLATES_CACHE = copy.deepcopy(contexts)
    if H.get_context_templates(H.model, H.tok) != contexts:
        raise ValueError("context-cache assignment was not preserved")


def values_for(H, words, block):
    values = words["values"] if block == "V2" else words["modifier_only"]["frozen_values"]
    if block == "F" and values != H.ARMS["A7_coined_coined"]:
        raise ValueError("frozen A7 values differ from build_stimuli")
    if list(values) != H.FICTION:
        raise ValueError("subject ordering differs")
    return dict(values)


def registration_words(words, values, kind):
    if kind == "multi":
        return []
    if kind == "mint1":
        return list(values.values())
    if kind == "mint1_48":
        return list(values.values()) + words["heads"]
    if kind == "mint2":
        return words["heads"] + [v.split()[1] for v in words["values"].values()]
    if kind == "modifier":
        return words["modifier_only"]["modifiers"]
    raise ValueError("unknown arm kind: " + kind)


def ids_of(tok, text):
    return list(tok(text, add_special_tokens=False)["input_ids"])


def p2_audit(base_tok, minted_tok, words, ids, values, subjects, frames, contexts, prompts, kind, block):
    """Token-only admission, including the engine's default decode/re-tokenise path."""
    plain = list(dict.fromkeys(prompts))
    inventory = list(dict.fromkeys(plain + [t.format(p) for g in contexts for t in g for p in plain]))
    changed = [p for p in inventory if ids_of(base_tok, p) != ids_of(minted_tok, p)]
    checks = {"inventory_unchanged": not changed, "registered_word_ids": len(words) == len(ids) and all(
        ids_of(minted_tok, " " + w) == [i] and minted_tok(" " + w)["input_ids"] == [i] for w, i in zip(words, ids))}
    lookup = dict(zip(words, ids))
    rows = []
    canon = "The capital of {} is the city of"
    for s in subjects:
        v = values[s]
        head, mod = v.split()
        target = ids_of(minted_tok, " " + v)
        if kind in ("mint1", "mint1_48"):
            expected = [lookup[v]]
        elif kind == "mint2":
            expected = [lookup[head], lookup[mod]]
        elif kind == "modifier":
            expected = ids_of(base_tok, " " + head) + [lookup[mod]]
        else:
            expected = ids_of(base_tok, " " + v)
        prefix = minted_tok.decode(target[:-1])
        contexts_ok = []
        for t in [t for g in contexts for t in g]:
            p = t.format(canon.format(s))
            contexts_ok.append({"template": t, "prefix_ids": ids_of(minted_tok, p + prefix) == ids_of(minted_tok, p) + target[:-1],
                                "whole_ids": ids_of(minted_tok, p + " " + v) == ids_of(minted_tok, p) + target,
                                "last_id": bool(target) and ids_of(minted_tok, p + " " + v)[-1] == target[-1]})
        row_checks = {"whole_target": target == expected, "decode": minted_tok.decode(target) == " " + v,
                      "engine_default_call": minted_tok(" " + v)["input_ids"] == target,
                      "contexts": all(all(x[k] for k in ("prefix_ids", "whole_ids", "last_id")) for x in contexts_ok)}
        if kind == "mint2":
            row_checks["head_decode"] = minted_tok.decode([lookup[head]]) == " " + head
        rows.append({"subj": s, "value": v, "target_ids": target, "expected_ids": expected, "contexts": contexts_ok,
                     "checks": row_checks, "ok": all(row_checks.values())})
    checks["all_target_rows"] = len(rows) == 24 and all(r["ok"] for r in rows)
    bigram = []
    if kind == "mint2":
        for s in [*subjects, *frames]:
            p = canon.format(s)
            for head in [values[c].split()[0] for c in subjects]:
                good = ids_of(minted_tok, p + " " + head) == ids_of(minted_tok, p) + [lookup[head]]
                bigram.append({"subj": s, "head": head, "ok": good})
        checks["bigram_720_prefix_ids"] = len(bigram) == 720 and all(x["ok"] for x in bigram)
    return {"ok": all(checks.values()), "checks": checks, "changed": changed, "inventory_n": len(inventory),
            "plain_n": len(plain), "rows": rows, "bigram_rows": bigram, "block": block, "kind": kind}


def constants_from(path, names):
    """Read literal harness constants without importing a second model-loading driver."""
    tree = ast.parse(Path(path).read_text())
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in names:
                found[name] = ast.literal_eval(node.value)
    if set(found) != set(names):
        raise ValueError("literal constants missing: " + repr(set(names) - set(found)))
    return found


def audit_prompts(H, M, root):
    """Superset of lib:178–185 and the 396-prompt published tokenizer pre-screen."""
    screens = [json.loads((root / f"configs/screens/{s}.json").read_text())["selected"]
               for s in ("g6_screen_qwen3b", "g6_screen_qwen3b_v2")]
    countries = sorted({c for screen in screens for c in screen})
    capitals = sorted({v["capital"]["truth"] for screen in screens for v in screen.values()})
    forms = [H.CANON, *H.PTEST, "{} is described as", "{} is a", "{} is associated with"]
    prompts = M.all_harness_prompts(H) + [p.format(s) for s in H.FICTION + FRAME_SUBJECTS + ["Zorbland"] for p in forms]
    prompts += [H.CANON.format(c) for c in countries] + H.GENERIC + M.UNRELATED + [" " + c for c in capitals]
    return list(dict.fromkeys(prompts)), countries, capitals


def static_wordlist_audit(H, base_tok, words, countries, capitals, M, root):
    """Replay §1.1's authored selection/relations; never repair the frozen file."""
    literals = constants_from(root / "experiments/track_c/c10e_bandknob.py", {"coined_head", "coined_mod"})
    names = {w.lower() for text in H.FICTION + FRAME_SUBJECTS + countries + capitals + literals["coined_head"] + literals["coined_mod"]
             for w in re.findall(r"[A-Za-z]+", text)}
    forms = [H.CANON, *H.PTEST, "{} is described as", "{} is a", "{} is associated with", *H.GENERIC, *M.UNRELATED, "Zorbland", "Cairo"]
    inventory = names | {w.lower() for text in forms for w in re.findall(r"[A-Za-z]+", text)}
    candidates = constants_from(root / "experiments/track_c/c10u_mint2_wordlist.py", {"HEAD_CANDIDATES"})["HEAD_CANDIDATES"]
    quota = {}
    for v in words["modifier_only"]["frozen_values"].values():
        n = len(ids_of(base_tok, " " + v.split()[0]))
        quota[n] = quota.get(n, 0) + 1
    left, selected, rows = dict(quota), [], []
    for head in candidates:
        h = head.lower()
        bad = sorted(w for w in inventory if h == w or h in w or ((w in names or len(w) >= 4) and w in h))
        n = len(ids_of(base_tok, " " + head))
        good = not bad and n >= 2 and head.isalpha() and head[0].isupper() and head[1:].islower()
        rows.append({"head": head, "n_pieces": n, "forbidden_relations": bad, "pass": good})
        if good and left.get(n, 0) > 0:
            selected.append(head)
            left[n] -= 1
    registered = words["heads"] + literals["coined_mod"]
    collisions = [[a, b] for a in registered for b in registered if a != b and a.lower() in b.lower()]
    inventory_sha = hashlib.sha256("\n".join(sorted(inventory)).encode()).hexdigest()
    return {"ok": selected == words["heads"] and not collisions and inventory_sha == words["inventory_sha256"]
                  and {str(k): v for k, v in quota.items()} == words["head_pieces_quota"],
            "selected": selected, "candidates": rows, "pairwise_relations": collisions, "inventory_sha256": inventory_sha,
            "quota": {str(k): v for k, v in quota.items()}}


def provenance(root, words, block, contexts, pairing=None):
    relation_table = {"block": block, "subject_values": words["values"] if block == "V2" else words["modifier_only"]["frozen_values"],
                      "candidates": words["candidates"], "pairwise_relations_among_48": words["pairwise_relations_among_48"],
                      "modifier_relations": words["modifier_only"]["pairwise_relations"],
                      "short_common_words_inside_heads": words["short_common_words_inside_heads"]}
    return {"heads_sha256": R.HEADS_SHA256, "modifiers_sha256": R.MODIFIERS_SHA256,
            "rules": words["rules"], "rules_sha256": R.json_digest(words["rules"]),
            "relation_table": relation_table, "relation_sha256": R.json_digest(relation_table),
            "wordlist_sha256": sha256_file(root / WORDLIST), "ctx_sha256": R.json_digest(contexts), "row_pairing": pairing}


def save_tensor(path, tensor, torch):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tensor = tensor.detach().cpu()
    with path.open("xb") as f:
        torch.save(tensor, f)
    loaded = torch.load(path, map_location="cpu", weights_only=True)
    if not torch.equal(loaded, tensor):
        raise RuntimeError("tensor did not round-trip: " + str(path))
    return sha256_file(path)


def rows_and_pairing(H, M, base_tok, registered, seed):
    # lib:60–92 draws N sequentially on CPU. Both prefix lengths must match.
    rows = M.build_init(H.model, base_tok, registered, "N", seed=seed).detach().float().cpu()
    n8 = M.build_init(H.model, base_tok, ["pairing"] * 8, "N", seed=seed).detach().float().cpu()
    n24 = M.build_init(H.model, base_tok, ["pairing"] * 24, "N", seed=seed).detach().float().cpu()
    torch = H.torch
    good = torch.equal(rows[:8], n8) and torch.equal(rows[:min(24, len(rows))], n24[:min(24, len(rows))])
    if not good:
        raise ValueError("N(seed) row-prefix pairing failed")
    return rows, {"rows_sha256": M.sha256_tensor(rows), "first8_sha256": M.sha256_tensor(n8),
                  "first24_sha256": M.sha256_tensor(n24), "pairing_ok": good, "n_rows": len(rows), "seed": seed}


def greedy_ids(H, prompt, n):
    with H.torch.no_grad():
        cur = H.tok(prompt, return_tensors="pt").to(H.DEV)["input_ids"]
        result = []
        for _ in range(n):
            nxt = int(H.model(cur).logits[0, -1].argmax())
            result.append(nxt)
            cur = H.torch.cat([cur, H.torch.tensor([[nxt]], dtype=cur.dtype, device=cur.device)], dim=1)
        return result


def teacher_position(H, prompt, target_ids):
    with H.torch.no_grad():
        base = H.tok(prompt, return_tensors="pt").to(H.DEV)["input_ids"]
        result = []
        for j, tid in enumerate(target_ids):
            suffix = H.torch.tensor([target_ids[:j]], dtype=base.dtype, device=base.device)
            cur = H.torch.cat([base, suffix], dim=1)
            logits = H.model(cur).logits[0, -1].float()
            result.append({"id": int(logits.argmax()), "correct": int(logits.argmax()) == tid,
                           "prob": float(logits.softmax(-1)[tid])})
        return result


def step0_probe(H, M, base_tok, values, registered, ids):
    """Whole-sequence recall; head/modifier rank at both ordered and misplaced slots."""
    recall, probes = [], []
    for s, value in values.items():
        target = H.tgt_ids(value)
        hits = [H.full_seq_match(p.format(s), target)[0] for p in H.PTEST]
        recall.append({"subj": s, "para_full_hits": hits})
        p = H.CANON.format(s)
        head_ids = ids_of(H.tok, " " + value.split()[0])
        diagnostics = {"head_at_value_slot": M.rank_prob(H, p, target[0]),
                       "modifier_misplaced_at_value_slot": M.rank_prob(H, p, target[-1]),
                       "modifier_after_head": M.rank_prob(H, p + H.tok.decode(head_ids), target[-1]),
                       "canonical_base_first": M.rank_prob(H, p, ids_of(base_tok, " " + value)[0])}
        para_mod = []
        for form in H.PTEST:
            probes_for_form = {}
            for name, text in (("misplaced", form.format(s)), ("after_head", form.format(s) + H.tok.decode(head_ids))):
                rank, prob, top1 = M.rank_prob(H, text, target[-1])
                probes_for_form[name] = {"rank": rank, "prob": prob, "top1": top1}
            para_mod.append({"prompt": form.format(s), **probes_for_form})
        probes.append({"subj": s, "target_ids": target, "head_ids": head_ids,
                       "rank_prob_top1": {k: {"rank": v[0], "prob": v[1], "top1": v[2]} for k, v in diagnostics.items()},
                       "modifier_paraphrase_probes": para_mod})
    inventory = []
    for w, tid in zip(registered, ids):
        ranks = [M.rank_prob(H, p, tid) for p in M.UNRELATED]
        inventory.append({"word": w, "id": tid, "unrelated": [{"rank": r, "prob": p, "top1": t} for r, p, t in ranks],
                          "unrelated_hits": sum(t == tid for _, _, t in ranks)})
    reading = R.i11_reading(inventory, recall)
    first_id_probe = M.i11_probe(H, list(values.values()), [H.tgt_ids(v)[0] for v in values.values()], base_tok)
    return {"recall_rows": recall, "recall_n": sum(sum(r["para_full_hits"]) for r in recall),
            "rank_probes": probes, "minted_inventory": inventory, "head_or_whole_id_classes": first_id_probe,
            "class_probe_note": "lib.i11_probe reports first-id ranks/classes; its legacy first-id para_full_step0 is diagnostic only. Binding uses recall_rows whole sequences.", **reading}


def fit_at_z(H, hp, subject, value, z):
    """Inject the engine-returned z at subject_last; read final and loss-layer logits."""
    CZ = importlib.import_module("memit.compute_z")
    nethook = importlib.import_module("util.nethook")
    layer = hp.layer_module_tmp.format(hp.layers[-1])
    loss_layer = hp.layer_module_tmp.format(max(hp.v_loss_layer, hp.layers[-1]))
    target = H.tgt_ids(value)
    key_idx = CZ.find_fact_lookup_idx(H.CANON, subject, H.tok, hp.fact_token, verbose=False)
    final, loss_probs = [], []
    ln_f = nethook.get_module(H.model, hp.ln_f_module)
    lm_w = nethook.get_parameter(H.model, hp.lm_head_module + ".weight").T
    try:
        lm_b = nethook.get_parameter(H.model, hp.lm_head_module + ".bias")
    except LookupError:
        lm_b = next(H.model.parameters()).new_zeros(H.model.config.vocab_size)
    def inject(output, name):
        if name == layer:
            output[0][0, key_idx, :] = z.to(output[0].device, output[0].dtype)
        return output
    with H.torch.no_grad():
        for j, tid in enumerate(target):
            text = H.CANON.format(subject) + H.tok.decode(target[:j])
            tokens = H.tok(text, return_tensors="pt").to(H.DEV)
            expected = ids_of(H.tok, H.CANON.format(subject)) + target[:j]
            if tokens["input_ids"][0].tolist() != expected:
                raise ValueError("identity-template fit input re-tokenised")
            with nethook.TraceDict(H.model, [layer, loss_layer], retain_input=False, retain_output=True, edit_output=inject) as tr:
                logits = H.model(**tokens).logits[0, -1].float()
            output = tr[loss_layer].output[0][0, -1]
            loss_logits = (ln_f(output) @ lm_w + lm_b).float()
            final.append(float(logits.softmax(-1)[tid]))
            loss_probs.append(float(loss_logits.softmax(-1)[tid]))
    return {"subj": subject, "target_ids": target, "probs": final, "loss_layer_probs": loss_probs,
            "max_readout_diff": max(abs(a - b) for a, b in zip(final, loss_probs))}


def capture_targets(H, hp, values, contexts):
    zs, aggregates, fits, logs = [], [], [], []
    for s, value in values.items():
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            z = H.compute_z(H.model, H.tok, H.req(H.CANON, s, value), hp, hp.layers[-1], contexts)
        stdout = buf.getvalue()
        matches = re.findall(r"avg prob of \[.*?\]\s+([0-9.eE+-]+)", stdout)
        if not matches:
            raise ValueError("engine compute_z aggregate was absent for " + s)
        aggregate = float(matches[-1])
        if not math.isfinite(aggregate) or not 0 <= aggregate <= 1:
            raise ValueError("engine compute_z aggregate was invalid for " + s)
        zs.append(z.detach().float().cpu())
        aggregates.append(aggregate)
        fits.append(fit_at_z(H, hp, s, value, z))
        logs.append({"subj": s, "stdout": stdout})
        print(f"  capture {s}: avgprob={aggregate:.6f}", flush=True)
    return H.torch.stack(zs), aggregates, fits, logs


def wrapper_inertness(H, hp, contexts):
    """Prove both new wrappers on one identity-equivalent Cairo edit, then restore.

    The actual science write still uses H.run_recipe's untouched LAW#5 gate.
    Native solve -> captured engine z -> override must agree in weights/output;
    assigning a deep copy of the cache must agree too. No override in LAW#5.
    """
    torch = H.torch
    snap = H.snap_layers(hp)
    P = H.compute_P(hp)
    request = H.req(H.CANON, "Zorbland", "Cairo")
    key = (request["subject"], request["target_new"]["str"])
    MM = importlib.import_module("memit.memit_main")
    MM.CONTEXT_TEMPLATES_CACHE = contexts
    with contextlib.redirect_stdout(io.StringIO()):
        z = H.compute_z(H.model, H.tok, request, hp, hp.layers[-1], contexts)
    def trial(override, reassigned):
        MM.CONTEXT_TEMPLATES_CACHE = copy.deepcopy(contexts) if reassigned else contexts
        H.Z_OVERRIDE = {key: z} if override else None
        H.Z_OVERRIDE_HITS = 0
        cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in hp.layers]
        with contextlib.redirect_stdout(io.StringIO()):
            H.my_edit(hp, [request], P, cache)
        weights = {k: v.detach().float().cpu() for k, v in H.snap_layers(hp).items()}
        output = H.predict(H.CANON.format("Zorbland"))["dist"].cpu().float()
        hits = H.Z_OVERRIDE_HITS
        H.restore_layers(hp, snap)
        return weights, output, hits
    try:
        native, p0, native_hits = trial(False, False)
        replay, p1, replay_hits = trial(True, False)
        assigned, p2, assigned_hits = trial(True, True)
        def relative(a, b):
            # MPS cannot represent double: transfer BEFORE casting (P-8).
            numerator = sum(float((a[k].cpu().double() - b[k].cpu().double()).square().sum()) for k in a)
            denominator = sum(float(a[k].cpu().double().square().sum()) for k in a)
            return math.sqrt(numerator / max(denominator, 1e-30))
        reading = R.inertness_reading(relative(native, replay), relative(replay, assigned),
                                      max(float((p0 - p1).abs().max()), float((p1 - p2).abs().max())))
        reading["native_hits"] = native_hits
        reading["replay_hits"] = replay_hits
        reading["assigned_hits"] = assigned_hits
        reading["counter_ok"] = (native_hits, replay_hits, assigned_hits) == (0, 1, 1)
        reading["ok"] = reading["ok"] and reading["counter_ok"]
        return reading
    finally:
        H.restore_layers(hp, snap)
        H.Z_OVERRIDE = None
        H.Z_OVERRIDE_HITS = 0
        set_contexts(H, contexts)


def position_curve(H, hp, values, fits):
    """All facts stay in the curve; a masked companion carries its own n."""
    positions = R.position_reading(fits)
    underfit = {r["subj"] for r in positions["rows"] if r["underfit"]}
    curve, masked, facts, states = {}, {}, [], []
    nethook = importlib.import_module("util.nethook")
    with H.torch.no_grad():
        for subject, value in values.items():
            target = H.tgt_ids(value)
            rows = []
            for form in H.PTEST:
                prompt = form.format(subject)
                tf = teacher_position(H, prompt, target)
                for j, cell in enumerate(tf):
                    for table in [curve] + ([] if subject in underfit else [masked]):
                        d = table.setdefault(str(j), {"hits": 0, "n": 0})
                        d["hits"] += cell["correct"]
                        d["n"] += 1
                rows.append([x["correct"] for x in tf])
                with nethook.Trace(H.model, hp.layer_module_tmp.format(hp.layers[-1]), retain_output=True) as tr:
                    H.model(**H.tok(prompt, return_tensors="pt").to(H.DEV))
                states.append(tr.output[0][0, -1].detach().float().cpu())
            facts.append({"subj": subject, "underfit": subject in underfit, "per_template_hits": rows})
    return {"per_position_teacher_forced": curve, "per_position_teacher_forced_masked": masked,
            "per_fact_position_curve": facts}, H.torch.stack(states)


def bigram_probe(H, values, kind):
    if kind not in ("mint2", "modifier"):
        return []
    subjects = list(values)
    rows = []
    for i, subject in enumerate(subjects):
        head, mod = values[subject].split()
        mod_id = H.tgt_ids(mod)[0]
        if kind == "mint2":
            swapped = subjects[(i + 12) % 24]
            sibling = None
        else:
            swapped = next(subjects[(i + j) % 24] for j in range(1, 24)
                           if values[subjects[(i + j) % 24]].split()[0] != head
                           and values[subjects[(i + j) % 24]].split()[1] != mod)
            sibling = next(s for s in subjects if s != subject and values[s].split()[0] == head)
        def hit(s):
            return int(H.predict(H.CANON.format(s) + " " + head)["id"] == mod_id)
        never = [hit(s) for s in FRAME_SUBJECTS]
        rows.append({"subj": subject, "head": head, "modifier": mod, "modifier_id": mod_id,
                     "swapped_subject": swapped, "sibling_subject": sibling,
                     "c_k": hit(subject), "s_k": hit(swapped), "b_k": hit(sibling) if sibling else 0,
                     "n_k": sum(never) / 6, "never_edited_hits": never})
    return rows


def p4_reference(H, M, values, registered, ids):
    groups = {"canon": [], "para": [], "L1": [], "L3": [], "unrelated": []}
    for s, value in values.items():
        target = H.tgt_ids(value)
        for group, prompts in (("canon", [H.CANON]), ("para", H.PTEST)):
            for form in prompts:
                prompt = form.format(s)
                groups[group].append({"subj": s, "prompt": prompt, "value": value, "expected_ids": target,
                                      "hf_ids": greedy_ids(H, prompt, len(target))})
    for group, prompts in (("L1", H.L1_PROMPTS), ("L3", H.L3_PROMPTS), ("unrelated", M.UNRELATED)):
        groups[group] = [{"prompt": p, "hf_ids": greedy_ids(H, p, 1), "expected_ids": None} for p in prompts]
    return {"decision_id": R.DECISION_ID, "minted": [{"word": w, "id": i} for w, i in zip(registered, ids)],
            "targets": [{"subj": s, "value": v, "expected_ids": H.tgt_ids(v)} for s, v in values.items()], "groups": groups}


def behavior_hook(H, M, hp, values, ids, kind, fits, z_rows, save_dir, root):
    before_rel = {name: [H.predict(form.format(s))["id"] for s in H.FICTION]
                  for name, form in (("is_a", "{} is a"), ("associated_with", "{} is associated with"))}
    def hook(arm_name, Vmap):
        if arm_name != "A7_coined_coined":
            return {}
        minted = set(ids)
        curve, states = position_curve(H, hp, values, fits)
        first_ids = {H.tgt_ids(v)[0] for v in values.values()}
        sibling = sum(H.predict(form.format(s))["id"] in minted
                      and H.predict(form.format(s))["id"] != H.tgt_ids(v)[0]
                      for s, v in values.items() for form in H.PTEST)
        unrelated = [H.predict(p)["id"] for p in M.UNRELATED]
        cannibal = R.i11_reading([{"id": i, "unrelated_hits": unrelated.count(i)} for i in ids], []) ["n_cannibal"]
        frame_rows = [{"subj": s, "id": H.predict(H.CANON.format(s))["id"]} for s in FRAME_SUBJECTS]
        frame_flips = sum(r["id"] in first_ids for r in frame_rows)
        fires = {"L1_minted_n": sum(H.predict(p)["id"] in minted for p in H.L1_PROMPTS),
                 "L3_minted_n": sum(H.predict(p)["id"] in minted for p in H.L3_PROMPTS),
                 "frame_minted_n": sum(r["id"] in minted for r in frame_rows),
                 "unrelated_minted_n": sum(i in minted for i in unrelated)}
        # Twenty generated ids per GENERIC sentence is a diagnostic-only budget.
        emissions = []
        for p in H.GENERIC:
            generated = greedy_ids(H, p, 20)
            emissions.append({"prompt": p, "ids": generated, "minted_positions": [j for j, i in enumerate(generated) if i in minted]})
        relations = {name: sum(H.predict(form.format(s))["id"] != pre for s, pre in zip(H.FICTION, before_rel[name]))
                     for name, form in (("is_a", "{} is a"), ("associated_with", "{} is associated with"))}
        extra = {**curve, **fires, "same_frame_flips": frame_flips, "frame_probe": frame_rows,
                 "para_sibling": sibling, "post_write_cannibal": cannibal, "generic_minted_emissions": emissions,
                 "generic_emission_rate": sum(len(r["minted_positions"]) for r in emissions) / (20 * len(emissions)),
                 "relation_flips": relations, "bigram": bigram_probe(H, values, kind),
                 "bigram_context_properties": {"head_is_edited_subject_n": sum(v.split()[0] in values for v in values.values()),
                                               "head_is_own_subject_n": sum(v.split()[0] == s for s, v in values.items()),
                                               "distinct_heads": len({v.split()[0] for v in values.values()}),
                                               "distinct_modifiers": len({v.split()[1] for v in values.values()})},
                 "post_geometry": {"value_slot_72": M.piv_stats(states.cpu()),
                                   "z_block": M.piv_stats(z_rows.cpu()) if z_rows is not None else None},
                 "embedding_rows_unchanged": M.sha256_tensor(M.get_rows(H.model, ids).cpu()) if ids else None}
        if save_dir:
            save_dir.mkdir(parents=True, exist_ok=False)
            H.model.save_pretrained(save_dir, safe_serialization=True)
            H.tok.save_pretrained(save_dir)
            ref = p4_reference(H, M, values, registration_words(frozen_words(root), values, kind), ids)
            ref.update(identity=IDENTITY, kind=kind, artifact_sha256={p.name: sha256_file(p) for p in sorted(save_dir.iterdir()) if p.is_file()})
            write_json(save_dir / "hf_fp16_sequences.json", ref)
            extra["p4_saved_to"] = str(save_dir)
        return extra
    return hook


def install_behavior_judgment(H):
    """Same fixed no-early-stop decode for CONTAINS and STARTSWITH."""
    original = H.eval_arm
    decoded = {}
    def contains(prompt, value, n):
        text = H.tok.decode(greedy_ids(H, prompt, n + 2))
        decoded[(prompt, value)] = text
        return " " + value in text
    H.string_match = contains
    def evaluate(values):
        arm = original(values)
        for row in arm["rows"]:
            row["para_startswith_hits"] = [decoded[(p.format(row["subj"]), row["val"])].startswith(" " + row["val"]) for p in H.PTEST]
            row["decoded_responses"] = [decoded[(p.format(row["subj"]), row["val"])] for p in H.PTEST]
            row["per_edge_3of3"] = all(row["para_full_hits"])
        arm["para_startswith_n"] = sum(sum(r["para_startswith_hits"]) for r in arm["rows"])
        arm["alt_tok_n"] = arm["para_string_n"] - arm["para_full_n"]
        arm["judgment_method"] = "exact_substring"
        arm["judgment_budget"] = "target_length + 2, greedy, no early stop"
        return arm
    H.eval_arm = evaluate


def context_job(root, out, block, fingerprint):
    name = f"contexts_{block}"
    occupied(out, [name + ".json", name + "_started.json"])
    write_json(out / (name + "_started.json"), {"identity": IDENTITY, "pid": os.getpid(), "block": block, "when_utc": utc_now()})
    H, M, hp = load_harness(root)
    # Untouched A7-multi precursor resolves §2's context/reproduction ordering.
    spare = list(range(M.SPARE_START, M.VOCAB_ROWS))
    spare_before = M.sha256_tensor(M.get_rows(H.model, spare))
    tokenizer_before = R.json_digest(H.tok.get_vocab())
    contexts = H.get_context_templates(H.model, H.tok)
    spare_after = M.sha256_tensor(M.get_rows(H.model, spare))
    tokenizer_after = R.json_digest(H.tok.get_vocab())
    if spare_after != spare_before or tokenizer_after != tokenizer_before:
        raise ValueError("context generation changed the untouched tokenizer/spare rows")
    words = frozen_words(root)
    values_for(H, words, block)
    rec = {"decision_id": R.DECISION_ID, "block": block, "identity": IDENTITY, "pid": os.getpid(),
           "kind": "A7-multi context-only precursor; no edit, no behavior count", "fingerprint": fingerprint,
           "ctx": contexts, "ctx_sha256": R.json_digest(contexts), "provenance": provenance(root, words, block, contexts),
           "tokenizer_untouched": True, "spare_rows_untouched": True,
           "spare_rows_sha256": spare_after, "tokenizer_vocab_sha256": tokenizer_after}
    assert_sources(IDENTITY, root)
    write_json(out / (name + ".json"), rec)


def read_context(root, out, block):
    data = json.loads((out / f"contexts_{block}.json").read_text())
    assert_sources(data["identity"], root)
    if not data["tokenizer_untouched"] or not data["spare_rows_untouched"] or data["ctx_sha256"] != R.json_digest(data["ctx"]):
        raise ValueError("context precursor failed its identity/untouched checks")
    return data["ctx"]


def step0_job(root, out, block, kind, seed, fingerprint):
    tag = record_name(block, 0, kind, seed)
    names = [f"step0/{tag}.json", f"step0/{tag}_started.json", f"inits/{tag}.pt", f"zs/{tag}.pt"]
    occupied(out, names)
    contexts = read_context(root, out, block)
    write_json(out / names[1], {"identity": IDENTITY, "pid": os.getpid(), "block": block, "kind": kind, "seed": seed})
    H, M, hp = load_harness(root)
    set_contexts(H, contexts)  # Before any registered word or solve.
    words = frozen_words(root)
    values = values_for(H, words, block)
    from transformers import AutoTokenizer
    base_tok = AutoTokenizer.from_pretrained(H.ID, revision=H.REV)
    prompts, countries, capitals = audit_prompts(H, M, root)
    static = static_wordlist_audit(H, base_tok, words, countries, capitals, M, root)
    registered = registration_words(words, values, kind)
    ids = M.register(H.tok, registered)  # lib:24–37: AddedToken + contiguous spare IDs.
    p2 = p2_audit(base_tok, H.tok, registered, ids, values, H.FICTION, FRAME_SUBJECTS, contexts, prompts, kind, block)
    p2["wordlist_replay"] = static
    p2["ok"] = p2["ok"] and static["ok"]
    if not p2["ok"]:
        write_json(out / names[0], {"decision_id": R.DECISION_ID, "identity": IDENTITY, "block": block, "kind": kind, "seed": seed,
                                  "P2": p2, "outcome": "INVALID", "wordlist_immutable": True})
        halt("P2 failed; frozen word list will not be automatically repaired", root, step0=names[0], P2=p2)
    rows, pairing = rows_and_pairing(H, M, base_tok, registered, seed)
    rows_sha = save_tensor(out / names[2], rows, H.torch)
    M.set_rows(H.model, ids, rows)  # lib:95–97: the sole embedding mutation.
    pairing["applied_rows_sha256"] = M.sha256_tensor(M.get_rows(H.model, ids))
    probe = step0_probe(H, M, base_tok, values, registered, ids)
    g = H.torch.Generator().manual_seed(1)
    ref_ids = H.torch.randperm(M.SPARE_START, generator=g)[:len(ids)]
    ref = M.embed(H.model).detach()[ref_ids.to(M.embed(H.model).device)].float().cpu()
    base_mean = float(M.embed(H.model).detach()[:M.SPARE_START].float().norm(dim=1).mean().cpu())
    geometry = {"rows": M.piv_stats(rows.cpu()), "applied_fp16_rows": M.piv_stats(M.get_rows(H.model, ids).cpu()),
                "random_base_same_count": M.piv_stats(ref.cpu()), "base_mean_norm": base_mean}
    geometry["norm_ratio"] = geometry["rows"]["mean_norm"] / base_mean
    zs, fits, positions, logs = capture_targets(H, hp, values, contexts)
    zs_sha = save_tensor(out / names[3], zs, H.torch)
    admission = R.admission_reading(p2, fits, probe)
    position_status = R.position_reading(positions)
    rec = {"decision_id": R.DECISION_ID, "block": block, "kind": kind, "seed": seed, "pid": os.getpid(),
           "identity": IDENTITY, "fingerprint": fingerprint, "ctx": contexts, "ctx_sha256": R.json_digest(contexts),
           "provenance": provenance(root, words, block, contexts, pairing), "values": values,
           "minted_words": registered, "minted_ids": ids, "P2": p2, "P3": admission["P3"],
           "admission": admission, "probe": probe, "per_position_fit": positions, "position_status": position_status,
           "geometry": {**geometry, **R.geometry_reading(geometry)}, "engine_solve_stdout": logs,
           "rows_file": names[2], "rows_file_sha256": rows_sha, "zs_file": names[3], "zs_file_sha256": zs_sha,
           "zs_tensor_sha256": M.sha256_tensor(zs), "outcome": admission["outcome"]}
    assert_sources(IDENTITY, root)
    write_json(out / names[0], rec)
    print(f"STEP0 {block} {kind} seed={seed}: {admission['outcome']}", flush=True)


def require_step0(root, out, block, kind, seed):
    path = out / "step0" / (record_name(block, 0, kind, seed) + ".json")
    rec = json.loads(path.read_text())
    assert_sources(rec["identity"], root)
    if (rec["block"], rec["kind"], rec["seed"]) != (block, kind, seed):
        raise ValueError("step0 arm identity differs")
    if rec["ctx_sha256"] != R.json_digest(read_context(root, out, block)):
        raise ValueError("step0 frozen context differs")
    for field in ("rows", "zs"):
        if sha256_file(out / rec[field + "_file"]) != rec[field + "_file_sha256"]:
            raise ValueError("step0 " + field + " tensor file hash differs")
    return rec


def behavior_job(root, out, block, replicate, kind, seed, fingerprint, save_for_p4=False, artifact_tag=None):
    tag = record_name(block, replicate, kind, seed)
    if artifact_tag is not None:
        if artifact_tag != "p4save_" + tag or not save_for_p4:
            raise ValueError("invalid P4-only artifact namespace")
        tag = artifact_tag
    save_dir = out / "edited" / ("c10u_mint2_" + tag) if save_for_p4 else None
    names = [tag + ".json", tag + "_started.json"] + ([str(save_dir.relative_to(out))] if save_dir else [])
    occupied(out, names)
    contexts = read_context(root, out, block)
    step = require_step0(root, out, block, kind, seed) if kind != "multi" else None
    if step is not None and step["outcome"] != "ADMITTED":
        # A failed aggregate screen has no behavioral run; retain an explicit record.
        rec = {"decision_id": R.DECISION_ID, "identity": IDENTITY, "block": block, "replicate": replicate,
               "kind": kind, "seed": seed, "pid": None, "outcome": step["outcome"], "step0_file": str(out / "step0" / (record_name(block, 0, kind, seed) + ".json")),
               "admission": step["admission"], "step0": step["probe"], "ctx": contexts, "ctx_sha256": R.json_digest(contexts),
               "fingerprint": fingerprint, "provenance": step["provenance"]}
        write_json(out / names[0], rec)
        return
    write_json(out / names[1], {"identity": IDENTITY, "pid": os.getpid(), "block": block, "replicate": replicate, "kind": kind, "seed": seed})
    H, M, hp = load_harness(root)
    set_contexts(H, contexts)  # Must precede LAW#5 apply; no minted sampling.
    words = frozen_words(root)
    values = values_for(H, words, block)
    ids, registered, rows, z_rows = [], [], None, None
    if step:
        registered = registration_words(words, values, kind)
        ids = M.register(H.tok, registered)
        if ids != step["minted_ids"] or registered != step["minted_words"] or values != step["values"]:
            raise ValueError("runtime registration differs from admitted step0")
        from transformers import AutoTokenizer
        base_tok = AutoTokenizer.from_pretrained(H.ID, revision=H.REV)
        prompts, countries, capitals = audit_prompts(H, M, root)
        p2 = p2_audit(base_tok, H.tok, registered, ids, values, H.FICTION, FRAME_SUBJECTS, contexts, prompts, kind, block)
        if not p2["ok"]:
            halt("behavior-process P2 replay failed", root, P2=p2)
        rows = H.torch.load(out / step["rows_file"], map_location="cpu", weights_only=True)
        z_rows = H.torch.load(out / step["zs_file"], map_location="cpu", weights_only=True)
        if M.sha256_tensor(rows) != step["provenance"]["row_pairing"]["rows_sha256"] or M.sha256_tensor(z_rows) != step["zs_tensor_sha256"]:
            raise ValueError("runtime init/z tensor content hash differs")
        regenerated, pairing = rows_and_pairing(H, M, base_tok, registered, seed)
        pairing["applied_rows_sha256"] = M.sha256_tensor(rows.to(M.embed(H.model).dtype).float().cpu())
        if not H.torch.equal(rows, regenerated) or pairing != step["provenance"]["row_pairing"]:
            raise ValueError("runtime N(seed) reproduction failed")
        M.set_rows(H.model, ids, rows)
        check_recall = step0_probe(H, M, base_tok, values, registered, ids)
        if check_recall["recall_rows"] != step["probe"]["recall_rows"]:
            raise ValueError("behavior pre-write whole-sequence recall differs from step0")
    inertness = wrapper_inertness(H, hp, contexts)
    if not inertness["ok"]:
        halt("z-override/context assignment did not reproduce native behavior", root, inertness=inertness)
    H.ARMS = {"A1_single": H.ARMS["A1_single"], "A7_coined_coined": values}
    install_behavior_judgment(H)
    fits = step["per_position_fit"] if step else []
    H.ARM_HOOKS.append(behavior_hook(H, M, hp, values, ids, kind, fits, z_rows, save_dir, root))
    H.Z_OVERRIDE = {(s, " " + value): z_rows[i] for i, (s, value) in enumerate(values.items())} if step else None
    # Multi also captures its own targets: geometry and the seam's counter are comparable.
    if step is None:
        z_rows, _, fits, _ = capture_targets(H, hp, values, contexts)
        H.Z_OVERRIDE = {(s, " " + value): z_rows[i] for i, (s, value) in enumerate(values.items())}
        H.ARM_HOOKS[-1] = behavior_hook(H, M, hp, values, ids, kind, fits, z_rows, save_dir, root)
    H.Z_OVERRIDE_HITS = 0
    original_law5 = H.run_law5
    law5_audit = {}
    def audited_law5(*args):
        before = H.Z_OVERRIDE_HITS
        result = original_law5(*args)
        law5_audit["override_hits"] = H.Z_OVERRIDE_HITS - before
        return result
    H.run_law5 = audited_law5
    recipe = H.run_recipe("mint2", str(root / HP_FILE))
    law5_hits = law5_audit["override_hits"]
    # run_recipe invokes LAW#5 before the two arms, with _LAW5_DEFAULT_CTX=True.
    # Audit the Cairo key is absent from the supplied table, and record standard gate.
    if ("Zorbland", " Cairo") in H.Z_OVERRIDE:
        raise ValueError("LAW#5 request unexpectedly present in target override")
    if not recipe["law5_gate"]["ok"]:
        halt("LAW#5 failed", root, recipe=recipe)
    arm = recipe["arms"]["A7_coined_coined"]
    arm["para_full_binding_n"] = arm["para_full_n"] - (step["probe"]["recall_n"] if step else 0)
    positions = R.position_reading(fits)
    eligible = {x["subj"] for x in positions["rows"] if not x["underfit"]} if step else set(values)
    details = recipe["detail"]["A7_coined_coined"]
    pre = {r["subj"]: r for r in step["probe"]["recall_rows"]} if step else {}
    arm["masked_binding_n"] = sum(sum(r["para_full_hits"]) - sum(pre[r["subj"]]["para_full_hits"]) if step else sum(r["para_full_hits"])
                                  for r in details if r["subj"] in eligible)
    arm["masked_binding_fact_n"] = len(eligible)
    arm["masked_binding_prompt_n"] = len(eligible) * 3
    if step and arm["extra"]["embedding_rows_unchanged"] != step["provenance"]["row_pairing"]["applied_rows_sha256"]:
        raise ValueError("embedding rows changed during FFN write")
    for field in ("arms", "detail", "delta_norms"):
        recipe[field]["candidate"] = recipe[field].pop("A7_coined_coined")
    rec = {"decision_id": R.DECISION_ID, "identity": IDENTITY, "block": block, "replicate": replicate, "kind": kind,
           "seed": seed, "pid": os.getpid(), "fingerprint": fingerprint, "ctx": contexts, "ctx_sha256": R.json_digest(contexts),
           "provenance": provenance(root, words, block, contexts, step["provenance"]["row_pairing"] if step else None),
           "inertness": inertness, "wrapper": {"z_override_hits": H.Z_OVERRIDE_HITS, "law5_override_hits": law5_hits},
           "admission": {"P2": step["P2"] if step else {"ok": True, "note": "tokenizer untouched"},
                         "P3": step["P3"] if step else {"ok": True, "fits": []},
                         "no_i11_exclusion": step["admission"]["no_i11_exclusion"] if step else True},
           "step0": {**(step["probe"] if step else {"recall_n": 0, "recall_rows": [], "n_cannibal": 0}), "per_position_fit": fits if step else []},
           "recipe": recipe, "arm": arm, "values": values, "minted_words": registered, "minted_ids": ids,
           "spec_amendment": "§8.1 / §8.4 / §8.10 — embedding-side write; compaction procedure undefined",
           "outcome": "DONE", "when_utc": utc_now()}
    assert_sources(IDENTITY, root)
    write_json(out / names[0], rec)
    reasons = R.run_validity(rec)
    if reasons:
        halt("completed run failed pure validity gates", root, record=names[0], reasons=reasons)
    print(f"BEHAVIOR {tag}: raw={arm['para_full_n']} binding={arm['para_full_binding_n']} string={arm['para_string_n']}", flush=True)


def read_records(out):
    pattern = re.compile(r"^(F|V2)_r[01]_(multi|mint1|modifier|mint2|mint1_48)_s(none|[012])\.json$")
    return [json.loads(p.read_text()) for p in sorted(out.glob("*.json")) if pattern.fullmatch(p.name)]


def spawn_job(root, out, reference_path, job, block, kind="multi", seed=None, replicate=0, save_for_p4=False, artifact_tag=None):
    command = [sys.executable, str(root / "experiments/track_c/c10u_mint2_arms.py"), "_job", "--job", job,
               "--block", block, "--kind", kind, "--replicate", str(replicate), "--root", str(root),
               "--out-dir", str(out), "--law3-ref", str(reference_path)]
    if seed is not None:
        command += ["--seed", str(seed)]
    if save_for_p4:
        command += ["--save-for-p4"]
    if artifact_tag:
        command += ["--artifact-tag", artifact_tag]
    tag = job + "_" + (artifact_tag or record_name(block, replicate, kind, seed))
    log = out / "logs" / (tag + ".log")
    occupied(out, [str(log.relative_to(out))])
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("x") as f:
        result = subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, env={**os.environ, "LLMDB_ROOT": str(root)})
    if result.returncode != 0 or not log.stat().st_size:
        halt("child failed; no automatic retry or fix", root, command=command, returncode=result.returncode, log=str(log))
    path = (out / f"contexts_{block}.json" if job == "contexts" else
            out / "step0" / (record_name(block, 0, kind, seed) + ".json") if job == "step0" else
            out / ((artifact_tag or record_name(block, replicate, kind, seed)) + ".json"))
    if not path.is_file():
        halt("child returned success without its result", root, command=command, path=str(path))
    record = json.loads(path.read_text())
    assert_sources(record["identity"], root)
    print(f"completed {tag}; log={log}", flush=True)
    return record


def ensure_context(root, out, reference_path, block):
    path = out / f"contexts_{block}.json"
    if not path.exists():
        spawn_job(root, out, reference_path, "contexts", block)
    read_context(root, out, block)


def ensure_step0(root, out, reference_path, descriptor):
    if descriptor["kind"] == "multi":
        return None
    block, kind, seed = (descriptor[k] for k in ("block", "kind", "seed"))
    path = out / "step0" / (record_name(block, 0, kind, seed) + ".json")
    if not path.exists():
        spawn_job(root, out, reference_path, "step0", block, kind, seed)
    return require_step0(root, out, block, kind, seed)


def reproduction_or_halt(root, out, require_multi=False, replicate=0):
    records = [r for r in read_records(out) if r["block"] == "F" and r["replicate"] == replicate]
    mint1 = [r for r in records if r["kind"] == "mint1"]
    multi = next((r for r in records if r["kind"] == "multi"), None)
    if require_multi and multi is None:
        raise ValueError("frozen multi reproduction reference is missing")
    reading = R.reproduction_gate(mint1, multi)
    if not reading["ok"]:
        halt("LAW#3 frozen mint-1/multi reproduction miss; stop both blocks", root, reproduction=reading)
    return reading


def p4_configurations(records):
    """Pure eligibility selection; no spending or permanent marker on a miss."""
    selected = []
    for block, kind in (("F", "modifier"), ("V2", "mint2")):
        originals = [r for r in records if r["block"] == block and r["replicate"] == 0]
        replicas = [r for r in records if r["block"] == block and r["replicate"] == 1]
        controls = [r for r in originals if r["kind"] == "mint1_48"]
        originals = [r for r in originals if r["kind"] != "mint1_48"]
        replicas = [r for r in replicas if r["kind"] != "mint1_48"]
        block_read = R.block_reading(originals, replicas or None, controls or None)
        if block_read.get("direction") in ("INVALID", "HALT-LAW3", "INCOMPLETE", "NOT-COMPARABLE"):
            continue
        multi = next((r for r in originals if r["kind"] == "multi"), None)
        replica_multi = next((r for r in replicas if r["kind"] == "multi"), None)
        for record in originals:
            if record["kind"] != kind:
                continue
            replica = next((r for r in replicas if r["kind"] == kind and r["seed"] == record["seed"]), None)
            reading = R.run_reading(multi, record, {"reference": replica_multi, "candidate": replica} if replica else None)
            if reading["label"].split("-")[0] in ("LEAD", "PARTIAL") and "NOT-REPLICATED" not in reading["label"]:
                selected.append(record)
    if not selected:
        raise ValueError("P4 requires replicated LEAD/PARTIAL mint-2 or modifier configuration")
    return selected


def p4_save_stage(root, out, reference_path, records, fingerprint):
    """Save only advanced configurations in dedicated P4 preparation processes."""
    selected = p4_configurations(records)
    for record in selected:
        tag = "p4save_" + record_name(record["block"], 0, record["kind"], record["seed"])
        occupied(out, [tag + ".json", tag + "_started.json", "edited/c10u_mint2_" + tag])
    for record in selected:
        tag = "p4save_" + record_name(record["block"], 0, record["kind"], record["seed"])
        replay = spawn_job(root, out, reference_path, "behavior", record["block"], record["kind"], record["seed"],
                           save_for_p4=True, artifact_tag=tag)
        multi = next(r for r in records if r["block"] == record["block"] and r["replicate"] == 0 and r["kind"] == "multi")
        reading = R.run_reading(multi, replay)
        if reading["label"].split("-")[0] not in ("LEAD", "PARTIAL"):
            halt("P4 save replay did not retain an advanced configuration", root, record=tag, reading=reading)
        write_json(out / (tag + "_admitted.json"), {"identity": IDENTITY, "original": record_name(record["block"], 0, record["kind"], record["seed"]) + ".json",
                                                  "original_sha256": sha256_file(out / (record_name(record["block"], 0, record["kind"], record["seed"]) + ".json")),
                                                  "replay": tag + ".json", "replay_sha256": sha256_file(out / (tag + ".json")), "reading": reading})


def stages(root, out, reference_path, stage, fingerprint):
    records = read_records(out)
    # All dependencies and output collisions are checked BEFORE the permanent marker.
    if stage == "frozen":
        reproduction_or_halt(root, out)
    elif stage in ("v2", "control", "replicate-F", "replicate-V2", "p4-save"):
        reproduction_or_halt(root, out, require_multi=True)
        if stage != "replicate-F" and len([r for r in records if r["block"] == "F" and r["replicate"] == 0]) != 7:
            raise ValueError("complete first block F is required")
    plan = [] if stage == "p4-save" else R.stage_plan(stage, records)
    p4_selected = p4_configurations(records) if stage == "p4-save" else []
    if stage != "p4-save" and not plan:
        raise ValueError("conditional stage is unnecessary or its prerequisites are incomplete/invalid")
    # Empty conditional plans have been refused; no permanent no-op markers.
    names = [f"{stage}_started.json", f"{stage}_complete.json"]
    for d in plan:
        tag = record_name(d["block"], d["replicate"], d["kind"], d["seed"])
        names += [tag + ".json", tag + "_started.json"]
        if d["kind"] != "multi":
            precursor = record_name(d["block"], 0, d["kind"], d["seed"])
            if not (out / "step0" / (precursor + ".json")).exists():
                names += [f"step0/{precursor}_started.json", f"inits/{precursor}.pt", f"zs/{precursor}.pt",
                          f"logs/step0_{precursor}.log"]
            else:
                require_step0(root, out, d["block"], d["kind"], d["seed"])
        if not (out / f"contexts_{d['block']}.json").exists():
            names += [f"contexts_{d['block']}_started.json", f"logs/contexts_{record_name(d['block'], 0, 'multi', None)}.log"]
        else:
            read_context(root, out, d["block"])
        names += ["logs/behavior_" + tag + ".log"]
    for record in p4_selected:
        tag = "p4save_" + record_name(record["block"], 0, record["kind"], record["seed"])
        names += [tag + ".json", tag + "_started.json", tag + "_admitted.json", "edited/c10u_mint2_" + tag,
                  "logs/behavior_" + tag + ".log"]
    occupied(out, names)
    write_json(out / names[0], {"identity": IDENTITY, "stage": stage, "fingerprint": fingerprint, "plan": plan, "when_utc": utc_now()})
    if stage == "p4-save":
        p4_save_stage(root, out, reference_path, records, fingerprint)
    else:
        for d in plan:
            ensure_context(root, out, reference_path, d["block"])
            ensure_step0(root, out, reference_path, d)
            result = spawn_job(root, out, reference_path, "behavior", d["block"], d["kind"], d["seed"], d["replicate"])
            if d["block"] == "F" and d["kind"] == "mint1" and d["seed"] == 2:
                reproduction_or_halt(root, out, replicate=d["replicate"])
            if d["block"] == "F" and d["kind"] == "multi":
                reproduction_or_halt(root, out, require_multi=True, replicate=d["replicate"])
    all_records = read_records(out)
    readings = {block: R.block_reading([r for r in all_records if r["block"] == block and r["replicate"] == 0 and r["kind"] != "mint1_48"],
                                      [r for r in all_records if r["block"] == block and r["replicate"] == 1 and r["kind"] != "mint1_48"] or None,
                                      [r for r in all_records if r["block"] == block and r["kind"] == "mint1_48"] or None)
                for block in ("F", "V2")}
    write_json(out / f"{stage}_complete.json", {"identity": IDENTITY, "stage": stage, "readings": readings, "when_utc": utc_now()})
    print(json.dumps(readings, indent=2), flush=True)


def step0_stage(root, out, reference_path, phase, fingerprint):
    # Optional explicit precursor command; normal behavioral stages call it per job.
    plan = R.stage_plan(phase, read_records(out))
    plan = [d for d in plan if d["kind"] != "multi"]
    if not plan or phase not in ("reproduce", "frozen", "v2", "control"):
        raise ValueError("step0 requires a necessary initial-admission phase")
    marker = "step0_" + phase
    names = [marker + "_started.json", marker + "_complete.json"] + ["step0/" + record_name(d["block"], 0, d["kind"], d["seed"]) + ".json" for d in plan]
    for d in plan:
        precursor = record_name(d["block"], 0, d["kind"], d["seed"])
        names += [f"step0/{precursor}_started.json", f"inits/{precursor}.pt", f"zs/{precursor}.pt", f"logs/step0_{precursor}.log"]
        if not (out / f"contexts_{d['block']}.json").exists():
            names += [f"contexts_{d['block']}_started.json", f"logs/contexts_{record_name(d['block'], 0, 'multi', None)}.log"]
        else:
            read_context(root, out, d["block"])
    occupied(out, names)
    if phase != "reproduce":
        reproduction_or_halt(root, out, require_multi=phase != "frozen")
    write_json(out / names[0], {"identity": IDENTITY, "fingerprint": fingerprint, "plan": plan})
    for d in plan:
        ensure_context(root, out, reference_path, d["block"])
        ensure_step0(root, out, reference_path, d)
    write_json(out / names[1], {"identity": IDENTITY, "completed": plan})


def main(argv=None, step0_only=False):
    global IDENTITY, STAGE, RUN_ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("reproduce", "frozen", "v2", "control", "replicate-F", "replicate-V2", "p4-save", "_job"))
    parser.add_argument("--root", type=Path, default=Path(LLMDB_ROOT))
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--law3-ref", type=Path, required=True)
    parser.add_argument("--job", choices=("contexts", "step0", "behavior"))
    parser.add_argument("--block", choices=("F", "V2"))
    parser.add_argument("--kind", choices=("multi", "mint1", "mint2", "modifier", "mint1_48"), default="multi")
    parser.add_argument("--seed", type=int, choices=(0, 1, 2))
    parser.add_argument("--replicate", type=int, choices=(0, 1), default=0)
    parser.add_argument("--save-for-p4", action="store_true")
    parser.add_argument("--artifact-tag")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    out = (args.out_dir or root / "results/c10u_mint2").resolve()
    RUN_ROOT, STAGE = root, args.stage
    try:
        if root != Path(__file__).resolve().parents[2]:
            raise ValueError("LLMDB_ROOT must be this driver worktree's root")
        out.relative_to(root / "results/c10u_mint2")
        fingerprint = preflight(root)
        frozen_words(root)
        reference = law3_reference(args.law3_ref)
        # Hash/inventory validation does not create a directory or marker.
        source_hashes(root)
        IDENTITY = initialise_identity(root, out, reference)
        if args.stage == "_job":
            if args.job is None or args.block is None:
                raise ValueError("internal job requires job and block")
            if args.kind != "multi" and args.seed is None:
                raise ValueError("minted job requires a seed")
            if args.job == "contexts":
                context_job(root, out, args.block, fingerprint)
            elif args.job == "step0":
                step0_job(root, out, args.block, args.kind, args.seed, fingerprint)
            else:
                behavior_job(root, out, args.block, args.replicate, args.kind, args.seed, fingerprint, args.save_for_p4, args.artifact_tag)
        elif step0_only:
            step0_stage(root, out, args.law3_ref.resolve(), args.stage, fingerprint)
        else:
            stages(root, out, args.law3_ref.resolve(), args.stage, fingerprint)
        return 0
    except Exception as exc:
        halt(str(exc), root, exception=type(exc).__name__, traceback=traceback.format_exc())


if __name__ == "__main__":
    sys.exit(main())
