"""D-C10u-mint2 word list (C10U_MINT2_PREREG.md §1): screen the authored V2 head candidates and the modifier-only arm's
modifiers against the published rules with the base tokenizer only (no model load), and write the frozen, hashed record
results/c10u_mint2/v2_wordlist.json. The binding admission is step 0's P2 on the engine's tokenizer object; this is the
pre-screen that fixes the list before freeze. The protected words come from the harness files: the constants by AST
extraction; the probe templates and the LAW#5 strings as literal copies of all_harness_prompts (c10l_mint_lib.py:182-183).
The sampled context templates are runtime-only and are audited by step 0, not here.
Usage: LLMDB_ROOT=<repo> .venv/bin/python experiments/track_c/c10u_mint2_wordlist.py
"""
import ast, datetime, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10l_mint_lib as M   # register(), sha256_text(), UNRELATED; imports torch + tokenizers only

ROOT = os.environ["LLMDB_ROOT"]   # [LAW:no-silent-failure] KeyError if unset, like every sibling driver
HARNESS = f"{ROOT}/experiments/track_c/c10e_bandknob.py"
TWOPASS = f"{ROOT}/experiments/track_c/c10p_twopass_arms.py"
OUT_DIR = f"{ROOT}/results/c10u_mint2"
OUT = f"{OUT_DIR}/v2_wordlist.json"
MIN_SUBSTRING_LEN = 4   # substring containment is checked against inventory words of this length or more (§1 rule text)

# Authored candidates, in order. The list = passing candidates taken in this order until the head piece-count
# multiset equals the frozen A7 heads' (so the V2 string baseline has the frozen values' length distribution).
HEAD_CANDIDATES = [
    "Tarvesk", "Molquenn", "Fendrax", "Ulbrisk", "Noxquill", "Sprennok", "Kalvoth", "Rimbrosk",
    "Zavrelk", "Pelthorn", "Vustrim", "Gorvande", "Hexmoril", "Tazbrenk", "Wolqetz", "Dravnisk",
    "Ombrixel", "Jorvenak", "Blemkarn", "Pyrvossk", "Nalthrik", "Skevrond", "Cravnolt", "Yembrisk",
    "Veltrosk", "Mirquand", "Ketravon", "Zumbrelk", "Faldrix", "Grentovar", "Isqeldra", "Brovquen",
    "Thanvorl", "Wexdorim", "Plaskovin", "Jaxbrenn",
    "Morvex", "Torvak", "Belmox", "Kurvin", "Zandel", "Norvek", "Palvex", "Garnoth", "Vexlan", "Tomrik",
    "Selvor", "Rundax", "Fenlor", "Dorvin", "Malvek", "Jorlex", "Wulmar", "Harvex", "Lindax", "Pelvok",
]


def harness_constants(path, names):
    """Module-level string/list constants by name; `os.environ.get(NAME, default)` yields the default (ID, REV)."""
    tree = ast.parse(open(path).read())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in names and name not in out:
                v = node.value
                out[name] = ast.literal_eval(v.args[1]) if isinstance(v, ast.Call) else ast.literal_eval(v)
        if isinstance(node, ast.FunctionDef) and node.name == "build_stimuli":   # coined_head / coined_mod live inside it
            for inner in ast.walk(node):
                if isinstance(inner, ast.Assign) and isinstance(inner.targets[0], ast.Name) and inner.targets[0].id in names:
                    out[inner.targets[0].id] = ast.literal_eval(inner.value)
    missing = names - set(out)
    if missing:
        raise SystemExit(f"{path}: constants not found: {sorted(missing)}")   # [LAW:no-silent-failure]
    return out


def words_of(strings):
    return sorted({w.lower() for s in strings for w in re.findall(r"[A-Za-z]+", s)})


def relation(head, word, is_name):
    """The §1 relations between a candidate head and one inventory word (case-insensitive), or None. The head-to-word
    directions are checked against every word (a registered ' Head' would re-tokenise any word it prefixes); the
    word-to-head directions against names of any length and common words of >= MIN_SUBSTRING_LEN letters."""
    h, w = head.lower(), word.lower()
    if h == w:
        return "equal"
    if w.startswith(h):
        return "head is a prefix of the word"
    if h in w:
        return "head is a substring of the word"
    if (is_name or len(w) >= MIN_SUBSTRING_LEN) and h.startswith(w):
        return "word is a prefix of the head"
    if (is_name or len(w) >= MIN_SUBSTRING_LEN) and w in h:
        return "word is a substring of the head"
    return None


