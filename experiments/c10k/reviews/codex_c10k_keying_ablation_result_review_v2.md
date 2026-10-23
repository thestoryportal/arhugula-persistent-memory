**Verdict: FIX-FIRST**

Single most important next action: fix the provenance/closeout package before relying on this as a closed result: correct the stale `decision_id` fields or explicitly explain them, create the missing `CORPUS/43_C10K_KEYING_ABLATION.md`, update trackers, and rerun `python3 -B tools/closeout_check.py D-C10k-keying-ablation` to green.

Specific issues, in priority order:

1. **Closeout claim is false in this worktree.** `CORPUS/43_C10K_KEYING_ABLATION.md` is absent, and `closeout_check.py D-C10k-keying-ablation` reports 13 missing tracker entries. The result can be a strong draft, but it is not ready to be leaned on as a closed CORPUS finding.

2. **Result attribution is dirty.** K1-K4 and all `n1/N1_*.json` files have top-level `decision_id = D-C10e-bandknob`; only `n1/framebleed.json` carries `D-C10k-keying-ablation`. This looks like wrapper provenance drift, not a science overturn, but it must be fixed or disclosed.

3. **The core scoped evidence is real.** K1/K2 support subject-keyed generalisation: K1 A1/A2 para `95.8/97.2`, K2 `91.7/88.9`; K3/K4 are invalid at N=24 by canon `<90` (`29.2/25.0` A1, `4.2/8.3` A2). `keygram.json` strongly supports interference: last-token key cosine means `0.985-0.991`, rank `1.02-1.03`, versus subject-key ranks `16.46-22.53`.

4. **Claim B is valid only in its narrow N=1 scope.** The N1 evidence is stark: last-token singles `6/6` land with `0/18` paraphrase hits; subject-keyed singles `6/6` land with `18/18`. But all six N1 values are `Beirut`, and the broader distinct-value evidence is only the three-subject frame-bleed probe.

5. **Frame-write language is slightly over-claimed.** The preregistered H-frame threshold was not met. The actual frame probe is `BETWEEN`: bystander flips are `2/6, 6/6, 6/6`; real flips are `0/12, 9/12, 0/12`. Say “partly frame-keyed / strong prior-free frame uptake,” not “read by every prior-free frame prompt.”

6. **Cheapest overturning control:** rerun the N=1 discriminator with distinct per-subject values for all six offsets, both loci, same w=5000. If any meaningful subset of last-token distinct-value singles gets ≥2/3 paraphrases, the “F3 sufficient” reading weakens sharply; if it repeats `0/18` vs `18/18`, the scoped claim becomes much cleaner.

Drift check: yes, this advances F1, but only as a scoped MEMIT mechanism result for keying/read-generalisation. It does not close C10/A7, Route A causality remains partly `I-INFER`, and the closeout gate is currently red.
