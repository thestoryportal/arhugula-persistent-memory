#!/usr/bin/env python3
"""D-C10k-keying-ablation dry run (tokenizer only, no model): for the subject-string design (subject = the prompt's final word "of",
placeholder at the end), print the token index and decoded token the vendored engine's subject_last path keys on, with and without
a context-template prefix, for 3 fictional subjects. Pre-registered validity criterion: decoded keyed token == "of" in every case."""
import os, sys, json
LLMDB_ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, f"{LLMDB_ROOT}/memit_dry_run/memit")
from transformers import AutoTokenizer
from rome import repr_tools
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B", revision="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", local_files_only=True)
CANON = "The capital of {} is the city of"
out = {}
for subj in ("Zorbland", "Quaxil", "Plurnak"):
    canon = CANON.format(subj); prompt_last = canon.rsplit(" ", 1)[0] + " {}"          # "The capital of Zorbland is the city {}"
    for tmpl_name, tmpl in (("no_template", "{}"), ("template", "The following is a short note. {}")):
        template = tmpl.format(prompt_last)                                              # engine composes context.format(prompt)
        idx = repr_tools.get_words_idxs_in_templates(tok, [template], ["of"], "last")[0][0]
        ids = tok(template.format("of"))["input_ids"]; decoded = tok.decode(ids[idx])
        out[f"{subj}/{tmpl_name}"] = {"template": template, "keyed_index": idx, "n_tokens": len(ids), "decoded": decoded, "is_last_token": idx == len(ids) - 1}
        print(f"{subj:9s} {tmpl_name:12s} idx={idx:3d}/{len(ids)-1} decoded={decoded!r} last={idx == len(ids) - 1}")
    sub_idx = repr_tools.get_words_idxs_in_templates(tok, [CANON], [subj], "last")[0][0]; ids = tok(canon)["input_ids"]
    print(f"{subj:9s} subject_last idx={sub_idx:3d}/{len(ids)-1} decoded={tok.decode(ids[sub_idx])!r}")
ok = all(v["decoded"].strip() == "of" and v["is_last_token"] for v in out.values()); out["valid"] = ok
os.makedirs(f"{LLMDB_ROOT}/results/c10k_keying_ablation", exist_ok=True); json.dump(out, open(f"{LLMDB_ROOT}/results/c10k_keying_ablation/dryrun_keyed_token.json", "w"), indent=1)
print("VALID" if ok else "INVALID"); sys.exit(0 if ok else 1)