def screen(head, inventory, names, tok):
    """Every rule on one head; the record keeps the first failing relation per rule so the table is legible."""
    hits = {}
    for w in inventory:
        r = relation(head, w, w in names)
        if r and w not in hits:
            hits[w] = r
    name_hits = {w: r for w, r in hits.items() if w in names}
    pieces = tok(" " + head, add_special_tokens=False)["input_ids"]
    return {"head": head, "n_pieces": len(pieces), "pieces": [tok.decode([i]) for i in pieces],
            "inventory_relations": hits, "name_relations": name_hits,
            "pass": not hits and len(pieces) >= 2 and head.isalpha() and head[0].isupper() and head[1:].islower()}


def pairwise_clean(words):
    """No equality / prefix / substring relation among the words that will be registered together."""
    bad = []
    for a in words:
        for b in words:
            if a != b and (b.lower().startswith(a.lower()) or a.lower() in b.lower()):
                bad.append((a, b))
    return bad


def p2a_prescreen(tok_before, tok_after, prompts):
    before = [tok_before(p, add_special_tokens=False)["input_ids"] for p in prompts]
    after = [tok_after(p, add_special_tokens=False)["input_ids"] for p in prompts]
    changed = [p for p, a, b in zip(prompts, before, after) if a != b]
    return {"identical": len(prompts) - len(changed), "n": len(prompts), "changed": changed[:10]}


