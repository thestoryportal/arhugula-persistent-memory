#!/usr/bin/env python3
"""Model-free D-C10t-secondkey v2 behaviour tests; stdlib only.

No torch, tokenizer download, harness import, model, GPU or operator driver run.
Engine word-index function is AST-loaded without its heavyweight module imports;
synthetic tokenizers, pass records and a recording my_edit exercise actual seams.
Stage entry points use synthetic files with harness loading blocked or stubbed.
All filesystem checks write exclusively into fresh TemporaryDirectory fixtures.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import ast, copy, hashlib, io, json, math, re, tempfile, types, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10t_secondkey_read as R
import c10t_secondkey_arms as A
import c10t_secondkey_step0 as S

ROOT = Path(__file__).resolve().parents[2]
CONTEXTS = [["{}"], ["The sun rose. {}", "You said it. {}"]]


class Tokenizer:
    def __init__(self):
        self.ids, self.text = {}, {}

    def encode(self, text):
        tokens = re.findall(r"\s*\S+", text)
        for token in tokens:
            if token not in self.ids:
                i = len(self.ids) + 1
                self.ids[token], self.text[i] = i, token
        return [self.ids[t] for t in tokens]

    def __call__(self, text):
        return [self.encode(s) for s in text] if isinstance(text, list) else {"input_ids": self.encode(text)}

    def decode(self, ids):
        return "".join(self.text[i] for i in ids)


def engine_word_index():
    """Execute the actual source function, no engine import or bytecode cache."""
    path = ROOT / "code/memit/vendor/rome/repr_tools.py"
    node = next(n for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "get_words_idxs_in_templates")
    for arg in node.args.args:
        arg.annotation = None
    node.returns = None
    ns = {"deepcopy": copy.deepcopy}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), ns)
    return ns[node.name]


IDX = engine_word_index()


def fixture_step():
    tok = Tokenizer()
    facts = []
    for i in range(R.N):
        c, value = "S" + str(i), "Foo Bar Baz"
        ids = A.token_ids(tok, " " + value)
        rows = [{"p": 0, "class": "subject", "j": None}, {"p": 1, "class": "value-writable", "j": 1},
                {"p": 2, "class": "value-writable", "j": 2}, {"p": 3, "class": "value-final", "j": 3}]
        facts.append({"subj": c, "value": value, "value_ids": ids,
                      "surprisal": {"values": [0.0, 9.0, 1.0], **R.surprisal_selection([0.0, 9.0, 1.0])},
                      "positions": rows,
                      "leverage": R.leverage_selection(rows, {str(l): [0.0, 9.0, 1.0, 0.0] for l in R.BAND}),
                      "leverage_layers": {str(l): {"protected_leverage": {str(R.COV_CUT): [0.0, 9.0, 1.0, 0.0]}} for l in R.BAND},
                      "admissible": [1, 2], "admissible_n": 2,
                      "admission": [A.alignment_audit(tok, c, value, ids, j, CONTEXTS, IDX) for j in (1, 2)]})
    selection = R.select_positions(facts)
    requests = {v: A.requests_for(tok, facts, js) for v, js in selection["arms"].items()}
    hashes = {"test_source": "1" * 64}
    identity = {"run_id": "synthetic-c10t", "source_sha256": hashes, "source_digest": A.source_digest(hashes),
                "program_rulings": dict(R.PROGRAM_RULINGS)}
    return {"facts": facts, "selection": selection, "requests": requests,
            "request_sha256": {v: R.json_digest(q) for v, q in requests.items()},
            "overlap": {v: R.overlap_audit(q) for v, q in requests.items()}, "identity": identity,
            "overturning": {v: {"layers": {str(l): {"PTEST" + str(t): {"facts": [f["subj"] for f in facts], "second": [0.8] * 24, "subject": [0.7] * 24} for t in range(3)} for l in R.BAND},
                                 "reading": R.overturning_reading([0.8] * 360, [0.7] * 360)} for v in selection["arms"]}}


def unmerged_step():
    step = fixture_step()
    for f in step["facts"][:5]:
        for l in R.BAND:
            f["leverage_layers"][str(l)]["protected_leverage"][str(R.COV_CUT)] = [0.0, 1.0, 9.0, 0.0]
        f["leverage"] = R.leverage_selection(f["positions"], {str(l): [0.0, 1.0, 9.0, 0.0] for l in R.BAND})
    step["selection"] = R.select_positions(step["facts"])
    tok = Tokenizer()
    A.token_ids(tok, " Foo Bar Baz")
    step["requests"] = {v: A.requests_for(tok, step["facts"], js) for v, js in step["selection"]["arms"].items()}
    step["request_sha256"] = {v: R.json_digest(q) for v, q in step["requests"].items()}
    step["overlap"] = {v: R.overlap_audit(q) for v, q in step["requests"].items()}
    template = next(iter(step["overturning"].values()))
    step["overturning"] = {v: copy.deepcopy(template) for v in step["requests"]}
    return step


def probes(step):
    variants = step["selection"]["arms"]
    subjects = [f["subj"] for f in step["facts"]]
    return {"F0": {"n": R.FRAME_N, "flips": 0},
            "prefixes": {v: [{"subj": s, "next_hits": [False] * 6, "full_hits": [False] * 6} for s in subjects] for v in variants},
            "subject_free": {v: [{"subj": s, "next_hit": False, "full_hit": False} for s in subjects] for v in variants},
            "prefix_reached": {v: {"n": 72, "count": 0, "per_fact": [0] * 24,
                                    "rows": [{"subj": s, "hits": [False] * 3, "count": 0} for s in subjects]} for v in variants},
            "bystanders": []}


def fixture_pass(step, count=32, ref=13, dup=13, pid=101):
    subjects = [f["subj"] for f in step["facts"]]
    variants = step["selection"]["arms"]
    canonical = next(iter(step["requests"].values()))[:R.N]
    requests = {R.SINGLE: canonical, R.DUP: canonical + copy.deepcopy(canonical), **step["requests"]}
    recipe = {"arms": {}, "detail": {}, "delta_norms": {}, "band": R.BAND, "projector": "nullspace",
              "law5_gate": {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0}}
    for name, n, canon in [("A1_single", 72, 24), ("A2_coherent2", 72, 24), (R.SINGLE, ref, 8), (R.DUP, dup, 8), *[(v, count, 8) for v in variants]]:
        rows = [{"subj": s, "canon_full": i < canon, "para_full_hits": [3 * i + t < n for t in range(3)],
                 "para_first_hits": [3 * i + t < n for t in range(3)], "para_string_hits": [3 * i + t < n for t in range(3)]} for i, s in enumerate(subjects)]
        arm = {"canon_n": 24, "para_n": 72, "canon_full_n": canon, "para_full_n": n, "para_string_n": n,
               "para_first_n": n, "tf_pertok_cont": 0.0, "cond_full_given_first": 1.0,
               "locality_described_as": 97.0, "locality_axes": {"L1_flipped_to_edited_value": 0, "L1_n": 12,
                   "L3_top1_agree": 30, "L3_n": 30, "generic_ppl_post": 20.0}}
        if name in requests:
            ex = probes(step)
            ex.update(fits=[{"request": rq, "nll": 0.1, "kl_loss": 0.01, "loss_evaluations": 25,
                             "adam_steps": 24, "clamp_hit": False, "clamp_hit_steps": 0} for rq in requests[name]],
                      requests_sha256=R.json_digest(requests[name]), hook_request_count=len(requests[name]),
                      keygram_solve={str(l): {"n_columns": len(requests[name])} for l in R.BAND},
                      residual={"canonical_keyed_positions": {"per_request": [1.0] * len(requests[name])},
                                "held_out_keyed_positions": {"per_request": [1.0] * (3 * len(requests[name]))}})
            arm["extra"] = ex
        recipe["arms"][name], recipe["detail"][name] = arm, rows
        recipe["delta_norms"][name] = {str(l): {"delta_norm": 1.0} for l in R.BAND}
    return {"identity": step["identity"], "positions_sha256": "2" * 64, "pid": pid,
            "fingerprint": {"sha256": R.FINGERPRINT + "0" * 56, "_cov_cpu": 3, "ok": True},
            "observer_inertness": [{"subject": rq["subject"], **R.observer_inertness_reading(0.0, 0.0)}
                                  for rq in (canonical[0], next(iter(step["requests"].values()))[R.N])],
            "admission": {"ok": True, "arms": {v: {"ok": True, "n_requests": 48} for v in variants}},
            "wrapper": {"candidate_substitutions": len(variants), "duplicate_substitutions": 1, "law5_substitutions": 0,
                        "order": [R.SINGLE, R.DUP, *variants], "z_override_none": True, "z_override_hits": 0,
                        "requests_sha256": {a: R.json_digest(q) for a, q in requests.items()},
                        "reached_my_edit_counts": {a: len(q) for a, q in requests.items()}},
            "base_report": {a: {"base": 0} for a in recipe["arms"]}, "base_probes": probes(step), "recipe": recipe}


class TestSelection(unittest.TestCase):
    def test_surprisal_boundary_and_ties(self):
        s = R.surprisal_selection([9.0, 8.0, 8.0, 1.0])
        self.assertEqual((s["j_star"], s["unconstrained_address_j"], s["p10"]), (1, 0, 1))
        self.assertFalse(s["unconstrained_writable"])
        s = R.surprisal_selection([0.0, 1.0, 2.0, 9.0])
        self.assertEqual((s["j_star"], s["p10"]), (4, 3))
        self.assertTrue(s["unconstrained_writable"])

    def test_protected_cut_includes_equality(self):
        self.assertEqual(R.cut_indices([0.0, 0.00499, 0.005, 0.05, 2.0]), [2, 3, 4])
        self.assertEqual(R.cut_indices([0.0, 0.00499, 0.005, 0.05, 2.0], R.CUT_CHECK), [3, 4])

    def test_leverage_raw_mean_and_normalised_alternative(self):
        positions = [{"p": 0, "class": "frame", "j": None}, {"p": 1, "class": "value-writable", "j": 1},
                     {"p": 2, "class": "value-writable", "j": 2}, {"p": 3, "class": "value-final", "j": 3}]
        v = {str(l): [0.0, 1.0, 10.0, 0.0] for l in R.BAND}
        v["4"] = [0.0, 1000.0, 0.0, 0.0]
        x = R.leverage_selection(positions, v)
        self.assertEqual(x["p5"], 1)
        self.assertEqual(x["normalised_internal_j"], 2)
        self.assertEqual(x["per_layer"]["4"]["margin"], 1000.0)
        self.assertEqual(x["selector"], "raw-five-layer-mean")

    def test_nearest_admission_tie_and_empty(self):
        self.assertEqual(R.nearest_admissible(2, [3, 1]), 1)
        with self.assertRaisesRegex(ValueError, "INVALID-ADMISSION"):
            R.nearest_admissible(2, [])

    def test_spending_boundary_and_single_survivor(self):
        fs = fixture_step()["facts"]
        for f in fs[:12]: f["surprisal"]["unconstrained_writable"] = False
        self.assertFalse(R.select_positions(fs)["dropped"]["surprisal"])
        fs[12]["surprisal"]["unconstrained_writable"] = False
        x = R.select_positions(fs)
        self.assertEqual(list(x["arms"]), ["A7-second-B5"])
        for f in fs[:13]: f["leverage"]["unconstrained_writable"] = False
        self.assertEqual(R.select_positions(fs)["outcome"], "BOTH-RULES-DROPPED")

    def test_merge_on_pre_admission_agreement(self):
        fs = fixture_step()["facts"]
        for f in fs[:4]: f["leverage"]["p5"] = 2
        x = R.select_positions(fs)
        self.assertEqual((x["agreement_before"], list(x["arms"])), (20, ["A7-second-B"]))
        self.assertEqual(set(x["arms"]["A7-second-B"].values()), {1})
        fs[4]["leverage"]["p5"] = 2
        for f in fs: f["admissible"] = [1]
        x = R.select_positions(fs)
        self.assertEqual((x["agreement_before"], x["agreement_after"]), (19, 24))
        self.assertEqual(set(x["arms"]), {"A7-second-B10", "A7-second-B5"})

    def test_empty_admission_population_never_shrinks(self):
        fs = fixture_step()["facts"]
        fs[3]["admissible"] = []
        x = R.select_positions(fs)
        self.assertEqual((x["outcome"], x["empty"], x["arms"]), ("INVALID-ADMISSION", ["S3"], {}))
        with self.assertRaisesRegex(ValueError, "24 distinct"):
            R.select_positions(fs[:-1])

    def test_overturning_equal_is_standing_not_stop(self):
        x = R.overturning_reading([0.25, 0.75], [0.5, 0.5])
        self.assertTrue(x["H_T4_standing"])
        self.assertFalse(x["stop"])
        self.assertFalse(R.overturning_reading([0.4], [0.3])["H_T4_standing"])


class TestAlignment(unittest.TestCase):
    def setUp(self):
        self.tok = Tokenizer()
        self.ids = A.token_ids(self.tok, " Foo Bar Baz")

    def test_request_block_order_and_no_double_space(self):
        rq = A.second_request(self.tok, "S", self.ids, 1)
        self.assertEqual(rq["subject"], "S is the city of Foo")
        self.assertEqual(rq["target_new"]["str"], " Bar Baz")
        facts = [{"subj": "S" + str(i), "value": "Foo Bar Baz", "value_ids": self.ids} for i in range(24)]
        qs = A.requests_for(self.tok, facts, {f["subj"]: 1 for f in facts})
        self.assertEqual(len(qs), 48)
        self.assertEqual([q["subject"] for q in qs[:24]], [f["subj"] for f in facts])
        self.assertEqual([q["target_new"]["str"] for q in qs[24:]], [" Bar Baz"] * 24)
        with self.assertRaises(ValueError): A.second_request(self.tok, "S", self.ids, 0)
        with self.assertRaises(ValueError): A.second_request(self.tok, "S", self.ids, len(self.ids))

    def test_all_internal_positions_and_sampled_templates(self):
        for j in (1, 2):
            a = A.alignment_audit(self.tok, "S", "Foo Bar Baz", self.ids, j, CONTEXTS, IDX)
            self.assertTrue(a["ok"], a)
            self.assertEqual(len(a["rows"]), 3)
            for r in a["rows"]:
                self.assertEqual(r["lookup_idx"], r["b"] - 1)
                self.assertEqual(len(r["truncated_ids"]), r["b"] + r["m"] - 1)
                self.assertEqual(r["label_positions"], list(range(r["b"] - 1, r["b"] + r["m"] - 1)))
        canonical = {"prompt": R.CANON, "subject": "S", "target_new": {"str": " Foo Bar Baz"}}
        self.assertTrue(A.canonical_audit(self.tok, canonical, CONTEXTS, IDX)["ok"])

    def test_wrong_lookup_and_separate_KL_rejected(self):
        def wrong(tok, prompts, words, subtoken):
            return [[x[0] + 1] for x in IDX(tok, prompts, words, subtoken)]
        self.assertFalse(A.alignment_audit(self.tok, "S", "Foo Bar Baz", self.ids, 1, CONTEXTS, wrong)["ok"])
        def wrong_kl(tok, prompts, words, subtoken):
            return [[0]] if prompts == ["{} is a"] else IDX(tok, prompts, words, subtoken)
        a = A.alignment_audit(self.tok, "S", "Foo Bar Baz", self.ids, 1, CONTEXTS, wrong_kl)
        self.assertTrue(all(r["ok"] for r in a["rows"]))
        self.assertFalse(a["kl"]["ok"])
        self.assertFalse(a["ok"])

    def test_prefix_retokenisation_rejected(self):
        original = self.tok.encode
        def corrupted(text):
            ids = original(text)
            return ids[:-1] + [999999] if text.endswith("of Foo Bar") else ids
        self.tok.encode = corrupted
        a = A.alignment_audit(self.tok, "S", "Foo Bar Baz", self.ids, 2, CONTEXTS, IDX)
        self.assertFalse(a["ok"])
        self.assertFalse(a["rows"][0]["checks"]["full_sentence_input_ids"])

    def test_overlap_report_does_not_select_positions(self):
        step = fixture_step()
        rows = R.overlap_audit(next(iter(step["requests"].values())))
        self.assertEqual(len(rows), 72)
        self.assertTrue(all("shared_words" in r and "shared_trigrams" in r for r in rows))


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.step = fixture_step()
        self.calls = []
        def edit(hp, requests, P, cache):
            self.calls.append(copy.deepcopy(requests))
            return {"unchanged_result": True}
        self.H = types.SimpleNamespace(my_edit=edit, _LAW5_DEFAULT_CTX=False, _ARM_STATE={"requests": []}, Z_OVERRIDE=None, Z_OVERRIDE_HITS=0)
        self.observed = []
        self.collector = types.SimpleNamespace(active=False, before=lambda name, reqs, hp, P: self.observed.append((name, copy.deepcopy(reqs))))
        self.wrapper = A.RequestWrapper(self.H, self.step["requests"], self.collector)

    def test_LAW5_and_controls_pass_through(self):
        canonical = self.wrapper.canonical
        self.H._LAW5_DEFAULT_CTX = True
        self.wrapper(None, canonical, None, None)
        self.H._LAW5_DEFAULT_CTX = False
        control = [{"prompt": R.CANON, "subject": "Zorbland", "target_new": {"str": " Cairo"}}]
        self.wrapper(None, control, None, None)
        self.assertEqual(self.calls, [canonical, control])
        self.assertEqual(self.wrapper.audit["order"], [])
        self.assertEqual(self.observed, [])

    def test_single_dup_and_second_reach_real_seam_and_hook(self):
        for _ in range(3):
            result = self.wrapper(None, self.wrapper.canonical, None, None)
            self.assertEqual(result, {"unchanged_result": True})
            self.assertEqual(self.calls[-1], self.H._ARM_STATE["requests"])
        self.assertEqual([len(q) for q in self.calls], [24, 48, 48])
        self.assertEqual(self.calls[1], self.calls[0] * 2)
        self.assertEqual(self.calls[2], self.step["requests"]["A7-second-B"])
        self.assertEqual((self.wrapper.audit["candidate_substitutions"], self.wrapper.audit["duplicate_substitutions"]), (1, 1))

    def test_target_match_does_not_accept_changed_canonical_prompt(self):
        changed = copy.deepcopy(self.wrapper.canonical)
        changed[0]["prompt"] = "Other {}"
        with self.assertRaisesRegex(ValueError, "construction/order"):
            self.wrapper(None, changed, None, None)
        self.assertEqual(self.calls, [])

    def test_actual_harness_recipe_ast_restores_base_and_uses_one_P(self):
        """Actual run_recipe/req source, deterministic stubs for effects. No
        c10e import, model or solve. Checks the seam in its real calling loop.
        """
        source = ROOT / "code/lab/track_c/c10e_bandknob.py"
        nodes = [n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in ("run_recipe", "req")]
        H = types.ModuleType("c10t_synthetic_harness")
        hp = types.SimpleNamespace(layers=R.BAND)
        H.__dict__.update(torch=types.SimpleNamespace(zeros=lambda *args: object()),
                          MEMITHyperParams=types.SimpleNamespace(from_json=lambda path: hp),
                          contextlib=__import__("contextlib"), io=io, os=os)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), "exec"), H.__dict__)
        shared_P = [types.SimpleNamespace(shape=(2, 2)) for _ in R.BAND]
        calls, caches, projector_calls, restores, model_state = [], [], [], [], [0]
        H.FICTION = [f["subj"] for f in self.step["facts"]]
        H.CANON, H.CANDIDATE_NAME, H.PROJECTOR = R.CANON, "secondkey", "nullspace"
        H.Z_OVERRIDE, H.Z_OVERRIDE_HITS, H._LAW5_DEFAULT_CTX, H._ARM_STATE = None, 0, False, None
        H.snap_layers = lambda hp: "BASE"
        def restore(hp, snapshot):
            self.assertEqual(snapshot, "BASE")
            model_state[0] = 0
            restores.append(snapshot)
        H.restore_layers = restore
        def projector(hp):
            projector_calls.append(hp)
            return shared_P
        H.compute_P = projector
        H.run_law5 = lambda hp, P, snapshot: {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0}
        H.cov_cache_sha256 = lambda hp: {}
        H.axes_pre, H.predict, H.locpct = lambda: {}, lambda p: {}, lambda *args: 97.0
        H.axes_post = lambda *args: {"L1_flipped_to_edited_value": 0, "L1_n": 12, "L3_top1_agree": 30, "L3_n": 30,
                                   "L3_mean_kl": 0.0, "generic_ppl_pre": 20.0, "generic_ppl_post": 20.0}
        def edit(hp, reqs, P, cache):
            self.assertEqual(model_state[0], 0)
            self.assertIs(P, shared_P)
            self.assertEqual(reqs, H._ARM_STATE["requests"])
            model_state[0] = 1
            calls.append(reqs)
            caches.append(cache)
            return {str(l): {"delta_norm": 1.0} for l in R.BAND}
        H.my_edit = edit
        observed = types.SimpleNamespace(active=False)
        observed.before = lambda name, reqs, hp, P: setattr(observed, "name", name)
        wrapper = A.RequestWrapper(H, self.step["requests"], observed)
        H.my_edit = wrapper
        V = {f["subj"]: f["value"] for f in self.step["facts"]}
        H.ARMS = {"A1_single": {s: "Cairo" for s in H.FICTION}, "A2_coherent2": {s: "New York" for s in H.FICTION},
                  R.SINGLE: V, R.DUP: V, **{v: V for v in self.step["selection"]["arms"]}}
        def evaluate(values):
            name = "A1_single" if set(values.values()) == {"Cairo"} else "A2_coherent2" if set(values.values()) == {"New York"} else observed.name
            x = copy.deepcopy(fixture_pass(self.step)["recipe"]["arms"][name])
            x.update(rows=[], canon_full=0.0, para_full=0.0, para_first=0.0)
            return x
        H.eval_arm = evaluate
        H.ARM_HOOKS = [lambda name, values: {"observed_count": len(H._ARM_STATE["requests"])}]
        with patch.dict(os.environ, {}, clear=True), __import__("contextlib").redirect_stdout(io.StringIO()):
            result = H.run_recipe("secondkey", "synthetic-settings")
        self.assertEqual([len(q) for q in calls], [24, 24, 24, 48, 48])
        self.assertEqual(len(projector_calls), 1)
        self.assertEqual(len(restores), 6)
        self.assertEqual(len({id(c) for c in caches}), 5)
        self.assertEqual(result["arms"]["A7-second-B"]["extra"]["observed_count"], 48)
        self.assertEqual(model_state[0], 0)
        self.assertIsNone(H._ARM_STATE)

    def test_override_and_extra_A7_call_refused(self):
        self.H.Z_OVERRIDE = {}
        with self.assertRaisesRegex(ValueError, "engine targets"):
            self.wrapper(None, self.wrapper.canonical, None, None)
        self.H.Z_OVERRIDE = None
        for _ in range(3): self.wrapper(None, self.wrapper.canonical, None, None)
        with self.assertRaisesRegex(ValueError, "construction/order"):
            self.wrapper(None, self.wrapper.canonical, None, None)

    def test_unmerged_wrapper_substitutes_each_candidate_once(self):
        step = unmerged_step()
        wrapper = A.RequestWrapper(self.H, step["requests"], self.collector)
        for _ in range(4): wrapper(None, wrapper.canonical, None, None)
        self.assertEqual(wrapper.audit["order"], [R.SINGLE, R.DUP, "A7-second-B10", "A7-second-B5"])
        self.assertEqual(wrapper.audit["candidate_substitutions"], 2)
        self.assertEqual([len(q) for q in self.calls], [24, 48, 48, 48])
        self.assertNotEqual(self.calls[2][24:], self.calls[3][24:])


class TestVerdict(unittest.TestCase):
    def setUp(self):
        step = fixture_step()
        self.run = {"identity": step["identity"], "positions_sha256": "2" * 64, "step0": step}
        self.p = fixture_pass(step)
        self.variant = "A7-second-B"

    def test_label_boundaries_and_locality_tradeoff(self):
        for n, ref, gates, expected in [(18, 5, True, "NULL"), (19, 9, True, "PARTIAL"), (29, 18, True, "PARTIAL"),
            (29, 20, True, "NULL"), (30, 18, True, "LEAD"), (30, 18, False, "TRADEOFF"), (25, 13, False, "TRADEOFF"), (18, 5, False, "NULL")]:
            self.assertEqual(R.single_label(n, ref, gates), expected)

    def test_each_prefix_gate_uses_new_hit_sets_not_totals(self):
        arms = self.p["recipe"]["arms"]
        ref, cand = arms[R.SINGLE], arms[self.variant]
        base = self.p["base_probes"]["prefixes"][self.variant][0]
        base["next_hits"] = [True, True, False, False, False, False]
        cand["extra"]["prefixes"][self.variant][0]["next_hits"] = [True, True, True, False, False, False]
        self.assertTrue(all(R.locality_gates(ref, cand, self.p["base_probes"], self.variant).values()))
        cand["extra"]["prefixes"][self.variant][0]["next_hits"] = [False, False, True, True, False, False]
        g = R.locality_gates(ref, cand, self.p["base_probes"], self.variant)
        self.assertFalse(g["F1:S0"])
        self.assertEqual(sum(not x for x in g.values()), 1)

    def test_all_locality_gate_boundaries(self):
        cand = self.p["recipe"]["arms"][self.variant]
        for key, value in [("L1_flipped_to_edited_value", 2), ("L3_top1_agree", 28), ("generic_ppl_post", 20.501)]:
            old = cand["locality_axes"][key]
            cand["locality_axes"][key] = value
            self.assertEqual(R.pass_reading(self.p, self.variant)["label"], "TRADEOFF")
            cand["locality_axes"][key] = old
        cand["locality_described_as"] = 93.99
        self.assertEqual(R.pass_reading(self.p, self.variant)["label"], "TRADEOFF")
        cand["locality_described_as"] = 94.0
        cand["locality_axes"].update(L1_flipped_to_edited_value=1, L3_top1_agree=29, generic_ppl_post=20.5)
        cand["extra"]["F0"]["flips"] = 1
        self.assertEqual(R.pass_reading(self.p, self.variant)["label"], "LEAD")
        cand["extra"]["F0"]["flips"] = 2
        self.assertEqual(R.pass_reading(self.p, self.variant)["label"], "TRADEOFF")

    def test_qualifier_strict_boundaries(self):
        arms = self.p["recipe"]["arms"]
        ref, cand, dup = arms[R.SINGLE], arms[self.variant], arms[R.DUP]
        self.assertEqual(R.qualifiers(ref, cand, dup, 1.5, self.variant), [])
        self.assertEqual(R.qualifiers(ref, cand, dup, 1.50001, self.variant), ["LARGE-WRITE"])
        cand["extra"]["subject_free"][self.variant][0]["full_hit"] = True
        self.assertEqual(R.qualifiers(ref, cand, dup, 1.0, self.variant), [])
        cand["extra"]["subject_free"][self.variant][1]["full_hit"] = True
        dup["para_full_n"] = 23
        self.assertEqual(R.qualifiers(ref, cand, dup, 1.0, self.variant), ["SUBJECT-FREE", "REQUEST-COUNT"])
        dup["para_full_n"] = 22
        self.assertEqual(R.qualifiers(ref, cand, dup, 1.0, self.variant), ["SUBJECT-FREE"])

    def test_valid_fixture_and_replication_pending(self):
        self.assertEqual(R.validity(self.run, self.p), [])
        v = R.verdict(self.run, self.p)
        self.assertTrue(v["replication_pending"])
        self.assertEqual(v["arms"][self.variant]["label"], "LEAD")
        self.assertFalse(v["arms"][self.variant]["H_T1_label_eligible"])

    def test_extra_string_hit_is_reported_without_changing_label(self):
        expected = R.verdict(self.run, self.p)["arms"][self.variant]["label"]
        for name in (R.SINGLE, R.DUP, self.variant):
            rows = self.p["recipe"]["detail"][name]
            row, t = next((r, t) for r in rows for t, hit in enumerate(r["para_string_hits"]) if not hit)
            row["para_string_hits"][t] = True
            self.p["recipe"]["arms"][name]["para_string_n"] += 1
        self.assertEqual(R.validity(self.run, self.p), [])
        v = R.verdict(self.run, self.p)["arms"][self.variant]
        self.assertEqual(v["label"], expected)
        self.assertEqual((v["pass1"]["count"], v["pass1"]["string_minus_full"]), (32, 1))
        p2 = copy.deepcopy(self.p)
        p2["pid"] = 202
        self.assertEqual(R.verdict(self.run, self.p, p2, {"identity": self.run["identity"], "pid": 202})["arms"][self.variant]["label"], expected)

    def test_observer_inertness_is_a_validity_gate(self):
        edits = [lambda p: p.pop("observer_inertness"), lambda p: p.update(observer_inertness=[]),
                 lambda p: p["observer_inertness"].pop(), lambda p: p["observer_inertness"][0].update(ok=False),
                 lambda p: p["observer_inertness"][0].update(subject="wrong locus"),
                 lambda p: p["observer_inertness"][0].update(tol=1.0),
                 lambda p: p["observer_inertness"][0].update(observed_rel=0.001, ok=True)]
        for edit in edits:
            p = copy.deepcopy(self.p)
            edit(p)
            self.assertEqual(R.verdict(self.run, p)["label"], "INVALID")

    def test_validity_precedes_every_replication_label(self):
        p2 = copy.deepcopy(self.p)
        p2["pid"] = 202
        start = {"identity": self.run["identity"], "pid": 202}
        self.assertEqual(R.verdict(self.run, self.p, p2, start)["arms"][self.variant]["label"], "LEAD")
        p2["fingerprint"]["_cov_cpu"] = 2
        self.assertEqual(R.verdict(self.run, self.p, p2, start)["label"], "INVALID")

    def test_lead_needs_lead_in_second_process(self):
        p2 = fixture_pass(self.run["step0"], count=29, pid=202)
        start = {"identity": self.run["identity"], "pid": 202}
        v = R.verdict(self.run, self.p, p2, start)
        self.assertEqual(v["arms"][self.variant]["label"], "LEAD-NOT-REPLICATED")
        self.assertFalse(v["replication_pending"])

    def test_partial_second_may_be_lead_but_still_needs_gain(self):
        p1 = fixture_pass(self.run["step0"], count=24)
        start = {"identity": self.run["identity"], "pid": 202}
        for n, ref, expected in [(31, 13, "PARTIAL"), (22, 12, "PARTIAL"), (22, 13, "PARTIAL-NOT-REPLICATED"), (18, 5, "PARTIAL-NOT-REPLICATED")]:
            p2 = fixture_pass(self.run["step0"], count=n, ref=ref, pid=202)
            self.assertEqual(R.verdict(self.run, p1, p2, start)["arms"][self.variant]["label"], expected)

    def test_second_process_locality_and_qualifiers_apply(self):
        p2 = copy.deepcopy(self.p)
        p2["pid"] = 202
        start = {"identity": self.run["identity"], "pid": 202}
        for d in p2["recipe"]["delta_norms"][self.variant].values(): d["delta_norm"] = 2.0
        v = R.verdict(self.run, self.p, p2, start)
        self.assertEqual(v["arms"][self.variant]["label"], "LEAD-LARGE-WRITE")
        p2["recipe"]["arms"][self.variant]["locality_axes"]["L3_top1_agree"] = 28
        self.assertEqual(R.verdict(self.run, self.p, p2, start)["arms"][self.variant]["label"], "LEAD-NOT-REPLICATED-LARGE-WRITE")

    def test_per_fact_agreement_and_direct_address_qualification(self):
        p2 = copy.deepcopy(self.p)
        p2["pid"] = 202
        start = {"identity": self.run["identity"], "pid": 202}
        v = R.verdict(self.run, self.p, p2, start)["arms"][self.variant]
        self.assertEqual(v["agreement"], {"facts_with_identical_hits": 24, "n": 24})
        self.assertTrue(v["H_T1_label_eligible"])
        self.assertEqual(len(v["pass1"]["binding"]["per_fact"]), 24)
        self.assertEqual(sum(v["pass1"]["binding"]["per_template"]), 32)

    def test_missing_or_stale_second_is_invalid_and_no_retry(self):
        start = {"identity": self.run["identity"], "pid": 202}
        self.assertEqual(R.verdict(self.run, self.p, second_started=start)["label"], "INVALID")
        self.assertEqual(R.verdict(self.run, self.p, second_started=start, second_halt={"outcome": "HALTED"})["label"], "INVALID")
        self.assertEqual(R.verdict(self.run, self.p, self.p, {"identity": self.run["identity"], "pid": 101})["label"], "INVALID")

    def test_each_validity_failure_is_detected(self):
        edits = [lambda p: p["fingerprint"].update(sha256="bad"), lambda p: p["fingerprint"].update(_cov_cpu=2),
                 lambda p: p["wrapper"].update(candidate_substitutions=0), lambda p: p["wrapper"].update(duplicate_substitutions=0),
                 lambda p: p["wrapper"].update(z_override_hits=1), lambda p: p["admission"].update(ok=False),
                 lambda p: p.update(positions_sha256="3" * 64), lambda p: p["identity"].update(run_id="other"),
                 lambda p: p["recipe"]["law5_gate"].update(expr_delta=0.05),
                 lambda p: p["recipe"]["arms"][R.SINGLE].update(para_full_n=19),
                 lambda p: p["recipe"]["arms"][self.variant].update(para_string_n=31),
                 lambda p: p["recipe"]["arms"][self.variant]["extra"]["prefixes"][self.variant].pop(),
                 lambda p: p["recipe"]["arms"][self.variant]["extra"]["keygram_solve"]["4"].update(n_columns=24),
                 lambda p: p["wrapper"]["reached_my_edit_counts"].update({self.variant: 24}),
                 lambda p: p["recipe"]["arms"][self.variant]["extra"]["fits"][0]["request"].update(prompt="Bad {}")]
        for edit in edits:
            p = copy.deepcopy(self.p)
            edit(p)
            self.assertEqual(R.verdict(self.run, p)["label"], "INVALID")

    def test_invalid_admission_stops_without_pass(self):
        run = copy.deepcopy(self.run)
        run["step0"]["facts"][0]["admissible"] = []
        run["step0"]["facts"][0]["admissible_n"] = 0
        run["step0"]["selection"] = R.select_positions(run["step0"]["facts"])
        run["step0"].update(requests={}, request_sha256={}, overlap={}, overturning={})
        self.assertEqual(R.verdict(run)["label"], "INVALID-ADMISSION")

    def test_unmerged_candidates_are_labelled_separately(self):
        step = unmerged_step()
        run = {"step0": step, "identity": step["identity"], "positions_sha256": "2" * 64}
        p = fixture_pass(step)
        replacement = fixture_pass(step, count=18)
        p["recipe"]["arms"]["A7-second-B5"] = replacement["recipe"]["arms"]["A7-second-B5"]
        p["recipe"]["detail"]["A7-second-B5"] = replacement["recipe"]["detail"]["A7-second-B5"]
        v = R.verdict(run, p)
        self.assertEqual(v["arms"]["A7-second-B10"]["label"], "LEAD")
        self.assertEqual(v["arms"]["A7-second-B5"]["label"], "NULL")

    def test_changed_published_requests_or_selector_are_invalid(self):
        for mutation in (lambda s: s["requests"][self.variant][24]["target_new"].update(str=" Bad"),
                         lambda s: s["facts"][0]["surprisal"].update(p10=2),
                         lambda s: s["overturning"][self.variant]["reading"].update(H_T4_standing=True)):
            run = copy.deepcopy(self.run)
            mutation(run["step0"])
            self.assertEqual(R.verdict(run, self.p)["label"], "INVALID")


class TestPersistence(unittest.TestCase):
    def test_exclusive_write_and_reread(self):
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            p = Path(d) / "record.json"
            A.write_json(p, {"count": 48})
            before = p.read_bytes()
            with self.assertRaises(FileExistsError): A.write_json(p, {"count": 24})
            self.assertEqual(p.read_bytes(), before)
            with self.assertRaisesRegex(ValueError, "occupied"):
                A.refuse_occupied(d, ["record.json"])
            with patch.object(Path, "read_text", return_value="stale"):
                with self.assertRaisesRegex(RuntimeError, "persist"):
                    A.write_json(Path(d) / "new.json", {"count": 48})

    def test_halt_has_own_path_and_preserves_prior_diagnostic(self):
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            for reason in ("first failure", "second failure"):
                with self.assertRaisesRegex(SystemExit, "HALT:"):
                    A.halt(reason, root=d)
            files = list((Path(d) / "architecture_profile").glob("*.json"))
            self.assertEqual(len(files), 2)
            self.assertEqual(json.loads((Path(d) / "experiments/c10t/runs/c10t_secondkey/halts/c10t_secondkey_halt_diagnostic.json").read_text())["reason"], "first failure")

    def test_current_source_hashes_gate_and_transitive_changes(self):
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            root = Path(d)
            for rel in A.SOURCE_FILES + ["code/memit/vendor/memit/compute_z.py", "code/memit/vendor/util/device.py"]:
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("# synthetic source\n")
            identity = A.make_identity(root)
            self.assertEqual(identity["program_rulings"], R.PROGRAM_RULINGS)
            A.require_sources(identity, root)
            (root / "code/memit/vendor/util/device.py").write_text("# changed transitive source\n")
            with self.assertRaisesRegex(ValueError, "source hashes differ"):
                A.require_sources(identity, root)

    def test_preflight_knobs_refused_before_model_import(self):
        for knob in ("Z_OVERRIDE", "C10_KEY_LOCUS", "C10_PROJECTOR", "C10_CTX_TEMPLATES"):
            with patch.dict(os.environ, {knob: ""}):
                with self.assertRaisesRegex(ValueError, "must be unset"):
                    A.preflight(ROOT)
        self.assertNotIn("c10e_bandknob", sys.modules)
        self.assertNotIn("torch", sys.modules)

    def _preflight_refusal(self, stage, inherited, error, message):
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            positions = Path(d) / "positions.json"
            A.write_json(positions, fixture_step())
            env = {"OUT_DIR": d, "POSITIONS": str(positions), **inherited}
            with patch.dict(os.environ, env, clear=True), patch.object(sys, "argv", ["synthetic-driver", stage]):
                with patch.object(A, "LLMDB_ROOT", str(ROOT)), patch.object(S, "LLMDB_ROOT", str(ROOT)), patch.object(A, "RUN_ROOT", ROOT), patch.object(S, "RUN_ROOT", ROOT):
                    with patch.object(A, "IDENTITY", None), patch.object(A, "STAGE", "not-started"), patch.object(A, "require_sources"), patch.object(A, "make_identity", return_value=fixture_step()["identity"]):
                        fp = types.SimpleNamespace(returncode=1, stdout="", stderr="synthetic fingerprint failure")
                        with patch.object(A.subprocess, "run", return_value=fp), patch.object(A, "load_harness", side_effect=AssertionError("model load forbidden")) as loader:
                            with self.assertRaisesRegex(error, message):
                                (S.main if stage == "step0" else A.main)()
                            loader.assert_not_called()
            for name in ("step0.json", "run.json", "pass1.json", "pass2.json", "second_started.json", "second_halt.json"):
                self.assertFalse((Path(d) / name).exists(), (stage, name))

    def test_stale_knob_leaves_no_stage_markers(self):
        for stage in ("first", "second", "step0"):
            self._preflight_refusal(stage, {"OUT": "stale"}, ValueError, "must be unset")

    def test_fingerprint_failure_leaves_no_stage_markers(self):
        for stage in ("first", "second", "step0"):
            self._preflight_refusal(stage, {}, RuntimeError, "engine fingerprint failed")

    def test_script_root_mismatch_refused_before_preflight(self):
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            with patch.object(A, "LLMDB_ROOT", d), patch.object(S, "LLMDB_ROOT", d), patch.object(A, "RUN_ROOT", ROOT), patch.object(S, "RUN_ROOT", ROOT):
                with patch.object(sys, "argv", ["synthetic-driver", "first"]), patch.object(A, "preflight", side_effect=AssertionError("preflight reached")) as preflight:
                    for main in (A.main, S.main):
                        with self.assertRaisesRegex(AssertionError, "script root differs"):
                            main()
                    preflight.assert_not_called()

    def test_halt_resolved_root_survives_working_directory_change(self):
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            root = (Path(d) / "relative-root").resolve()
            elsewhere = Path(d) / "engine-cwd"
            elsewhere.mkdir()
            cwd = Path.cwd()
            try:
                os.chdir(elsewhere)
                with patch.object(A, "LLMDB_ROOT", "relative-root"), patch.object(A, "RUN_ROOT", root):
                    with self.assertRaisesRegex(SystemExit, "HALT:"):
                        A.halt("cwd changed", root=A.RUN_ROOT)
            finally:
                os.chdir(cwd)
            self.assertEqual(json.loads((root / "experiments/c10t/runs/c10t_secondkey/halts/c10t_secondkey_halt_diagnostic.json").read_text())["reason"], "cwd changed")
            self.assertFalse((elsewhere / "relative-root").exists())

    def test_p5_ruling_is_required_in_frozen_identity(self):
        for ruling in (None, {"D-C10t-p5rule": "normalised mean"}):
            step = fixture_step()
            step["identity"]["program_rulings"] = ruling
            with self.assertRaisesRegex(ValueError, "program rulings"):
                A.require_sources(step["identity"], ROOT)
            self.assertIn("p5 ruling missing or changed", R.step0_validity(step))
            self.assertFalse(R.identity_matches(fixture_step()["identity"], step["identity"]))

    def test_invalid_admission_first_records_outcome_without_halt(self):
        step = fixture_step()
        step["facts"][0].update(admissible=[], admissible_n=0)
        step.update(selection=R.select_positions(step["facts"]), requests={}, request_sha256={}, overlap={}, overturning={})
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            positions = Path(d) / "positions.json"
            A.write_json(positions, step)
            with patch.dict(os.environ, {"OUT_DIR": d, "POSITIONS": str(positions)}, clear=True), patch.object(sys, "argv", ["synthetic-driver", "first"]):
                with patch.object(A, "LLMDB_ROOT", str(ROOT)), patch.object(A, "RUN_ROOT", ROOT), patch.object(A, "IDENTITY", None), patch.object(A, "STAGE", "not-started"):
                    with patch.object(A, "require_sources"), patch.object(A, "preflight", return_value={"ok": True}), patch.object(A, "load_harness", side_effect=AssertionError("model load forbidden")) as loader:
                        with patch.object(A, "halt", side_effect=AssertionError("HALT forbidden")) as halt, __import__("contextlib").redirect_stdout(io.StringIO()):
                            self.assertEqual(A.main(), 0)
                            halt.assert_not_called()
                        loader.assert_not_called()
            self.assertEqual(R.verdict(json.loads((Path(d) / "run.json").read_text()))["label"], "INVALID-ADMISSION")
            self.assertFalse((Path(d) / "architecture_profile").exists())

    def test_invalid_admission_step0_publishes_outcome_without_halt(self):
        step = fixture_step()
        by_subject = {f["subj"]: f for f in step["facts"]}
        H = types.SimpleNamespace(model=object(), tok=Tokenizer(), FICTION=list(by_subject),
            ARMS={"A7_coined_coined": {s: f["value"] for s, f in by_subject.items()}},
            req=lambda form, s, v: {"prompt": form, "subject": s, "target_new": {"str": " " + v}}, cov_cache_sha256=lambda hp: {})
        def leverage(H, hp, facts):
            for f in facts:
                f.update({k: copy.deepcopy(by_subject[f["subj"]][k]) for k in ("leverage", "leverage_layers")})
        engine = types.ModuleType("memit.memit_main")
        engine.get_context_templates = lambda model, tok: CONTEXTS
        repr_tools = types.ModuleType("rome.repr_tools")
        repr_tools.get_words_idxs_in_templates = IDX
        modules = {"memit": types.ModuleType("memit"), "memit.memit_main": engine,
                   "rome": types.ModuleType("rome"), "rome.repr_tools": repr_tools}
        with tempfile.TemporaryDirectory(prefix="c10t-selftest-") as d:
            with patch.dict(os.environ, {"OUT_DIR": d}, clear=True), patch.dict(sys.modules, modules):
                with patch.object(S, "LLMDB_ROOT", str(ROOT)), patch.object(S, "RUN_ROOT", ROOT), patch.object(A, "IDENTITY", None), patch.object(A, "STAGE", "not-started"):
                    with patch.object(A, "make_identity", return_value=step["identity"]), patch.object(A, "require_sources"), patch.object(A, "preflight", return_value={"ok": True}), patch.object(A, "load_harness", return_value=(H, None, {"ok": True})):
                        with patch.object(S, "position_classes", side_effect=lambda H, s, v, ids: (R.CANON.format(s) + " " + v, copy.deepcopy(by_subject[s]["positions"]))), patch.object(S, "surprisal", side_effect=lambda H, s, ids: copy.deepcopy(by_subject[s]["surprisal"])), patch.object(S, "leverage", side_effect=leverage):
                            with patch.object(A, "canonical_audit", side_effect=lambda tok, rq, *args: {"ok": rq["subject"] != "S0"}), patch.object(A, "halt", side_effect=AssertionError("HALT forbidden")) as halt, __import__("contextlib").redirect_stdout(io.StringIO()):
                                self.assertEqual(S.main(), 0)
                                halt.assert_not_called()
            published = json.loads((Path(d) / "step0.json").read_text())
            self.assertEqual(published["selection"]["outcome"], "INVALID-ADMISSION")
            self.assertEqual(R.step0_validity(published), [])
            self.assertFalse((Path(d) / "architecture_profile").exists())


class TestTelemetry(unittest.TestCase):
    def _observer_case(self, triples):
        class Scalar:
            def __init__(self, x): self.x = x
            def item(self): return self.x
            def detach(self): return self
            def float(self): return self
            def cpu(self): return self
            def tolist(self): return [self.x]
            def norm(self): return abs(self.x)
            def __sub__(self, other): return Scalar(self.x - other.x)
        targets = iter(x for triple in triples for x in triple)
        calls = []
        def compute_z(model, tok, request, hp, layer, ctx):
            calls.append((request, layer, ctx, sys.gettrace() is not None))
            it, lookup_idxs = 0, [0, 1]
            nll_loss, kl_loss, loss, weight_decay = Scalar(0.2), Scalar(0.01), Scalar(0.2), Scalar(0.001)
            nll_loss_each, target_init, delta = Scalar(0.2), Scalar(1.0), Scalar(0.0)
            return Scalar(next(targets))
        step = fixture_step()
        H = types.SimpleNamespace(model=object(), tok=object(), compute_z=compute_z)
        rows = A.observer_inertness(H, types.SimpleNamespace(layers=R.BAND), CONTEXTS, next(iter(step["requests"].values())))
        return rows, calls, step

    def test_observer_floor_rule_includes_both_tolerance_boundaries(self):
        for floor, rel, ok in [(0.0, 1e-4, True), (0.0, math.nextafter(1e-4, math.inf), False),
                               (0.001, 0.01, True), (0.001, math.nextafter(0.01, math.inf), False),
                               (-0.001, 0.0, False), (math.inf, 0.0, False), (math.nan, 0.0, False),
                               (0.0, math.inf, False), (0.0, math.nan, False)]:
            self.assertIs(R.observer_inertness_reading(floor, rel)["ok"], ok)

    def test_observer_inertness_runs_three_solves_at_each_locus(self):
        rows, calls, step = self._observer_case([(1.0, 1.0, 1.0), (1.0, 1.0, 1.0)])
        requests = next(iter(step["requests"].values()))
        self.assertEqual([c[0] for c in calls], [requests[0]] * 3 + [requests[R.N]] * 3)
        self.assertEqual([c[3] for c in calls], [False, False, True] * 2)
        self.assertTrue(all(c[1] == R.BAND[-1] and c[2] is CONTEXTS for c in calls))
        self.assertTrue(all(r["ok"] and r["floor"] == 0 and r["tol"] == 1e-4 for r in rows))
        self.assertIsNone(sys.gettrace())

    def test_observer_inertness_uses_measured_noise_floor(self):
        rows, _, _ = self._observer_case([(1.0, 1.0001, 1.0009)] * 2)
        self.assertTrue(all(r["ok"] and r["observed_rel"] > 1e-4 for r in rows))
        self.assertTrue(all(r["tol"] == 10 * r["floor"] for r in rows))

    def test_observer_inertness_failure_stops_and_clears_trace(self):
        with self.assertRaisesRegex(ValueError, "compute_z observer not inert"):
            self._observer_case([(1.0, 1.0, 1.001), (1.0, 1.0, 1.0)])
        self.assertIsNone(sys.gettrace())

    def test_read_only_frame_observation_returns_same_target(self):
        class Scalar:
            def __init__(self, x): self.x = x
            def item(self): return self.x
            def detach(self): return self
            def float(self): return self
            def cpu(self): return self
            def tolist(self): return [self.x]
            def norm(self): return self.x
            def __float__(self): return float(self.x)
        target = object()
        ns = {"Scalar": Scalar, "target": target}
        source = "\n" * 170 + "def synthetic_engine():\n    it = 3\n    nll_loss = Scalar(0.2)\n    kl_loss = Scalar(0.01)\n    loss = Scalar(0.04)\n    weight_decay = Scalar(0.001)\n    nll_loss_each = Scalar(0.2)\n    delta = Scalar(1.0)\n    target_init = Scalar(5.0)\n    lookup_idxs = [2, 7]\n    return target\n"
        exec(compile(source, "synthetic_engine.py", "exec"), ns)
        before = sys.gettrace()
        z, fit = A.observe_solve(ns["synthetic_engine"], (), clamp_line=178)
        self.assertIs(z, target)
        self.assertIs(sys.gettrace(), before)
        self.assertEqual((fit["loss_evaluations"], fit["adam_steps"], fit["clamp_hit_steps"]), (4, 3, 1))
        self.assertEqual(fit["stopped_by"], "loss<0.05")
        self.assertAlmostEqual(fit["exp_minus_nll"], math.exp(-0.2))
        self.assertEqual(fit["kl_loss"], 0.01)

    def test_failed_solve_removes_trace(self):
        def fail(): raise RuntimeError("intentional synthetic failure")
        with self.assertRaisesRegex(RuntimeError, "intentional"):
            A.observe_solve(fail, ())
        self.assertIsNone(sys.gettrace())


if __name__ == "__main__":
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    if "torch" in sys.modules or "transformers" in sys.modules or "c10e_bandknob" in sys.modules:
        raise RuntimeError("model-free selftest imported a forbidden runtime module")
    if result.wasSuccessful():
        print("C10T_SECONDKEY_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)")
    sys.exit(0 if result.wasSuccessful() else 1)
