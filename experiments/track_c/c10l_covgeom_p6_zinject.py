#!/usr/bin/env python3
"""D-C10l-covgeom P6 (step -1): the z-injection ceiling.

For each of the 24 A7 coined-coined requests, compute zs with the harness's own compute_z at the band's z-layer
(layer 8, canonical prompt, engine context templates), then PATCH that vector into the residual stream output of
layer 8 at the subject-last token (forward hook, no weight change) and greedy-decode len(target) tokens on CANON and on
each PTEST paraphrase. If the paraphrase count is < 30/72 no solve aimed at zs can reach LEAD (the target itself is the
bottleneck, I-1 territory); if >= 30/72 the ceiling admits LEAD.

No edit. Output results/c10l_covgeom/p6_zinject.json. Env: LLMDB_ROOT, OUT.
"""
import os, sys, io, json, contextlib, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["LLMDB_ROOT"] = LLMDB_ROOT
os.environ["C10_ARMS"] = "A7_coined_coined"
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/track_c")
import c10e_bandknob as H   # loads the model; chdir to the engine root
import torch
from memit.memit_hparams import MEMITHyperParams
from memit.compute_z import compute_z
from memit.memit_main import get_context_templates
from rome.repr_tools import get_words_idxs_in_templates

OUT = os.environ.get("OUT", f"{LLMDB_ROOT}/results/c10l_covgeom/p6_zinject.json")
hp = MEMITHyperParams.from_json(H.HP_BASE)
Z_LAYER = hp.layers[-1]
V = H.ARMS["A7_coined_coined"]
block = H.model.model.layers[Z_LAYER]


class Inject:
    """Forward hook on the z-layer block: overwrite the residual output at one position with z. [LAW:effects-at-boundaries]
    the only effect is the hook; it is installed and removed inside the context."""
    def __init__(self, idx, z):
        self.idx, self.z, self.h = idx, z, None

    def __enter__(self):
        def fn(_m, _i, out):
            hid = out[0] if isinstance(out, tuple) else out
            hid[0, self.idx, :] = self.z.to(hid.dtype)
            return out
        self.h = block.register_forward_hook(fn)
        return self

    def __exit__(self, *a):
        self.h.remove()


@torch.no_grad()
def decode(prompt, n):
    ids = H.tok(prompt, return_tensors="pt").to(H.DEV)["input_ids"]
    cur = ids
    for _ in range(n):
        nxt = int(H.model(cur).logits[0, -1].argmax())
        cur = torch.cat([cur, torch.tensor([[nxt]], device=H.DEV)], dim=1)
    return cur[0, ids.shape[1]:].tolist()


def main():
    ctx = get_context_templates(H.model, H.tok)
    templates = [H.CANON] + H.PTEST
    rows = []
    t0 = time.time()
    for c in H.FICTION:
        val = V[c]
        tids = H.tgt_ids(val)
        with contextlib.redirect_stdout(io.StringIO()):
            z = compute_z(H.model, H.tok, H.req(H.CANON, c, val), hp, Z_LAYER, ctx).detach()
        row = {"subj": c, "val": val, "ntok": len(tids), "z_norm": round(float(z.float().norm()), 3), "per_template": []}
        for t in templates:
            prompt = t.format(c)
            idx = get_words_idxs_in_templates(H.tok, [t], [c], "last")[0][0]
            base = decode(prompt, len(tids))
            with Inject(idx, z):
                gen = decode(prompt, len(tids))
                gen2 = decode(prompt, len(tids) + 2)
            row["per_template"].append({
                "template": t, "idx": idx, "keyed_tok": H.tok.decode(H.tok(prompt)["input_ids"][idx]),
                "base_full": base == tids, "inj_full": gen == tids, "inj_first": gen[0] == tids[0],
                "inj_string": H.tok.decode(gen2).startswith(" " + val), "inj_text": H.tok.decode(gen2),
            })
        rows.append(row)
        print(f"  {c:10} {val:22} canon_inj={row['per_template'][0]['inj_full']} para_inj={[r['inj_full'] for r in row['per_template'][1:]]} base={[r['base_full'] for r in row['per_template']]} ({time.time()-t0:.0f}s)", flush=True)
    canon_inj = sum(r["per_template"][0]["inj_full"] for r in rows)
    para_inj = sum(sum(x["inj_full"] for x in r["per_template"][1:]) for r in rows)
    para_first_inj = sum(sum(x["inj_first"] for x in r["per_template"][1:]) for r in rows)
    para_str_inj = sum(sum(x["inj_string"] for x in r["per_template"][1:]) for r in rows)
    per_template = {t: sum(r["per_template"][k]["inj_full"] for r in rows) for k, t in enumerate(templates)}
    base_leak = sum(sum(x["base_full"] for x in r["per_template"]) for r in rows)
    summary = {
        "decision_id": "D-C10l-covgeom", "prereg": f"{LLMDB_ROOT}/docs/C10L_COVGEOM_SPARSEBAND_PREREG.md", "step": "P6 z-injection ceiling",
        "z_layer": Z_LAYER, "hparams": H.HP_BASE, "n_subjects": len(rows),
        "canon_full_inj": canon_inj, "canon_n": len(rows),
        "para_full_inj": para_inj, "para_first_inj": para_first_inj, "para_string_inj": para_str_inj, "para_n": 3 * len(rows),
        "per_template_full_inj": per_template, "base_full_without_injection": base_leak,
        "reading": ("ceiling admits LEAD (para_full_inj >= 30/72)" if para_inj >= 30 else
                    "TARGET-BOUND: para_full_inj < 30/72 — no solve aimed at zs can reach LEAD; arms run once for the record; next queue item = I-1"),
        "rows": rows,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(summary, open(OUT, "w"), indent=2)
    print(f"\nP6: canon_full_inj {canon_inj}/24  para_full_inj {para_inj}/72  para_first_inj {para_first_inj}/72  string {para_str_inj}/72  base-leak {base_leak}  per-template {per_template}")
    print(summary["reading"]); print(f"wrote {OUT}"); print("P6_DONE", flush=True)


if __name__ == "__main__":
    main()
