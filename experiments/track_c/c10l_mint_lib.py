"""D-C10l-mint shared primitives: token registration (P2), the four input-side initialisations (§4), the I-11
step-zero probe, P-iv statistics, and the A1-rare value list. Pure functions over the harness module H plus the model;
nothing here edits weights other than the 24 spare embedding rows it is asked to set. Imported by
c10l_mint_step0.py and c10l_mint_arms.py.
"""
import json, hashlib, random
import torch
from tokenizers import AddedToken

SPARE_START = 151665          # first spare row: len(tokenizer) at the pinned revision (vocab 151,643 + 22 added tokens)
VOCAB_ROWS = 151936           # embed_tokens rows (config.vocab_size); 271 spare rows, no resize
INITS = ("M", "G", "N", "Z")
UNRELATED = [
    "The weather today is", "She opened the window and", "The committee will meet on", "He poured a cup of",
    "The train to the coast", "Water boils at one hundred", "The museum's new exhibition", "Please remember to lock",
    "The recipe calls for two", "Children played football in the",
]


def minted_strings(values):
    return [" " + v for v in values]


def register(tok, values):
    """Add one token per coined value (leading space; matched before BPE). Returns ids; asserts the design facts."""
    toks = [AddedToken(s, normalized=False, lstrip=False, rstrip=False, single_word=False) for s in minted_strings(values)]
    n_added = tok.add_tokens(toks)
    if n_added != len(values):
        raise SystemExit(f"registered {n_added} tokens, expected {len(values)}")   # [LAW:no-silent-failure]
    ids = [tok.convert_tokens_to_ids(s) for s in minted_strings(values)]
    if ids != list(range(SPARE_START, SPARE_START + len(values))):
        raise SystemExit(f"minted ids are not the spare rows: {ids[:3]}...")
    for v, i in zip(values, ids):
        got = tok(" " + v, add_special_tokens=False)["input_ids"]
        if got != [i]:
            raise SystemExit(f"tok(' {v}') = {got}, expected [{i}]")
    return ids


def embed(model):
    return model.model.embed_tokens.weight


def assert_tied(model):
    if model.lm_head.weight.data_ptr() != embed(model).data_ptr():
        raise SystemExit("embeddings are not tied; the prereg's one-row design does not hold")
    if embed(model).shape[0] != VOCAB_ROWS:
        raise SystemExit(f"embed rows {embed(model).shape[0]} != {VOCAB_ROWS}")


ABTT_K = 20   # all-but-the-top (Mu & Viswanath 2018): remove the mean and the top d/100 ≈ 20 principal directions


def top_directions(base, mu, k=ABTT_K):
    """Top-k principal directions of the centred base embedding (151,665 x 2048), via randomised PCA on CPU."""
    _, _, V = torch.pca_lowrank(base - mu, q=k, center=False, niter=4)
    return V[:, :k]   # hidden x k, orthonormal


def build_init(model, base_tok, values, kind, seed=0, U=None):
    """24 x hidden rows. M = mean of the constituent rows (P-iv predicts collapse). G = all-but-the-top of the
    constituent rows (amendment B1: subtract the base mean row AND project out the top-k principal directions of the
    centred base embedding, average, norm-match to the base rows' mean norm; the mean is NOT added back - adding it back
    cancels the de-meaning and leaves M with a rescale, which is what v2's §4 text and the first implementation did).
    N = matched-norm Gaussian. Z = the spare rows as they are. Input-side only: no frame, no hidden state."""
    W = embed(model).detach().float()
    base = W[:SPARE_START]
    mu = base.mean(0)
    target_norm = float(base.norm(dim=1).mean())
    if kind == "G" and U is None:
        U = top_directions(base, mu)
    g = torch.Generator().manual_seed(seed)
    rows = []
    for k, v in enumerate(values):
        cids = base_tok(" " + v, add_special_tokens=False)["input_ids"]
        R = W[cids]
        if kind == "M":
            r = R.mean(0)
        elif kind == "G":
            C = R - mu
            C = C - (C @ U) @ U.T
            r = C.mean(0)
            r = r * (target_norm / r.norm())
        elif kind == "N":
            r = torch.randn(W.shape[1], generator=g)
            r = r * (target_norm / r.norm())
        elif kind == "Z":
            r = W[SPARE_START + k]
        else:
            raise SystemExit(f"unknown init {kind}")
        rows.append(r)
    return torch.stack(rows, 0)


def set_rows(model, ids, rows):
    with torch.no_grad():
        embed(model)[ids] = rows.to(embed(model).device, embed(model).dtype)


def get_rows(model, ids):
    return embed(model)[ids].detach().float().cpu().clone()


