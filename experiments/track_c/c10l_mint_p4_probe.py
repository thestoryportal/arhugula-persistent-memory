#!/usr/bin/env python3
"""D-C10l-mint P4 (amendment B2, advisor FIX-FIRST folded): probe ONE running llama-server serving a GGUF compiled from the
mint-edited model, scoring TOKEN IDS, not decoded strings.
Readouts: (a) /tokenize(" " + coined) == [minted id] for all 24 values; (b) per prompt (24 CANON, 72 PTEST, 12 L1, 30 L3,
10 unrelated): the GGUF top-1 token id vs the HF-fp16 top-1 id recorded at save time (`hf_fp16_top1_ids.json`) — PARITY —
and vs the minted id — CORRECTNESS; (c) a failure signature per prompt: tokenizer / generation-id / string-only / none.
Paired fp16→Q4_K_M retention (CORPUS/17's surv/elig) is computed by c10l_mint_p4_verdict.py from two of these outputs.
Usage: c10l_mint_p4_probe.py <server_url> <save_dir> <out_json> [label]
"""
import sys, json, time, urllib.request, os
URL, SAVE_DIR, OUT = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
LABEL = sys.argv[4] if len(sys.argv) > 4 else URL
ref = json.load(open(f"{SAVE_DIR}/hf_fp16_top1_ids.json"))
MINTED = ref["minted_ids"]


def post(path, body):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(5):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=120).read())
        except Exception:
            if attempt == 4: raise
            time.sleep(2)


def top1(prompt):
    r = post("/completion", {"prompt": prompt, "n_predict": 1, "temperature": 0.0, "top_k": 1, "cache_prompt": False, "n_probs": 0, "return_tokens": True})
    if "tokens" not in r or not r["tokens"]:
        raise SystemExit(f"server did not return token ids (return_tokens unsupported?): keys {list(r)}")   # [LAW:no-silent-failure]
    return int(r["tokens"][0]), r["content"]


def tokenize(text):
    return post("/tokenize", {"content": text, "add_special": False})["tokens"]


for _ in range(150):
    try:
        urllib.request.urlopen(URL + "/health", timeout=3); break
    except Exception:
        time.sleep(2)

tok_rows = []
for k, mid in enumerate(MINTED):
    # the coined string is what the minted id decodes to; detokenize it from the server so the check is self-contained
    s = post("/detokenize", {"tokens": [mid]})["content"]
    ids = tokenize(s)
    tok_rows.append({"k": k, "minted_id": mid, "string": s, "ids": ids, "single_minted": ids == [mid]})
rows = {}
for group, prompts in ref["prompts"].items():
    rows[group] = []
    for p, hf_id in zip(prompts, ref["top1"][group]):
        gid, content = top1(p)
        same_string = post("/detokenize", {"tokens": [hf_id]})["content"] == content
        sig = "none" if gid == hf_id else ("string-only" if same_string else "generation-id")
        rows[group].append({"prompt": p, "hf_id": hf_id, "gguf_id": gid, "content": content, "parity": gid == hf_id,
                            "correct": (gid in MINTED) if group in ("canon", "para") else None, "signature": sig})
summary = {"label": LABEL, "save_dir": SAVE_DIR,
           "tokenisation_single_minted": sum(r["single_minted"] for r in tok_rows), "n_values": len(tok_rows),
           "tokeniser_failures": [r for r in tok_rows if not r["single_minted"]]}
for g, rs in rows.items():
    summary[f"{g}_parity"] = sum(r["parity"] for r in rs); summary[f"{g}_n"] = len(rs)
    if g in ("canon", "para"):
        summary[f"{g}_correct"] = sum(r["correct"] for r in rs)
    summary[f"{g}_signatures"] = {s: sum(r["signature"] == s for r in rs) for s in ("none", "string-only", "generation-id")}
summary["L1_flipped_to_minted"] = sum(r["gguf_id"] in MINTED for r in rows["L1"])
summary["rows"] = rows; summary["tokenisation"] = tok_rows
json.dump(summary, open(OUT, "w"), indent=2)
print(f"{LABEL}: tokenise {summary['tokenisation_single_minted']}/{summary['n_values']} | canon parity {summary['canon_parity']}/{summary['canon_n']} correct {summary['canon_correct']} | para parity {summary['para_parity']}/{summary['para_n']} correct {summary['para_correct']} | L1 parity {summary['L1_parity']}/12 flips {summary['L1_flipped_to_minted']} | L3 parity {summary['L3_parity']}/30 | signatures canon {summary['canon_signatures']} para {summary['para_signatures']}", flush=True)