def main():
    from transformers import AutoTokenizer
    H = harness_constants(HARNESS, {"ID", "REV", "CANON", "PTEST", "FICTION", "GENERIC", "coined_head", "coined_mod"})
    F = harness_constants(TWOPASS, {"FRAME_SUBJECTS"})["FRAME_SUBJECTS"]
    screens = {k: json.load(open(f"{ROOT}/configs/screens/{k}.json"))["selected"] for k in ("g6_screen_qwen3b", "g6_screen_qwen3b_v2")}
    countries = sorted(set(screens["g6_screen_qwen3b"]) | set(screens["g6_screen_qwen3b_v2"]))
    capitals = sorted({s[c]["capital"]["truth"] for s in screens.values() for c in s})
    fiction = H["FICTION"]
    probes = [H["CANON"], *H["PTEST"], "{} is described as", "{} is a", "{} is associated with"]

    names = set(words_of(fiction + F + countries + capitals + H["coined_head"] + H["coined_mod"]))
    inventory = sorted(names | set(words_of(probes + H["GENERIC"] + M.UNRELATED + ["Zorbland", "Cairo"])))

    tok = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])
    mods = H["coined_mod"]
    n_pieces = lambda s: len(tok(" " + s, add_special_tokens=False)["input_ids"])
    # The frozen A7 values (build_stimuli's (i*2+1) % 24 head and (i*3+2) % 24 modifier assignment) set the length quota.
    frozen = {c: f"{H['coined_head'][(i * 2 + 1) % 24]} {mods[(i * 3 + 2) % 24]}" for i, c in enumerate(fiction)}
    frozen_mods = list(dict.fromkeys(v.split()[1] for v in frozen.values()))   # first-use order
    quota = {}
    for v in frozen.values():
        quota[n_pieces(v.split()[0])] = quota.get(n_pieces(v.split()[0]), 0) + 1

    rows = [screen(h, inventory, names, tok) for h in HEAD_CANDIDATES]
    heads, left = [], dict(quota)
    for r in rows:
        if r["pass"] and left.get(r["n_pieces"], 0) > 0:
            heads.append(r["head"])
            left[r["n_pieces"]] -= 1
    if len(heads) < 24:
        raise SystemExit(f"quota {quota} unfilled, still need {left}; author more candidates")   # [LAW:no-silent-failure]
    values = {c: f"{heads[i]} {mods[i]}" for i, c in enumerate(fiction)}   # injective: head i <-> modifier i

    # P2a pre-screen inventory = all_harness_prompts (c10l_mint_lib.py:178-185) rebuilt from the constants, with every
    # capital as an A1/A2 value (a superset of the 48 the harness selects), plus the probes this arm adds (§2).
    prompts = [p.format(c) for c in fiction + F + ["Zorbland"] for p in probes]
    prompts += [H["CANON"].format(c) for c in countries] + H["GENERIC"] + M.UNRELATED + [" " + k for k in capitals]
    prompts = list(dict.fromkeys(prompts))
    # Bigram-control prompts contain the minted head by design: edited and never-edited subjects x every head.
    bigram_prompts = [(H["CANON"].format(c), h) for c in fiction + F for h in heads]

    # Registration pre-screens on fresh tokenizer copies (register() asserts tok(' '+w) == [id] for every word).
    tok_v2 = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])
    ids_v2 = M.register(tok_v2, heads + mods)
    pairs_ok = sum(tok_v2(" " + v, add_special_tokens=False)["input_ids"] == [ids_v2[i], ids_v2[24 + i]] for i, v in enumerate(values.values()))
    bigram_ok = sum(tok_v2(p + " " + h, add_special_tokens=False)["input_ids"] == tok_v2(p, add_special_tokens=False)["input_ids"] + [ids_v2[heads.index(h)]]
                    for p, h in bigram_prompts)
    in_context_ok = sum(tok_v2(H["CANON"].format(c) + " " + v, add_special_tokens=False)["input_ids"]
                        == tok_v2(H["CANON"].format(c), add_special_tokens=False)["input_ids"] + [ids_v2[i], ids_v2[24 + i]]
                        for i, (c, v) in enumerate(values.items()))
    # The solve's decode path (compute_z.py:46-50): the rewriting prompt is context + decode(target_ids[:-1]).
    decode_ok = sum(tok_v2.decode([ids_v2[i]]) == " " + h and tok_v2.decode([ids_v2[i], ids_v2[24 + i]]) == " " + v
                    and tok_v2(" " + v)["input_ids"] == [ids_v2[i], ids_v2[24 + i]]   # the engine's default call, no add_special_tokens flag
                    for i, (h, v) in enumerate(zip(heads, values.values())))
    tok_m1 = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])   # mint-1(V2): the 24 whole strings
    ids_m1 = M.register(tok_m1, list(values.values()))
    tok_m1_48 = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])   # the matched 48-row control: strings + the 24 heads
    ids_m1_48 = M.register(tok_m1_48, list(values.values()) + heads)
    m1_48_strings_single = sum(tok_m1_48(" " + v, add_special_tokens=False)["input_ids"] == [ids_m1_48[i]] for i, v in enumerate(values.values()))
    tok_mo = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])
    ids_mo = M.register(tok_mo, frozen_mods)
    mo_targets = {c: tok_mo(" " + v, add_special_tokens=False)["input_ids"] for c, v in frozen.items()}
    mo_complete = sum(t == tok(" " + frozen[c].split()[0], add_special_tokens=False)["input_ids"] + [ids_mo[frozen_mods.index(frozen[c].split()[1])]]
                      for c, t in mo_targets.items())   # the whole target = the head's base pieces + the minted modifier id
    mo_decode = sum(tok_mo.decode(t) == " " + frozen[c] for c, t in mo_targets.items())
    short_common = {h: sorted(w for w in inventory if w not in names and len(w) < MIN_SUBSTRING_LEN and w in h.lower()) for h in heads}

    record = {
        "decision_id": "D-C10u-mint2", "prereg": "docs/C10U_MINT2_PREREG.md", "kind": "word-list pre-screen; base tokenizer only, no model",
        "timestamp": datetime.datetime.now().astimezone().isoformat(), "tokenizer": {"id": H["ID"], "revision": H["REV"]},
        "rules": {
            "head_form": "alphabetic, capitalised, lowercase after the first letter",
            "inventory": "every word (letters only, case-insensitive) of: FICTION (24), FRAME_SUBJECTS (6), every country and capital of both g6 screens, coined_head (24), coined_mod (24), CANON/PTEST/described-as/is-a/associated-with templates, GENERIC (20), UNRELATED (10), the LAW#5 strings",
            "relations_forbidden": f"equality; head a prefix of a word; head a substring of a word (every inventory word); a word a prefix of the head; a word a substring of the head (names of any length, common words of >= {MIN_SUBSTRING_LEN} letters)",
            "bpe": "tok(' ' + head) has >= 2 pieces in the base tokenizer",
            "registration": "after register(heads + coined_mod): tok(' ' + w) == [id] for all 48; tok(' ' + head + ' ' + mod) == [id_head, id_mod] and CANON + value == CANON ids + the pair for all 24; P2a pre-screen identical over the deduplicated inventory prompts; every bigram-control prompt CANON(subject) + head == CANON ids + [id_head] over the 24 edited and 6 never-edited subjects (these prompts contain the minted head by design and are excluded from P2a); arm B: every frozen value == the head's base pieces + [id_mod]",
            "pairing": "value i = heads[i] + ' ' + coined_mod[i] for FICTION[i] (injective; every head identifies its modifier)",
            "selection": "passing candidates in authored order until the head piece-count multiset equals the frozen A7 heads' (head_pieces_quota)",
        },
        "head_pieces_quota": quota,
        "value_pieces": {"frozen": sorted(n_pieces(v) for v in frozen.values()), "v2": sorted(n_pieces(v) for v in values.values())},
        "inventory_sha256": M.sha256_text("\n".join(inventory)), "inventory_size": len(inventory),
        "candidates": rows,
        "heads": heads, "heads_sha256": M.sha256_text("\n".join(heads)),
        "values": values, "values_sha256": M.sha256_text(json.dumps(values, sort_keys=True)),
        "pairwise_relations_among_48": pairwise_clean(heads + mods),
        "v2_registration": {"ids": [ids_v2[0], ids_v2[-1]], "pairs_two_id": f"{pairs_ok}/24", "canon_plus_pair": f"{in_context_ok}/24",
                            "p2a_prescreen": p2a_prescreen(tok, tok_v2, prompts), "bigram_prompts_prefix_plus_head_id": f"{bigram_ok}/{len(bigram_prompts)}",
                            "string_baseline_pieces": {v: len(tok(" " + v, add_special_tokens=False)["input_ids"]) for v in values.values()}},
        "decode_path": {"head_and_pair_decode_and_default_call": f"{decode_ok}/24"},
        "short_common_words_inside_heads": short_common,
        "mint1_v2_registration": {"ids": [ids_m1[0], ids_m1[-1]], "p2a_prescreen": p2a_prescreen(tok, tok_m1, prompts)},
        "mint1_v2_48row_control": {"extra_words": "the 24 V2 heads (never a target in mint-1)", "ids": [ids_m1_48[0], ids_m1_48[-1]],
                                   "strings_single_id": f"{m1_48_strings_single}/24", "p2a_prescreen": p2a_prescreen(tok, tok_m1_48, prompts)},
        "modifier_only": {"modifiers": frozen_mods, "modifiers_sha256": M.sha256_text("\n".join(frozen_mods)), "ids": [ids_mo[0], ids_mo[-1]],
                          "frozen_values": frozen, "target_lengths": sorted({len(t) for t in mo_targets.values()}),
                          "target_is_head_pieces_plus_modifier_id": f"{mo_complete}/24", "target_decodes_to_value": f"{mo_decode}/24",
                          "pairwise_relations": pairwise_clean(frozen_mods),
                          "p2a_prescreen": p2a_prescreen(tok, tok_mo, prompts)},
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(record, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"heads {len(heads)}/24 from {sum(r['pass'] for r in rows)} passing of {len(rows)} candidates; quota {quota}; sha256 {record['heads_sha256'][:12]}")
    print(f"value pieces frozen {record['value_pieces']['frozen']}\n             v2     {record['value_pieces']['v2']}")
    print(f"heads: {heads}")
    for r in rows:
        print(f"  {'PASS' if r['pass'] else 'FAIL'} {r['head']:<10} pieces={r['n_pieces']} {r['pieces']} {r['inventory_relations'] or ''}")
    v2 = record["v2_registration"]
    print(f"V2: pairs {v2['pairs_two_id']}, canon+pair {v2['canon_plus_pair']}, P2a {v2['p2a_prescreen']['identical']}/{v2['p2a_prescreen']['n']}, "
          f"bigram prompts {v2['bigram_prompts_prefix_plus_head_id']}, pairwise {record['pairwise_relations_among_48']}")
    m1 = record["mint1_v2_registration"]["p2a_prescreen"]
    c48 = record["mint1_v2_48row_control"]
    print(f"decode path {record['decode_path']['head_and_pair_decode_and_default_call']}; heads containing a short common word: "
          f"{sum(bool(v) for v in short_common.values())}/24")
    print(f"mint-1(V2): P2a {m1['identical']}/{m1['n']}; 48-row control: strings single-id {c48['strings_single_id']}, P2a {c48['p2a_prescreen']['identical']}/{c48['p2a_prescreen']['n']}")
    mo = record["modifier_only"]
    print(f"modifier-only: {mo['modifiers']} lengths {mo['target_lengths']} whole-target {mo['target_is_head_pieces_plus_modifier_id']} "
          f"decodes {mo['target_decodes_to_value']} P2a {mo['p2a_prescreen']['identical']}/{mo['p2a_prescreen']['n']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