def piv_stats(rows):
    """Participation-ratio effective rank + pairwise cosines (keygram stats(), columns = items)."""
    K = rows.T.double()
    Kn = K / K.norm(dim=0, keepdim=True); G = Kn.T @ Kn; n = G.shape[0]; off = G[~torch.eye(n, dtype=torch.bool)]
    ev = torch.linalg.eigvalsh(K.T @ K); pr = float(ev.sum() ** 2 / (ev ** 2).sum())
    return {"cos_mean": round(float(off.mean()), 4), "cos_min": round(float(off.min()), 4), "cos_max": round(float(off.max()), 4),
            "frac_cos_gt_0.9": round(float((off > 0.9).float().mean()), 3), "effective_rank": round(pr, 2), "n": n,
            "mean_norm": round(float(rows.norm(dim=1).mean()), 3)}


@torch.no_grad()
def rank_prob(H, prompt, tid):
    ids = H.tok(prompt, return_tensors="pt").to(H.DEV)
    logits = H.model(**ids).logits[0, -1].float()
    pr = torch.softmax(logits, dim=-1)
    return int((logits > logits[tid]).sum()) + 1, float(pr[tid]), int(logits.argmax())


def i11_probe(H, values, ids, base_tok):
    """Per minted token: rank/prob of ĥ at the value slot on CANON, the 3 PTEST prompts and 10 unrelated prompts;
    classes cannibal / live / shadowed / dead / free; step-0 para_full (/72) and canon (/24) for the init."""
    rows = []
    for k, (c, v) in enumerate(zip(H.FICTION, values)):
        tid = ids[k]
        canon = rank_prob(H, H.CANON.format(c), tid)
        paras = [rank_prob(H, p.format(c), tid) for p in H.PTEST]
        unrel = [rank_prob(H, u, tid) for u in UNRELATED]
        first_c = base_tok(" " + v, add_special_tokens=False)["input_ids"][0]
        c_rank = rank_prob(H, H.CANON.format(c), first_c)[0]
        cannibal = sum(r[2] == tid for r in unrel) >= 3
        para_hits = sum(r[2] == tid for r in paras)
        live = para_hits >= 1
        shadowed = canon[0] == c_rank + 1
        dead = min([canon[0]] + [r[0] for r in paras] + [r[0] for r in unrel]) > 1000
        cls = "cannibal" if cannibal else "live" if live else "shadowed" if shadowed else "dead" if dead else "free"
        rows.append({"subj": c, "val": v, "id": tid, "canon_rank": canon[0], "canon_prob": canon[1], "canon_top1": canon[2] == tid,
                     "para_ranks": [r[0] for r in paras], "para_probs": [r[1] for r in paras], "para_hits": para_hits,
                     "unrelated_top1_count": sum(r[2] == tid for r in unrel), "unrelated_min_rank": min(r[0] for r in unrel),
                     "constituent_first_rank_canon": c_rank, "class": cls})
    return {"rows": rows, "para_full_step0": sum(r["para_hits"] for r in rows), "canon_step0": sum(r["canon_top1"] for r in rows),
            "n_cannibal": sum(r["class"] == "cannibal" for r in rows), "n_live": sum(r["para_hits"] >= 1 for r in rows),
            "classes": {k: sum(r["class"] == k for r in rows) for k in ("cannibal", "live", "shadowed", "dead", "free")}}


def a1_rare_list(base_tok, seed=0, n=24):
    """24 existing single-token lowercase alphabetic words with id > 50,000 (BPE merge order ≈ frequency rank), length ≥ 6,
    not in a small place-name stoplist; frozen in the result JSON before any run."""
    stop = {"london", "berlin", "madrid", "paris", "lisbon", "vienna", "prague", "warsaw", "moscow", "dublin", "athens", "cairo", "tokyo", "seoul"}
    cands = []
    for i in range(50001, SPARE_START):
        s = base_tok.decode([i])
        w = s[1:]
        if s.startswith(" ") and w.isascii() and w.isalpha() and w.islower() and len(w) >= 6 and w not in stop and base_tok(" " + w, add_special_tokens=False)["input_ids"] == [i]:
            cands.append((i, w))
    random.Random(seed).shuffle(cands)
    return cands[:n]


def sha256_tensor(t):
    return hashlib.sha256(t.contiguous().cpu().numpy().tobytes()).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def all_harness_prompts(H):
    """Every prompt string the harness feeds (P2a): CANON/PTEST for the 24 subjects, described-as, L1, L3, generic,
    LAW#5 strings, and A1/A2 value strings. A7 values are the minted strings themselves and are checked by P2b instead."""
    full = H.build_stimuli()
    ps = [t.format(c) for c in H.FICTION for t in [H.CANON] + H.PTEST] + [f"{c} is described as" for c in H.FICTION]
    ps += H.L1_PROMPTS + H.L3_PROMPTS + H.GENERIC + [H.CANON.format("Zorbland"), "Zorbland is described as", " Cairo"]
    ps += [" " + v for v in list(full["A1_single"].values()) + list(full["A2_coherent2"].values())]
    return ps
