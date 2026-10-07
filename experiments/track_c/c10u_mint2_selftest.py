#!/usr/bin/env python3
"""D-C10u-mint2 v3 model-free rule and safety tests; stdlib only.

Synthetic complete records exercise the frozen counts and failure precedence.
Temporary directories are the only test writes. No model or driver is run.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import copy, hashlib, importlib, io, json, tempfile, unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
R = importlib.import_module("c10u_mint2_read") if (HERE / "c10u_mint2_read.py").exists() else None


def source_digest(hashes):
    return hashlib.sha256("\n".join(k + " " + v for k, v in sorted(hashes.items())).encode()).hexdigest()


def fixture_record(block="V2", kind="mint2", seed=0, count=32, replicate=0, pid=None, recall=0):
    """Counts are distributed over distinct fact/template trials, never pooled."""
    subjects = ["S" + str(i) for i in range(24)]
    values = {s: ("Head" + str(i if block == "V2" else i % 12) + " Modifier" + str(i if block == "V2" else i % 8)) for i, s in enumerate(subjects)}
    ntok = {"multi": 5, "mint1": 1, "modifier": 3, "mint2": 2, "mint1_48": 1}[kind]
    full = count + recall if kind != "multi" else count
    first, canon = (54, 8) if kind == "multi" else (full if kind in ("mint1", "mint1_48") else max(full, 54), 16)
    rows = [{"subj": s, "val": values[s], "ntok": ntok, "canon_full": i < canon,
             "canon_first": i < canon, "para_full_hits": [i * 3 + t < full for t in range(3)],
             "para_first_hits": [i * 3 + t < first for t in range(3)],
             "para_string_hits": [i * 3 + t < full for t in range(3)],
             "para_startswith_hits": [i * 3 + t < full for t in range(3)]}
            for i, s in enumerate(subjects)]
    pre = [{"subj": s, "para_full_hits": [i * 3 + t < recall for t in range(3)]}
           for i, s in enumerate(subjects)]
    fits = [] if kind == "multi" else [{"subj": s, "probs": [0.99] * ntok,
                                         "loss_layer_probs": [0.99] * ntok} for s in subjects]
    norms = {str(l): {"delta_norm": 1.0} for l in range(4, 9)}
    arm = {"para_full_n": full, "para_full_binding_n": count, "canon_full_n": canon,
           "para_first_n": first, "para_string_n": full, "para_startswith_n": full,
           "canon_n": 24, "para_n": 72, "locality_described_as": 97.0,
           "tf_pertok_cont": 100.0, "cond_full_given_first": full / first,
           "locality_axes": {"L1_n": 12, "L1_flipped_to_edited_value": 0,
                             "L3_n": 30, "L3_top1_agree": 30,
                             "generic_ppl_pre": 20.0, "generic_ppl_post": 20.0},
           "extra": {"same_frame_flips": 0, "frame_n": 6, "frame_minted_n": 0,
                     "L1_minted_n": 0, "L3_minted_n": 0, "para_sibling": 0,
                     "post_write_cannibal": 0,
                     "bigram": [{"subj": s, "c_k": 1, "s_k": 0, "b_k": 0, "n_k": 0.0}
                                for s in subjects] if kind in ("mint2", "modifier") else [],
                     "per_position_teacher_forced": {str(j): {"hits": first if j == 0 else full, "n": 72}
                                                     for j in range(ntok)}}}
    controls = {"para_full_n": 72, "para_string_n": 72, "canon_full_n": 24,
                "para_first_n": 72, "para_n": 72, "canon_n": 24}
    hashes = {R.PREREG: "1" * 64, "results/c10u_mint2/v2_wordlist.json": "2" * 64,
              "experiments/track_c/c10u_mint2_read.py": "3" * 64}
    rules = {"synthetic": "frozen test rules"}
    context = [["{}"], ["A clean context. {}"]]
    rows_hash = hashlib.sha256((str(seed) + "rows").encode()).hexdigest()
    relation_table = {"block": block, "subject_values": values, "candidates": [],
                      "pairwise_relations_among_48": [], "modifier_relations": [],
                      "short_common_words_inside_heads": []}
    words = [] if kind == "multi" else list(values.values()) if kind == "mint1" else list(values.values()) + [v.split()[0] for v in values.values()] if kind == "mint1_48" else [v.split()[0] for v in values.values()] + [v.split()[1] for v in values.values()] if kind == "mint2" else ["Modifier" + str(i) for i in range(8)]
    ids = list(range(151665, 151665 + len(words)))
    lookup = dict(zip(words, ids))
    p2rows = []
    for i, s in enumerate(subjects):
        head, mod = values[s].split()
        target = [lookup[values[s]]] if kind in ("mint1", "mint1_48") else [lookup[head], lookup[mod]] if kind == "mint2" else [10 + i, 100 + i, lookup[mod]] if kind == "modifier" else list(range(5))
        p2rows.append({"subj": s, "value": values[s], "target_ids": target, "expected_ids": target,
                       "contexts": [{"template": t, "prefix_ids": True, "whole_ids": True, "last_id": True} for g in context for t in g],
                       "checks": {"whole_target": True, "decode": True, "engine_default_call": True, "contexts": True, **({"head_decode": True} if kind == "mint2" else {})}, "ok": True})
    p2 = {"ok": True, "checks": {"inventory_unchanged": True, "registered_word_ids": True, "all_target_rows": True, **({"bigram_720_prefix_ids": True} if kind == "mint2" else {})},
          "changed": [], "inventory_n": 48, "plain_n": 24, "rows": p2rows,
          "bigram_rows": [{"ok": True} for _ in range(720)] if kind == "mint2" else [], "block": block, "kind": kind}
    return {"block": block, "replicate": replicate, "kind": kind,
            "seed": None if kind == "multi" else seed,
            "pid": pid if pid is not None else 1000 + replicate * 100 + seed +
                   {"multi": 10, "mint1": 20, "modifier": 30, "mint2": 40, "mint1_48": 50}[kind],
            "identity": {"source_sha256": hashes, "source_digest": source_digest(hashes)},
            "ctx": context, "ctx_sha256": R.json_digest(context),
            "provenance": {"heads_sha256": R.HEADS_SHA256, "modifiers_sha256": R.MODIFIERS_SHA256,
                           "wordlist_sha256": "2" * 64, "rules": rules, "rules_sha256": R.json_digest(rules),
                           "relation_table": relation_table, "relation_sha256": R.json_digest(relation_table),
                           "row_pairing": {"rows_sha256": rows_hash, "first8_sha256": rows_hash,
                                           "first24_sha256": rows_hash, "pairing_ok": True}},
            "fingerprint": {"ok": True, "sha256": "d941a9fb" + "0" * 56, "_cov_cpu": 3},
            "inertness": {"ok": True, "override_rel": 0.0, "context_rel": 0.0, "expr_delta": 0.0},
            "wrapper": {"z_override_hits": 1, "law5_override_hits": 0},
            "admission": {"P2": p2, "P3": {"fits": [] if kind == "multi" else [0.99] * 24},
                          "no_i11_exclusion": True},
            "step0": {"recall_n": recall, "n_cannibal": 0, "recall_rows": pre, "per_position_fit": fits},
            "recipe": {"law5_gate": {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0},
                       "arms": {"A1_single": copy.deepcopy(controls), "A2_coherent2": copy.deepcopy(controls),
                                "candidate": arm}, "detail": {"candidate": rows},
                       "delta_norms": {"candidate": norms}}, "arm": arm,
            "minted_words": words, "minted_ids": ids, "outcome": "DONE"}


def fixture_block(block="V2", m1=(34, 36, 46), candidate=(21, 22, 24), ref=11, replicate=0):
    kind = "mint2" if block == "V2" else "modifier"
    return [fixture_record(block, "multi", count=ref, replicate=replicate),
            *[fixture_record(block, "mint1", s, n, replicate) for s, n in enumerate(m1)],
            *[fixture_record(block, kind, s, n, replicate) for s, n in enumerate(candidate)]]


def fixture_controls(counts=(34, 36, 46)):
    return [fixture_record("V2", "mint1_48", s, n) for s, n in enumerate(counts)]


def fixture_p4(kind="mint2"):
    words = ["Head" + str(i) for i in range(24)] + ["Mod" + str(i) for i in range(24)] if kind == "mint2" else ["Mod" + str(i) for i in range(8)]
    minted = [{"word": w, "id": 151665 + i, "ids": [151665 + i], "ok": True} for i, w in enumerate(words)]
    targets, groups = [], {"canon": [], "para": [], "L1": [], "L3": [], "unrelated": []}
    for i in range(24):
        ids = [151665 + i, 151689 + i] if kind == "mint2" else [10 + i, 100 + i, 151665 + i % 8]
        value = "Head" + str(i) + " Mod" + str(i if kind == "mint2" else i % 8)
        target = {"subj": "S" + str(i), "expected_ids": ids, "ids": ids, "ok": True}
        targets.append(target)
        row = {"subj": target["subj"], "value": value, "expected_ids": ids,
               "hf_ids": ids, "gguf_ids": ids, "parity": True, "correct": True, "signature": "fixture"}
        groups["canon"].append(copy.deepcopy(row))
        groups["para"].extend(copy.deepcopy(row) for _ in range(3))
    for key, n in (("L1", 12), ("L3", 30), ("unrelated", 10)):
        groups[key] = [{"expected_ids": None, "hf_ids": [5], "gguf_ids": [5], "parity": True,
                        "correct": None, "signature": "fixture"} for _ in range(n)]
    probe = {"reference_sha256": "b" * 64, "minted_tokenization": minted, "target_tokenization": targets,
             "groups": groups, "tokenizer_ok": True, "identity": fixture_record()["identity"]}
    return {"kind": kind, "fp16": {**copy.deepcopy(probe), "label": "fp16"},
            "q4km": {**copy.deepcopy(probe), "label": "q4km"}}


class Tokenizer:
    """Character base tokens plus exact leading-space added-token strings."""
    def __init__(self, words=()):
        self.minted = {" " + word: 151665 + i for i, word in enumerate(words)}
        self.reverse = {i: text for text, i in self.minted.items()}

    def __call__(self, text, **kwargs):
        ids, position = [], 0
        while position < len(text):
            matched = next((w for w in sorted(self.minted, key=len, reverse=True) if text.startswith(w, position)), None)
            if matched is None:
                ids.append(ord(text[position]) + 1)
                position += 1
            else:
                ids.append(self.minted[matched])
                position += len(matched)
        return {"input_ids": ids}

    def decode(self, ids):
        return "".join(self.reverse[i] if i in self.reverse else chr(i - 1) for i in ids)


def fixture_p2(kind="mint2", contexts=None):
    subjects = ["S" + str(i).zfill(2) for i in range(24)]
    heads = ["H" + str(i).zfill(2) for i in range(24)]
    modifiers = ["M" + str(i).zfill(2) for i in range(24 if kind == "mint2" else 8)]
    values = {s: heads[i] + " " + modifiers[i % len(modifiers)] for i, s in enumerate(subjects)}
    words = heads + modifiers if kind == "mint2" else modifiers
    contexts = [["{}"], ["Clean. {}"]] if contexts is None else contexts
    prompts = ["The capital of " + s + " is the city of" for s in subjects]
    frames = ["F" + str(i).zfill(2) for i in range(6)]
    tok = Tokenizer(words)
    return [Tokenizer(), tok, words, list(range(151665, 151665 + len(words))), values,
            subjects, frames, contexts, prompts, kind, "V2" if kind == "mint2" else "F"]


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(R, "new pure reader is not implemented")

    def test_complete_record_and_raw_minus_pre_binding(self):
        ref, cand = fixture_record(kind="multi", count=11), fixture_record(count=32, recall=2)
        self.assertEqual(R.run_validity(cand), [])
        read = R.run_reading(ref, cand)
        self.assertEqual((read["binding"], read["raw"], read["pre_recall"]), (32, 34, 2))
        self.assertEqual(read["label"], "LEAD-NOT-REPLICATED")
        self.assertTrue(read["replication_pending"])

    def test_contains_allows_alternative_ids_and_startswith_is_separate(self):
        ref, cand = fixture_record(kind="multi", count=11), fixture_record(count=31)
        cand["recipe"]["detail"]["candidate"][10]["para_string_hits"][1] = True
        cand["arm"]["para_string_n"] = 32
        self.assertEqual(R.run_validity(cand), [])
        read = R.run_reading(ref, cand)
        self.assertEqual((read["alt_tok_n"], read["string_contains"], read["string_startswith"]), (1, 32, 31))

    def test_string_below_full_invalid_even_when_binding_is_lead(self):
        cand = fixture_record(count=40)
        cand["arm"]["para_string_n"] = 39
        self.assertTrue(R.run_validity(cand))
        self.assertEqual(R.run_reading(fixture_record(kind="multi", count=11), cand)["label"], "INVALID")

    def test_a1_68_boundary_and_missing_shape_fail_closed(self):
        for n, valid in ((68, True), (67, False)):
            cand = fixture_record()
            cand["recipe"]["arms"]["A1_single"]["para_full_n"] = n
            self.assertEqual(not R.run_validity(cand), valid)
        for key in ("provenance", "wrapper", "ctx", "recipe", "admission"):
            cand = fixture_record()
            del cand[key]
            self.assertTrue(R.run_validity(cand), key)

    def test_admission_22_values_and_per_position_underfit_remain_distinct(self):
        cand = fixture_record()
        cand["admission"]["P3"]["fits"][:2] = [0.97, 0.97]
        self.assertEqual(R.run_validity(cand), [])
        cand["admission"]["P3"]["fits"][2] = 0.97
        self.assertTrue(R.run_validity(cand))
        records = fixture_block()
        records[4]["step0"]["per_position_fit"][0]["probs"][1] = 0.97
        self.assertEqual(R.run_validity(records[4]), [])
        self.assertEqual(R.block_reading(records)["direction"], "ROUTING-BLOCKED-UNDERFIT")

    def test_underfit_mask_is_reported_without_changing_binding(self):
        ref, cand = fixture_record(kind="multi", count=11), fixture_record(count=32)
        cand["step0"]["per_position_fit"][0]["probs"][1] = 0.97
        read = R.run_reading(ref, cand)
        self.assertEqual((read["binding"], read["masked_binding"], read["masked_n"]), (32, 29, 69))
        self.assertEqual(read["per_position_curve"][0]["underfit"], True)

    def test_inertness_fingerprint_and_override_audits_reject_tampering(self):
        for path, value in [(('fingerprint', 'ok'), False), (('fingerprint', '_cov_cpu'), 2),
                            (('inertness', 'ok'), False), (('wrapper', 'z_override_hits'), 0),
                            (('wrapper', 'law5_override_hits'), 1)]:
            cand = fixture_record()
            cand[path[0]][path[1]] = value
            self.assertTrue(R.run_validity(cand), path)
        cand = fixture_record()
        cand["recipe"]["law5_gate"]["expr_delta"] = 0.05
        self.assertTrue(R.run_validity(cand))

    def test_hashes_context_and_row_counts_are_recomputed(self):
        mutations = [lambda r: r["ctx"][1].append("changed {}"),
                     lambda r: r["identity"].update(source_digest="f" * 64),
                     lambda r: r["provenance"].update(heads_sha256="f" * 64),
                     lambda r: r["provenance"]["rules"].update(changed=True),
                     lambda r: r["provenance"]["row_pairing"].update(pairing_ok=False),
                     lambda r: r["recipe"]["detail"]["candidate"].pop(),
                     lambda r: r["recipe"]["detail"]["candidate"][0]["para_full_hits"].__setitem__(0, False),
                     lambda r: r["step0"]["recall_rows"][0]["para_full_hits"].__setitem__(0, True)]
        for mutate in mutations:
            cand = fixture_record()
            mutate(cand)
            self.assertTrue(R.run_validity(cand))

    def test_locality_boundaries_and_falsefires(self):
        ref, cand = fixture_record(kind="multi", count=11), fixture_record()
        ax, ex = cand["arm"]["locality_axes"], cand["arm"]["extra"]
        ax.update(L1_flipped_to_edited_value=1, L3_top1_agree=29, generic_ppl_post=20.5)
        ex.update(same_frame_flips=1, post_write_cannibal=2, para_sibling=3)
        cand["arm"]["locality_described_as"] = 94.0
        self.assertTrue(all(R.locality_gates(ref, cand).values()))
        for target, key, bad in ((ax, "L1_flipped_to_edited_value", 2), (ax, "L3_top1_agree", 28),
                                 (ax, "generic_ppl_post", 20.50001), (ex, "same_frame_flips", 2),
                                 (ex, "post_write_cannibal", 3), (ex, "para_sibling", 4),
                                 (ex, "L1_minted_n", 1), (ex, "L3_minted_n", 1), (ex, "frame_minted_n", 1)):
            old = target[key]
            target[key] = bad
            self.assertFalse(all(R.locality_gates(ref, cand).values()), key)
            target[key] = old

    def test_null_band_precedes_gain_and_tradeoff_uses_binding(self):
        for count, ref_count, want in ((18, 5, "NULL"), (19, 9, "PARTIAL-NOT-REPLICATED"),
                                       (29, 20, "NULL"), (30, 20, "LEAD-NOT-REPLICATED")):
            ref, cand = fixture_record(kind="multi", count=ref_count), fixture_record(count=count)
            self.assertEqual(R.run_reading(ref, cand)["label"], want)
        ref, cand = fixture_record(kind="multi", count=11), fixture_record(count=30)
        cand["arm"]["extra"]["frame_minted_n"] = 1
        self.assertEqual(R.run_reading(ref, cand)["label"], "TRADEOFF")

    def test_replication_uses_same_seed_context_rows_and_fresh_pid(self):
        a, b = fixture_block(), fixture_block(replicate=1)
        read = R.run_reading(a[0], a[4], {"reference": b[0], "candidate": b[4]})
        self.assertEqual(read["label"], "PARTIAL")
        for change in (lambda x: x.update(pid=a[4]["pid"]),
                       lambda x: x.update(seed=1),
                       lambda x: x["provenance"]["row_pairing"].update(first24_sha256="f" * 64)):
            replica = copy.deepcopy(b[4])
            change(replica)
            self.assertEqual(R.run_reading(a[0], a[4], {"reference": b[0], "candidate": replica})["label"], "INVALID")

    def test_replica_locality_miss_prevents_replication(self):
        a, b = fixture_block(candidate=(30, 31, 32)), fixture_block(candidate=(30, 31, 32), replicate=1)
        b[4]["arm"]["extra"]["frame_minted_n"] = 1
        self.assertEqual(R.run_reading(a[0], a[4], {"reference": b[0], "candidate": b[4]})["label"], "LEAD-NOT-REPLICATED")

    def test_large_write_is_qualifier_not_gate(self):
        ref, cand = fixture_record(kind="multi", count=11), fixture_record()
        for v in cand["recipe"]["delta_norms"]["candidate"].values():
            v["delta_norm"] = 1.5
        self.assertEqual(R.run_reading(ref, cand)["write_ratio"], 1.5)
        self.assertNotIn("LARGE-WRITE", R.run_reading(ref, cand)["qualifiers"])
        cand["recipe"]["delta_norms"]["candidate"]["4"]["delta_norm"] += 0.0001
        self.assertIn("LARGE-WRITE", R.run_reading(ref, cand)["qualifiers"])

    def test_direction_keeps_candidate_large_write_and_bigram_qualifiers(self):
        a, b = fixture_block(candidate=(11, 14, 20)), fixture_block(candidate=(11, 14, 20), replicate=1)
        for v in a[4]["recipe"]["delta_norms"]["candidate"].values():
            v["delta_norm"] = 2.0
        self.assertEqual(R.block_reading(a, b)["direction"], "PAIR-DIRECTION-LARGE-WRITE")
        for row in a[4]["arm"]["extra"]["bigram"]:
            row["c_k"] = 0
        a[4]["arm"]["extra"]["bigram"][0].update(c_k=1, s_k=1)
        self.assertEqual(R.block_reading(a, b)["direction"], "PAIR-DIRECTION-BIGRAM-LARGE-WRITE")

    def test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff(self):
        ref, cand = fixture_record(kind="multi", count=11), fixture_record(count=32)
        read = R.run_reading(ref, cand)
        self.assertIn("position_mechanism", read)
        self.assertEqual(read["position_mechanism"]["state"], "POSITION-0-LOSS")
        cand["arm"]["para_first_n"] = 72
        for row in cand["recipe"]["detail"]["candidate"]:
            row["para_first_hits"] = [True] * 3
        cand["arm"]["extra"]["per_position_teacher_forced"]["0"]["hits"] = 72
        read = R.run_reading(ref, cand)
        self.assertEqual(read["position_mechanism"]["state"], "POSITION-1-LOSS")
        self.assertEqual(read["position_mechanism"]["misses_per_position"], {"0": 0, "1": 40})

    def test_law3_seed_envelopes_median_and_multi_envelope(self):
        for counts, ok in (((32, 24, 30), True), ((56, 44, 46), True), ((31, 34, 36), False),
                           ((46, 23, 36), False), ((46, 34, 47), False), ((32, 24, 26), False)):
            rows = [fixture_record("F", "mint1", s, n) for s, n in enumerate(counts)]
            self.assertEqual(R.reproduction_gate(rows)["ok"], ok, counts)
        rows = fixture_block("F")[1:4]
        multi = fixture_record("F", "multi", count=11)
        self.assertTrue(R.reproduction_gate(rows, multi)["ok"])
        multi["arm"]["para_full_n"] = 19
        self.assertFalse(R.reproduction_gate(rows, multi)["ok"])
        self.assertFalse(R.reproduction_gate(rows[:2])["ok"])

    def test_law3_miss_suspends_frozen_block(self):
        records = fixture_block("F", m1=(31, 34, 36), candidate=(34, 36, 46))
        self.assertEqual(R.block_reading(records)["direction"], "HALT-LAW3")

    def test_bigram_uses_fact_union_and_zero_correct_is_no_continuation(self):
        rows = fixture_record()["arm"]["extra"]["bigram"]
        for r in rows: r["c_k"] = 0
        self.assertEqual(R.bigram_reading(rows, "V2")["reading"], "NO-CONTINUATION")
        rows[0].update(c_k=1, s_k=1, n_k=1.0)
        read = R.bigram_reading(rows, "V2")
        self.assertEqual((read["C"], read["X"], read["qualifier"]), (1, 1, "BIGRAM"))
        rows[0].update(s_k=0, n_k=0.0, b_k=1)
        self.assertIsNone(R.bigram_reading(rows, "V2")["qualifier"])
        self.assertEqual(R.bigram_reading(rows, "F")["qualifier"], "BIGRAM")
        rows[0]["n_k"] = 1 / 3
        rows[0]["b_k"] = 0
        self.assertIsNone(R.bigram_reading(rows, "F")["qualifier"])
        rows[0]["n_k"] = 0.5
        self.assertEqual(R.bigram_reading(rows, "F")["qualifier"], "BIGRAM")

    def test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction(self):
        rows = fixture_record()["arm"]["extra"]["bigram"]
        for bad in (rows[:23], rows[:23] + [rows[0]], [{**r, "n_k": 1.1} for r in rows]):
            with self.assertRaises(ValueError):
                R.bigram_reading(bad, "V2")

    def test_span_requires_replication_and_matched48_control(self):
        a, b = fixture_block(), fixture_block(replicate=1)
        pending = R.block_reading(a)
        self.assertEqual(pending["direction"], "PENDING-REPLICATION")
        self.assertTrue(pending["controls_pending"])
        self.assertEqual(R.block_reading(a, b)["direction"], "PENDING-CONTROL")
        self.assertEqual(R.block_reading(a, b, fixture_controls())["direction"], "SPAN-DIRECTION")
        self.assertEqual(R.block_reading(a, b, fixture_controls((33, 34, 34)))["direction"], "SPAN-CONFOUNDED")

    def test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control(self):
        a = fixture_block()
        b = fixture_block(m1=(36, 36, 46), candidate=(23, 24, 26), replicate=1)
        self.assertEqual(R.block_reading(a, b, fixture_controls())["direction"], "SPAN-DIRECTION")

    def test_pair_nonoverlap_rule_and_seed_range(self):
        a = fixture_block(candidate=(11, 14, 20))
        b = fixture_block(candidate=(11, 14, 20), replicate=1)
        self.assertEqual(R.block_reading(a, b)["direction"], "PAIR-DIRECTION")
        self.assertEqual(R.block_reading(a, b)["candidate_range"], 9)
        a, b = fixture_block(candidate=(21, 22, 25)), fixture_block(candidate=(21, 22, 25), replicate=1)
        self.assertEqual(R.block_reading(a, b)["direction"], "MIXED")
        a, b = fixture_block(m1=(34, 36, 42), candidate=(34, 38, 46)), fixture_block(m1=(34, 36, 42), candidate=(34, 38, 46), replicate=1)
        self.assertEqual(R.block_reading(a, b)["direction"], "MIXED")

    def test_modifier_recovery_truth_table_frozen_at_v3(self):
        cases = [(18, (34, 35, 36), (28, 29, 30), "MIXED"),
                 (11, (34, 36, 46), (34, 36, 46), "MODIFIER-RECOVERY"),
                 (11, (34, 34, 36), (25, 28, 31), "MIXED"),
                 (11, (34, 36, 46), (11, 14, 20), "NO-MODIFIER-GAIN")]
        for s, m1, mo, want in cases:
            a, b = fixture_block("F", m1, mo, s), fixture_block("F", m1, mo, s, 1)
            self.assertEqual(R.block_reading(a, b)["direction"], want)

    def test_not_comparable_and_underfit_precede_direction(self):
        a, b = fixture_block(ref=19), fixture_block(ref=19, replicate=1)
        self.assertEqual(R.block_reading(a, b)["direction"], "NOT-COMPARABLE")
        self.assertTrue(all("NOT-COMPARABLE" in x["label"] for x in R.block_reading(a, b)["arms"].values()))
        a, b = fixture_block(m1=(29, 29, 46)), fixture_block(m1=(29, 29, 46), replicate=1)
        self.assertEqual(R.block_reading(a, b)["direction"], "NOT-COMPARABLE")
        a, b = fixture_block(), fixture_block(replicate=1)
        b[1]["step0"]["per_position_fit"][23]["probs"][0] = 0.97
        self.assertEqual(R.block_reading(a, b)["direction"], "ROUTING-BLOCKED-UNDERFIT")

    def test_blocks_never_pool_or_recover_missing_seed(self):
        a = fixture_block()
        self.assertEqual(R.block_reading(a[:6])["direction"], "INCOMPLETE")
        self.assertEqual(R.block_reading(a[:6] + [fixture_record("F", "modifier", 2, 24)])["direction"], "INVALID")
        self.assertEqual(R.block_reading(a + [copy.deepcopy(a[1])])["direction"], "INVALID")
        self.assertEqual(R.block_reading(a, fixture_block(replicate=1)[:6])["direction"], "INCOMPLETE")

    def test_malformed_block_objects_fail_closed_without_raising(self):
        for records in ([None], [{"block": "V2", "kind": "mint2", "seed": []}], [0]):
            try:
                reading = R.block_reading(records)
            except (AttributeError, TypeError, ValueError) as e:
                self.fail("malformed records raised instead of INVALID: " + str(e))
            self.assertEqual(reading["direction"], "INVALID")

    def test_missing_norm_layer_and_empty_p2_rows_are_invalid(self):
        record = fixture_record()
        record["recipe"]["delta_norms"]["candidate"].pop("4")
        self.assertTrue(R.run_validity(record))
        record = fixture_record()
        record["admission"]["P2"]["rows"] = []
        self.assertTrue(R.run_validity(record))

    def test_reproduction_provenance_is_checked_before_any_new_arm(self):
        records = fixture_block("F")[1:4]
        records[0]["ctx"][1].append("Different. {}")
        records[0]["ctx_sha256"] = R.json_digest(records[0]["ctx"])
        self.assertFalse(R.reproduction_gate(records)["ok"])

    def test_block_rejects_changed_context_data_and_pairing(self):
        for mutate in (lambda r: r["identity"]["source_sha256"].update(extra="f" * 64),
                       lambda r: r["provenance"]["relation_table"]["subject_values"].update(S0="changed"),
                       lambda r: r["provenance"]["row_pairing"].update(first24_sha256="f" * 64)):
            a = fixture_block()
            mutate(a[4])
            a[4]["identity"]["source_digest"] = source_digest(a[4]["identity"]["source_sha256"])
            a[4]["provenance"]["relation_sha256"] = R.json_digest(a[4]["provenance"]["relation_table"])
            self.assertEqual(R.block_reading(a)["direction"], "INVALID")

    def test_full_fourteen_schedule_and_conditional_stages(self):
        def brief(plan):
            return [(x["block"], x["replicate"], x["kind"], x["seed"]) for x in plan]
        self.assertEqual(brief(R.stage_plan("reproduce")), [("F", 0, "mint1", 0), ("F", 0, "mint1", 1), ("F", 0, "mint1", 2)])
        self.assertEqual(brief(R.stage_plan("frozen")), [("F", 0, "multi", None), ("F", 0, "modifier", 0), ("F", 0, "modifier", 1), ("F", 0, "modifier", 2)])
        self.assertEqual(brief(R.stage_plan("v2")), [("V2", 0, "multi", None), ("V2", 0, "mint1", 0), ("V2", 0, "mint1", 1), ("V2", 0, "mint1", 2), ("V2", 0, "mint2", 0), ("V2", 0, "mint2", 1), ("V2", 0, "mint2", 2)])
        self.assertEqual(len(R.stage_plan("reproduce") + R.stage_plan("frozen") + R.stage_plan("v2")), 14)
        self.assertEqual(len(R.stage_plan("control", fixture_block())), 3)
        self.assertEqual(R.stage_plan("control", fixture_block(candidate=(11, 14, 20))), [])
        self.assertEqual(len(R.stage_plan("replicate-V2", fixture_block())), 7)
        self.assertEqual(len(R.stage_plan("replicate-F", fixture_block("F", candidate=(34, 36, 46)))), 7)
        self.assertEqual(R.stage_plan("replicate-V2", fixture_block()[:6]), [])

    def test_control_spending_requires_a_routable_valid_span_block(self):
        records = fixture_block()
        records[4]["step0"]["per_position_fit"][0]["probs"][0] = 0.97
        self.assertEqual(R.stage_plan("control", records), [])
        records = fixture_block()
        records[4]["arm"]["extra"]["frame_minted_n"] = 1
        self.assertEqual(R.stage_plan("control", records), [])
        self.assertEqual(R.stage_plan("control", fixture_block(m1=(40, 44, 46), candidate=(29, 30, 30), ref=19)), [])

    def test_blocked_direction_has_no_pending_control(self):
        underfit = fixture_block()
        underfit[4]["step0"]["per_position_fit"][0]["probs"][0] = 0.97
        locality = fixture_block()
        locality[4]["arm"]["extra"]["frame_minted_n"] = 1
        incomparable = fixture_block(m1=(40, 44, 46), candidate=(29, 30, 30), ref=19)
        for records in (underfit, locality, incomparable):
            self.assertFalse(R.block_reading(records)["controls_pending"])

    def test_public_readings_round_trip_as_strict_json(self):
        a, b = fixture_block(), fixture_block(replicate=1)
        outputs = [R.block_reading(a, b, fixture_controls()), R.reproduction_gate(fixture_block("F")[1:4]),
                   R.run_reading(a[0], a[4]), R.p4_reading(fixture_p4()), R.stage_plan("reproduce")]
        for output in outputs:
            self.assertEqual(json.loads(json.dumps(output, allow_nan=False)), output)

    def test_cli_reads_only_records_and_excludes_context_bootstrap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "F_ctx_bootstrap.json").write_text("not a run")
            before = sorted(p.name for p in root.iterdir())
            output = io.StringIO()
            with redirect_stdout(output):
                code = R.main([str(root)])
            read = json.loads(output.getvalue())
            self.assertEqual([read[b]["direction"] for b in ("F", "V2")], ["INCOMPLETE", "INCOMPLETE"])
            self.assertEqual(before, sorted(p.name for p in root.iterdir()))
            self.assertEqual(code, 0)

    def test_i11_admission_boundaries_and_geometry_is_diagnostic(self):
        self.assertTrue(hasattr(R, "admission_reading"), "pure admission rule is not implemented")
        for recall, cannibal, admitted in ((2, 2, True), (3, 2, False), (2, 3, False)):
            a = R.admission_reading({"ok": True}, [0.99] * 24,
                                    {"recall_n": recall, "n_cannibal": cannibal, "collapsed": True})
            self.assertEqual(a["no_i11_exclusion"], admitted)
            self.assertEqual(a["excluded"], not admitted)
        a = R.admission_reading({"ok": True}, [0.97] * 3 + [0.99] * 21,
                                {"recall_n": 0, "n_cannibal": 0})
        self.assertEqual((a["outcome"], a["P3"]["n_ge_0.98"]), ("UNDERFIT", 21))

    def test_inertness_precision_gate(self):
        self.assertTrue(hasattr(R, "inertness_reading"), "pure inertness rule is not implemented")
        self.assertTrue(R.inertness_reading(1e-5, 1e-5, 1e-5)["ok"])
        self.assertFalse(R.inertness_reading(1.0001e-5, 0.0, 0.0)["ok"])
        self.assertFalse(R.inertness_reading(float("nan"), 0.0, 0.0)["ok"])

    def test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall(self):
        self.assertTrue(hasattr(R, "law3_reference_reading"), "reference rule is not implemented")
        self.assertTrue(R.law3_reference_reading({"A1_single": 68, "A2_coherent2": 68})["ok"])
        self.assertFalse(R.law3_reference_reading({"A1_single": 68, "A2_coherent2": 67})["ok"])
        self.assertTrue(hasattr(R, "i11_reading"), "I-11 rule is not implemented")
        inventory = [{"id": 151665 + i, "unrelated_hits": 3 if i < 2 else 2} for i in range(8)]
        recalls = [{"subj": "S" + str(i), "para_full_hits": [i == 0, False, False]} for i in range(24)]
        reading = R.i11_reading(inventory, recalls)
        self.assertEqual((reading["n_cannibal"], reading["recall_n"], reading["no_i11_exclusion"]), (2, 1, True))
        inventory[2]["unrelated_hits"] = 3
        self.assertFalse(R.i11_reading(inventory, recalls)["no_i11_exclusion"])

    def test_geometry_collapse_boundaries_are_diagnostic(self):
        self.assertTrue(hasattr(R, "geometry_reading"), "geometry rule is not implemented")
        geometry = {"rows": {"cos_mean": 0.9, "effective_rank": 18, "mean_norm": 2.0},
                    "random_base_same_count": {"effective_rank": 24}, "base_mean_norm": 2.0}
        self.assertEqual(R.geometry_reading(geometry), {"collapsed": False, "norm_ratio": 1.0})
        geometry["rows"]["effective_rank"] = 17.999
        self.assertTrue(R.geometry_reading(geometry)["collapsed"])
        geometry["rows"].update(effective_rank=18, cos_mean=0.9001)
        self.assertTrue(R.geometry_reading(geometry)["collapsed"])

    def test_p4_full_sequences_gate_and_q4_correctness_is_report_only(self):
        self.assertTrue(hasattr(R, "p4_reading"), "P4 rule is not implemented")
        for kind in ("mint2", "modifier"):
            record = fixture_p4(kind)
            self.assertTrue(R.p4_reading(record)["ok"])
            row = record["q4km"]["groups"]["canon"][0]
            row.update(gguf_ids=list(reversed(row["expected_ids"])), correct=False, parity=False)
            self.assertTrue(R.p4_reading(record)["ok"])
            row = record["fp16"]["groups"]["canon"][0]
            row.update(gguf_ids=list(reversed(row["expected_ids"])), correct=False, parity=False)
            self.assertEqual(R.p4_reading(record)["label"], "FAIL")

    def test_p4_tokenizer_population_and_subject_specific_ids_fail_closed(self):
        self.assertTrue(hasattr(R, "p4_reading"), "P4 rule is not implemented")
        record = fixture_p4()
        record["fp16"]["target_tokenization"].pop()
        self.assertEqual(R.p4_reading(record)["label"], "INVALID")

    def test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator(self):
        record = fixture_p4()
        a, b = record["fp16"]["groups"]["para"][0], record["q4km"]["groups"]["para"][0]
        wrong = list(reversed(a["expected_ids"]))
        a.update(hf_ids=wrong, parity=False)
        b.update(hf_ids=wrong, gguf_ids=wrong, correct=False, parity=True)
        read = R.p4_reading(record)
        self.assertTrue(read["ok"])
        self.assertIn("fp16_to_q4_survival", read)
        self.assertEqual(read["fp16_to_q4_survival"]["para"], {"retained": 71, "n": 72})
        self.assertEqual(read["q4km"]["para_retention"], {"retained": 71, "n": 71})
        record = fixture_p4()
        record["fp16"]["groups"]["canon"][0]["expected_ids"] = record["fp16"]["groups"]["canon"][1]["expected_ids"]
        self.assertEqual(R.p4_reading(record)["label"], "INVALID")


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((HERE / "c10u_mint2_arms.py").exists(), "new stdlib-only arms module is not implemented")
        self.A = importlib.import_module("c10u_mint2_arms")

    def test_write_json_is_exclusive_and_rereads_exact_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "record.json"
            payload = {"a": [1, {"b": "line\ntext"}]}
            self.A.write_json(p, payload)
            self.assertEqual(json.loads(p.read_text()), payload)
            with self.assertRaises(FileExistsError):
                self.A.write_json(p, {"changed": True})
            self.assertEqual(json.loads(p.read_text()), payload)

    def test_preflight_rejects_inherited_knobs_before_external_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.dict(os.environ, {"C10_ARMS": "dangerous"}, clear=True):
                with patch.object(self.A.subprocess, "run", side_effect=AssertionError("external call preceded knob refusal")):
                    with self.assertRaisesRegex(ValueError, "knob|unset|inherited"):
                        self.A.preflight(root)
            self.assertEqual(list(root.iterdir()), [])

    def test_import_does_not_load_runtime(self):
        self.assertFalse({"torch", "transformers", "c10e_bandknob"} & set(sys.modules))

    def test_p2_audits_two_ids_and_all_720_bigram_prompts(self):
        result = self.A.p2_audit(*fixture_p2())
        self.assertTrue(result["ok"])
        self.assertEqual((len(result["rows"]), len(result["bigram_rows"])), (24, 720))
        self.assertTrue(all(len(r["target_ids"]) == 2 for r in result["rows"]))

    def test_p2_detects_runtime_context_retokenization(self):
        result = self.A.p2_audit(*fixture_p2(contexts=[["{}"], [" M00 {}"]]))
        self.assertFalse(result["ok"])
        self.assertTrue(result["changed"])

    def test_p2_checks_the_whole_modifier_target_even_when_last_id_matches(self):
        args = fixture_p2("modifier")
        class CorruptedHead(Tokenizer):
            def __call__(self, text, **kwargs):
                result = super().__call__(text, **kwargs)
                if text == " H00 M00":
                    result["input_ids"][1] = ord("X") + 1
                return result
        args[1] = CorruptedHead(args[2])
        result = self.A.p2_audit(*args)
        row = result["rows"][0]
        self.assertEqual(row["target_ids"][-1], row["expected_ids"][-1])
        self.assertFalse(row["checks"]["whole_target"])
        self.assertFalse(result["ok"])

    def test_p2_audits_the_engine_default_tokenizer_call(self):
        args = fixture_p2()
        class DefaultCallDiffers(Tokenizer):
            def __call__(self, text, **kwargs):
                result = super().__call__(text, **kwargs)
                if "add_special_tokens" not in kwargs:
                    result["input_ids"] = [1] + result["input_ids"]
                return result
        args[1] = DefaultCallDiffers(args[2])
        self.assertFalse(self.A.p2_audit(*args)["ok"])

    def test_conditional_empty_stage_refuses_before_any_marker(self):
        records = fixture_block("F") + fixture_block(candidate=(11, 14, 20))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(self.A, "read_records", return_value=records), patch.object(self.A, "reproduction_or_halt", return_value={"ok": True}):
                with self.assertRaisesRegex(ValueError, "unnecessary|incomplete|conditional"):
                    self.A.stages(root, root, root / "reference.json", "control", {"ok": True})
            self.assertEqual(list(root.iterdir()), [])

    def test_p4_selection_requires_replication_and_comparability(self):
        with self.assertRaisesRegex(ValueError, "replicated"):
            self.A.p4_configurations(fixture_block(candidate=(30, 31, 32)))
        a, b = fixture_block(candidate=(30, 31, 32)), fixture_block(candidate=(30, 31, 32), replicate=1)
        self.assertEqual(len(self.A.p4_configurations(a + b)), 3)
        a, b = fixture_block(candidate=(30, 31, 32), ref=19), fixture_block(candidate=(30, 31, 32), ref=19, replicate=1)
        with self.assertRaisesRegex(ValueError, "replicated"):
            self.A.p4_configurations(a + b)


class AenvTests(unittest.TestCase):
    def setUp(self):
        self.A = importlib.import_module("c10u_mint2_arms")

    def multi(self, block, replicate=0, **counts):
        record = fixture_record(block, "multi", count=counts.get("para_full_n", 11), replicate=replicate)
        for key, field in (("canon_full_n", "canon_full"), ("para_first_n", "para_first_hits")):
            if key in counts:
                record["arm"][key] = counts[key]
                for i, row in enumerate(record["recipe"]["detail"]["candidate"]):
                    row[field] = i < counts[key] if key == "canon_full_n" else [i * 3 + t < counts[key] for t in range(3)]
                if key == "para_first_n":
                    record["arm"]["extra"]["per_position_teacher_forced"]["0"]["hits"] = counts[key]
        self.assertEqual(R.run_validity(record), [])
        return record

    def test_aenv_baseline_boundaries_in_both_blocks_and_replicates(self):
        cases = {"para_full_n": (4, 5, 18, 19), "canon_full_n": (4, 5, 10, 11),
                 "para_first_n": (41, 42, 59, 60)}
        for block in ("F", "V2"):
            for replicate in (0, 1):
                for key, values in cases.items():
                    for value, ok in zip(values, (False, True, True, False)):
                        with self.subTest(block=block, replicate=replicate, metric=key, value=value):
                            a, b = fixture_block(block), fixture_block(block, replicate=1)
                            records = (a, b)[replicate]
                            records[0] = self.multi(block, replicate, **{key: value})
                            pop = R._population(records, block, replicate)
                            self.assertEqual(pop["reasons"], [])
                            gate = R.reproduction_gate(records[1:4], records[0])["ok"] if block == "F" else R._comparability(pop)
                            self.assertEqual(gate, ok)
                            reading = R.block_reading(a, b)
                            if ok:
                                self.assertTrue(reading["comparability_ok"])
                            else:
                                self.assertEqual(reading["direction"], "HALT-LAW3" if block == "F" else "NOT-COMPARABLE")
        self.assertEqual(R.BASELINE_WINDOW, {"para_full_n": (5, 18), "canon_full_n": (5, 10), "para_first_n": (42, 59)})

    def test_aenv_null_boundaries_and_replication_exclusion(self):
        for count, want in ((10, "PARTIAL"), (11, "NULL"), (18, "NULL"), (19, "PARTIAL")):
            with self.subTest(count=count):
                self.assertEqual(R._single_label(count, 0, True), want)
                a, b = fixture_block(candidate=(19, 19, 19), ref=0), fixture_block(candidate=(count, count, count), ref=0, replicate=1)
                reading = R.run_reading(a[0], a[4], {"reference": b[0], "candidate": b[4]})
                self.assertEqual(reading["label"], "PARTIAL-NOT-REPLICATED" if want == "NULL" else "PARTIAL")
        self.assertEqual(R.NULL_BAND, (11, 18))

    def test_aenv_truth_table_verbatim_through_range_and_replication(self):
        cases = [("F", 5, (40, 36, 41), (15, 25, 36), "MIXED"),
                 ("F", 5, (36, 40, 41), (19, 22, 36), "MODIFIER-RECOVERY"),
                 ("F", 11, (34, 35, 36), (21, 25, 36), "MODIFIER-RECOVERY"),
                 ("F", 5, (34, 36, 46), (15, 16, 18), "NO-MODIFIER-GAIN"),
                 ("F", 5, (34, 36, 46), (12, 14, 19), "MIXED"),
                 ("V2", 5, (34, 36, 46), (15, 16, 18), "PAIR-DIRECTION"),
                 ("V2", 12, (34, 36, 46), (13, 17, 21), "PAIR-DIRECTION")]
        for block, s, m1, candidate, want in cases:
            with self.subTest(block=block, S=s, M1=m1, candidate=candidate):
                a, b = fixture_block(block, m1, candidate, s), fixture_block(block, m1, candidate, s, 1)
                for replicate, records in enumerate((a, b)):
                    pop = R._population(records, block, replicate)
                    self.assertEqual(pop["reasons"], [])
                    self.assertEqual(R._range_direction(pop, block)["label"], want)
                self.assertEqual(R.block_reading(a)["raw_direction"], want)
                reading = R.block_reading(a, b)
                self.assertEqual(reading["replica_ranges"]["label"], want)
                self.assertEqual(reading["direction"], want)

    def test_aenv_envelope_review_counterexamples_keep_null_precedence(self):
        for block, candidate, m1, old, want, labels in (
                ("V2", (15, 16, 18), (34, 36, 46), "SPAN-DIRECTION", "PAIR-DIRECTION", ["NULL", "NULL", "NULL"]),
                ("F", (15, 25, 36), (40, 36, 41), "MODIFIER-RECOVERY", "MIXED", ["NULL", "PARTIAL", "LEAD"])):
            with self.subTest(block=block):
                frozen = "SPAN-DIRECTION" if block == "V2" and min(m1) - max(candidate) >= 10 and min(candidate) - 5 >= 10 else "MODIFIER-RECOVERY" if block == "F" and min(candidate) - 5 >= 10 and max(candidate) >= min(m1) else "MIXED"
                self.assertEqual(frozen, old)
                records = fixture_block(block, m1, candidate, 5)
                self.assertEqual(R._range_direction(R._population(records, block, 0), block)["label"], want)
                self.assertEqual([R._single_label(n, 5, True) for n in candidate], labels)
                self.assertEqual(R.stage_plan("control", records), [])

    def test_aenv_schedule_keeps_reference_and_negative_direction_replication(self):
        for block in ("F", "V2"):
            for s, candidate, want in ((5, (15, 16, 18), "NO-MODIFIER-GAIN" if block == "F" else "PAIR-DIRECTION"),
                                       (11, (12, 13, 14), "NO-MODIFIER-GAIN" if block == "F" else "PAIR-DIRECTION"),
                                       (5, (12, 14, 19), "MIXED")):
                with self.subTest(block=block, S=s, candidate=candidate):
                    records = fixture_block(block, candidate=candidate, ref=s)
                    reading = R.block_reading(records)
                    self.assertEqual(reading["raw_direction"], want)
                    self.assertEqual(reading["direction"], "MIXED" if want == "MIXED" else "PENDING-REPLICATION")
                    self.assertTrue(reading["replication_pending"])
                    self.assertTrue(any(reading["arms"]["mint1_s" + str(seed)]["replication_pending"] for seed in R.SEEDS))
                    if want != "MIXED":
                        kind = "modifier" if block == "F" else "mint2"
                        self.assertTrue(all(reading["arms"][kind + "_s" + str(seed)]["label"] == "NULL" for seed in R.SEEDS))
                    self.assertEqual(R.stage_plan("control", records), [])
                    self.assertEqual(len(R.stage_plan("replicate-" + block, records)), 7)
        positive = fixture_block(ref=5, candidate=(19, 22, 24))
        self.assertEqual(R.block_reading(positive)["raw_direction"], "SPAN-DIRECTION")
        self.assertEqual(len(R.stage_plan("control", positive)), 3)

    def test_aenv_replica_compatibility_can_overturn_positive_routing(self):
        for block, candidate, m1, replica_candidate, replica_want in (
                ("F", (19, 22, 36), (36, 40, 41), (15, 25, 36), "MIXED"),
                ("V2", (19, 22, 24), (34, 36, 46), (15, 16, 18), "PAIR-DIRECTION")):
            with self.subTest(block=block):
                a = fixture_block(block, m1, candidate, 5)
                b = fixture_block(block, m1, replica_candidate, 5, 1)
                reading = R.block_reading(a, b, fixture_controls() if block == "V2" else None)
                self.assertEqual(reading["replica_ranges"]["label"], replica_want)
                self.assertEqual(reading["direction"], "MIXED")

    def test_aenv_stage_completion_round_trips_missing_and_replication_missing(self):
        a, b = fixture_block("F"), fixture_block("F", replicate=1)
        halted = fixture_block("F", ref=19)
        cases = [("partial-F", a[:4], None, "missing", "INCOMPLETE"),
                 ("partial-replication", a, b[:4], "replication_missing", "INCOMPLETE"),
                 ("halt-law3", halted, None, None, "HALT-LAW3")]
        with tempfile.TemporaryDirectory() as directory:
            for stage, initial, replicas, field, want in cases:
                with self.subTest(stage=stage):
                    reading = R.block_reading(initial, replicas)
                    self.assertEqual(reading["direction"], want)
                    record = {"identity": a[0]["identity"], "stage": stage,
                              "readings": {"F": reading, "V2": R.block_reading([])}, "when_utc": "2026-10-07T00:00:00+00:00"}
                    path = Path(directory) / (stage + "_complete.json")
                    self.A.write_json(path, record)
                    self.assertEqual(json.loads(path.read_text()), record)
                    if field:
                        self.assertEqual(reading[field], [["modifier", "0"], ["modifier", "1"], ["modifier", "2"]])
                        self.assertTrue(all(type(pair) is list for name in ("missing", "replication_missing") for pair in reading[name]))
            with self.assertRaisesRegex(RuntimeError, "JSON did not persist exactly"):
                self.A.write_json(Path(directory) / "tuple.json", {"missing": [("modifier", "0")]})

    def test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages(self):
        for replicate in (0, 1):
            for key, value in (("para_full_n", 19), ("para_first_n", 60)):
                with self.subTest(replicate=replicate, metric=key):
                    initial = fixture_block("F")
                    records = initial[1:4] if replicate == 0 else initial[:]
                    bad = self.multi("F", replicate, **{key: value})
                    def spawn(root, out, reference, job, block, kind, seed, rep):
                        record = bad if kind == "multi" else fixture_record(block, kind, seed, (34, 36, 46)[seed], rep)
                        records.append(record)
                        return record
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        with patch.object(self.A, "read_records", side_effect=lambda out: records), patch.object(self.A, "ensure_context"), patch.object(self.A, "ensure_step0"), patch.object(self.A, "spawn_job", side_effect=spawn) as child:
                            stage = "frozen" if replicate == 0 else "replicate-F"
                            with self.assertRaisesRegex(SystemExit, "LAW#3.*stop both blocks"):
                                self.A.stages(root, root, root / "reference.json", stage, {"ok": True})
                            self.assertEqual(child.call_count, 1 if replicate == 0 else 4)
                            self.assertTrue(all(call.args[5] != "modifier" for call in child.call_args_list))
                            self.assertFalse((root / (stage + "_complete.json")).exists())
                            diagnostic = json.loads((root / "architecture_profile/c10u_mint2_halt_diagnostic.json").read_text())
                            self.assertFalse(diagnostic["state"]["reproduction"]["ok"])
                            self.assertTrue(any(key in reason for reason in diagnostic["state"]["reproduction"]["reasons"]))
                            if replicate == 0:
                                child.reset_mock()
                                with self.assertRaisesRegex(SystemExit, "LAW#3.*stop both blocks"):
                                    self.A.stages(root, root, root / "reference.json", "v2", {"ok": True})
                                child.assert_not_called()
                                self.assertFalse((root / "v2_started.json").exists())

    def test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1(self):
        old = {"para_full_n": (11, 18), "canon_full_n": (5, 10), "para_first_n": (48, 62)}
        for replicate in (0, 1):
            records = fixture_block("F", m1=(40, 36, 41), replicate=replicate)
            records[0] = self.multi("F", replicate, para_full_n=10, canon_full_n=8, para_first_n=55)
            self.assertTrue(R.reproduction_gate(records[1:4], records[0])["ok"])
            self.assertFalse(all(lo <= records[0]["arm"][key] <= hi for key, (lo, hi) in old.items()))

    def test_aenv_source_identity_pins_amended_prereg_reader_and_driver(self):
        root = HERE.parents[1]
        hashes = self.A.source_hashes(root)
        self.assertEqual(hashes[self.A.PREREG], "c54f443c70fecd12dce5440cbe7d606587ed1c8384542345f0411cfd0ba15a76")
        for name in ("read", "arms"):
            path = "experiments/track_c/c10u_mint2_" + name + ".py"
            self.assertEqual(hashes[path], self.A.sha256_file(root / path))
        identity = {"source_sha256": hashes, "source_digest": self.A.source_digest(hashes)}
        self.A.assert_sources(identity, root)
        identity["source_sha256"][self.A.PREREG] = "0" * 64
        identity["source_digest"] = self.A.source_digest(identity["source_sha256"])
        with self.assertRaisesRegex(ValueError, "frozen source identity differs"):
            self.A.assert_sources(identity, root)


if __name__ == "__main__":
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    if {"torch", "transformers", "c10e_bandknob"} & set(sys.modules):
        raise RuntimeError("model-free selftest imported a forbidden runtime module")
    if result.wasSuccessful():
        print("C10U_MINT2_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)")
    sys.exit(0 if result.wasSuccessful() else 1)
