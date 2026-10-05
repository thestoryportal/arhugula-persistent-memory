#!/usr/bin/env python3
"""D-C10l-mint P4 (amendment B2): probe ONE running llama-server that serves a GGUF compiled from the mint-edited model.
Readouts (prereg §10 B2): (a) /tokenize of " " + coined → the single minted id for all 24 values; (b) top-1 next token on
the 24 CANON and 72 PTEST prompts (greedy, n_predict=1) compared with the coined string; (c) top-1 on the 12 L1 and 30 L3
prompts for locality (agreement with the HF pre-edit top-1 recorded in the arm JSON is not available per prompt, so the
L3 readout here is the real capital's first token from the screen file; L1 = flips to any minted string).
Usage: c10l_mint_p4_probe.py <server_url> <arm_json> <out_json> [label]
"""
import sys, json, time, urllib.request, os
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URL, ARM_JSON, OUT = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
LABEL = sys.argv[4] if len(sys.argv) > 4 else URL
SPARE_START = 151665


def post(path, body):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(5):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=120).read())
        except Exception:
            if attempt == 4: raise
            time.sleep(2)


def top1(prompt):
    r = post("/completion", {"prompt": prompt, "n_predict": 1, "temperature": 0.0, "top_k": 1, "cache_prompt": False, "n_probs": 0})
    return r["content"]


def tokenize(text):
    return post("/tokenize", {"content": text, "add_special": False})["tokens"]


for _ in range(150):
    try:
        urllib.request.urlopen(URL + "/health", timeout=3); break
    except Exception:
        time.sleep(2)

arm = json.load(open(ARM_JSON))
stim = arm["stimulus"]
CANON, PTEST, FICTION = stim["CANON"], stim["PTEST"], stim["FICTION"]
values = stim["V_A7_coined_coined"]
scr = json.load(open(f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"))["selected"]
# (a) tokenisation
tok_rows = []
for k, c in enumerate(FICTION):
    ids = tokenize(" " + values[c])
    tok_rows.append({"subj": c, "val": values[c], "ids": ids, "single_minted": ids == [SPARE_START + k]})
# (b) canonical + paraphrase top-1
canon = []; para = []
for c in FICTION:
    v = values[c]
    t = top1(CANON.format(c)); canon.append({"subj": c, "top1": t, "hit": t.strip() == v or t == " " + v})
    for p in PTEST:
        t = top1(p.format(c)); para.append({"subj": c, "template": p, "top1": t, "hit": t.strip() == v or t == " " + v})
# (c) locality
minted = {" " + v for v in values.values()} | {v for v in values.values()}
l1 = [{"country": c, "top1": top1(CANON.format(c))} for c in stim["L1_countries"]]
l3 = [{"country": c, "top1": top1(CANON.format(c)), "truth": scr[c]["capital"]["truth"]} for c in stim["L3_countries"]]
out = {"label": LABEL, "arm_json": ARM_JSON,
       "tokenisation_single_minted": sum(r["single_minted"] for r in tok_rows), "n_values": len(tok_rows),
       "canon_hits": sum(r["hit"] for r in canon), "canon_n": len(canon),
       "para_hits": sum(r["hit"] for r in para), "para_n": len(para),
       "L1_flipped_to_minted": sum(r["top1"].strip() in {m.strip() for m in minted} for r in l1), "L1_n": len(l1),
       "L3_truth_first_token_match": sum(r["top1"].strip() and r["truth"].startswith(r["top1"].strip()) for r in l3), "L3_n": len(l3),
       "tokenisation": tok_rows, "canon": canon, "para": para, "l1": l1, "l3": l3}
json.dump(out, open(OUT, "w"), indent=2)
print(f"{LABEL}: tokenise {out['tokenisation_single_minted']}/{out['n_values']} canon {out['canon_hits']}/{out['canon_n']} para {out['para_hits']}/{out['para_n']} L1 {out['L1_flipped_to_minted']}/{out['L1_n']} L3 {out['L3_truth_first_token_match']}/{out['L3_n']}", flush=True)
